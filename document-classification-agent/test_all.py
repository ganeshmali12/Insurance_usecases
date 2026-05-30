import json
import os
from PIL import Image
from classifier import classify_document

# --------------------------------------------------
# Helper — generate JPG and single-page PDF from PNG
# --------------------------------------------------
def make_test_files(png_path):
    """Create JPG and PDF versions of a PNG sample for format testing."""
    base = png_path.replace(".png", "")
    jpg_path = base + "_test.jpg"
    pdf_path = base + "_test.pdf"

    img = Image.open(png_path).convert("RGB")
    img.save(jpg_path, "JPEG", quality=90)
    img.save(pdf_path, "PDF")

    return jpg_path, pdf_path


def cleanup(paths):
    for p in paths:
        if os.path.exists(p):
            os.remove(p)


# --------------------------------------------------
# Test cases: (expected_type, file_path)
# --------------------------------------------------
SAMPLE_DOCS = [
    ("Invoice",           "data/sample_docs/invoice_sample.png"),
    ("Claim Form",        "data/sample_docs/claim_form_sample.png"),
    ("Inspection Report", "data/sample_docs/inspection_report_sample.png"),
]

# Build full test list: PNG + JPG + PDF for each doc + Unknown PDF
test_cases = []
generated_files = []

for expected, png_path in SAMPLE_DOCS:
    jpg_path, pdf_path = make_test_files(png_path)
    generated_files += [jpg_path, pdf_path]
    test_cases.append((expected, png_path,  "PNG"))
    test_cases.append((expected, jpg_path,  "JPG"))
    test_cases.append((expected, pdf_path,  "PDF (scanned)"))

# Unknown document — a non-insurance native PDF
test_cases.append(("Unknown", "data/uploads/Abcdefghigklamgnondrere.pdf", "PDF (native/digital)"))

# --------------------------------------------------
# Run tests
# --------------------------------------------------
all_pass = True
results_summary = []

for expected, path, fmt in test_cases:
    print("=" * 60)
    print(f"Format   : {fmt}")
    print(f"File     : {path}")
    print(f"Expected : {expected}")

    result = classify_document(path)
    got    = result["document_type"]
    conf   = result["confidence"]
    reason = result["reason"]
    status = "PASS" if got == expected else "FAIL"
    if got != expected:
        all_pass = False

    print(f"Got      : {got}  (confidence: {conf})")
    print(f"Reason   : {reason}")
    print(f"Result   : {status}")
    print()
    results_summary.append((fmt, expected, got, conf, status))

# --------------------------------------------------
# Cleanup generated test files
# --------------------------------------------------
cleanup(generated_files)

# --------------------------------------------------
# Summary table
# --------------------------------------------------
print("=" * 60)
print(f"{'Format':<22} {'Expected':<22} {'Got':<22} {'Conf':<6} {'Status'}")
print("-" * 60)
for fmt, expected, got, conf, status in results_summary:
    print(f"{fmt:<22} {expected:<22} {got:<22} {conf:<6} {status}")
print("=" * 60)
print("ALL TESTS PASSED" if all_pass else "SOME TESTS FAILED")

