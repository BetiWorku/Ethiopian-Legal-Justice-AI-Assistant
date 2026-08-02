# Ethiopian Legal AI Assistant

## 1. Project Overview

### Project Description
The Ethiopian Legal AI Assistant is a bilingual RAG-based system that answers legal questions using official Ethiopian legal documents. It combines OCR, document processing, semantic search, and Large Language Models to provide evidence-based legal responses.

### Problem Statement
Ethiopian legal documents are large, complex, and often stored as scanned PDFs, making it difficult for users to quickly find relevant legal information. This project solves this problem by providing an AI assistant that can retrieve and explain relevant legal articles.

### Why Legal AI
Legal AI helps users access legal information faster and reduces incorrect answers by generating responses based only on retrieved legal evidence from official documents.

### Supported Legal Documents
The system supports the FDRE Constitution, Civil Code, and Family Code in both English and Amharic versions.

### Supported Languages
The system supports bilingual queries and answers in English and Amharic using multilingual AI models.


## 2. Project Objective

Explain:

The objective of this project is to build a bilingual RAG-based legal assistant capable of answering Ethiopian legal questions by retrieving evidence from official legal documents.

Main goals:

- Create Ethiopian legal knowledge base
- Process PDF legal documents
- Support Amharic and English
- Implement semantic retrieval
- Reduce hallucination
- Generate evidence-based answers


## 3. System Architecture

Full diagram:

PDF Documents
        |
        ↓
Document Processing
        |
        ↓
Knowledge Base Creation
        |
        ↓
Vector Database
        |
        ↓
RAG Pipeline
        |
        ↓
LLM Response


## 4. Knowledge Base Creation Pipeline (Before RAG)

Explain step by step:

### 4.1 Document Collection

Documents:

- FDRE Constitution English
- FDRE Constitution Amharic
- Civil Code English
- Civil Code Amharic
- Family Code English
- Family Code Amharic


Location:

backend/data/documents


---

### 4.2 PDF Classification

File:

scripts/ingest.py


Purpose:

Determine whether PDF is:

- Digital PDF
- Scanned PDF


Flow:

PDF

↓

Check text layer

↓

If available:
PyMuPDF extraction

If unavailable:
OCR


---

### 4.3 OCR Pipeline


For scanned documents:


PDF

↓

Image Conversion

↓

OpenCV preprocessing

↓

Tesseract OCR

↓

Extract text


Used tools:

- Tesseract
- OpenCV
- PyMuPDF


---

### 4.4 Text Cleaning


Operations:

- Remove noise
- Normalize Unicode
- Remove extra spaces
- Clean OCR errors


---

### 4.5 Legal Chunking

Split documents based on legal structure.


Example:

Article 25

↓

Single legal chunk


Metadata:


{
 article,
 document,
 language,
 text
}


---

### 4.6 Embedding Generation


File:

embedding_e5.py


Model:

intfloat/multilingual-e5-base


Process:


Legal text

↓

Embedding Model

↓

768-dimensional vector


Example:

[
0.023,
-0.034,
...
768 values
]


---

### 4.7 Vector Proof


File:

vector_proof.py


Purpose:

Demonstrate how legal knowledge becomes mathematical vectors.


Example:


Article 25:

"All persons are equal before the law"


↓

Embedding Model


↓

Vector:


Index 0
Index 1
Index 2

...

Index 767


The computer does not understand words directly.

It compares mathematical representations of meaning.


---

### 4.8 Vector Database Storage


Database:

Qdrant


Collection:

legal_documents


Stored:


- Article number
- Text
- Document
- Language
- Vector
- Metadata



# 5. RAG Pipeline (After Knowledge Base)


## 5.1 User Query


Example:

"What is equality before the law?"


## 5.2 Query Embedding


Question converted into vector:


Question

↓

Embedding Model

↓

768 values



## 5.3 Hybrid Retrieval


File:

retrieval.py


Methods:


Dense Search:

Qdrant semantic search


Sparse Search:

BM25 keyword search


Fusion:


Dense 60%

+

BM25 40%


## 5.4 Context Retrieval


Retrieve:


Article 25

Equality before the law


## 5.5 LLM Generation


File:

rag_pipeline.py


Gemini receives:


Question

+

Retrieved legal evidence


Rules:

- Do not invent laws
- Answer only from context
- Mention article number


# 6. Complete Project Structure


(show your real folders)


# 7. Technology Stack


Frontend: React,Tailwind CSS
Backend:FastAPI,Python
AI:Gemini, multilingual-e5-base
Database: Qdrant
OCR:Tesseract, OpenCV
Retrieval:BM25,Vector Search


## 8. Retrieval Evaluation Test Cases

The system was evaluated using 15 comprehensive test cases covering different query types, including direct legal questions, Amharic queries, cross-language questions, article-number searches, and unsupported queries to test retrieval accuracy and hallucination prevention.

| No. | Category | Question | Expected Result |
|---|---|---|---|
| 1 | Direct | What does the constitution say about equality before the law? | Article 25 |
| 2 | Direct | What is the right to freedom of expression in the constitution? | Article 29 |
| 3 | Direct | Does the constitution guarantee the right to privacy? | Article 26 |
| 4 | Amharic | በሕገ መንግሥት የእኩልነት መብት ምንድነው? | Article 25 |
| 5 | Cross-Language | What does the constitution say about ግል ሕይወት (privacy)? | Article 26 |
| 6 | Direct | What does the family code say about free and full consent for a valid marriage? | Article 6 |
| 7 | Direct | What does the family code say about prohibited relatives (ርክርክ)? | Article 8 |
| 8 | Article Number | What is article 6 in the family code? | Article 6 |
| 9 | Amharic | በቤተሰብ ሕግ የጋብቻ ፈቃደኝነት ምንድን ነው? | Article 6 |
| 10 | Article Number | What is article 4 in the civil code? | Article 4 |
| 11 | Article Number | What is article 6 in the civil code? | Article 6 |
| 12 | Article Number | What is article 5 in the civil code? | Article 5 |
| 13 | Unsupported | How do I file for a divorce in Addis Ababa? | No Article (Rejected) |
| 14 | Unsupported | Can you help me hire a lawyer for tax evasion? | No Article (Rejected) |
| 15 | Direct | Explain the right to life in the constitution. | Article 14 |

### Evaluation Metrics

| Metric | Value | Description |
|---|---|---|
| Total Questions | 15 | Total number of test cases evaluated |
| Total Hits | 15 | Number of questions where the correct article was retrieved |
| Hit Rate @ 5 | 100.00% | Percentage of questions where the correct article appeared in the Top-5 results |
| MRR | 0.9000 | Mean Reciprocal Rank score (1.0 represents perfect ranking) |

### Evaluation Summary

The retrieval system achieved a **100% Hit Rate @ 5**, successfully retrieving the correct legal article for all 15 test cases. The evaluation included English, Amharic, cross-language, and unsupported queries, demonstrating the system's ability to retrieve relevant legal evidence while avoiding incorrect responses for unsupported questions.



# 9. Installation


Requirements:

- Python 3.10+
- Node.js
- Docker
- Tesseract OCR


Backend:


python -m venv .venv

pip install -r requirements.txt


Run Qdrant:


docker run...


Run API:


uvicorn scripts.api:app --reload


Frontend:


npm install

npm run dev

### 10. Admin Dashboard

The Ethiopian Legal AI Assistant includes an Admin Dashboard for managing and monitoring the complete RAG pipeline. The dashboard provides a user-friendly interface that allows administrators to control document ingestion, processing, embedding generation, and vector database monitoring without manually executing backend commands.

Main Features
Legal Document Upload

Administrators can upload new Ethiopian legal PDF documents through the dashboard.

Supported documents:

Constitution
Civil Code
Family Code
Other Ethiopian legal documents

# 11. Future Improvements

- More Ethiopian laws
- Better OCR
- Cross encoder reranking
- Cloud deployment
