from flask import Flask, render_template, request
import json
import os
from dotenv import load_dotenv

from quote_comparison_agent import compare_quotes
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

app = Flask(__name__)

# -----------------------------
# LLM for text → JSON normalization
# -----------------------------
normalizer_llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
    temperature=0
)

normalizer_prompt = ChatPromptTemplate.from_template("""
You are an insurance data extraction assistant.

Convert the following raw insurance quote text into a structured JSON format.

Rules:
- Extract multiple quotes if present
- Use this exact JSON structure:
{{
  "quotes": [
    {{
      "quote_id": "Q1",
      "provider_name": "",
      "premium": {{ "amount": number }},
      "deductible": {{ "amount": number }},
      "coverage": {{
        "child_coverage": true/false/null,
        "maternity": true/false/null,
        "room_rent_limit": ""
      }}
    }}
  ]
}}
- If information is missing, use null
- Output ONLY valid JSON, nothing else

RAW TEXT:
{raw_text}
""")


json_parser = JsonOutputParser()


def normalize_text_to_quotes(raw_text: str) -> dict:
    """Convert free text insurance quotes into structured JSON"""
    chain = normalizer_prompt | normalizer_llm | json_parser
    return chain.invoke({"raw_text": raw_text})


# -----------------------------
# Flask Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    error = None

    if request.method == "POST":
        quotes_input = request.form["quotes"]
        question = request.form["question"]

        try:
            # Step 1: Try JSON directly
            try:
                quotes_data = json.loads(quotes_input)
            except json.JSONDecodeError:
                # Step 2: Normalize plain text → JSON
                quotes_data = normalize_text_to_quotes(quotes_input)

            # Step 3: Compare quotes
            response = compare_quotes(quotes_data, question)

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        response=response,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
