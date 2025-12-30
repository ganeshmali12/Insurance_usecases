import os
from typing import List, Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# =========================
# ENV & LLM SETUP
# =========================
load_dotenv()

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    temperature=0
)

# =========================
# OUTPUT SCHEMA
# =========================
class ClaimNormalized(BaseModel):
    loss_type: Literal[
        "Fire",
        "Theft",
        "Water Damage",
        "Accident",
        "Medical",
        "Other"
    ] = Field(description="Type of insurance loss")

    severity: Literal[
        "Low",
        "Medium",
        "High"
    ] = Field(description="Severity of the claim")

    affected_asset: List[str] = Field(
        description="Assets affected in the incident"
    )

    incident_summary: str = Field(
        description="Short factual summary"
    )

parser = PydanticOutputParser(pydantic_object=ClaimNormalized)

# =========================
# PROMPT
# =========================
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an insurance claims normalization engine. "
            "Use semantic understanding, not keyword matching. "
            "Normalize claims into structured data."
        ),
        (
            "human",
            "{claim_text}\n\n{format_instructions}"
        )
    ]
)

# =========================
# AGENT FUNCTION
# =========================
def normalize_claim(claim_text: str) -> dict:
    chain = prompt | llm | parser
    result = chain.invoke(
        {
            "claim_text": claim_text,
            "format_instructions": parser.get_format_instructions()
        }
    )
    return result.model_dump()
