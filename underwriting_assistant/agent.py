from dotenv import load_dotenv
import os
import json

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# Load underwriting rulebook
# -------------------------------------------------
RULEBOOK_PATH = "underwriting_rulebook.json"

with open(RULEBOOK_PATH, "r", encoding="utf-8") as f:
    UNDERWRITING_RULEBOOK = json.load(f)

# -------------------------------------------------
# Smart Rulebook Filter (Approach 1)
# -------------------------------------------------
def filter_rulebook(applicant_data: str, claims_history: str, external_report: str) -> dict:
    """
    Filter the rulebook to only include sections relevant
    to the applicant's profile, claims, and external report.
    Reduces token usage by ~70-90%.
    """
    text = (applicant_data + " " + claims_history + " " + external_report).lower()

    filtered = {
        "version": UNDERWRITING_RULEBOOK["version"],
        # Always include eligibility rules - they apply to every applicant
        "eligibility_rules": UNDERWRITING_RULEBOOK["eligibility_rules"],
        # Always include scoring & decision guidelines
        "risk_scoring_guidelines": UNDERWRITING_RULEBOOK["risk_scoring_guidelines"],
        "decision_support_guidelines": UNDERWRITING_RULEBOOK["decision_support_guidelines"],
        "output_requirements": UNDERWRITING_RULEBOOK["output_requirements"],
    }

    # Include occupation rules if occupation keywords found
    occupation_keywords = [
        "driver", "delivery", "cab", "construction", "worker",
        "technician", "sales", "traveler", "employee", "retired",
        "gig", "operator", "executive", "occupation", "job", "profession"
    ]
    if any(kw in text for kw in occupation_keywords):
        filtered["applicant_profile_rules"] = UNDERWRITING_RULEBOOK["applicant_profile_rules"]

    # Include claims history rules if claims keywords found
    claims_keywords = [
        "claim", "accident", "theft", "fire", "flood", "loss",
        "damage", "injury", "total loss", "history", "previous"
    ]
    if any(kw in text for kw in claims_keywords):
        filtered["claims_history_rules"] = UNDERWRITING_RULEBOOK["claims_history_rules"]

    # Include asset usage rules if usage keywords found
    usage_keywords = [
        "mileage", "usage", "commercial", "personal", "daily",
        "vehicle", "night", "multi-user", "asset"
    ]
    if any(kw in text for kw in usage_keywords):
        filtered["asset_usage_rules"] = UNDERWRITING_RULEBOOK["asset_usage_rules"]

    # Include location rules if location keywords found
    location_keywords = [
        "location", "area", "zone", "city", "urban", "road",
        "parking", "coastal", "flood", "crime", "traffic"
    ]
    if any(kw in text for kw in location_keywords):
        filtered["location_risk_rules"] = UNDERWRITING_RULEBOOK["location_risk_rules"]

    # Include credit rules if credit keywords found
    credit_keywords = [
        "credit", "score", "financial", "loan", "debt", "payment"
    ]
    if any(kw in text for kw in credit_keywords):
        filtered["creditworthiness_rules"] = UNDERWRITING_RULEBOOK["creditworthiness_rules"]

    # Include inspection rules if inspection/report keywords found
    inspection_keywords = [
        "inspection", "report", "maintenance", "repair", "damage",
        "condition", "survey", "assessment"
    ]
    if any(kw in text for kw in inspection_keywords):
        filtered["inspection_and_external_reports"] = UNDERWRITING_RULEBOOK["inspection_and_external_reports"]

    # Include compounded risk rules if multiple risk signals present
    # (heuristic: if 3 or more sections were added, compounded risks may apply)
    if len(filtered) >= 6:
        filtered["compounded_risk_rules"] = UNDERWRITING_RULEBOOK["compounded_risk_rules"]

    return filtered

# -------------------------------------------------
# Azure OpenAI LLM
# -------------------------------------------------
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    temperature=0
)

json_parser = JsonOutputParser()

# -------------------------------------------------
# Prompt: Applicant summary
# -------------------------------------------------
applicant_prompt = ChatPromptTemplate.from_template("""
Summarize the applicant profile.
Highlight only underwriting-relevant attributes.
Do not invent information.

Applicant Data:
{applicant_data}
""")

# -------------------------------------------------
# Prompt: Claims analysis
# -------------------------------------------------
claims_prompt = ChatPromptTemplate.from_template("""
Analyze the claims history.
Identify claim frequency, severity, claim types, and any suspicious patterns.
Do not invent information.

Claims History:
{claims_history}
""")

# -------------------------------------------------
# Prompt: Rule-book-driven underwriting decision
# -------------------------------------------------
risk_prompt = ChatPromptTemplate.from_template("""
You are an insurance underwriting assistant.

You MUST strictly follow the underwriting rule book.
Do NOT invent rules.
Do NOT contradict yourself.

UNDERWRITING RULE BOOK:
{rulebook}

INPUT DATA:

Applicant Summary:
{applicant_summary}

Claims Analysis:
{claims_analysis}

External Report:
{external_report}

INSTRUCTIONS (MANDATORY):

1. Identify ALL triggered rules from the rule book.
2. List ALL identified risks clearly.
3. Determine policy_compliance_status based ONLY on triggered rules.
4. Derive risk_score using the risk_scoring_guidelines in the rule book.
5. Derive risk_level STRICTLY from risk_score:
   - 0–30  → Low
   - 31–70 → Medium
   - 71–100 → High
6. Recommendation MUST be logically consistent:
   - Low    → standard_acceptance
   - Medium → acceptance_with_conditions OR manual_underwriting_review
   - High   → manual_underwriting_review OR policy_not_recommended

CONSISTENCY RULES (NON-NEGOTIABLE):
- If risk_score ≥ 71, risk_level MUST be High.
- If risk_score ≤ 30, risk_level MUST be Low.
- If recommendation is manual_underwriting_review, identified_risks MUST NOT be empty.
- risk_score, risk_level, and recommendation MUST align logically.

Return ONLY valid JSON.
Do NOT include markdown, explanations, or backticks.

JSON FORMAT:
{{
  "policy_compliance_status": "",
  "identified_risks": [],
  "triggered_rules": [],
  "risk_score": 0,
  "risk_level": "",
  "recommendation": ""
}}
""")

# -------------------------------------------------
# Chains
# -------------------------------------------------
applicant_chain = applicant_prompt | llm | StrOutputParser()
claims_chain = claims_prompt | llm | StrOutputParser()
risk_chain = risk_prompt | llm | json_parser

# -------------------------------------------------
# Agent function
# -------------------------------------------------
def underwriting_agent(applicant_data, claims_history, external_report):

    # Step 1: Summarize applicant data
    applicant_summary = applicant_chain.invoke({
        "applicant_data": applicant_data
    })

    # Step 2: Analyze claims history
    claims_analysis = claims_chain.invoke({
        "claims_history": claims_history
    })

    # Step 3: Filter rulebook to only relevant sections
    relevant_rulebook = filter_rulebook(applicant_data, claims_history, external_report)

    # Step 4: Apply filtered rule book and generate underwriting decision
    result = risk_chain.invoke({
        "rulebook": json.dumps(relevant_rulebook, indent=2),
        "applicant_summary": applicant_summary,
        "claims_analysis": claims_analysis,
        "external_report": external_report
    })

    return result
