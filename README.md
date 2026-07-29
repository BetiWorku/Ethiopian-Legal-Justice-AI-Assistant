# Ethiopian Legal RAG Response Generation System (Task 9)

## Overview

The **Ethiopian Legal RAG Response Generation System** extends the semantic retrieval system developed in Task 7 by integrating a Large Language Model (LLM) for grounded legal response generation.

The system retrieves relevant legal provisions from the **FDRE Constitution**, builds structured legal context, and sends it to **Google Gemini** using a controlled RAG prompt.

The generated responses are:

- Based only on retrieved legal evidence
- Traceable through metadata citations
- Protected against hallucinated legal information
- Returned with a legal disclaimer for safe usage

This completes the end-to-end Legal AI Assistant pipeline:

**Document Processing → Retrieval → Context Building → LLM Generation → Legal Response**

---

# Objective

The goal of Task 9 is to develop an LLM-based legal information generation system that:

- Accepts legal questions in English and Amharic
- Retrieves relevant legal chunks using semantic search
- Validates retrieved context using similarity thresholds
- Generates grounded legal responses using Google Gemini
- Provides citation information from metadata
- Returns safe fallback responses when evidence is insufficient

---

# End-to-End RAG Architecture

```
                Legal PDF Documents
                        |
                        ▼
              OCR / Text Extraction
                        |
                        ▼
              Document Cleaning
                        |
                        ▼
              Metadata Generation
                        |
                        ▼
              Legal Chunking
                        |
                        ▼
            Multilingual Embedding Model
                        |
                        ▼
              Qdrant Vector Database
                        |
                        ▼
              Semantic Retrieval
                        |
                        ▼
            Retrieved Legal Context
                        |
                        ▼
             Context Builder Module
                        |
                        ▼
          Controlled Legal RAG Prompt
                        |
                        ▼
                 Google Gemini LLM
                        |
                        ▼
          Grounded Legal Response
                        |
                        ▼
          Citation + Legal Disclaimer
```

---

# System Workflow

```
User Question
      |
      ▼
Input Validation
      |
      ▼
Semantic Retrieval (Task 7)
      |
      ▼
Top-K Legal Chunks
      |
      ▼
Similarity Threshold Checking
      |
      ▼
Metadata Validation
      |
      ▼
Context Construction
      |
      ▼
Legal Prompt Generation
      |
      ▼
Google Gemini Response Generation
      |
      ▼
Citation Validation
      |
      ▼
Response Logging
```

---

# Key Features

## 1. LLM-Based Legal Response Generation

The system uses **Google Gemini** to generate legal information responses.

The LLM is controlled by a RAG prompt that forces it to:

- Use only retrieved legal context
- Avoid unsupported legal claims
- Never create fake citations
- Provide safe responses when information is missing


---

## 2. Semantic Retrieval Integration

The system integrates the Task 7 semantic retrieval engine.

Features:

- Multilingual embedding search
- Top-K document retrieval
- Similarity score validation
- Metadata preservation
- Duplicate removal


---

## 3. Context Builder

Retrieved chunks are converted into structured legal context.

Each context contains:

```
Document Title
Chapter
Article Number
Article Title
Page Number
Source
Similarity Score
Legal Text
```

This context is provided to the LLM before response generation.

---

## 4. Citation Traceability

Citations are generated from retrieved metadata.

The system displays:

```
Document:
FDRE Constitution

Article:
Article 25

Page:
8

Source:
FDRE Constitution
```

The LLM is not allowed to generate new citations.

---

## 5. Safe Fallback Handling

If retrieved legal evidence is insufficient:

```
Answer:
The answer is not available in the retrieved legal documents.


Relevant Sources:
No sufficiently relevant legal source was retrieved.


Important Note:
This response is provided for general legal information only and does not replace advice from a qualified legal professional.
```

---

# Legal Disclaimer

Every generated response includes:

```
Important Note:

This response is provided for general legal information only 
and does not replace advice from a qualified legal professional.
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Backend development |
| Google Gemini API | LLM response generation |
| Sentence Transformers | Multilingual embeddings |
| intfloat/multilingual-e5-base | Embedding model |
| Qdrant | Vector database |
| Deep Translator | Language translation |
| NumPy | Vector processing |
| Python-dotenv | Environment configuration |

---

# Project Structure

```
AILegalAssistant
│
├── backend
│   │
│   ├── data
│   │   │
│   │   ├── chunks
│   │   │   ├── article_chunks.json
│   │   │   ├── article_chunks_metadata.json
│   │   │   ├── fixed_chunks.json
│   │   │   └── paragraph_chunks.json
│   │   │
│   │   ├── documents
│   │   │   ├── Ethiopia_Constitution_Amharic.pdf
│   │   │   └── Ethiopia_Constitution_English.pdf
│   │   │
│   │   ├── raw
│   │   │   └── extracted_pages.txt
│   │   │
│   │   ├── vectors
│   │   │   ├── e5_metadata.pkl
│   │   │   ├── legal.index
│   │   │   ├── legal_e5.index
│   │   │   └── metadata.pkl
│   │   │
│   │   └── embeddings
│   │
│   ├── images
│   │   └── amharic
│   │
│   ├── output
│   │   └── reports
│   │       ├── Task0Week1Report.md
│   │       ├── Task2Week2Report.md
│   │       ├── Task3Week2Report.md
│   │       ├── Task4Week2Report.md
│   │       ├── Task5Week2Report.md
│   │       ├── Task6Week2_vector_database.md
│   │       ├── Task7Week2_Semantic_Retrieval.md
│   │       ├── Task8Week2Report.md
│   │       └── Task1pdfinspection.md
│   │
│   ├── scripts
│   │   ├── api.py
│   │   ├── chatbot.py
│   │   ├── chunking.py
│   │   ├── clean_text.py
│   │   ├── context_builder.py
│   │   ├── embedding.py
│   │   ├── embedding_e5.py
│   │   ├── extract_json.py
│   │   ├── ingest.py
│   │   ├── language_detector.py
│   │   ├── legal_structure_chunking.py
│   │   ├── llm_service.py
│   │   ├── prompt_template.py
│   │   ├── qdrant_insert.py
│   │   ├── qdrant_setup.py
│   │   ├── qdrant_test.py
│   │   ├── rag_pipeline.py
│   │   ├── retrieval.py
│   │   └── reset_qdrant.py
│   │
│   ├── services
│   │
│   ├── tests
│   │   ├── test_api.py
│   │   ├── test_evaluation.py
│   │   ├── test_pipeline.py
│   │   └── test_retrieval.py
│   │
│   ├── requirements.txt
│   └── README.md
│
├── frontend
│   │
│   ├── public
│   ├── src
│   │   ├── assets
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── eslint.config.js
│
└── .gitignore
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/AILegalAssistant.git

cd AILegalAssistant/backend
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file inside the backend folder:

```env
LLM_PROVIDER=gemini

LLM_MODEL=gemini-1.5-flash

LLM_API_KEY=YOUR_API_KEY

LLM_TEMPERATURE=0.1

TOP_K=3

SIMILARITY_THRESHOLD=0.65

EMBEDDING_MODEL=intfloat/multilingual-e5-base
```

---

# Start Qdrant Vector Database

Run:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Make sure the collection:

```
legal_documents
```

is already populated with legal embeddings.

---

# Running the Legal RAG System

Run the complete pipeline:

```bash
python -m scripts.rag_pipeline
```

---

# Example

## Input

```
What does Article 25 of the FDRE Constitution say?
```

## Output

```
Answer:

Article 25 of the FDRE Constitution states that all persons 
are equal before the law and are entitled to equal protection 
of the law without discrimination.


Relevant Sources:

Document:
FDRE Constitution

Article:
Article 25

Pages:
8


Important Note:

This response is provided for general legal information only 
and does not replace advice from a qualified legal professional.
```

---

# Evaluation

The RAG system was evaluated using 15 legal questions covering:

- Direct legal questions
- Article-based questions
- Paraphrased questions
- Amharic questions
- English questions
- Cross-language queries
- Unsupported questions


Evaluation criteria:

- Retrieval relevance
- Answer correctness
- Groundedness
- Citation accuracy
- Hallucination detection
- Safe fallback handling

