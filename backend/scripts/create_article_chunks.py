import json
import re
from pathlib import Path


INPUT_FILE = Path("output/constitution_full.txt")
OUTPUT_FILE = Path("data/chunks/article_chunks.json")


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


print("Loading constitution text...")


with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()



# Find only Amharic Article numbers
pattern = r"አንቀጽ\s+(\d+)"

matches = list(
    re.finditer(pattern, text)
)


chunks = []


seen_articles = set()



for i, match in enumerate(matches):

    article_number = match.group(1)

    
    # remove duplicates
    if article_number in seen_articles:
        continue


    seen_articles.add(article_number)


    start = match.start()

    
    if i + 1 < len(matches):
        end = matches[i+1].start()
    else:
        end = len(text)


    article_text = text[start:end].strip()



    # remove very small noise
    if len(article_text) < 100:
        continue



    # extract title
    lines = article_text.split("\n")

    title = "Unknown"


    for line in lines[1:6]:

        clean = line.strip()

        if (
            len(clean) > 5
            and "አንቀጽ" not in clean
        ):
            title = clean
            break



    chunks.append({

        "chunk_id": len(chunks)+1,

        "article": 
        f"Article {article_number}",

        "title": title,

        "source":
        "Ethiopia_Constitution_Amharic.pdf",

        "page":
        "Unknown",

        "text":
        article_text,

        "length":
        len(article_text)

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
    "Articles created:",
    len(chunks)
)

print(
    "Saved:",
    OUTPUT_FILE
)