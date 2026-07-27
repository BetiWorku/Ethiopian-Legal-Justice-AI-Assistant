import json
from pathlib import Path
import pickle

from sentence_transformers import SentenceTransformer
import faiss


# ======================
# Files
# ======================

CHUNKS_FILE = Path("data/chunks/article_chunks.json")
VECTOR_DIR = Path("data/vectors")
VECTOR_DIR.mkdir(
    parents=True,
    exist_ok=True
)

INDEX_FILE = VECTOR_DIR / "legal.index"
META_FILE = VECTOR_DIR / "metadata.pkl"



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
# Prepare embedding text
# ======================


texts = []


for chunk in chunks:

    article = chunk.get(
        "article",
        ""
    )

    title = chunk.get(
        "title",
        ""
    )

    text = chunk.get(
        "text",
        ""
    )


    combined_text = f"""
Article: {article}

Title: {title}

Content:
{text}
"""


    texts.append(
        combined_text
    )



# ======================
# Model
# ======================


print(
    "Loading embedding model..."
)


model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)



# ======================
# Embeddings
# ======================


print(
    "Creating embeddings..."
)


embeddings = model.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True
)


embeddings = embeddings.astype(
    "float32"
)



# ======================
# FAISS
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
# Save
# ======================


print(
    "Saving index..."
)


faiss.write_index(
    index,
    str(INDEX_FILE)
)



with open(
    META_FILE,
    "wb"
) as f:

    pickle.dump(
        chunks,
        f
    )



print(
    "Embedding completed successfully!"
)

print(
    f"Saved: {INDEX_FILE}"
)

print(
    f"Saved: {META_FILE}"
)