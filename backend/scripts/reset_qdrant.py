from qdrant_client import QdrantClient


client = QdrantClient(
    host="localhost",
    port=6333
)


COLLECTION_NAME = "legal_documents"


if client.collection_exists(
    COLLECTION_NAME
):

    client.delete_collection(
        COLLECTION_NAME
    )

    print(
        "Collection deleted successfully"
    )

else:

    print(
        "Collection does not exist"
    )