import re
import json
from pathlib import Path

# Input OCR text
INPUT_FILE = Path("output/constitution_full.txt")

# Output JSON file
OUTPUT_FILE = Path("data/fdre_constitution_articles.json")

# Only the articles we want
TARGET_ARTICLES = [13, 14, 15, 16, 17, 18, 19, 20, 25, 29]

ARTICLE_INFO = {
    13: {
        "topic": "መሰረታዊ መብቶችና ነፃነቶች",
        "keywords": ["መብት", "ነፃነት", "ሕገ መንግሥት", "አንቀጽ 13"]
    },
    14: {
        "topic": "የሕይወት መብት",
        "keywords": ["ሕይወት", "መብት", "አንቀጽ 14"]
    },
    15: {
        "topic": "የሕይወት ጥበቃ",
        "keywords": ["ሕይወት", "ጥበቃ", "አንቀጽ 15"]
    },
    16: {
        "topic": "የሰው አካል ደህንነት",
        "keywords": ["ሰው", "ደህንነት", "አንቀጽ 16"]
    },
    17: {
        "topic": "የነፃነት መብት",
        "keywords": ["ነፃነት", "እስር", "አንቀጽ 17"]
    },
    18: {
        "topic": "ኢሰብአዊ አያያዝ ክልከላ",
        "keywords": ["ማሰቃየት", "ሰብዓዊ", "አንቀጽ 18"]
    },
    19: {
        "topic": "የተከሳሽ መብቶች",
        "keywords": ["ተከሳሽ", "መብት", "አንቀጽ 19"]
    },
    20: {
        "topic": "ፍትሃዊ ፍርድ የማግኘት መብት",
        "keywords": ["ፍርድ", "ፍትሕ", "አንቀጽ 20"]
    },
    25: {
        "topic": "በሕግ ፊት እኩልነት",
        "keywords": ["እኩልነት", "ሕግ", "አንቀጽ 25"]
    },
    29: {
        "topic": "የመናገርና የመግለጽ ነፃነት",
        "keywords": ["መናገር", "መግለጽ", "ነፃነት", "አንቀጽ 29"]
    }
}


def extract_articles(text):
    articles = []

    for i, article_num in enumerate(TARGET_ARTICLES):

        if i < len(TARGET_ARTICLES) - 1:
            next_article = TARGET_ARTICLES[i + 1]
            pattern = rf"አንቀጽ\s*{article_num}\s*(.*?)(?=አንቀጽ\s*{next_article})"
        else:
            pattern = rf"አንቀጽ\s*{article_num}\s*(.*)$"

        match = re.search(pattern, text, re.DOTALL)

        if match:
            content = re.sub(r"\s+", " ", match.group(1)).strip()

            articles.append({
                "id": f"eth_const_{article_num:03d}",
                "title": "የኢትዮጵያ ፌዴራላዊ ዲሞክራሲያዊ ሪፐብሊክ ሕገ መንግሥት",
                "article": f"አንቀጽ {article_num}",
                "topic": ARTICLE_INFO[article_num]["topic"],
                "keywords": ARTICLE_INFO[article_num]["keywords"],
                "content": content,
                "source": "FDRE Constitution (Amharic)"
            })

    return articles


def main():

    if not INPUT_FILE.exists():
        print("❌ constitution_full.txt not found")
        return

    text = INPUT_FILE.read_text(encoding="utf-8")

    articles = extract_articles(text)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Created {OUTPUT_FILE}")
    print(f"✅ Extracted {len(articles)} articles")


if __name__ == "__main__":
    main()