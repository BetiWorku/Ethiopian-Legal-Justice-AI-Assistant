import json
import re
from pypdf import PdfReader


PDF_PATH = "data/documents/Ethiopia_Constitution_English.pdf"
OUTPUT_PATH = "data/fdre_constitution_english.json"


SELECTED_ARTICLES = [
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "25",
    "29"
]


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    full_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text + "\n"

    return full_text


def split_articles(text):

    articles = []

    pattern = r"(Article\s+\d+)"

    sections = re.split(pattern, text)


    for i in range(1, len(sections), 2):

        article_title = sections[i]
        content = sections[i + 1]


        article_number = (
            article_title
            .replace("Article", "")
            .strip()
        )


        if article_number in SELECTED_ARTICLES:

            articles.append({

                "id": f"fdre_const_article_{article_number}",

                "title": "FDRE Constitution",

                "article": article_title.strip(),

                "topic": "",

                "keywords": [
                    f"Article {article_number}",
                    "FDRE Constitution",
                    "Human Rights"
                ],

                "content": content.strip(),

                "source": "Ethiopia Constitution PDF"

            })


    return articles



def save_json(data, output_path):

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )



if __name__ == "__main__":

    print("Reading PDF...")

    text = extract_text_from_pdf(PDF_PATH)


    print("Extracting Selected Articles...")


    articles = split_articles(text)


    print(
        f"Found {len(articles)} articles"
    )


    save_json(
        articles,
        OUTPUT_PATH
    )


    print(
        "JSON created successfully!"
    )