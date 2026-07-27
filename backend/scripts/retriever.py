import os
import re
import pickle
import faiss

from sentence_transformers import SentenceTransformer


# ==========================
# Paths
# ==========================

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)


INDEX_PATH = os.path.join(
    BASE_DIR,
    "data",
    "vectors",
    "legal.index"
)


METADATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "vectors",
    "metadata.pkl"
)



# ==========================
# Load Embedding Model
# ==========================

print("Loading embedding model...")


model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)



# ==========================
# Load FAISS
# ==========================

print("Loading FAISS index...")


index = faiss.read_index(
    INDEX_PATH
)



# ==========================
# Load Metadata
# ==========================

print("Loading metadata...")


with open(
    METADATA_PATH,
    "rb"
) as f:

    metadata = pickle.load(f)



print("Retriever ready!")




# ==========================
# Detect Article Number
# ==========================

def find_article_number(query):

    match = re.search(
        r"(Article|አንቀጽ)\s*(\d+)",
        query,
        re.IGNORECASE
    )


    if match:

        return match.group(2)


    return None




# ==========================
# Semantic Search
# ==========================

def search_legal_documents(
        query,
        top_k=5,
        threshold=0.55
):


    # ---------------------------------
    # 1. Direct Article Search
    # ---------------------------------

    article_number = find_article_number(
        query
    )


    if article_number:


        results = []


        for item in metadata:


            if item.get("article") == f"Article {article_number}":


                results.append({

                    "rank": 1,

                    "score": 1.0,

                    "source": item.get(
                        "source",
                        "Unknown"
                    ),

                    "page": item.get(
                        "page",
                        "Unknown"
                    ),

                    "article": item.get(
                        "article",
                        "Unknown"
                    ),

                    "title": item.get(
                        "title",
                        "Unknown"
                    ),

                    "text": item.get(
                        "text",
                        ""
                    )

                })


                return results




    # ---------------------------------
    # 2. Semantic Retrieval
    # ---------------------------------


    query_vector = model.encode(

        [query],

        normalize_embeddings=True

    )


    query_vector = query_vector.astype(
        "float32"
    )



    distances, indices = index.search(

        query_vector,

        top_k

    )



    results = []



    for rank, idx in enumerate(indices[0]):


        if idx == -1:
            continue



        score = float(
            distances[0][rank]
        )



        if score < threshold:
            continue



        item = metadata[idx]



        results.append({

            "rank": rank + 1,

            "score": score,


            "source": item.get(
                "source",
                "Unknown"
            ),


            "page": item.get(
                "page",
                "Unknown"
            ),


            "article": item.get(
                "article",
                "Unknown"
            ),


            "title": item.get(
                "title",
                "Unknown"
            ),


            "text": item.get(
                "text",
                ""
            )

        })



    return results






# ==========================
# Testing
# ==========================


if __name__ == "__main__":


    question = "የጋብቻ መብት"


    results = search_legal_documents(
        question
    )



    for item in results:


        print("\n-------------------")


        print(
            "Rank:",
            item["rank"]
        )


        print(
            "Article:",
            item["article"]
        )


        print(
            "Title:",
            item["title"]
        )


        print(
            "Page:",
            item["page"]
        )


        print(
            "Score:",
            item["score"]
        )


        print(
            item["text"][:700]
        )