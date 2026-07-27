from pathlib import Path
import json
import re


# ==========================
# Paths
# ==========================

INPUT_FILE = Path("data/raw/extracted_pages.txt")

OUTPUT_DIR = Path("data/chunks")
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE = OUTPUT_DIR / "legal_chunks.json"



# ==========================
# Chunk Settings
# ==========================

CHUNK_SIZE = 1200
OVERLAP = 200



# ==========================
# Read text
# ==========================

def read_text():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



# ==========================
# Clean OCR text
# ==========================

def clean_text(text):

    # Remove page separators
    text = re.sub(
        r"={10,}",
        "",
        text
    )


    # Remove SOURCE line
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


    # Remove extra empty lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )


    return text.strip()



# ==========================
# Extract pages
# ==========================

def extract_pages(text):

    pages = []

    pattern = r"PAGE:\s*(\d+)(.*?)(?=PAGE:\s*\d+|$)"


    matches = re.findall(
        pattern,
        text,
        re.DOTALL
    )


    for page_number, content in matches:

        pages.append(
            {
                "page": int(page_number),
                "text": content.strip()
            }
        )


    return pages



# ==========================
# Create chunks
# ==========================

def create_chunks(pages):

    chunks = []

    chunk_id = 1


    for page in pages:

        text = clean_text(page["text"])

        start = 0


        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end]


            # stop creating very small chunks
            if len(chunk_text.strip()) < 200:
                break


            # split at space
            if end < len(text):

                last_space = chunk_text.rfind(" ")

                if last_space != -1:
                    end = start + last_space
                    chunk_text = text[start:end]


            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "source": "Ethiopia_Constitution_Amharic.pdf",
                    "page": page["page"],
                    "text": chunk_text.strip(),
                    "length": len(chunk_text.strip())
                }
            )


            chunk_id += 1


            start = end - OVERLAP


    return chunks

    chunks = []

    chunk_id = 1


    for page in pages:

        text = clean_text(
            page["text"]
        )


        start = 0


        while start < len(text):

            end = start + CHUNK_SIZE


            chunk_text = text[start:end]


            if end < len(text):

                last_space = chunk_text.rfind(" ")

                if last_space != -1:

                    end = start + last_space

                    chunk_text = text[start:end]


            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "source": "Ethiopia_Constitution_Amharic.pdf",
                    "page": page["page"],
                    "text": chunk_text.strip(),
                    "length": len(chunk_text.strip())
                }
            )


            chunk_id += 1


            start = end - OVERLAP


    return chunks



# ==========================
# Save JSON
# ==========================

def save_chunks(chunks):

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=4
        )


    print(
        f"Saved {len(chunks)} chunks"
    )

    print(
        OUTPUT_FILE
    )



# ==========================
# Main
# ==========================

if __name__ == "__main__":

    print("Reading text...")

    text = read_text()


    print(
        "Characters:",
        len(text)
    )


    pages = extract_pages(
        text
    )


    print(
        "Pages detected:",
        len(pages)
    )


    chunks = create_chunks(
        pages
    )


    save_chunks(
        chunks
    )