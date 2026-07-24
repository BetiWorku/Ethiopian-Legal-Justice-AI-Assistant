# ⚖️ Ethiopian Legal & Justice AI Assistant

An AI-powered legal assistant for Ethiopian legal documents.

The system uses Large Language Models (LLM), legal document extraction, OCR, and FastAPI + React architecture to provide legal question answering.

---

# 📌 Project Overview

The Ethiopian Legal & Justice AI Assistant helps users ask questions about Ethiopian legal documents.

Current implemented features:

✅ FDRE Constitution English PDF extraction  
✅ FDRE Constitution Amharic PDF OCR extraction  
✅ Legal articles converted into JSON format  
✅ Language detection (English / Amharic)  
✅ Gemini LLM integration  
✅ FastAPI backend API  
✅ React frontend interface  

Future improvements:

- RAG (Retrieval Augmented Generation)
- Vector database
- Semantic search
- More Ethiopian laws
- Citation-based answers

---

# 🏗️ Project Structure


AILegalAssistant
│
├── backend
│   │
│   ├── data
│   │   ├── documents
│   │   │   ├── Ethiopia_Constitution_Amharic.pdf
│   │   │   └── Ethiopia_Constitution_English.pdf
│   │   │
│   │   ├── images
│   │   │   └── amharic
│   │   │       ├── page-001.png
│   │   │       ├── page-002.png
│   │   │       └── page-003.png
│   │   │
│   │   ├── fdre_constitution_articles.json
│   │   └── fdre_constitution_english.json
│   │
│   ├── output
│   │   ├── constitution_full.txt
│   │   ├── page-001.txt
│   │   └── page-002.txt
│   │
│   ├── scripts
│   │   ├── api.py
│   │   ├── chatbot.py
│   │   ├── data_extraction.py
│   │   ├── extract_json.py
│   │   ├── language_detector.py
│   │   ├── legal_knowledge.py
│   │   ├── llm_service.py
│   │   ├── main.py
│   │   ├── pdf_to_json.py
│   │   └── prompt_template.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend
│   ├── src
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── App.css
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md

---

# ⚙️ Backend Setup

Move to backend folder:

```bash
cd backend

Create virtual environment:

python -m venv venv

Activate virtual environment:

Windows PowerShell
.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
📄 English Constitution PDF → JSON Extraction

The English constitution PDF is extracted using PyPDF.

File:

data/documents/Ethiopia_Constitution_English.pdf

Run:

python scripts/pdf_to_json.py

Process:

English PDF

      |
      v

PyPDF Extraction

      |
      v

Text Extraction

      |
      v

JSON Database

fdre_constitution_english.json
🇪🇹 Amharic Constitution OCR Pipeline

The Amharic constitution PDF is scanned, therefore OCR is required.

Tools used:

Tesseract OCR
Poppler (pdftoppm)
Python extraction scripts
Step 1: Convert PDF Pages to Images

Install Poppler first.

Run:

pdftoppm -png -r 300 data/documents/Ethiopia_Constitution_Amharic.pdf output/page

Generated images:

output/

page-001.png
page-002.png
page-003.png
Step 2: Run Tesseract OCR

Amharic OCR:

tesseract output/page-001.png output/page-001 -l amh

Amharic + English OCR:

tesseract output/page-001.png output/page-001 -l amh+eng

Generated text:

page-001.txt
page-002.txt
Step 3: Combine OCR Text

Windows PowerShell:

type output\page-*.txt > output\constitution_full.txt

Linux:

cat output/page-*.txt > output/constitution_full.txt

Result:

constitution_full.txt
Step 4: Convert TXT → JSON

Run:

python scripts/extract_json.py

Workflow:

Amharic PDF

      |
      v

PDF Images

      |
      v

Tesseract OCR

      |
      v

TXT File

      |
      v

Python Parser

      |
      v

JSON Database

Output:

data/fdre_constitution_articles.json
🔑 Environment Variables

Create:

backend/.env

Add:

GEMINI_API_KEY=your_api_key_here
🚀 Run Backend API

Open PowerShell inside the backend folder.

Start FastAPI server:

uvicorn scripts.api:app --reload

Backend API:

http://localhost:8000

Swagger Documentation:

http://localhost:8000/docs
🔌 API Example

Endpoint:

POST /chat

Request:

{
  "question": "What is Article 25?"
}

Response:

{
  "answer": "Article 25 explains the right to equality..."
}
🎨 Frontend Setup

Open another terminal:

cd frontend

Install packages:

npm install

Run React:

npm run dev

Frontend:

http://localhost:5173
🔄 System Architecture
                User
                 |
                 v

          React Frontend

                 |
                 v

          FastAPI Backend

                 |
        -------------------
        |                 |
        v                 v

 Legal JSON Database     Gemini LLM

                 |
                 v

          Legal Answer
🧪 Testing

Example questions:

English:

What does Article 25 say about equality?

Amharic:

የእኩልነት መብት ምንድነው?
🛠️ Technologies Used
Backend
Python
FastAPI
Gemini API
PyPDF
Tesseract OCR
JSON
Frontend
React
Vite
JavaScript
CSS
AI
Large Language Models
Prompt Engineering
Context Engineering
RAG Preparation
👩‍💻 Developer

Betelhem Worku

Software Engineering Student

AI Legal Assistant Project