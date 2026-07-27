import json
from pathlib import Path


FILES = [
    Path("data/chunks/fixed_chunks.json"),
    Path("data/chunks/paragraph_chunks.json"),
    Path("data/chunks/article_chunks.json")
]


print("Chunk Statistics")
print("=================")


for file in FILES:

    if not file.exists():
        print("\nMissing:", file)
        continue


    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:
        chunks = json.load(f)


    if len(chunks) == 0:
        print("\n", file.name)
        print("No chunks found")
        continue


    sizes = []

    for chunk in chunks:
        sizes.append(
            len(chunk.get("text", ""))
        )


    print("\n--------------------")
    print("File:", file.name)

    print(
        "Number of chunks:",
        len(chunks)
    )

    print(
        "Average size:",
        round(sum(sizes) / len(sizes), 2),
        "characters"
    )

    print(
        "Minimum size:",
        min(sizes),
        "characters"
    )

    print(
        "Maximum size:",
        max(sizes),
        "characters"
    )