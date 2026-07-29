import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models

# ======================
# Paths
# ======================

BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_FILE = BASE_DIR / "data" / "chunks" / "article_chunks_metadata.json"

# ======================
# Qdrant Configuration
# ======================

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "legal_documents"
# MiniLM model uses 384 dimensions
VECTOR_SIZE = 384 

# ======================
# Load chunks
# ======================

print("Loading chunks...")

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Chunks loaded: {len(chunks)}")

# ======================
# Initialize Qdrant Client
# ======================

print("Connecting to Qdrant...")

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# FIX: Delete collection if it already exists (to avoid dimension mismatch errors)
collections = client.get_collections().collections
collection_names = [c.name for c in collections]

if COLLECTION_NAME in collection_names:
    print(f"Deleting existing collection '{COLLECTION_NAME}' to reset dimensions...")
    client.delete_collection(COLLECTION_NAME)

# Create new collection with the correct vector size (384 for MiniLM)
print(f"Creating collection '{COLLECTION_NAME}' with size {VECTOR_SIZE}...")
client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE
    )
)
print("Collection created.")

# ======================
# Embedding model
# ======================

print("Loading embedding model...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# ======================
# Prepare and Upload to Qdrant
# ======================

print("Creating embeddings and uploading to Qdrant...")

points_to_upload = []

for index, chunk in enumerate(chunks):
    text = chunk.get("text", "")
    meta = chunk.get("metadata", {})
    
    if not text.strip():
        continue

    # Create a rich text for embedding
    embedding_text = f"""
Article: {meta.get("article", "")}
Title: {meta.get("article_title", "")}
Topic: {meta.get("topic", "")}
Content: {text}
    """.strip()

    # Generate embedding
    vector = model.encode(embedding_text, normalize_embeddings=True).tolist()

    # Prepare Qdrant Point
    point = models.PointStruct(
        id=index,  # Simple integer ID
        vector=vector,
        payload={
            "id": chunk.get("id", str(index)),
            "text": text,
            "document_title": meta.get("document_title", "FDRE Constitution"),
            "document_type": meta.get("document_type", ""),
            "article": meta.get("article", ""),
            "article_title": meta.get("article_title", ""),
            "topic": meta.get("topic", ""),
            "language": meta.get("language", "am"),
            "jurisdiction": meta.get("jurisdiction", ""),
            "page_start": meta.get("page_start"),
            "page_end": meta.get("page_end"),
            "source": meta.get("source", ""),
            "chunk_index": meta.get("chunk_index", 0)
        }
    )
    
    points_to_upload.append(point)

    # Upload in batches of 64
    if len(points_to_upload) >= 64 or index == len(chunks) - 1:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points_to_upload
        )
        points_to_upload = []  # Reset batch
        print(f"Uploaded {index + 1}/{len(chunks)} chunks...")

print("============================")
print("Ingestion completed successfully!")
print("============================")
print(f"Total documents uploaded to Qdrant: {len(chunks)}")