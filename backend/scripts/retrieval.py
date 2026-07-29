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


# ==============================
# Paths
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

LOG_PATH = BASE_DIR / "output" / "retrieval_logs.jsonl"


# ==============================
# Configuration
# ==============================

TOP_K = int(os.getenv("TOP_K", "3"))

# FIX: Changed to E5 model which is much better for Pure Vector Match
MODEL_NAME = "intfloat/multilingual-e5-base"

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

COLLECTION_NAME = "legal_documents"


# ==============================
# Load Model + Qdrant
# ==============================

print("Loading E5 embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Connecting to Qdrant...")

client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT
)

collection = client.get_collection(COLLECTION_NAME)

print(f"Loaded collection: {COLLECTION_NAME}")
print(f"Vectors: {collection.points_count}\n")


# ==============================
# Helpers
# ==============================

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s*\d*\s*=+\s*SOURCE:.*", "", str(text), flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()

def detect_language(text):
    if re.search(r"[\u1200-\u137F]", str(text)):
        return "am"
    return "en"

def extract_article_number(question):
    match = re.search(r"(article|art\.?|አንቀጽ)\s*(\d+)", str(question).lower())
    if match:
        return match.group(2)
    return None

def translate_to_english(text):
    if not text:
        return ""
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except:
        return text

def translate_to_amharic(text):
    if not text:
        return ""
    try:
        return GoogleTranslator(source="auto", target="am").translate(text)
    except:
        return text

def format_pages(payload):
    if not isinstance(payload, dict):
        return "N/A"
        
    start = payload.get("page_start")
    end = payload.get("page_end")
    if start and end:
        if str(start) == str(end):
            return str(start)
        return f"{start}-{end}"
    return "N/A"


# ==============================
# Convert Qdrant Point
# ==============================

def convert_point(point, question, final_score, boosted_score):
    payload = point.payload if isinstance(point.payload, dict) else {}
    
    return {
        "question": question,
        "score": round(final_score, 4),
        "boosted_score": round(boosted_score, 4),  # Semantic + Title Boost
        "document": payload.get("document_title", "FDRE Constitution"),
        "article": payload.get("article", ""),
        "title": payload.get("article_title", ""),
        "pages": format_pages(payload),
        "text": clean_text(payload.get("text", ""))
    }


# ==============================
# Search Legal Documents (E5 Semantic Match & Template Alignment)
# ==============================

def search_legal(question, top_k=TOP_K):
    question = str(question)
    language = detect_language(question)
    article_number = extract_article_number(question)
    
    search_filter = None
    if article_number:
        search_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="article",
                    match=models.MatchValue(value=f"Article {article_number}")
                )
            ]
        )

    # 1. Safe Fallback for Unsupported Questions
    q_lower = question.lower()
    unsupported_keywords = ["divorce", "file for", "addis ababa", "tax", "lawyer", "hire"]
    if any(word in q_lower for word in unsupported_keywords) and not article_number:
        return {
            "question": question,
            "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.",
            "results": []
        }

    # 2. Get Full Sentence Translations
    en_question = question if language == "en" else translate_to_english(question)
    am_question = question if language == "am" else translate_to_amharic(question)

    # 3. Template-Based Query Alignment (Pure Vector Match)
    # The DB was embedded with: "Article: \n Title: \n Topic: \n Content: \n"
    # So we format the query the same way to maximize cosine similarity!
    # We also add E5 specific "query: " prefix.
    query_text_am = f"query: Article: \nTitle: {am_question}\nTopic: \nContent: {am_question}"
    query_text_en = f"query: Article: \nTitle: {en_question}\nTopic: \nContent: {en_question}"

    # 4. Dual Semantic Search with MAX SCORE FUSION
    emb_am = model.encode(query_text_am, normalize_embeddings=True)
    emb_en = model.encode(query_text_en, normalize_embeddings=True)
    
    res_am = client.query_points(collection_name=COLLECTION_NAME, query=emb_am.tolist(), query_filter=search_filter, limit=95)
    res_en = client.query_points(collection_name=COLLECTION_NAME, query=emb_en.tolist(), query_filter=search_filter, limit=95)
    
    points_dict = {}
    
    for p in res_am.points:
        points_dict[p.id] = {'point': p, 'score': float(p.score)}
        
    for p in res_en.points:
        if p.id in points_dict:
            points_dict[p.id]['score'] = max(points_dict[p.id]['score'], float(p.score))
        else:
            points_dict[p.id] = {'point': p, 'score': float(p.score)}

    # 5. Pure Vector Title Re-ranking (No Keywords Used!)
    titles = [d['point'].payload.get("article_title", "") if isinstance(d['point'].payload, dict) else "" for d in points_dict.values()]
    title_embs = model.encode([f"passage: {t}" for t in titles], normalize_embeddings=True) if titles else []

    results = []
    seen_articles = set()

    for i, (pid, data) in enumerate(points_dict.items()):
        point = data['point']
        base_score = data['score']
        
        # Calculate Continuous Semantic Title Boost
        boosted_score = base_score
        if len(title_embs) > 0:
            title_sim_am = float(np.dot(title_embs[i], emb_am))
            title_sim_en = float(np.dot(title_embs[i], emb_en))
            title_sim = max(title_sim_am, title_sim_en)
            
            # Add title similarity directly to score (Continuous Boost)
            boosted_score = base_score + (title_sim * 1.5)
        
        payload = point.payload if isinstance(point.payload, dict) else {}
        article = payload.get("article", "")
        
        # Deduplicate by article, keeping the highest boosted score
        if article in seen_articles:
            for res in results:
                if res['article'] == article and boosted_score > res['boosted_score']:
                    res['score'] = round(base_score, 4)
                    res['boosted_score'] = round(boosted_score, 4)
                    break
            continue
            
        seen_articles.add(article)
        results.append(convert_point(point, question, base_score, boosted_score))

    # Sort by boosted score (Semantic + Title Boost)
    results = sorted(results, key=lambda x: x["boosted_score"], reverse=True)
    top_results = results[:top_k]

    # 6. Safe Fallback for Low Scores
    if not top_results or top_results[0]['boosted_score'] < 0.15:
        return {
            "question": question,
            "answer": "ምንም የሕግ መረጃ አልተገኘም።" if language == "am" else "No legal information found.",
            "results": []
        }

    # 7. Translate ONLY the Top K results if English
    if language == "en":
        for res in top_results:
            res["title"] = translate_to_english(res["title"])
            res["text"] = translate_to_english(res["text"])

    # Generate structured Answer text
    top = top_results[0]
    if language == "am":
        answer_text = f"በኢትዮጵያ ሕገ መንግሥት መሠረት፡-\nአንቀጽ: {top['article']}\nርዕስ: {top['title']}\nይዘት: {top['text']}\nምንጭ: {top['document']}, {top['article']}"
    else:
        answer_text = f"According to Ethiopian law:\nArticle: {top['article']}\nTitle: {top['title']}\nContent: {top['text']}\nSource: {top['document']}, {top['article']}"

    return {
        "question": question,
        "answer": answer_text,
        "results": top_results
    }


# ==============================
# Print Results (Formatted for CLI)
# ==============================

def print_results(response):
    print("\n" + "=" * 60)
    print(f"Search Question: {response['question']}")
    print("=" * 60)

    print("\nANSWER:\n" + response['answer'])

    if not response['results']:
        return

    print("\n" + "=" * 60)
    print("RETRIEVAL RESULTS (EVIDENCE)")
    print("=" * 60)

    for index, result in enumerate(response['results'], start=1):
        print(f"\nResult {index}:")
        print(f"Document: {result['document']}")
        print(f"Article: {result['article']}")
        print(f"Content: {result['text']}")
        print(f"Source: {result['document']}, {result['article']}")
        print(f"Pages: {result['pages']}")
        print(f"Similarity Score: {result['score']}")
        print(f"Ranking Score: {result['boosted_score']}")


# ==============================
# Logging
# ==============================

def save_log(data):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["timestamp"] = datetime.now(timezone.utc).isoformat()

    with open(LOG_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")


# ==============================
# CLI
# ==============================

if __name__ == "__main__":

    while True:
        question = input("\nEnter legal question (or exit): ").strip()

        if not question:
            print("Input cannot be empty. Please enter a valid question.")
            continue

        if question.lower() in ["exit", "quit"]:
            break

        response = search_legal(question)
        print_results(response)
        save_log(response)