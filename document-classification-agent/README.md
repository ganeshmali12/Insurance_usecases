#  Document Classification Agent (Insurance Domain)

An AI-powered application that classifies insurance-related documents such as **Claim Forms**, **Inspection Reports**, and **Invoices** using **OCR, rule-based validation, and Azure OpenAI**.

The system is designed to behave like a real-world solution and can safely return **`Unknown`** for irrelevant documents instead of forcing incorrect classifications.

---

##  Features
- Upload **Images (PNG/JPG)** and **PDF documents**
- Free OCR using **Tesseract**
- Insurance-domain validation
- Rule-based signal generation
- Semantic classification using **Azure OpenAI**
- Confidence score with explanation
- Simple and clean **Flask web UI**
- Safe handling of irrelevant documents (`Unknown`)

---

##  How It Works
1. User uploads an image or PDF document  
2. OCR extracts readable text from the document  
3. Insurance-domain relevance is checked  
4. Rule-based signals are generated  
5. Azure OpenAI performs semantic reasoning  
6. Final output includes document type, confidence, and reason  

---
##  Supported Document Types
- Claim Form  
- Inspection Report  
- Invoice  
- Unknown (non-insurance documents)

---

##  Tech Stack
- Python  
- Flask  
- Tesseract OCR  
- Azure OpenAI  
- HTML, CSS, JavaScript  

---

##  Project Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install Tesseract OCR

Tesseract is used to extract text from image and PDF documents.

Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki

Verify the installation:
```
tesseract --version
```

### Step 3: Configure Azure OpenAI

Create a .env file in the project root directory and add:
```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```
---
### Run the Application

Start the Flask server:
```
python app.py
```
Open your browser and visit:
```
http://127.0.0.1:5000
```
Upload a document to view the classification result.

### Example Output

Insurance Document
~~~
{
  "document_type": "Invoice",
  "confidence": 0.92,
  "reason": "Contains invoice number, GST details, and total amount"
}
~~~
Irrelevant Document
~~~
{
  "document_type": "Unknown",
  "confidence": 0.2,
  "reason": "Document is not insurance-related"
}
~~~
---

### Future Enhancements

- Batch document upload

- Key-field extraction after classification

- Cloud deployment (Azure / Render)

- Multi-language document support