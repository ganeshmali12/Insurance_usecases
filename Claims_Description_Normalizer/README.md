# Claims Description Normalizer

##  Project Overview

**Turn unstructured insurance claim text into structured, machine-readable JSON.**

Powered by **LangChain** and **Azure OpenAI**, this tool solves the problem of processing free-text claim descriptions by automatically extracting key attributes like loss type, severity, and affected assets.

## Problem Statement

Insurance companies receive claim descriptions like:

> “Water leaked from the bathroom ceiling and damaged the sofa and wooden flooring. Repair cost is very high.”

Such unstructured text:
- Cannot be directly stored in databases
- Is difficult to analyze automatically
- Slows down claim processing and triaging

This project aims to **normalize** such descriptions into a clean and consistent structure that downstream systems can easily consume.

---

## Solution Approach

The project applies **semantic NLP instead of hardcoded rules**:

1. Accepts free-text insurance claim descriptions
2. Uses an LLM to understand the **meaning and context** of the text
3. Extracts key entities such as damaged assets
4. Classifies the type and severity of the claim
5. Outputs structured JSON in a fixed schema

The output structure remains consistent even when the input wording varies significantly.

---

## Key Concepts Used

- **Natural Language Processing (NLP)**  
  Understanding unstructured human-written text.

- **Entity Extraction**  
  Identifying important entities such as affected assets from claim text.

- **Prompt-Based Data Structuring**  
  Guiding the LLM to return data in a predefined JSON schema.

- **Schema Enforcement**  
  Ensuring reliable and predictable output using structured parsers.

---

##  Technology Stack

- **Python**
- **LangChain**
- **Azure OpenAI**
- **Pydantic**
- **Flask**
- **HTML (basic UI)**

---

## Project Structure

```text
claims-normalizer/
│
├── app.py              # Single-file app (Agent + Flask UI)
├── requirements.txt    # Python dependencies
├── .env                # Azure OpenAI credentials (excluded from Git)
└── README.md
