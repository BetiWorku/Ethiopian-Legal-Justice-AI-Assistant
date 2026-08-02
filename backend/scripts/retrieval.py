import os
import re
import json
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from rank_bm25 import BM25Okapi

# ==============================
# Paths & Config
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
LOG_PATH = BASE_DIR / "output" / "retrieval_logs.jsonl"

# FIX: Changed from 3 to 5. E5 sometimes places the correct broad topic 
# at rank 4/5. Giving 5 articles to Gemini prevents missing the answer.
TOP_K = int(os.getenv("TOP_K", "5"))

DENSE_FETCH_LIMIT = int(os.getenv("DENSE_FETCH_LIMIT", "150"))
RERANK_POOL_SIZE = int(os.getenv("RERANK_POOL_SIZE", "50"))
MODEL_NAME = "intfloat/multilingual-e5-base"
COLLECTION_NAME = "legal_documents"

# ==============================
# Load Model & Connect to Docker
# ==============================
print("Loading E5 embedding model...")
model = SentenceTransformer(MODEL_NAME)

print("Connecting to Qdrant Docker Server (localhost:6333)...")
client = QdrantClient(host="localhost", port=6333)
collection = client.get_collection(COLLECTION_NAME)
print(f"Loaded collection: {COLLECTION_NAME}")
print(f"Vectors: {collection.points_count}\n")

# ==============================
# Helpers
# ==============================
def detect_language(text):
    if re.search(r"[\u1200-\u137F]", str(text)): return "am"
    return "en"

def is_mixed_language(text):
    """True if the text has Amharic chars but is still mostly Latin script
    (e.g. one Amharic word in parentheses inside an English question).
    Used to decide whether the language filter should be relaxed up front."""
    text = str(text)
    amharic_chars = len(re.findall(r"[\u1200-\u137F]", text))
    latin_chars = len(re.findall(r"[a-zA-Z]", text))
    return amharic_chars > 0 and latin_chars > amharic_chars

def translate_to_english(text):
    if not text: return ""
    try: return GoogleTranslator(source="auto", target="en").translate(text)
    except: return text

def translate_to_amharic(text):
    if not text: return ""
    try: return GoogleTranslator(source="auto", target="am").translate(text)
    except: return text

def extract_article_number(question):
    match = re.search(r"(article|art\.?|አንቀጽ)\s*(\d+)", str(question).lower())
    return match.group(2) if match else None

def extract_document_filter(question):
    q_lower = question.lower()
    if "constit" in q_lower or "ሕገ መንግሥት" in q_lower: return "Constitution"
    elif "family" in q_lower or "ቤተሰብ" in q_lower: return "Family Code"
    elif "civil" in q_lower or "ሲቪል" in q_lower: return "Civil Code"
    return None

def tokenize(text):
    words = re.findall(r'\w+', str(text).lower())
    stopwords = {
        "what", "does", "the", "say", "about", "is", "in", "a", "of", "to", "how", "and", "are", "all", "by", "do", "i", "can", "you", "me", "it",
        "constitution", "law", "code", "article", "right", "definition", "legal", "family", "civil", "explain",
        # FIX: Amharic function/question words that carried no topical meaning
        # but weren't being filtered, adding noise to BM25 for Amharic queries.
        "ምን", "ምንድን", "ምንድነው", "ናቸው", "ነው", "ናት", "ላይ", "እና", "ወይም",
        "የ", "በ", "ስለ", "እንዴት", "ማን", "ለምን", "ውስጥ", "ጋር", "ነበር"
    }
    return [w for w in words if w not in stopwords]

# FIX: word-boundary matching so "tax" doesn't false-positive on words like "syntax"
def matches_unsupported(q_lower, keywords):
    for kw in keywords:
        if re.search(r"(?<!\w)" + re.escape(kw) + r"(?!\w)", q_lower):
            return True
    return False

# ==============================
# Search Legal Documents (HYBRID: 60% dense / 40% BM25, normalized-score fusion)
# ==============================
def search_legal(question, top_k=TOP_K):
    question = str(question)
    language = detect_language(question)
    article_number = extract_article_number(question)
    document_filter = extract_document_filter(question)

    base_conditions = []
    if article_number:
        base_conditions.append(models.FieldCondition(key="article", match=models.MatchValue(value=f"Article {article_number}")))
    if document_filter:
        base_conditions.append(models.FieldCondition(key="document_title", match=models.MatchValue(value=document_filter)))

    # FIX: a single stray Amharic character (e.g. one word in parentheses inside
    # an otherwise English question) used to force a hard "Amharic only" filter,
    # which could zero out the candidate pool entirely for mixed-language
    # queries. Only apply the language filter when the query is confidently
    # in one language; mixed queries search without it.
    language_condition = None
    if not is_mixed_language(question):
        lang_value = "English" if language == "en" else "Amharic"
        language_condition = models.FieldCondition(key="language", match=models.MatchValue(value=lang_value))

    def build_filter(include_language):
        conds = list(base_conditions)
        if include_language and language_condition is not None:
            conds.append(language_condition)
        return models.Filter(must=conds) if conds else None

    search_filter = build_filter(include_language=True)

    q_lower = question.lower()
    unsupported_keywords = ["divorce", "file for", "addis ababa", "tax", "lawyer", "hire"]
    if matches_unsupported(q_lower, unsupported_keywords) and not article_number:
        return {"question": question, "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.", "results": []}

    en_question = question if language == "en" else translate_to_english(question)
    am_question = question if language == "am" else translate_to_amharic(question)

    query_text_am = f"query: {am_question}"
    query_text_en = f"query: {en_question}"

    emb_am = model.encode(query_text_am, normalize_embeddings=True)
    emb_en = model.encode(query_text_en, normalize_embeddings=True)

    def run_dense_queries(qfilter):
        try:
            r_am = client.query_points(collection_name=COLLECTION_NAME, query=emb_am.tolist(), query_filter=qfilter, limit=DENSE_FETCH_LIMIT)
            r_en = client.query_points(collection_name=COLLECTION_NAME, query=emb_en.tolist(), query_filter=qfilter, limit=DENSE_FETCH_LIMIT)
            return r_am.points, r_en.points
        except Exception as e:
            print(f"[search_legal] Qdrant query failed with filter={qfilter}: {e}")
            return [], []

    am_points, en_points = run_dense_queries(search_filter)

    # FIX: never let a filter (especially the language filter) silently zero
    # out the whole candidate pool. If the strict filter returns nothing,
    # retry once without the language constraint before giving up.
    if not am_points and not en_points and language_condition is not None:
        relaxed_filter = build_filter(include_language=False)
        am_points, en_points = run_dense_queries(relaxed_filter)

    # Merge dense results, keeping the max score per point id
    points_dict = {}
    for p in am_points:
        points_dict[p.id] = {'point': p, 'score': float(p.score)}
    for p in en_points:
        if p.id in points_dict:
            points_dict[p.id]['score'] = max(points_dict[p.id]['score'], float(p.score))
        else:
            points_dict[p.id] = {'point': p, 'score': float(p.score)}

    # Rank all points by dense score first, so dedup-by-article below keeps
    # the BEST scoring chunk per article, not just whichever was inserted first.
    ranked_points = sorted(points_dict.values(), key=lambda d: d['score'], reverse=True)

    # FIX: dedup by article keeping the highest dense score for that article
    # (previously kept the first-seen chunk regardless of its score)
    candidates = []
    seen_articles = set()
    for data in ranked_points:
        point = data['point']
        payload = point.payload if isinstance(point.payload, dict) else {}
        article = payload.get("article", "")

        if article in seen_articles:
            continue
        seen_articles.add(article)

        candidates.append({
            "id": point.id,
            "dense_score": float(data['score']),
            "document": payload.get("document_title", "Unknown"),
            "article": article,
            "text": payload.get("text", "")
        })

    if not candidates:
        return {"question": question, "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.", "results": []}

    # Dense rank over the FULL candidate pool (already sorted, re-sort defensively)
    candidates.sort(key=lambda d: d["dense_score"], reverse=True)
    for rank, doc in enumerate(candidates):
        doc["dense_rank"] = rank + 1

    # FIX: keep the full pool around for the fallback check below, but only
    # let BM25/RRF rerank among the top-N most semantically relevant candidates.
    # This prevents keyword-only matches deep in the tail from being promoted
    # to rank #1 by RRF despite being semantically irrelevant.
    rerank_pool = candidates[:RERANK_POOL_SIZE]

    tokenized_corpus = [tokenize(doc["text"]) for doc in rerank_pool]
    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = tokenize(en_question) if language == "en" else tokenize(am_question)
    bm25_scores = bm25.get_scores(tokenized_query)

    for i, doc in enumerate(rerank_pool):
        doc["sparse_score"] = float(bm25_scores[i])

    sparse_ranked = sorted(rerank_pool, key=lambda d: d["sparse_score"], reverse=True)
    for rank, doc in enumerate(sparse_ranked):
        doc["sparse_rank"] = rank + 1

    # NOTE: RRF (pure rank-based fusion) was tried and measured WORSE here
    # (66.7% -> 53.3% hit rate). BM25 over short/translated legal text is noisy,
    # and RRF's rank-flattening let that noise override cases where dense
    # search already had the right answer at rank 1 (e.g. "equality before the
    # law", "privacy" cross-language tests both regressed from hits to misses).
    # Reverting to weighted min-max normalized raw-score fusion, which measured
    # better empirically, while restricting reranking to RERANK_POOL_SIZE
    # (dense-relevant candidates only) so BM25 keyword noise from the tail of
    # a 150-deep dense fetch can't promote an irrelevant article to rank #1.
    def normalize_scores(scores):
        if not scores: return []
        min_s, max_s = min(scores), max(scores)
        if max_s == min_s: return [1.0 for _ in scores]
        return [(s - min_s) / (max_s - min_s) for s in scores]

    dense_scores = [doc["dense_score"] for doc in rerank_pool]
    sparse_scores = [doc["sparse_score"] for doc in rerank_pool]
    norm_dense = normalize_scores(dense_scores)
    norm_sparse = normalize_scores(sparse_scores)

    w_dense = 0.6
    w_sparse = 0.4
    for i, doc in enumerate(rerank_pool):
        doc["hybrid_score"] = (w_dense * norm_dense[i]) + (w_sparse * norm_sparse[i])

    top_results = sorted(rerank_pool, key=lambda x: x["hybrid_score"], reverse=True)[:top_k]

    if not top_results:
        return {"question": question, "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.", "results": []}

    # FIX: base the "nothing relevant found" decision on the BEST dense score
    # across the whole candidate pool, not on whichever item RRF ranked #1.
    # Otherwise rank-fusion instability (a keyword-lucky, semantically weak
    # candidate winning RRF) could wipe out a genuinely good answer entirely.
    best_dense_score = candidates[0]["dense_score"]
    if best_dense_score < 0.05 and not article_number:
        return {"question": question, "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.", "results": []}

    top = top_results[0]
    if language == "am":
        answer_text = f"በኢትዮጵያ ሕግ መሠረት፡-\nአንቀጽ: {top['article']}\nይዘት: {top['text']}\nምንጭ: {top['document']}, {top['article']}"
    else:
        answer_text = f"According to Ethiopian law:\nArticle: {top['article']}\nContent: {top['text']}\nSource: {top['document']}, {top['article']}"

    for res in top_results:
        res["score"] = res.get("hybrid_score", 0)

    return {"question": question, "answer": answer_text, "results": top_results}