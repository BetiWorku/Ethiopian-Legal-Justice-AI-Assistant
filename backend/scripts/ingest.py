from pathlib import Path
import fitz  # PyMuPDF
import pytesseract
import cv2
import numpy as np
from PIL import Image
import re
import json
import hashlib
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

# ==========================
# Configuration
# ==========================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "data" / "documents"
CACHE_PATH = BASE_DIR / "data" / "extracted_documents.json" # Cache file path
DASHBOARD_LOG = BASE_DIR / "data" / "processing_dashboard.json"

PDF_METADATA_MAP = {
    "Ethiopia_Constitution_English.pdf": {"name": "Constitution", "language": "English"},
    "Ethiopia_Constitution_Amharic.pdf": {"name": "Constitution", "language": "Amharic"},
    "Civil_Code_EN.pdf": {"name": "Civil Code", "language": "English"},
    "Civil_Code_AM.pdfpdf.pdf": {"name": "Civil Code", "language": "Amharic"},
    "Family_Code_EN.pdf": {"name": "Family Code", "language": "English"},
    "Family_Code_AM.pdf": {"name": "Family Code", "language": "Amharic"}
}

# ==========================
# Load Model & Connect to Qdrant
# ==========================
print("Loading E5 model...")
model = SentenceTransformer("intfloat/multilingual-e5-base")

print("Connecting to Qdrant Docker...")
client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "legal_documents"

if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)
    print("Deleted old collection.")

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)

# ==========================
# Dashboard Log Setup
# ==========================
dashboard_data = {
    "documents": [],
    "duplicates_removed": 0,
    "total_chunks": 0
}

# ==========================
# PDF Classification & OCR Confidence
# ==========================
def classify_pdf_and_extract(pdf_path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    digital_pages = 0
    scanned_pages = 0
    pages_text = []
    
    for page in doc:
        text = page.get_text().strip()
        if len(text) > 50:
            digital_pages += 1
            pages_text.append({"text": text})
        else:
            scanned_pages += 1
            pages_text.append({"text": ""}) # Placeholder for OCR
            
    doc.close()
    
    pdf_type = "Digital"
    if scanned_pages > 0 and digital_pages > 0:
        pdf_type = "Mixed"
    elif scanned_pages > 0:
        pdf_type = "Scanned"
        
    return pdf_type, pages_text, digital_pages, scanned_pages

def run_ocr_with_confidence(pdf_path, pages_data):
    doc = fitz.open(pdf_path)
    total_confidence = 0
    ocr_pages_count = 0
    
    for i, page in enumerate(doc):
        if not pages_data[i]["text"]: # If empty, run OCR
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Preprocess image
            np_img = np.array(img)
            gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Get OCR Data with confidence scores
            data = pytesseract.image_to_data(thresh, lang="amh+eng", output_type=pytesseract.Output.DICT)
            confidences = [int(c) for c in data['conf'] if int(c) > 0]
            avg_conf = sum(confidences) / len(confidences) if confidences else 0
            
            text = " ".join(data['text'])
            pages_data[i]["text"] = text
            pages_data[i]["conf"] = round(avg_conf, 2)
            total_confidence += avg_conf
            ocr_pages_count += 1
            
    doc.close()
    avg_ocr_conf = (total_confidence / ocr_pages_count) if ocr_pages_count > 0 else 100.0
    return pages_data, round(avg_ocr_conf, 2)

# ==========================
# Main Pipeline
# ==========================
if __name__ == "__main__":
    all_legal_documents = []
    seen_hashes = set() # For Duplicate Detection

    pdf_files = list(PDF_DIR.glob("*.pdf"))
    pdfs_to_process = [p for p in pdf_files if p.name in PDF_METADATA_MAP]

    for pdf in pdfs_to_process:
        meta = PDF_METADATA_MAP[pdf.name]
        print(f"\nProcessing: {pdf.name}")
        
        # 1. Check if a clean Google Drive OCR text file exists!
        txt_path = pdf.with_suffix('.txt')
        if txt_path.exists():
            print(f"  ✓ Found Google OCR text file: {txt_path.name}. Using it directly!")
            with open(txt_path, "r", encoding="utf-8") as f:
                full_text = f.read()
            pdf_type = "Digital (Google OCR)"
            ocr_conf = 100.0
            
        else:
            # 2. Classify PDF
            pdf_type, pages_data, digital_count, scanned_count = classify_pdf_and_extract(pdf)
            print(f"  Type: {pdf_type} (Digital: {digital_count}, Scanned: {scanned_count})")
            
            # 3. Run OCR if needed and get confidence
            ocr_conf = 100.0
            if pdf_type in ["Scanned", "Mixed"]:
                print("  Running OCR...")
                pages_data, ocr_conf = run_ocr_with_confidence(pdf, pages_data)
                
            full_text = "\n".join([p["text"] for p in pages_data])
            
        low_conf_flag = ocr_conf < 70.0
        full_text = re.sub(r'\n+', '\n', full_text).strip()
        
        # 4. Chunking by Article
        pattern = r'((?:Article|Art\.?|አንቀጽ)\s*\d+)'
        parts = re.split(f'({pattern})', full_text, flags=re.IGNORECASE)
        
        chunks_added = 0
        for i in range(1, len(parts), 2):
            if i+1 < len(parts):
                article_id_raw = parts[i].replace('\n', ' ').strip()
                article_body = parts[i+1].strip()
                
                if len(article_body) < 30: continue
                
                match_num = re.search(r'\d+', article_id_raw)
                if not match_num: continue
                article_id = f"Article {match_num.group()}"
                
                # 5. Duplicate Detection (Hashing)
                chunk_hash = hashlib.md5(article_body.encode('utf-8')).hexdigest()
                if chunk_hash in seen_hashes:
                    dashboard_data["duplicates_removed"] += 1
                    continue
                seen_hashes.add(chunk_hash)
                
                all_legal_documents.append({
                    "text": article_body,
                    "document_title": meta["name"],
                    "article": article_id,
                    "language": meta["language"],
                    "chunk_hash": chunk_hash
                })
                chunks_added += 1

        dashboard_data["documents"].append({
            "filename": pdf.name,
            "type": pdf_type,
            "ocr_confidence": ocr_conf,
            "low_confidence_flag": low_conf_flag,
            "chunks_added": chunks_added
        })
        print(f"  Added {chunks_added} chunks. OCR Confidence: {ocr_conf}%")

    dashboard_data["total_chunks"] = len(all_legal_documents)

    # Save Dashboard Log
    with open(DASHBOARD_LOG, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, indent=4)
    print("\nDashboard log saved.")

    # Save Cache (So we never OCR again)
    print("Saving extracted text to cache...")
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(all_legal_documents, f, ensure_ascii=False, indent=4)

    # 6. Embed and Upload to Qdrant
    print(f"\nTotal unique articles: {len(all_legal_documents)}")
    print("Creating E5 embeddings and uploading to Qdrant Server...")
    point_id_counter = 1

    for doc in all_legal_documents:
        text_to_embed = f"passage: {doc['text']}"
        vector = model.encode(text_to_embed, normalize_embeddings=True).tolist()
        
        payload = {
            "document_title": doc["document_title"],
            "article": doc["article"],
            "text": doc["text"],
            "language": doc["language"],
            "chunk_hash": doc["chunk_hash"]
        }
        
        client.upsert(
            collection_name=COLLECTION_NAME, 
            points=[PointStruct(id=point_id_counter, vector=vector, payload=payload)]
        )
        point_id_counter += 1

    print("\n✅ Ingestion Complete!")