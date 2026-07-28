import re


def detect_language(text):

    if not text:
        return "en"


    amharic_count = 0
    english_count = 0


    for char in text:

        # Amharic Unicode range
        if '\u1200' <= char <= '\u137F':

            amharic_count += 1


        elif ('a' <= char.lower() <= 'z'):

            english_count += 1



    if amharic_count > english_count:

        return "am"


    return "en"