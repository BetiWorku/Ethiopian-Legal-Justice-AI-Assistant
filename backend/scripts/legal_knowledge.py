import json
import os
import re



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


    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)





def search_legal_content(question, language="am"):


    legal_data = load_legal_content(language)


    question_lower = question.lower().strip()


    best_match = None
    highest_score = 0



    article_match = re.search(
        r"(article|አንቀጽ)\s*(\d+)",
        question_lower
    )


    requested_article = None


    if article_match:

        requested_article = article_match.group(2)



    for item in legal_data:


        score = 0



        article_text = item.get(
            "article",
            ""
        ).lower()



        # Article number matching

        if requested_article:


            item_number = re.search(
                r"\d+",
                article_text
            )


            if item_number:

                if item_number.group() == requested_article:

                    score += 10





        # Topic matching

        topic = item.get(
            "topic",
            ""
        ).lower()


        if topic and topic in question_lower:

            score += 3





        # Keyword matching

        for keyword in item.get(
            "keywords",
            []
        ):


            if keyword.lower() in question_lower:

                score += 1





        if score > highest_score:

            highest_score = score

            best_match = item





    return best_match