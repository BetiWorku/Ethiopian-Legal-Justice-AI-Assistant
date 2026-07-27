import json
from pathlib import Path
import pickle
import time

from sentence_transformers import SentenceTransformer
import faiss


# ======================
# Files
# ======================

CHUNKS_FILE = Path(
    "data/chunks/article_chunks.json"
)

VECTOR_DIR = Path(
    "data/vectors"
)

VECTOR_DIR.mkdir(
    parents=True,
    exist_ok=True
)


INDEX_FILE = VECTOR_DIR / "legal_e5.index"

META_FILE = VECTOR_DIR / "e5_metadata.pkl"



# ======================
# Model
# ======================

MODEL_NAME = "intfloat/multilingual-e5-base"



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
passage:

Article: {article}

Title: {title}

Content:
{text}
"""


    texts.append(
        combined_text
    )



# ======================
# Load Model
# ======================


print(
    "Loading embedding model..."
)

print(
    "Model:",
    MODEL_NAME
)


model = SentenceTransformer(
    MODEL_NAME
)



# ======================
# Generate Embeddings
# ======================


print(
    "Creating embeddings..."
)


start_time = time.time()


embeddings = model.encode(
    texts,
    batch_size=16,
    show_progress_bar=True,
    normalize_embeddings=True
)


end_time = time.time()



embeddings = embeddings.astype(
    "float32"
)



# ======================
# Embedding Information
# ======================


dimension = embeddings.shape[1]


print(
    "Embedding dimension:",
    dimension
)


print(
    "Generation time:",
    round(
        end_time - start_time,
        2
    ),
    "seconds"
)



# ======================
# Create FAISS Index
# ======================


print(
    "Creating FAISS index..."
)



index = faiss.IndexFlatIP(
    dimension
)


index.add(
    embeddings
)



# ======================
# Save Index
# ======================


print(
    "Saving FAISS index..."
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



# ======================
# Finished
# ======================


print(
    "\nEmbedding completed successfully!"
)


print(
    "Model:",
    MODEL_NAME
)


print(
    "Vectors:",
    index.ntotal
)


print(
    "Dimension:",
    dimension
)


print(
    "Saved index:",
    INDEX_FILE
)


print(
    "Saved metadata:",
    META_FILE
)