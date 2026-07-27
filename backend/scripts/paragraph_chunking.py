import json
import re
from pathlib import Path


INPUT_FILE = Path("output/constitution_full.txt")
OUTPUT_FILE = Path("data/chunks/paragraph_chunks.json")


MAX_CHARS = 1500
OVERLAP = 200


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


print("Loading text...")


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:
    text = f.read()



# Detect legal paragraphs using:
# Article numbers and numbered provisions

parts = re.split(
    r'(?=አንቀጽ\s+\d+|\n\d+\.|\n\.)',
    text
)



paragraphs = []

for p in parts:

    p = p.strip()

    if len(p) > 50:
        paragraphs.append(p)



chunks = []


current = ""


for para in paragraphs:


    if len(current) + len(para) > MAX_CHARS:


        if current.strip():

            chunks.append({

                "chunk_id": len(chunks)+1,

                "strategy": "paragraph",

                "text": current.strip(),

                "length": len(current)

            })


            current = current[-OVERLAP:]



    current += "\n" + para



if current.strip():

    chunks.append({

        "chunk_id": len(chunks)+1,

        "strategy": "paragraph",

        "text": current.strip(),

        "length": len(current)

    })




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


print(
    "Paragraph chunks:",
    len(chunks)
)

print(
    "Saved:",
    OUTPUT_FILE
)