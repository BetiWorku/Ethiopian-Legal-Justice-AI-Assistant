import pickle
from pathlib import Path

import faiss
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


# ======================
# Configuration
# ======================

INDEX_FILE = Path("data/vectors/legal.index")
META_FILE = Path("data/vectors/metadata.pkl")

COLLECTION_NAME = "legal_documents"


# ======================
# Qdrant Connection
# ======================

print("Connecting to Qdrant...")

client = QdrantClient(
    host="localhost",
    port=6333
)


# ======================
# Load FAISS vectors
# ======================

print("Loading FAISS index...")

index = faiss.read_index(
    str(INDEX_FILE)
)

print(
    "Vectors loaded:",
    index.ntotal
)


# ======================
# Load Metadata
# ======================

print("Loading metadata...")

with open(
    META_FILE,
    "rb"
) as f:
    chunks = pickle.load(f)


print(
    "Metadata loaded:",
    len(chunks)
)


# ======================
# Extract vectors
# ======================

vectors = index.reconstruct_n(
    0,
    index.ntotal
)


# ======================
# Prepare Qdrant Points
# ======================

points = []


for i, chunk in enumerate(chunks):


    metadata = chunk.get(
        "metadata",
        {}
    )


    article = (
        metadata.get("article")
        or chunk.get("article", "")
    )


    article_title = (
        metadata.get("article_title")
        or chunk.get("article_title", "")
        or chunk.get("title", "")
    )


    topic = (
        metadata.get("topic")
        or chunk.get("topic", "")
    )


    source = (
        metadata.get("source")
        or chunk.get("source", "")
    )


    page_start = (
        metadata.get("page_start")
        or chunk.get("page_start")
        or chunk.get("page")
    )


    page_end = (
        metadata.get("page_end")
        or chunk.get("page_end")
        or page_start
    )


    text = chunk.get(
        "text",
        ""
    )


    # ======================
    # Payload
    # ======================

    payload = {

        "chunk_id": chunk.get(
            "chunk_id",
            f"chunk_{i}"
        ),


        "document_id": chunk.get(
            "document_id",
            "fdre_constitution"
        ),


        "document_title": chunk.get(
            "document_title",
            "FDRE Constitution"
        ),


        "document_type": chunk.get(
            "document_type",
            "constitution"
        ),


        "article": article,


        "article_title": article_title,


        "topic": topic,


        "language": chunk.get(
            "language",
            "am"
        ),


        "jurisdiction": chunk.get(
            "jurisdiction",
            "Federal"
        ),


        # FIXED PAGE DATA
        "page_start": page_start,

        "page_end": page_end,


        "source": source,


        "status": chunk.get(
            "status",
            "active"
        ),


        "text": text
    }



    points.append(

        PointStruct(

            id=i + 1,

            vector=vectors[i].tolist(),

            payload=payload

        )
    )



# ======================
# Upload to Qdrant
# ======================

print(
    "Uploading vectors to Qdrant..."
)


client.upsert(

    collection_name=COLLECTION_NAME,

    points=points

)


print(
    "Insertion completed!"
)



# ======================
# Statistics
# ======================

info = client.get_collection(
    collection_name=COLLECTION_NAME
)


print("\nCollection Statistics")
print("====================")


print(
    "Vectors count:",
    info.points_count
)


print(
    "Vector dimension:",
    info.config.params.vectors.size
)


print(
    "Distance:",
    info.config.params.vectors.distance
)