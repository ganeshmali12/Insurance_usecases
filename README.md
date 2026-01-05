## Insurance_Usecases

This repository contains multiple AI, LLM, and NLP-based projects built using modern technologies such as LangChain, Azure OpenAI, Flask, and Hugging Face models.
Each project demonstrates a real-world use case with a focus on practical implementation, clean architecture, and explainability.

📁 Repository Structure

This repository contains the following projects:

Insurance_usecases/
│
├── Quote_Comparison_Chatbot/
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


Each project folder has its own README.md with detailed explanation, setup steps, and usage instructions.

## Projects Overview
# 1.Insurance Quote Comparison Chatbot

An AI-powered chatbot that compares multiple insurance quotes and explains differences in premium, deductible, and coverage in simple language.

# Key Highlights:

Supports JSON and plain-text insurance quotes

Uses Retrieval-Augmented Generation (RAG)

Scenario-based reasoning (e.g., family of 4)

Flask-based interactive UI

Hugging Face MiniLM embeddings (free & local)

Folder: Quote_Comparison_Chatbot/

# 2️.Claims Description Normalizer

An NLP-based system that converts unstructured insurance claim descriptions into clean, structured JSON data.

Key Highlights:

Converts messy claim text into structured format

Entity extraction using LLMs

Prompt-based normalization

Useful for downstream automation and analytics

Folder: Claims_Description_Normalizer/

# 3️.Underwriting Assistant

An AI assistant designed to support insurance underwriting decisions by analyzing applicant details against predefined underwriting rules.

Key Highlights:

Rule-based + LLM reasoning

Explains underwriting decisions clearly

Uses structured rulebooks

Suitable for decision-support systems

Folder: Underwriting_Assistant/

## Common Tech Stack Used

Python

LangChain

Azure OpenAI

Hugging Face (MiniLM)

Flask

Chroma Vector Database

Prompt Engineering

Retrieval-Augmented Generation (RAG)

## Purpose of This Repository

Showcase real-world AI/LLM projects

Demonstrate end-to-end AI application development

Serve as a learning and reference repository

Provide interview-ready projects with clean architecture

## How to Use

Clone the repository

Navigate into any project folder

Follow the instructions in that project’s README.md

Run and explore the application

## Note

Environment variables (.env) are required for Azure OpenAI–based projects

.env files are intentionally excluded from version control

Each project is self-contained and can be run independently