# Insurance Quote Comparison Chatbot

A conversational AI application that compares multiple insurance quotes and explains differences in coverage, premium, and deductible in simple, human-friendly language.

The system supports both **structured JSON input** and **plain-text insurance quotes**, making it practical for real-world use.

---

## Features

- Compare 2 or more insurance quotes
- Accepts JSON and free-text inputs
- Simple, non-technical explanations
- Scenario-based reasoning (e.g. family of 4)
- Retrieval-Augmented Generation (RAG)
- Clean and eye-catching Flask UI
- Free, local embeddings using Hugging Face MiniLM

---

## How It Works

1. User enters insurance quotes (JSON or text)
2. Plain text is normalized into structured JSON using LLM
3. Insurance knowledge is retrieved using RAG
4. Quotes are compared together
5. Best option is explained with clear reasons

---

##  Project Structure
Quote_Comparison_Chatbot/
│
├── app.py
├── quote_comparison_agent.py
├── rag_store.py
│
├── knowledge/
│ ├── deductible.txt
│ ├── room_rent.txt
│ ├── copay.txt
│ └── family_insurance.txt
│
├── sample_quotes.json
│  
├── tests/
│ ├── test_rag.py
│ └── test_agent.py
│
├── templates/
│ └── index.html
│
├── static/
│ └── style.css
│
├── requirements.txt
├── .env
└── README.md

Create Virtual Environment

python -m venv venv
venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt
pip install sentence-transformers langchain-text-splitters langchain-huggingface langchain-chroma

Environment Variables

Create a .env file in the project root:
for example whatever API your using use through this .env file

Initialize RAG

Run this once to create the vector database:

Run the Application

python app.py

Open your browser and visit:

http://127.0.0.1:5000

Example Inputs

JSON input:

{
"quotes": [
{
"quote_id": "Q1",
"premium": { "amount": 16000 },
"deductible": { "amount": 5000 },
"coverage": {
"child_coverage": true,
"maternity": false,
"room_rent_limit": "2% of sum insured"
}
},
{
"quote_id": "Q2",
"premium": { "amount": 18500 },
"deductible": { "amount": 2000 },
"coverage": {
"child_coverage": true,
"maternity": true,
"room_rent_limit": "No limit"
}
}
]
}

Plain-text input:

Quote 1 costs 16,000 with deductible 5,000 and no maternity.
Quote 2 costs 18,500 with deductible 2,000, includes maternity and no room rent limit.

Sample Questions

Which insurance is best for a family of 4?

Which plan is cheapest but risky?

Which quote should I avoid and why?

Why is low deductible important?

Explain the difference between these quotes

Skills Demonstrated

Conversational AI, Retrieval-Augmented Generation (RAG), prompt engineering, data reasoning, NLP-based text normalization, and full-stack AI application development.

Future Enhancements

PDF and Excel upload support, structured comparison tables, chat history, multi-language support, and advanced recommendation logic.