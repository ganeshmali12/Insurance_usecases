import pytesseract
import pdfplumber
import fitz  # PyMuPDF — self-contained PDF renderer, no Poppler needed
from PIL import Image, ImageOps
import io
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


def _extract_native_pdf(file_path: str) -> str:
    """
    Extract embedded text directly from a native/digital PDF using pdfplumber.
    Returns empty string if the PDF has no embedded text (i.e. it is scanned).
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF or image file.

    For PDFs:
      1. Try native text extraction with pdfplumber (fast, perfect for
         digital PDFs like resumes, invoices created in Word/Docs etc.)
      2. If result is too short (<50 chars), the PDF is scanned —
         fall back to Tesseract OCR on rendered page images.

    Images are always processed with Tesseract OCR.
    """
    if file_path.lower().endswith(".pdf"):
        native_text = _extract_native_pdf(file_path)
        if len(native_text) >= 50:
            return native_text
        # Scanned PDF — fall back to OCR using PyMuPDF (no Poppler needed)
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            pix = page.get_pixmap(dpi=450)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text += _ocr_image(img) + "\n"
        doc.close()
        return text.strip()

    else:
        image = Image.open(file_path)
        return _ocr_image(image)
