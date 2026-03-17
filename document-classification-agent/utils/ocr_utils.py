import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import os

# Set tesseract path (Windows users only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image to improve OCR accuracy on colored/stylized documents.
    Steps: convert to grayscale, enhance contrast, sharpen.
    """
    # Convert to grayscale (removes color confusion from teal/blue text)
    image = image.convert("L")

    # Enhance contrast so light-colored text becomes darker
    image = ImageEnhance.Contrast(image).enhance(2.5)

    # Sharpen edges so characters are crisper
    image = image.filter(ImageFilter.SHARPEN)

    # Scale up small images — Tesseract works best at 300 DPI equivalent
    w, h = image.size
    if w < 1500:
        scale = 2
        image = image.resize((w * scale, h * scale), Image.LANCZOS)

    return image


def extract_text(file_path: str) -> str:
    """
    Extract text from PDF or Image using Tesseract OCR
    """
    text = ""

    if file_path.lower().endswith(".pdf"):
        pages = convert_from_path(file_path)
        for page in pages:
            processed = preprocess_image(page)
            text += pytesseract.image_to_string(processed)

    else:
        image = Image.open(file_path)
        processed = preprocess_image(image)
        text = pytesseract.image_to_string(processed)

    return text.strip()
