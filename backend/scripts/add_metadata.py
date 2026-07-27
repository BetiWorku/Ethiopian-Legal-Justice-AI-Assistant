import json
from pathlib import Path


INPUT_FILE = Path("data/chunks/article_chunks.json")

OUTPUT_FILE = Path(
    "data/chunks/article_chunks_metadata.json"
)


# -----------------------------
# Metadata Validation
# -----------------------------

def validate_chunk(chunk):

    required_fields = [
        "id",
        "text",
        "metadata"
    ]


    for field in required_fields:
        if field not in chunk:
            return False


    metadata = chunk["metadata"]


    required_metadata = [
        "document_id",
        "article",
        "language",
        "source",
        "status",
        "chunk_index"
    ]


    for field in required_metadata:
        if field not in metadata:
            return False


    if not chunk["text"].strip():
        return False


    if metadata["language"] not in ["am", "en"]:
        return False


    if metadata["status"] not in ["active", "inactive"]:
        return False


    return True



# -----------------------------
# Add Metadata
# -----------------------------

def add_metadata():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)



    metadata_chunks = []


    for index, chunk in enumerate(chunks):

        article = chunk["article"]
        article_number = article.replace(
            "Article ",
            ""
        )


        new_chunk = {

            "id":
            f"fdre_constitution_article_{article_number}_chunk_{index+1:03}",


            "text":
            chunk["text"],


            "metadata": {

                "document_id":
                "fdre_constitution_amharic_1995",


                "document_title":
                "FDRE Constitution",


                "document_type":
                "constitution",


                "article":
                article,


                "article_title":
                chunk.get(
                    "title",
                    "Unknown"
                ),


                "topic":
                chunk.get(
                    "title",
                    "Unknown"
                ),


                "language":
                "am",


                "jurisdiction":
                "Federal",


                "page_start":
                chunk.get(
                    "page",
                    "Unknown"
                ),


                "page_end":
                chunk.get(
                    "page",
                    "Unknown"
                ),


                "source":
                f"FDRE Constitution, {article}",


                "status":
                "active",


                "chunk_index":
                index + 1
            }

        }


        if validate_chunk(new_chunk):

            metadata_chunks.append(new_chunk)



    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata_chunks,
            f,
            ensure_ascii=False,
            indent=4
        )



    print(
        "Metadata chunks created:",
        len(metadata_chunks)
    )

    print(
        "Saved:",
        OUTPUT_FILE
    )



if __name__ == "__main__":

    add_metadata()