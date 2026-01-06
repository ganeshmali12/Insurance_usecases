import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Set tesseract path (Windows users only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(file_path: str) -> str:
    """
    Extract text from PDF or Image using Tesseract OCR
    """
    text = ""

    if file_path.lower().endswith(".pdf"):
        pages = convert_from_path(file_path)
        for page in pages:
            text += pytesseract.image_to_string(page)

    else:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)

    return text.strip()
