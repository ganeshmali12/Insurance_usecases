import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageOps
import os

# Set tesseract path (Windows users only)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image for OCR.
    - 2x upscale gives Tesseract more pixels to work with
    - Grayscale removes color confusion without destroying character detail
    - autocontrast normalises brightness across different scan/print qualities
    No binary threshold — that destroys small colored text (e.g. teal invoices).
    The confidence filter in _ocr_image handles noise separately.
    """
    w, h = image.size
    if w < 2000:
        image = image.resize((w * 2, h * 2), Image.LANCZOS)

    image = image.convert("L")
    image = ImageOps.autocontrast(image, cutoff=1)

    return image


def _ocr_image(image: Image.Image) -> str:
    """
    Run Tesseract on a preprocessed image.
    Uses word-level confidence filtering to discard OCR noise caused by
    table borders and form cell lines, keeping only reliably recognised text.
    """
    processed = preprocess_image(image)
    config = "--oem 3 --psm 6"

    data = pytesseract.image_to_data(
        processed,
        config=config,
        output_type=pytesseract.Output.DICT
    )

    lines = {}
    for i, word in enumerate(data["text"]):
        word = word.strip()
        conf = int(data["conf"][i])
        line_key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])

        # Keep words with confidence >= 40; skip empty strings and noise
        if conf >= 40 and word:
            lines.setdefault(line_key, []).append(word)

    return "\n".join(" ".join(words) for words in lines.values()).strip()


def extract_text(file_path: str) -> str:
    """
    Extract text from PDF or Image using Tesseract OCR
    """
    text = ""

    if file_path.lower().endswith(".pdf"):
        pages = convert_from_path(file_path, dpi=300)
        for page in pages:
            text += _ocr_image(page) + "\n"

    else:
        image = Image.open(file_path)
        text = _ocr_image(image)

    return text.strip()
