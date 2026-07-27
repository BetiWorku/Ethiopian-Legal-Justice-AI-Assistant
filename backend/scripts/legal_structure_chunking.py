import json
import re
from pathlib import Path


# ==========================
# Paths
# ==========================

INPUT_FILE = Path("data/raw/extracted_pages.txt")

OUTPUT_FILE = Path(
    "data/chunks/article_chunks.json"
)


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)



# ==========================
# Load text
# ==========================

print("Loading extracted pages...")


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    text = f.read()



# ==========================
# Extract pages
# ==========================

def extract_pages(text):

    pages = []

    pattern = r"PAGE:\s*(\d+)(.*?)(?=PAGE:\s*\d+|$)"


    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )


    for page_number, content in matches:

        pages.append(
            {
                "page": int(page_number),
                "text": content.strip()
            }
        )


    return pages



# ==========================
# Extract articles
# ==========================

pages = extract_pages(text)


print(
    "Pages detected:",
    len(pages)
)


chunks = []

seen_articles = set()



for page in pages:


    page_text = page["text"]


    matches = list(
        re.finditer(
            r"አንቀጽ\s+(\d+)",
            page_text
        )
    )


    for i, match in enumerate(matches):


        article_number = match.group(1)



        # avoid duplicate articles
        if article_number in seen_articles:
            continue


        seen_articles.add(
            article_number
        )



        start = match.start()



        if i + 1 < len(matches):

            end = matches[i+1].start()

        else:

            end = len(page_text)



        article_text = page_text[start:end].strip()



        # remove very small noise

        if len(article_text) < 100:
            continue



        # Extract title

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



        chunks.append(

            {

                "chunk_id":
                    len(chunks)+1,


                "article":
                    f"Article {article_number}",


                "title":
                    title,


                "source":
                    "Ethiopia_Constitution_Amharic.pdf",


                "page":
                    page["page"],


                "text":
                    article_text,


                "length":
                    len(article_text)

            }

        )



# ==========================
# Save JSON
# ==========================


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