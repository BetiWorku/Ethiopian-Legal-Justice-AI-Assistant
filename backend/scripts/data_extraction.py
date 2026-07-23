import fitz
import json
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DOCUMENTS_DIR = BASE_DIR / "data" / "documents"


def extract_text_from_pdf(pdf_path):

    print(f"Opening: {pdf_path}")

    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        return ""

    document = fitz.open(str(pdf_path))

    print(f"Number of pages: {len(document)}")

    text = ""

    for page_number, page in enumerate(document):

        page_text = page.get_text()

        print(
            f"Page {page_number + 1}: "
            f"{len(page_text)} characters"
        )

        text += page_text + "\n"

    document.close()

    return text


def save_as_json(text, output_path, language):

    data = {
        "language": language,
        "source": output_path.name,
        "content": text
    }

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


def main():

    english_pdf = (
        DOCUMENTS_DIR /
        "Ethiopia_Constitution_English.pdf"
    )

    amharic_pdf = (
        DOCUMENTS_DIR /
        "Ethiopia_Constitution_Amharic.pdf"
    )

    english_output = (
        BASE_DIR /
        "data" /
        "legal_knowledge.json"
    )

    amharic_output = (
        BASE_DIR /
        "data" /
        "legal_knowledge_am.json"
    )

    english_text = extract_text_from_pdf(
        english_pdf
    )

    amharic_text = extract_text_from_pdf(
        amharic_pdf
    )

    save_as_json(
        english_text,
        english_output,
        "English"
    )

    save_as_json(
        amharic_text,
        amharic_output,
        "Amharic"
    )

    print("\n✅ Extraction completed!")


if __name__ == "__main__":
    main()