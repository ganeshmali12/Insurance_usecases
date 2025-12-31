import json
import os
from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag_store import load_vector_store

load_dotenv()

# -----------------------------
# LLM (Reasoning Model)
# -----------------------------
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    deployment_name=os.getenv("AZURE_DEPLOYMENT_NAME"),
    temperature=0
)

# -----------------------------
# Prompt Template
# -----------------------------
prompt = ChatPromptTemplate.from_template("""
You are a helpful insurance advisor.

Use the insurance knowledge below to explain concepts clearly.
Avoid technical jargon. Be simple and practical.

INSURANCE KNOWLEDGE:
{knowledge}

INSURANCE QUOTES:
{quotes}

USER QUESTION:
{question}

TASK:
Compare the insurance quotes and answer the user's question.
Explain which option is best and why.
Mention trade-offs if any.
""")

# -----------------------------
# Main Agent Function
# -----------------------------
def compare_quotes(quotes: dict, user_question: str) -> str:
    """
    Compare multiple insurance quotes and explain the best option.
    """

    # Load vector DB
    vectordb = load_vector_store()

    # Retrieve relevant insurance knowledge
    docs = vectordb.similarity_search(user_question, k=3)
    knowledge_context = "\n\n".join(doc.page_content for doc in docs)

    # Prepare input
    chain_input = {
        "knowledge": knowledge_context,
        "quotes": json.dumps(quotes, indent=2),
        "question": user_question
    }

    # Run chain
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke(chain_input)

    return response
