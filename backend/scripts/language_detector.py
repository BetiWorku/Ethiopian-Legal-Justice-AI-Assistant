def detect_language(text):
    """
    Returns:
        "am" -> Amharic
        "en" -> English
    """

    for char in text:
        if '\u1200' <= char <= '\u137F':
            return "am"

    return "en"