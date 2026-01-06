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
    "Unknown"
]

# --------------------------------------------------
# Rule-based scoring
# --------------------------------------------------
def rule_based_scores(text: str) -> dict:
    text = text.lower()

    scores = {
        "Claim Form": 0,
        "Inspection Report": 0,
        "Invoice": 0
    }

    # Claim Form rules
    if "policy number" in text:
        scores["Claim Form"] += 1
    if "claim number" in text:
        scores["Claim Form"] += 1

    # Inspection Report rules
    if "surveyor" in text:
        scores["Inspection Report"] += 1
    if "inspection date" in text or "damage assessment" in text:
        scores["Inspection Report"] += 1

    # Invoice rules
    if "invoice" in text:
        scores["Invoice"] += 1
    if "total amount" in text or "gst" in text:
        scores["Invoice"] += 1

    return scores


# --------------------------------------------------
# Insurance-domain validation
# --------------------------------------------------
def is_insurance_related(text: str) -> bool:
    keywords = [
        "insurance",
        "policy",
        "claim",
        "invoice",
        "surveyor",
        "insured",
        "damage",
        "gst",
        "premium"
    ]

    text = text.lower()
    matches = sum(1 for k in keywords if k in text)

    return matches >= 2


# --------------------------------------------------
# Minimum rule score check
# --------------------------------------------------
def has_minimum_rule_score(rule_scores: dict) -> bool:
    return max(rule_scores.values()) >= 1


# --------------------------------------------------
# LLM Classification (Azure OpenAI)
# --------------------------------------------------
def llm_classify(text: str, rule_scores: dict) -> dict:
    prompt = f"""
You are an insurance document classification AI.

Document types:
- Claim Form
- Inspection Report
- Invoice
- Unknown

Rule-based hints:
{json.dumps(rule_scores, indent=2)}

Instructions:
- Use semantic understanding, not just keywords.
- If the document does NOT clearly match an insurance document,
  return "Unknown" with low confidence.
- Do NOT guess.

Return JSON ONLY in this format:

{{
  "document_type": "<type>",
  "confidence": <0-1>,
  "reason": "<short explanation>"
}}

Document text:
{text[:3000]}
"""

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)


# --------------------------------------------------
# Main Classification Pipeline (SAFE VERSION)
# --------------------------------------------------
def classify_document(file_path: str) -> dict:
    text = extract_text(file_path)

    # 1️⃣ No text / very small text
    if not text or len(text.strip()) < 50:
        return {
            "document_type": "Unknown",
            "confidence": 0.0,
            "reason": "No meaningful readable text found"
        }

    # 2️⃣ Not insurance-related
    if not is_insurance_related(text):
        return {
            "document_type": "Unknown",
            "confidence": 0.2,
            "reason": "Document is not insurance-related"
        }

    # 3️⃣ Rule-based pattern check
    rules = rule_based_scores(text)

    if not has_minimum_rule_score(rules):
        return {
            "document_type": "Unknown",
            "confidence": 0.3,
            "reason": "No insurance document patterns detected"
        }

    # 4️⃣ Final LLM decision
    return llm_classify(text, rules)


# --------------------------------------------------
# Local Test
# --------------------------------------------------
if __name__ == "__main__":
    file_path = "data/sample_docs/invoice_sample.png"
    result = classify_document(file_path)
    print(json.dumps(result, indent=2))
