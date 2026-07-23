import json
import os


def load_legal_content(language="am"):

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    if language == "am":
     file_name = "fdre_constitution_articles.json"
    else:
     file_name = "fdre_constitution_english.json"

    file_path = os.path.join(
        base_dir,
        "data",
        file_name
    )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def search_legal_content(question, language="am"):

    legal_data = load_legal_content(language)

    question = question.lower().strip()

    best_match = None
    highest_score = 0

    for item in legal_data:

        score = 0

        # Article matching
        if item.get("article"):
            if item["article"].lower() in question:
                score += 5

        # Topic matching
        if item.get("topic"):
            if item["topic"].lower() in question:
                score += 3

        # Title matching
        if item.get("title"):
            if item["title"].lower() in question:
                score += 2

        # Keyword matching
        for keyword in item.get("keywords", []):

            if keyword.lower() in question:
                score += 1


        # Content matching
        if item.get("content"):
            if item["content"].lower() in question:
                score += 1


        if score > highest_score:
            highest_score = score
            best_match = item


    return best_match


def format_legal_response(result):

    if not result:
        return (
            "ይቅርታ፣ በሕግ መረጃ ውሂብ ውስጥ "
            "ተዛማጅ መረጃ አልተገኘም።"
        )

    response = f"""
ርዕስ: {result['title']}

አንቀጽ: {result['article']}

ርዕስ:
{result['topic']}

መልስ:
{result['content']}

ምንጭ:
{result['source']}
"""

    return response.strip()