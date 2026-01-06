# 🏦 Insurance Use Cases – AI & LLM Projects

This repository contains multiple **AI, LLM, and NLP-based projects** focused on **real-world insurance use cases**.  
Each project demonstrates **practical implementation**, **clean architecture**, and **explainable AI workflows** using modern technologies such as **Azure OpenAI, LangChain, Flask, and OCR**.

All projects are designed to be **interview-ready**, **educational**, and **industry-aligned**.

---

## 📂 Repository Structure (with File Descriptions)

```text
Insurance_usecases/
│
├── Quote_Comparison_Chatbot/                # AI chatbot for comparing insurance quotes
│   ├── app.py                               # Flask entry point for the chatbot UI
│   ├── quote_comparison_agent.py            # Core LLM logic for comparing quotes
│   ├── rag_store.py                         # RAG pipeline and vector store logic
│   ├── knowledge/                           # Reference documents for RAG
│   ├── data/                                # Sample insurance quote data
│   ├── templates/                           # HTML templates for Flask UI
│   ├── static/                              # CSS and frontend assets
│   └── README.md                            # Project-specific documentation
│
├── Claims_Description_Normalizer/           # Converts unstructured claims into structured JSON
│   ├── app.py                               # Flask application entry point
│   ├── normalizer.py                        # LLM-based claim normalization logic
│   ├── sample_data/                         # Sample raw claim descriptions
│   └── README.md                            # Project-specific documentation
│
├── Underwriting_Assistant/                  # AI assistant for underwriting decision support
│   ├── app.py                               # Flask application entry point
│   ├── underwriting_agent.py                # Core underwriting logic (rules + LLM)
│   ├── rules/                               # Underwriting rulebooks and constraints
│   └── README.md                            # Project-specific documentation
│
├── Document_Classification_Agent/           # OCR + AI-based insurance document classifier
│   ├── app.py                               # Flask UI for document upload and results
│   ├── classifier.py                        # Core classification logic (OCR + rules + LLM)
│   ├── utils/                               # Helper utilities
│   │   └── ocr_utils.py                     # OCR logic using Tesseract and PDF handling
│   ├── data/                                # Uploaded and sample documents
│   ├── templates/                           # HTML templates for Flask UI
│   ├── static/                              # CSS and frontend assets
│   └── README.md                            # Project-specific documentation
│
└── README.md                                # Root repository documentation (this file)
```
Each project folder contains its own dedicated README.md explaining setup, architecture, and usage.

---

## 🧠 Projects Overview
### 1️. Insurance Quote Comparison Chatbot

An AI-powered chatbot that compares multiple insurance quotes and explains differences in premium, deductible, and coverage in simple language.

Key Highlights:

- Supports JSON and plain-text insurance quotes

- Uses Retrieval-Augmented Generation (RAG)

- Scenario-based reasoning (e.g., family size, coverage needs)

- Flask-based interactive UI

- Hugging Face MiniLM embeddings (free & local)

Folder: Quote_Comparison_Chatbot/

---

### 2️. Claims Description Normalizer

An NLP-based system that converts unstructured insurance claim descriptions into clean, structured JSON data.

Key Highlights:

- Converts messy claim text into structured format

- Entity extraction using LLMs

- Prompt-based normalization

- Useful for automation and analytics

Folder: Claims_Description_Normalizer/

---

### 3️. Underwriting Assistant

An AI assistant designed to support insurance underwriting decisions by evaluating applicant details against predefined rules.

Key Highlights:
~~~
- Rule-based + LLM reasoning

- Transparent and explainable decisions

- Uses structured underwriting rulebooks

- Suitable for decision-support systems

Folder: Underwriting_Assistant/
~~~
---

### 4️. Document Classification Agent

An AI-powered system that classifies insurance documents such as Claim Forms, Inspection Reports, and Invoices using OCR, rules, and Azure OpenAI.

The system safely returns Unknown for irrelevant documents instead of forcing incorrect classifications.

Key Highlights:

- Supports images and PDFs

- Free OCR using Tesseract

- Insurance-domain validation and rejection logic

- Semantic document understanding using Azure OpenAI

- Confidence score with explanation

- Clean Flask-based UI

Folder: Document_Classification_Agent/

---

## Common Tech Stack Used

- Python

- Flask

- Azure OpenAI

- LangChain

- Hugging Face (MiniLM)

- Tesseract OCR

- Chroma Vector Database

- Prompt Engineering

- Retrieval-Augmented Generation (RAG)

---
## Purpose of This Repository

- Showcase real-world AI/LLM insurance applications

- Demonstrate end-to-end AI system development

- Provide clean, explainable, and scalable designs

- Serve as a learning and reference repository

- Offer interview-ready projects with practical relevance

---

## How to Use

Step1. Clone the repository

Step2. Navigate into any project folder

Step3. Follow the instructions in that project’s README.md

Step4. Run and explore the application

Each project is self-contained and can be executed independently.

---

## Notes


- Environment variables (.env) are required for Azure OpenAI–based projects

- .env files are intentionally excluded from version control

- No real or sensitive insurance data is used