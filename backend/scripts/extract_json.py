import re
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


client = genai.Client(
    api_key=API_KEY
)


MODEL_NAME = "gemini-3.1-flash-lite"



INPUT_FILE = Path(
    "output/constitution_full.txt"
)


OUTPUT_FILE = Path(
    "data/fdre_constitution_articles.json"
)


MAX_ARTICLES = 15



def extract_articles(text):

    articles = []


    pattern = (
        r"(አንቀጽ\s*\d+)"
        r"(.*?)(?=አንቀጽ\s*\d+|$)"
    )


    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )


    existing = set()


    for title, content in matches:


        number_match = re.search(
            r"\d+",
            title
        )


        if not number_match:
            continue


        article_number = number_match.group()


        if article_number in existing:
            continue


        existing.add(
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
                "title": title.strip(),
                "content": clean_content
            }
        )


    return articles





def generate_metadata(content):


    prompt = f"""

እርስዎ የሕግ ሰነድ መረጃ ማውጫ ረዳት ነዎት።

የሚከተለውን የኢትዮጵያ ሕገ መንግሥት አንቀጽ ይመርምሩ።

Topic እና Keywords ያመንጩ።

ONLY valid JSON ይመልሱ።


Format:

{{
 "topic": "አጭር የሕግ ርዕስ",
 "keywords": [
    "ቁልፍ ቃል 1",
    "ቁልፍ ቃል 2",
    "ቁልፍ ቃል 3",
    "ቁልፍ ቃል 4",
    "ቁልፍ ቃል 5"
 ]
}}


አንቀጽ:

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
            "topic": "የሕገ መንግሥት ድንጋጌ",
            "keywords": [
                "ሕግ",
                "መብት"
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
                f"eth_const_{int(article['number']):03d}",


                "title":
                "የኢትዮጵያ ፌዴራላዊ ዲሞክራሲያዊ ሪፐብሊክ ሕገ መንግሥት",


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
                "FDRE Constitution (Amharic)"
            }
        )


    return dataset





def main():


    if not INPUT_FILE.exists():

        print(
            "❌ constitution_full.txt not found"
        )

        return



    text = INPUT_FILE.read_text(
        encoding="utf-8"
    )


    print(
        "Extracting Amharic articles..."
    )


    articles = extract_articles(
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


    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )


    print(
        "✅ JSON created successfully"
    )


    print(
        f"Saved: {OUTPUT_FILE}"
    )





if __name__ == "__main__":

    main()