import json
import re


INPUT = "data/chunks/legal_chunks.json"
OUTPUT = "data/chunks/legal_chunks_metadata.json"


with open(INPUT,"r",encoding="utf-8") as f:
    chunks=json.load(f)


current_article="Unknown"


for chunk in chunks:

    text = chunk["text"]

    # detect Amharic Article
    match = re.search(
        r"አንቀጽ\s+(\d+)",
        text
    )

    if match:
        current_article = "Article " + match.group(1)


    chunk["article"] = current_article


    # title extraction
    lines=text.split("\n")

    if len(lines)>1:
        chunk["title"]=lines[1].strip()
    else:
        chunk["title"]="Unknown"



with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        chunks,
        f,
        ensure_ascii=False,
        indent=2
    )


print("Metadata added!")