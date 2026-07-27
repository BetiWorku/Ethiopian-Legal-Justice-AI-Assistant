from qdrant_client import QdrantClient


client = QdrantClient(
    host="localhost",
    port=6333
)


COLLECTION_NAME = "legal_documents"


# =========================
# Retrieve by ID
# =========================

point_id = 1


result = client.retrieve(
    collection_name=COLLECTION_NAME,
    ids=[point_id]
)


print("Retrieved Record")
print("================")

print(result[0].payload)



# =========================
# Language Filter
# =========================

print("\nAmharic Documents")
print("=================")


records = client.scroll(
    collection_name=COLLECTION_NAME,
    scroll_filter={
        "must": [
            {
                "key": "language",
                "match": {
                    "value": "am"
                }
            }
        ]
    },
    limit=5
)


for r in records[0]:

    print(
        r.payload["article"],
        "-",
        r.payload["article_title"]
    )



# =========================
# Article Filter
# =========================

print("\nArticle Filter")
print("================")


records = client.scroll(
    collection_name=COLLECTION_NAME,
    scroll_filter={
        "must": [
            {
                "key": "article",
                "match": {
                    "value": "Article 25"
                }
            }
        ]
    },
    limit=5
)


for r in records[0]:

    print(
        r.payload["article"],
        r.payload["text"][:100]
    )