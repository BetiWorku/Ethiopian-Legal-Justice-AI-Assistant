from pathlib import Path
import re


# ==========================
# Paths
# ==========================

INPUT_FILE = Path(
    "data/raw/extracted_pages.txt"
)

OUTPUT_FILE = Path(
    "output/constitution_full.txt"
)


OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)



# ==========================
# Read Raw OCR Text
# ==========================

def read_text():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



# ==========================
# Cleaning Function
# ==========================

def clean_text(text):


    # Remove OCR page separators
    text = re.sub(
        r"={5,}",
        "",
        text
    )


    # Remove SOURCE metadata
    text = re.sub(
        r"SOURCE:.*",
        "",
        text
    )


    # Remove PAGE numbers
    text = re.sub(
        r"PAGE:\s*\d+",
        "",
        text
    )


    # Remove standalone numbers (page noise)
    text = re.sub(
        r"\n\d+\n",
        "\n",
        text
    )


    # Remove invalid OCR symbols
    text = re.sub(
        r"[■□◆●]+",
        "",
        text
    )


    # Normalize spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )


    # Fix too many empty lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )


    # Remove spaces around lines
    lines = []

    for line in text.split("\n"):

        clean_line = line.strip()

        if clean_line:
            lines.append(clean_line)


    text = "\n".join(lines)



    return text.strip()



# ==========================
# Save Clean Text
# ==========================

def save_text(text):

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(text)


    print(
        "Cleaning completed"
    )

    print(
        "Saved:",
        OUTPUT_FILE
    )



# ==========================
# Main
# ==========================

if __name__ == "__main__":


    print(
        "Loading raw OCR text..."
    )


    raw_text = read_text()


    print(
        "Original characters:",
        len(raw_text)
    )


    cleaned_text = clean_text(
        raw_text
    )


    print(
        "Cleaned characters:",
        len(cleaned_text)
    )


    save_text(
        cleaned_text
    )