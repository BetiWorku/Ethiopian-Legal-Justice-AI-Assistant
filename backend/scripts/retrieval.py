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
TOP_K = int(os.getenv("TOP_K", "3"))
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
    # Added fuzzy matching for typos like "constition"
    if "constit" in q_lower or "ሕገ መንግሥት" in q_lower: return "Constitution"
    elif "family" in q_lower or "ቤተሰብ" in q_lower: return "Family Code"
    elif "civil" in q_lower or "ሲቪል" in q_lower: return "Civil Code"
    return None

def tokenize(text):
    return re.findall(r'\w+', str(text).lower())

# ==============================
# Search Legal Documents (PURE HYBRID: 60% DENSE + 40% SPARSE)
# ==============================
def search_legal(question, top_k=TOP_K):
    question = str(question)
    language = detect_language(question)
    article_number = extract_article_number(question)
    document_filter = extract_document_filter(question)
    
    # Build Filter
    conditions = []
    if article_number:
        conditions.append(models.FieldCondition(key="article", match=models.MatchValue(value=f"Article {article_number}")))
    if document_filter:
        conditions.append(models.FieldCondition(key="document_title", match=models.MatchValue(value=document_filter)))
            
    search_filter = models.Filter(must=conditions) if conditions else None

    # 1. Safe Fallback for Unsupported Questions
    q_lower = question.lower()
    unsupported_keywords = ["divorce", "file for", "addis ababa", "tax", "lawyer", "hire"]
    if any(word in q_lower for word in unsupported_keywords) and not article_number:
        return {"question": question, "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.", "results": []}

    # 2. Get Full Sentence Translations
    en_question = question if language == "en" else translate_to_english(question)
    am_question = question if language == "am" else translate_to_amharic(question)

    # 3. Template-Based Query Alignment (Simplified for E5)
    query_text_am = f"query: {am_question}"
    query_text_en = f"query: {en_question}"

    # 4. Dual Semantic Search (Dense) - Fetch Top 100 for Re-ranking
    emb_am = model.encode(query_text_am, normalize_embeddings=True)
    emb_en = model.encode(query_text_en, normalize_embeddings=True)
    
    res_am = client.query_points(collection_name=COLLECTION_NAME, query=emb_am.tolist(), query_filter=search_filter, limit=100)
    res_en = client.query_points(collection_name=COLLECTION_NAME, query=emb_en.tolist(), query_filter=search_filter, limit=100)
    
    points_dict = {}
    for p in res_am.points:
        points_dict[p.id] = {'point': p, 'score': float(p.score)}
    for p in res_en.points:
        if p.id in points_dict:
            points_dict[p.id]['score'] = max(points_dict[p.id]['score'], float(p.score))
        else:
            points_dict[p.id] = {'point': p, 'score': float(p.score)}

    # 5. Process Candidates
    candidates = []
    seen_articles = set()
    for pid, data in points_dict.items():
        point = data['point']
        payload = point.payload if isinstance(point.payload, dict) else {}
        article = payload.get("article", "")
        
        if article in seen_articles: continue
        seen_articles.add(article)
        
        candidates.append({
            "id": pid,
            "dense_score": float(data['score']),
            "document": payload.get("document_title", "Unknown"),
            "article": article,
            "text": payload.get("text", "")
        })

    if not candidates:
        return {"question": question, "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.", "results": []}

    # 6. SPARSE SEARCH (BM25) & Normalized Score Fusion
    tokenized_corpus = [tokenize(doc["text"]) for doc in candidates]
    bm25 = BM25Okapi(tokenized_corpus)
    
    tokenized_query = tokenize(en_question)
    bm25_scores = bm25.get_scores(tokenized_query)
    
    for i, doc in enumerate(candidates):
        doc["sparse_score"] = float(bm25_scores[i])

    # Normalize scores to 0-1 range
    def normalize_scores(scores):
        if not scores: return []
        min_s, max_s = min(scores), max(scores)
        if max_s == min_s: return [1.0 for _ in scores]
        return [(s - min_s) / (max_s - min_s) for s in scores]

    dense_scores = [doc["dense_score"] for doc in candidates]
    sparse_scores = [doc["sparse_score"] for doc in candidates]
    
    norm_dense = normalize_scores(dense_scores)
    norm_sparse = normalize_scores(sparse_scores)
    
    # FIX: 60% Dense (Meaning), 40% Sparse (Keywords) to catch exact legal terms better
    w_dense = 0.6
    w_sparse = 0.4
    
    for i, doc in enumerate(candidates):
        doc["hybrid_score"] = (w_dense * norm_dense[i]) + (w_sparse * norm_sparse[i])

    top_results = sorted(candidates, key=lambda x: x["hybrid_score"], reverse=True)[:top_k]

    # 7. Safe Fallback for Low Scores
    # FIX: Threshold lowered to 0.05 to prevent blocking valid answers
    if not top_results:
        return {"question": question, "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.", "results": []}
        
    if top_results[0]['dense_score'] < 0.05 and not article_number:
        return {"question": question, "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.", "results": []}

    # 8. Generate Answer Text
    top = top_results[0]
    if language == "am":
        answer_text = f"በኢትዮጵያ ሕግ መሠረት፡-\nአንቀጽ: {top['article']}\nይዘት: {top['text']}\nምንጭ: {top['document']}, {top['article']}"
    else:
        answer_text = f"According to Ethiopian law:\nArticle: {top['article']}\nContent: {top['text']}\nSource: {top['document']}, {top['article']}"

    for res in top_results:
        res["score"] = res.get("hybrid_score", 0)

    return {"question": question, "answer": answer_text, "results": top_results}