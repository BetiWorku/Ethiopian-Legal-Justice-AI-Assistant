def detect_language(text):

    amharic_count = 0
    english_count = 0


    for char in text:
     if '\u1200' <= char <= '\u137F':
        return "am"

    return "en"


    if amharic_count > english_count:
        return "am"

    return "en"