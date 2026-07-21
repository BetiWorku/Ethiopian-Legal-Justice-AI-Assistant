import json
import os


def load_legal_content():

    base_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    file_path = os.path.join(
        base_dir,
        "data",
        "sample_legal_content.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)



def search_legal_content(question):

    legal_data = load_legal_content()

    question = question.lower()

    best_match = None
    highest_score = 0

    for item in legal_data:

        score = 0

        # Check article
        if item["article"].lower() in question:
            score += 5

        # Check topic
        if item["topic"].lower() in question:
            score += 3

        # Check keywords
        for keyword in item["keywords"]:

            if keyword.lower() in question:
                score += 1

        if score > highest_score:
            highest_score = score
            best_match = item


    if highest_score == 0:
        return None

    return best_match