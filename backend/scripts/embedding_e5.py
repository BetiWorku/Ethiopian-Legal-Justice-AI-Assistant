import json
from pathlib import Path
import time

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models

# ======================
# Files
# ======================

BASE_DIR = Path(__file__).resolve().parent.parent

# Use the metadata file if it exists, otherwise fallback to the basic chunks file
CHUNKS_FILE = BASE_DIR / "data" / "chunks" / "article_chunks_metadata.json"
if not CHUNKS_FILE.exists():
    CHUNKS_FILE = BASE_DIR / "data" / "chunks" / "article_chunks.json"

# ======================
# Qdrant Configuration
# ======================

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "legal_documents"

# multilingual-e5-base uses 768 dimensions
VECTOR_SIZE = 768 

# ======================
# Model
# ======================

MODEL_NAME = "intfloat/multilingual-e5-base"

print("Loading chunks...")

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Chunks loaded: {len(chunks)}")

# ======================
# Initialize Qdrant Client
# ======================

print("Connecting to Qdrant...")

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Delete collection if it already exists (to avoid dimension mismatch errors)
collections = client.get_collections().collections
collection_names = [c.name for c in collections]

if COLLECTION_NAME in collection_names:
    print(f"Recreating collection '{COLLECTION_NAME}'...")
    client.delete_collection(COLLECTION_NAME)

# Create new collection with the correct vector size (768)
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE
    )
)
print(f"Collection '{COLLECTION_NAME}' created with size {VECTOR_SIZE}.")

# ======================
# Load Model
# ======================

print("Loading embedding model...")
print("Model:", MODEL_NAME)

model = SentenceTransformer(MODEL_NAME)

# ======================
# Generate Embeddings & Upload
# ======================

print("Creating embeddings and uploading to Qdrant...")

start_time = time.time()

points_to_upload = []

for index, chunk in enumerate(chunks):
    # Handle both nested metadata and flat chunk structures safely
    meta = chunk.get("metadata", chunk)
    
    text = chunk.get("text", "") or meta.get("text", "")
    article = meta.get("article", "") or chunk.get("article", "")
    title = meta.get("article_title", "") or chunk.get("title", "")
    
    if not text.strip():
        continue

    # E5 models require "passage: " prefix for documents
    combined_text = f"passage: \nArticle: {article}\nTitle: {title}\nContent:\n{text}"

    # Generate embedding
    vector = model.encode(combined_text, normalize_embeddings=True).tolist()

    # FIX: Safely get page numbers from either 'meta' or 'chunk' directly
    page_start = meta.get("page_start") or chunk.get("page_start")
    page_end = meta.get("page_end") or chunk.get("page_end")

    # Prepare Qdrant Point
    point = models.PointStruct(
        id=index,  # Simple integer ID
        vector=vector,
        payload={
            "id": chunk.get("id", str(index)),
            "text": text,
            "document_title": meta.get("document_title", "FDRE Constitution"),
            "document_type": meta.get("document_type", ""),
            "article": article,
            "article_title": title,
            "topic": meta.get("topic", ""),
            "language": meta.get("language", "am"),
            "jurisdiction": meta.get("jurisdiction", ""),
            "page_start": page_start,
            "page_end": page_end,
            "source": meta.get("source", ""),
            "chunk_index": meta.get("chunk_index", 0)
        }
    )
    
    points_to_upload.append(point)

    # Upload in batches of 32
    if len(points_to_upload) >= 32 or index == len(chunks) - 1:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points_to_upload
        )
        points_to_upload = []  # Reset batch
        print(f"Uploaded {index + 1}/{len(chunks)} chunks...")

end_time = time.time()

# ======================
# Finished
# ======================

print("\n============================")
print("Embedding and Qdrant upload completed successfully!")
print("============================")
print("Model:", MODEL_NAME)
print("Total Vectors Uploaded:", len(chunks))
print("Dimension:", VECTOR_SIZE)
print("Generation time:", round(end_time - start_time, 2), "seconds")