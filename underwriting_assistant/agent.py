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
# Azure OpenAI LLM
# -------------------------------------------------
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
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
{
  "policy_compliance_status": "",
  "identified_risks": [],
  "triggered_rules": [],
  "risk_score": 0,
  "risk_level": "",
  "recommendation": ""
}
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

    # Step 3: Apply rule book and generate underwriting decision
    result = risk_chain.invoke({
        "rulebook": json.dumps(UNDERWRITING_RULEBOOK, indent=2),
        "applicant_summary": applicant_summary,
        "claims_analysis": claims_analysis,
        "external_report": external_report
    })

    return result
