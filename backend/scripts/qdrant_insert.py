import pickle
from pathlib import Path

import faiss
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


# ======================
# Configuration
# ======================

INDEX_FILE = Path("data/vectors/legal_e5.index")
META_FILE = Path("data/vectors/e5_metadata.pkl")

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
# Load metadata
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


    # Support both formats
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
        or chunk.get("title", "")
    )


    source = (
        metadata.get("source")
        or chunk.get("source", "")
    )


    page = (
        metadata.get("page_start")
        or chunk.get("page", None)
    )


    text = chunk.get(
        "text",
        ""
    )


    payload = {


        "chunk_id":
        chunk.get(
            "id",
            f"chunk_{i+1}"
        ),


        "document_id":
        metadata.get(
            "document_id",
            "fdre_constitution_amharic_1995"
        ),


        "document_title":
        metadata.get(
            "document_title",
            "FDRE Constitution"
        ),


        "document_type":
        metadata.get(
            "document_type",
            "constitution"
        ),


        "article":
        article,


        "article_title":
        article_title,


        "topic":
        (
            metadata.get("topic")
            or article_title
        ),


        "language":
        metadata.get(
            "language",
            "am"
        ),


        "jurisdiction":
        metadata.get(
            "jurisdiction",
            "Federal"
        ),


        "page_start":
        page,


        "page_end":
        (
            metadata.get("page_end")
            or page
        ),


        "source":
        source,


        "status":
        metadata.get(
            "status",
            "active"
        ),


        "text":
        text
    }



    points.append(

        PointStruct(

            id=i + 1,

            vector=
            vectors[i].tolist(),

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
# Collection Statistics
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