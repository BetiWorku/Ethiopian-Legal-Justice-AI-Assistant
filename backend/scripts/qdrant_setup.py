from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance
)


# ==========================
# Qdrant Configuration
# ==========================

HOST = "localhost"
PORT = 6333

COLLECTION_NAME = "legal_documents"

VECTOR_SIZE = 384   # multilingual-e5-base dimension


# ==========================
# Connect to Qdrant
# ==========================

print("Connecting to Qdrant...")

client = QdrantClient(
    host=HOST,
    port=PORT
)


# ==========================
# Create Collection
# ==========================

try:

    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]


    if COLLECTION_NAME in existing:

        print(
            "Collection already exists"
        )


    else:

        client.create_collection(

            collection_name=COLLECTION_NAME,

            vectors_config=VectorParams(

                size=VECTOR_SIZE,

                distance=Distance.COSINE

            )

        )


        print(
            "Collection created successfully"
        )


except Exception as e:

    print(
        "Collection creation error:",
        e
    )



# ==========================
# Collection Statistics
# ==========================

try:

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


except Exception as e:

    print(
        "Statistics error:",
        e
    )