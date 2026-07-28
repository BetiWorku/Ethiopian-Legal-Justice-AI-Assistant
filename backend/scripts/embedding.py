import json
from pathlib import Path
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# ======================
# Paths
# ======================

BASE_DIR = Path(__file__).resolve().parent.parent


CHUNKS_FILE = BASE_DIR / "data" / "chunks" / "article_chunks_metadata.json"

VECTOR_DIR = BASE_DIR / "data" / "vectors"

VECTOR_DIR.mkdir(
    parents=True,
    exist_ok=True
)


INDEX_FILE = VECTOR_DIR / "legal.index"

META_FILE = VECTOR_DIR / "metadata.pkl"



# ======================
# Load chunks
# ======================

print("Loading chunks...")


with open(
    CHUNKS_FILE,
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)



print(
    f"Chunks loaded: {len(chunks)}"
)



# ======================
# Prepare text + metadata
# ======================


texts = []

metadata = []


for chunk in chunks:


    text = chunk.get(
        "text",
        ""
    )


    meta = chunk.get(
        "metadata",
        {}
    )


    if not text.strip():
        continue



    # Add metadata into embedding text
    # This improves Amharic topic search

    embedding_text = f"""

Article:
{meta.get("article","")}

Title:
{meta.get("article_title","")}

Topic:
{meta.get("topic","")}

Content:
{text}

"""


    texts.append(
        embedding_text
    )



    # Save complete metadata

    metadata.append({

        "id": chunk.get(
            "id",
            ""
        ),

        "text": text,


        "document_title": meta.get(
            "document_title",
            ""
        ),


        "document_type": meta.get(
            "document_type",
            ""
        ),


        "article": meta.get(
            "article",
            ""
        ),


        "article_title": meta.get(
            "article_title",
            ""
        ),


        "topic": meta.get(
            "topic",
            ""
        ),


        "language": meta.get(
            "language",
            "am"
        ),


        "jurisdiction": meta.get(
            "jurisdiction",
            ""
        ),


        "page_start": meta.get(
            "page_start",
            None
        ),


        "page_end": meta.get(
            "page_end",
            None
        ),


        "source": meta.get(
            "source",
            ""
        ),


        "chunk_index": meta.get(
            "chunk_index",
            0
        )

    })



print(
    f"Prepared {len(texts)} documents"
)



# ======================
# Embedding model
# ======================


print(
    "Loading embedding model..."
)


model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)



# ======================
# Create embeddings
# ======================


print(
    "Creating embeddings..."
)


embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True
)



embeddings = np.array(
    embeddings,
    dtype="float32"
)



# ======================
# Create FAISS
# ======================


print(
    "Creating FAISS index..."
)


dimension = embeddings.shape[1]


index = faiss.IndexFlatIP(
    dimension
)


index.add(
    embeddings
)



# ======================
# Save FAISS
# ======================


faiss.write_index(
    index,
    str(INDEX_FILE)
)



# ======================
# Save metadata
# ======================


with open(
    META_FILE,
    "wb"
) as f:

    pickle.dump(
        metadata,
        f
    )



print("============================")
print("Embedding completed")
print("============================")

print(
    f"FAISS index: {INDEX_FILE}"
)

print(
    f"Metadata: {META_FILE}"
)

print(
    f"Documents: {len(metadata)}"
)