import os
import json
from dotenv import load_dotenv
from utils.ocr_utils import extract_text
from openai import AzureOpenAI

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Azure OpenAI Client
# --------------------------------------------------
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

# --------------------------------------------------
# Supported Document Types
# --------------------------------------------------
DOCUMENT_TYPES = [
    "Claim Form",
    "Inspection Report",
    "Invoice",
    "Policy Document",
    "Medical Bill",
    "Unknown"
]

# --------------------------------------------------
# LLM Classification — always runs, no blocking gates
# --------------------------------------------------
def llm_classify(text: str) -> dict:
    prompt = f"""You are an expert insurance document classifier.

Read the following text extracted from a scanned document using OCR and classify it.
Note: OCR may produce some garbled characters from form tables — focus on the readable parts.

Supported document types:
- Claim Form: contains policy/claim number, patient or claimant info, incident or medical details, subscriber info
- Inspection Report: contains inspection findings, surveyor/inspector details, property or damage assessment, four-point inspection
- Invoice: contains invoice number, billing line items, price/amount columns, total charges, service fees
- Policy Document: contains policy terms, coverage details, premium amounts, exclusions
- Medical Bill: contains patient details, hospital or clinic charges, treatment item costs
- Unknown: truly unrecognizable content, blank, or completely unrelated to insurance

Instructions:
- Use semantic understanding of the full text — do NOT rely only on keywords.
- Even if OCR produced some garbled text, classify based on the readable portions.
- Each document type has distinct characteristics — use them all:
  * Invoice → look for line items with prices and a TOTAL
  * Claim Form → look for claimant/patient name, policy number, incident description
  * Inspection Report → look for inspection, surveyor, property condition, four-point
- Only return Unknown if the readable text gives no clear signal at all.
- Provide a real confidence score: 0.9+ if very clear, 0.6-0.8 if mostly clear, below 0.5 if uncertain.

Return ONLY valid JSON in this exact format:
{{
  "document_type": "<type from the list above>",
  "confidence": <number between 0.0 and 1.0>,
  "reason": "<one sentence explaining what evidence in the text led to this classification>"
}}

Document text:
{text[:4000]}"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=300
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if LLM wraps response in ```json ... ```
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    result = json.loads(raw)

    # Validate document_type is one of the known types
    if result.get("document_type") not in DOCUMENT_TYPES:
        result["document_type"] = "Unknown"

    return result


# --------------------------------------------------
# Main Classification Pipeline
# --------------------------------------------------
def classify_document(file_path: str) -> dict:
    # Step 1: Extract text via OCR
    try:
        text = extract_text(file_path)
    except Exception as e:
        return {
            "document_type": "Unknown",
            "confidence": 0.0,
            "reason": f"Could not read file: {str(e)}"
        }

    print(f"[DEBUG] Extracted text length: {len(text.strip())} chars")
    print(f"[DEBUG] Text preview:\n{text[:500]}\n")

    # Step 2: If truly no text at all, return Unknown immediately
    if not text or len(text.strip()) < 20:
        return {
            "document_type": "Unknown",
            "confidence": 0.0,
            "reason": "No readable text could be extracted from the document"
        }

    # Step 3: Send all text directly to LLM — no keyword gates
    try:
        return llm_classify(text)
    except json.JSONDecodeError:
        return {
            "document_type": "Unknown",
            "confidence": 0.0,
            "reason": "LLM returned an unexpected response format"
        }
    except Exception as e:
        return {
            "document_type": "Unknown",
            "confidence": 0.0,
            "reason": f"Classification failed: {str(e)}"
        }


# --------------------------------------------------
# Local Test
# --------------------------------------------------
if __name__ == "__main__":
    file_path = "data/sample_docs/invoice_sample.png"
    result = classify_document(file_path)
    print(json.dumps(result, indent=2))
