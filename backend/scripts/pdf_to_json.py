import json
import re
import os
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai


load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

client = genai.Client(
    api_key=API_KEY
)

MODEL_NAME = "gemini-3.1-flash-lite"


PDF_PATH = Path(
    "data/documents/Ethiopia_Constitution_English.pdf"
)

OUTPUT_PATH = Path(
    "data/fdre_constitution_english.json"
)

MAX_ARTICLES = 15



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

    existing_articles = set()

    pattern = (
        r"(Article\s+\d+)"
        r"(.*?)(?=Article\s+\d+|$)"
    )

    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )


    for article_title, content in matches:

        number_match = re.search(
            r"\d+",
            article_title
        )

        if not number_match:
            continue


        article_number = number_match.group()


        if article_number in existing_articles:
            continue


        existing_articles.add(
            article_number
        )


        clean_content = re.sub(
            r"\s+",
            " ",
            content
        ).strip()


        articles.append(
            {
                "number": article_number,
                "title": article_title.strip(),
                "content": clean_content
            }
        )


    return articles



def generate_metadata(content):

    prompt = f"""

You are a legal information extraction assistant.

Analyze the following FDRE Constitution article.

Return ONLY valid JSON.

Format:

{{
 "topic": "short legal topic",
 "keywords": [
    "keyword1",
    "keyword2",
    "keyword3",
    "keyword4",
    "keyword5"
 ]
}}

Article:

{content}

"""


    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )


    result = response.text.strip()


    if result.startswith("```"):

        result = (
            result
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    try:

        return json.loads(result)

    except Exception:

        return {
            "topic": "Constitutional Provision",
            "keywords": [
                "law",
                "rights"
            ]
        }



def create_json(articles):

    dataset = []


    for article in articles:

        print(
            f"Processing Article {article['number']}..."
        )


        metadata = generate_metadata(
            article["content"]
        )


        dataset.append(
            {
                "id":
                f"fdre_const_article_{article['number']}",

                "title":
                "FDRE Constitution",

                "article":
                article["title"],

                "topic":
                metadata.get(
                    "topic",
                    ""
                ),

                "keywords":
                metadata.get(
                    "keywords",
                    []
                ),

                "content":
                article["content"],

                "source":
                "FDRE Constitution 1995 - Official English PDF"
            }
        )


    return dataset



def save_json(data, output_path):

    output_path.parent.mkdir(
        exist_ok=True
    )


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

    print(
        "Reading PDF..."
    )


    text = extract_text_from_pdf(
        PDF_PATH
    )


    print(
        "Extracting all articles..."
    )


    articles = split_articles(
        text
    )


    print(
        f"Found total {len(articles)} articles"
    )


    articles = articles[:MAX_ARTICLES]


    print(
        f"Processing only {len(articles)} articles"
    )


    print(
        "Generating Gemini metadata..."
    )


    data = create_json(
        articles
    )


    save_json(
        data,
        OUTPUT_PATH
    )


    print(
        "✅ JSON created successfully!"
    )


    print(
        f"Saved: {OUTPUT_PATH}"
    )