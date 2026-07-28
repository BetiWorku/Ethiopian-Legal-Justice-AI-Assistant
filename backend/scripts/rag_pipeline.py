import json
from datetime import datetime, timezone
from pathlib import Path

from scripts.retrieval import search_legal
from scripts.prompt_template import create_prompt
from scripts.llm_service import generate_response
from scripts.language_detector import detect_language

# ==========================
# Configuration
# ==========================

SIMILARITY_THRESHOLD = 0.15
BASE_DIR = Path(__file__).resolve().parent.parent

LOG_PATH = BASE_DIR / "output" / "rag_logs.jsonl"

# ==========================
# Save Logs
# ==========================

def save_rag_log(data):
    LOG_PATH.parent.mkdir(exist_ok=True)
    data["timestamp"] = datetime.now(timezone.utc).isoformat()

    with open(LOG_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")

# ==========================
# RAG Pipeline
# ==========================

def generate_legal_answer(question):

    # ==========================
    # Input Validation
    # ==========================

    if not question or not str(question).strip():
        return {
            "answer": "Please enter a legal question.",
            "sources": [],
            "important_note": "This response is provided for general legal information only and does not replace advice from a qualified legal professional."
        }

    # ==========================
    # Detect Language
    # ==========================
    language = detect_language(question)

    # ==========================
    # Semantic Retrieval
    # ==========================
    retrieval_response = search_legal(question, top_k=5)

    # Bulletproof check: Ensure retrieval_response is a dictionary
    if not isinstance(retrieval_response, dict):
        retrieval_response = {"results": [], "answer": "Retrieval system error."}

    documents = retrieval_response.get("results", [])

    # ==========================
    # Similarity Threshold
    # ==========================
    filtered_documents = []

    for doc in documents:
        # Bulletproof check: Ensure doc is a dictionary
        if not isinstance(doc, dict):
            continue
            
        score = float(doc.get("score", 0))
        if score >= SIMILARITY_THRESHOLD:
            filtered_documents.append(doc)

    # ==========================
    # Safe Fallback (Multilingual)
    # ==========================
    # Helper function to generate the clean fallback response
    def get_safe_fallback(lang):
        if lang == "am":
            fallback_text = """መልስ:
መልሱ በተገኙት የሕግ ሰነዶች ውስጥ አልተገኘም።

ተዛማጅ ምንጮች:
በቂ የሆነ የሕግ ምንጭ አልተገኘም።

አስፈላጊ ማስታወሻ:
ይህ መልስ ለአጠቃላይ የሕግ መረጃ ብቻ ሲሆን ከብቁ የሕግ ባለሙያዎች ምክር አያግድም።"""
            disclaimer = "ይህ መልስ ለአጠቃላይ የሕግ መረጃ ብቻ ሲሆን ከብቁ የሕግ ባለሙያዎች ምክር አያግድም።"
        else:
            fallback_text = """Answer:
The answer is not available in the retrieved legal documents.

Relevant Sources:
No sufficiently relevant legal source was retrieved.

Important Note:
This response is provided for general legal information only and does not replace advice from a qualified legal professional."""
            disclaimer = "This response is provided for general legal information only and does not replace advice from a qualified legal professional."
            
        return {
            "answer": fallback_text,
            "sources": [],
            "important_note": disclaimer
        }

    # 1. First Safe Fallback: If NO documents pass the threshold
    if not filtered_documents:
        result = get_safe_fallback(language)
        save_rag_log({"question": question, "language": language, "response": result})
        return result

    # ==========================
    # Controlled RAG Prompt
    # ==========================
    prompt = create_prompt(
        filtered_documents, 
        question,
        language
    )

    # ==========================
    # LLM Generation
    # ==========================
    try:
        answer = generate_response(prompt)
    except Exception as e:
        result = {
            "answer": "LLM service is unavailable.",
            "sources": [],
            "important_note": str(e)
        }
        save_rag_log({"question": question, "error": str(e)})
        return result

    # ==========================
    # Insufficient Context Check (LLM Fallback)
    # ==========================
    # 2. Second Safe Fallback: If LLM determines the context is insufficient
    # (even if documents were retrieved, they might be irrelevant like for "abbe")
    answer_lower = str(answer).lower()
    if "not available" in answer_lower or "አልተገኘም" in answer_lower or "not sufficient" in answer_lower:
        result = get_safe_fallback(language)
        save_rag_log({"question": question, "language": language, "response": result, "llm_raw_answer": answer})
        return result

    # ==========================
    # Citation Generation
    # ==========================
    sources = []

    for doc in filtered_documents:
        if isinstance(doc, dict):
            doc_title = doc.get("document", "FDRE Constitution")
            art_num = doc.get("article", "Unknown")
            source_str = f"{doc_title}, {art_num}"

            sources.append({
                "document": doc_title,
                "article": art_num,
                "title": doc.get("title", "Unknown"),
                "pages": doc.get("pages", "Unknown"),
                "source": source_str,
                "similarity_score": doc.get("score", 0)
            })

    # ==========================
    # Final Response (Multilingual Formatting)
    # ==========================
    
    # 1. Build the sources string
    sources_str = ""
    for src in sources:
        sources_str += f"\n- {src['document']}, {src['article']}, Page {src['pages']}"

    # 2. Clean up the LLM answer
    clean_answer = answer.replace("Answer:", "").replace("መልስ:", "").strip()

    # 3. Build the exact final answer text based on language
    if language == "am":
        final_answer_text = f"""መልስ:
{clean_answer}

ተዛማጅ ምንጮች:{sources_str}

አስፈላጊ ማስታወሻ:
ይህ መልስ ለአጠቃላይ የሕግ መረጃ ብቻ ሲሆን ከብቁ የሕግ ባለሙያዎች ምክር አያግድም።"""
        disclaimer_note = "ይህ መልስ ለአጠቃላይ የሕግ መረጃ ብቻ ሲሆን ከብቁ የሕግ ባለሙያዎች ምክር አያግድም።"
    else:
        final_answer_text = f"""Answer:
{clean_answer}

Relevant Sources:{sources_str}

Important Note:
This response is provided for general legal information only and does not replace advice from a qualified legal professional."""
        disclaimer_note = "This response is provided for general legal information only and does not replace advice from a qualified legal professional."

    result = {
        "answer": final_answer_text,
        "sources": sources,
        "important_note": disclaimer_note
    }

    # ==========================
    # Save RAG Logs
    # ==========================
    save_rag_log({
        "question": question,
        "language": language,
        "retrieved_documents": filtered_documents,
        "response": result
    })

    return result

# ==========================
# CLI Testing
# ==========================
if __name__ == "__main__":
    print("Ethiopian Legal RAG Assistant")
    print("Type exit to quit")

    while True:
        question = input("\nAsk legal question: ")
        if question.lower() == "exit":
            break

        response = generate_legal_answer(question)

        print("\n========== FINAL RESPONSE ==========")
        print(response.get("answer", "No answer provided."))