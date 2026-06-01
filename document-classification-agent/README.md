# Document Classification Agent (Insurance Domain)

An AI-powered web application that classifies insurance-related documents using **OCR + Azure OpenAI GPT-4.1-mini**. Designed for real-world insurance workflows — supports batch uploads, secure login, automatic folder segregation, and smart duplicate file naming.

---

## Features

- **Secure Login / Logout** with 30-minute session timeout
- **Batch Upload** — upload multiple files at once, processed in parallel chunks of 5
- **Live Progress Bar** during batch classification
- **OCR Pipeline**:
  - `pdfplumber` for digital PDFs (native text extraction)
  - `PyMuPDF (fitz)` + `Tesseract` for scanned PDFs and images
- **Azure OpenAI GPT-4.1-mini** for intelligent semantic classification
- **Confidence Score** with reasoning for every document
- **Modal Preview** — click any result row to preview the document alongside its extracted text
- **Automatic Folder Segregation** — classified files are copied into type-specific folders under `data/classified/`
- **Smart Duplicate Naming** — re-uploading `invoice.pdf` saves as `invoice_2.pdf`, `invoice_3.pdf`, etc.
- **CSV Export** of classification results
- Clean, responsive **Flask web UI**

---

## Supported Document Types

| Type | Description |
|---|---|
| Claim Form | Insurance claim submission forms |
| Inspection Report | Vehicle or property inspection documents |
| Invoice | Bills with invoice number, GST, totals |
| Medical Bill | Hospital/clinic bills with patient and treatment details |
| Unknown | Non-insurance or unrecognisable documents |

---

## Folder Structure After Classification

```
data/
├── uploads/              ← temporary upload staging area
└── classified/
    ├── claim_form/
    ├── inspection_report/
    ├── invoice/
    ├── medical_bill/
    └── unknown/
```

---

## Tech Stack

- Python, Flask
- PyMuPDF (fitz), pdfplumber, pytesseract
- Azure OpenAI (GPT-4.1-mini)
- HTML, CSS, JavaScript (Fetch API, FileReader API)

---

## Project Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install Tesseract OCR

Download and install from:  
https://github.com/UB-Mannheim/tesseract/wiki

Default expected path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

Verify:
```bash
tesseract --version
```

### Step 3: Configure Environment Variables

Create a `.env` file in the **project root** (`c:\Insurance_usecases\.env`) and add:

```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4.1-mini

SECRET_KEY=your_random_secret_key_here
APP_USERNAME=admin
APP_PASSWORD=your_password_here
```

> `SECRET_KEY` is required — the app will refuse to start if it is missing.

### Step 4: Run the Application

```bash
python app.py
```

Open your browser and visit:
```
http://127.0.0.1:5000
```

Login with the credentials set in `.env`, then upload documents to classify them.

---

## Example Output

```json
{
  "document_type": "Invoice",
  "confidence": 0.92,
  "reason": "Contains invoice number, GST details, and total amount payable.",
  "saved_to": "data/classified/invoice"
}
```

```json
{
  "document_type": "Unknown",
  "confidence": 0.18,
  "reason": "Document does not contain insurance-related content.",
  "saved_to": "data/classified/unknown"
}
```

---

## Future Enhancements

- Key-field extraction after classification (e.g., claim number, patient name, invoice total)
- Browse/download UI for classified folders
- Excel (.xlsx) export
- Summary count panel (e.g., "3 Invoices, 2 Claim Forms")
- Cloud deployment (Azure App Service / Docker)
- Multi-language document support
