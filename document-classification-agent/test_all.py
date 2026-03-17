import json
from classifier import classify_document

docs = [
    ("Invoice",           "data/sample_docs/invoice_sample.png"),
    ("Claim Form",        "data/sample_docs/claim_form_sample.png"),
    ("Inspection Report", "data/sample_docs/inspection_report_sample.png"),
]

all_pass = True
for expected, path in docs:
    print("=" * 60)
    print("Expected :", expected)
    result = classify_document(path)
    got = result["document_type"]
    conf = result["confidence"]
    reason = result["reason"]
    status = "PASS" if got == expected else "FAIL"
    if got != expected:
        all_pass = False
    print("Got      :", got, " (confidence:", conf, ")")
    print("Reason   :", reason)
    print("Result   :", status)
    print()

print("=" * 60)
print("ALL TESTS PASSED" if all_pass else "SOME TESTS FAILED")
