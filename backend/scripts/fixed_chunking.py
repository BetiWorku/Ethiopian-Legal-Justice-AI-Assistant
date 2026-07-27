import json
from pathlib import Path


INPUT_FILE = Path("output/constitution_full.txt")
OUTPUT_FILE = Path("data/chunks/fixed_chunks.json")


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


CHUNK_SIZE = 250
OVERLAP = 40


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()


words = text.split()


chunks = []

start = 0
chunk_id = 1


while start < len(words):

    end = start + CHUNK_SIZE

    chunk_words = words[start:end]


    chunks.append({

        "chunk_id": chunk_id,

        "strategy": "fixed_size",

        "size": CHUNK_SIZE,

        "overlap": OVERLAP,

        "text": " ".join(chunk_words)

    })


    chunk_id += 1

    start = end - OVERLAP



with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunks,
        f,
        ensure_ascii=False,
        indent=4
    )


print("Fixed chunks:", len(chunks))
print("Saved:", OUTPUT_FILE)