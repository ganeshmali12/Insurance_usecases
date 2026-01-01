# Insurance_usecases
This repository contains multiple AI, LLM, and NLP-based projects built using modern technologies such as LangChain, Azure OpenAI, Flask, and Hugging Face models.
Each project demonstrates a real-world use case with a focus on practical implementation, clean architecture, and explainability.

# Projects Overview
1️.Insurance Quote Comparison Chatbot

An AI-powered chatbot that compares multiple insurance quotes and explains differences in premium, deductible, and coverage in simple language.

Key Highlights:

Supports JSON and plain-text insurance quotes

Uses Retrieval-Augmented Generation (RAG)

Scenario-based reasoning (e.g., family of 4)

Flask-based interactive UI

Hugging Face MiniLM embeddings (free & local)

 Folder: Insurance_Quote_Comparison_Chatbot/

2️.Claims Description Normalizer

An NLP-based system that converts unstructured insurance claim descriptions into clean, structured JSON data.

Key Highlights:

Converts messy claim text into structured format

Entity extraction using LLMs

Prompt-based normalization

Useful for downstream automation and analytics

Folder: Claims_Description_Normalizer/

3️.Underwriting Assistant

An AI assistant designed to support insurance underwriting decisions by analyzing applicant details against predefined underwriting rules.

Key Highlights:

Rule-based + LLM reasoning

Explains underwriting decisions clearly

Uses structured rulebooks

Suitable for decision-support systems

 Folder: Underwriting_Assistant/

# Repository Structure
AI_Projects/
│
├── Insurance_Quote_Comparison_Chatbot/
│   ├── app.py
│   ├── quote_comparison_agent.py
│   ├── rag_store.py
│   ├── knowledge/
│   ├── data/
│   ├── templates/
│   ├── static/
│   └── README.md
│
├── Claims_Description_Normalizer/
│   ├── app.py
│   ├── normalizer.py
│   ├── sample_data/
│   └── README.md
│
├── Underwriting_Assistant/
│   ├── app.py
│   ├── underwriting_agent.py
│   ├── rules/
│   └── README.md
│
└── README.md   ← (You are here)
