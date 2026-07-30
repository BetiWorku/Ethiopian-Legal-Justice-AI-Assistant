from pathlib import Path
import fitz
import pytesseract
import cv2
import numpy as np
from PIL import Image

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ==========================
# Project Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = BASE_DIR / "data" / "documents"

OUTPUT_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "extracted_pages.txt"

# ==========================
# OpenCV Image Preprocessing
# ==========================

def preprocess_image_for_ocr(pil_image):
    """
    Uses OpenCV to clean and prepare a scanned legal document for Tesseract OCR.
    """
    # Convert PIL Image to OpenCV format (NumPy array)
    img = np.array(pil_image)
    
    # Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Binarization using Otsu's Thresholding (Separates text from background)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Noise Removal (Morphological Opening)
    kernel = np.ones((1, 1), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    return cleaned

# ==========================
# Direct PDF Text Extraction
# ==========================

def extract_text_from_pdf(pdf_path):
    print("Trying direct text extraction...")
    pages = []
    doc = fitz.open(pdf_path)

    for page_number, page in enumerate(doc, start=1):
        text = page.get_text()
        pages.append({
            "source": pdf_path.name,
            "page": page_number,
            "text": text.strip()
        })

    doc.close()
    return pages

# ==========================
# OCR Extraction (with OpenCV)
# ==========================

def extract_text_with_ocr(pdf_path):
    print("Running OCR with OpenCV preprocessing...")
    pages = []
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    for index, page in enumerate(doc, start=1):
        print(f"OCR processing page {index}/{total_pages}")

        # Render PDF page to image
        pix = page.get_pixmap(dpi=300)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Preprocess the image using OpenCV
        processed_img = preprocess_image_for_ocr(image)

        # OCR Amharic + English on the cleaned OpenCV image
        text = pytesseract.image_to_string(processed_img, lang="amh+eng")

        pages.append({
            "source": pdf_path.name,
            "page": index,
            "text": text.strip()
        })

    doc.close()
    return pages

# ==========================
# Hybrid Decision Rule
# ==========================

def process_pdf(pdf_path):
    print(f"\nProcessing PDF: {pdf_path.name}")
    
    extracted_pages = extract_text_from_pdf(pdf_path)
    
    readable_pages = [
        page for page in extracted_pages if len(page["text"]) > 50
    ]

    # If enough text exists
    if len(readable_pages) == len(extracted_pages):
        print("✓ Text layer available. Using direct extraction.")
        return extracted_pages
    else:
        print("⚠ Text layer not sufficient. Switching to OCR.")
        return extract_text_with_ocr(pdf_path)

# ==========================
# Save Raw Page Output
# ==========================

def save_output(pages):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        for page in pages:
            file.write("\n\n=================================\n")
            file.write(f"SOURCE: {page['source']}\n")
            file.write(f"PAGE: {page['page']}\n")
            file.write("=================================\n\n")
            file.write(page["text"])

    print("\nSaved raw output:")
    print(OUTPUT_FILE)

# ==========================
# Main
# ==========================

if __name__ == "__main__":
    pdf_files = list(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/documents")
        exit()

    print("\nFound PDF files:")
    for pdf in pdf_files:
        print("-", pdf.name)

    all_pages = []

    for pdf in pdf_files:
        pages = process_pdf(pdf)
        all_pages.extend(pages)

    save_output(all_pages)