# Ethiopian Legal Semantic Retrieval System (Task 7)

## Overview

The Ethiopian Legal Semantic Retrieval System is a semantic search application that retrieves relevant legal provisions from the **FDRE (Federal Democratic Republic of Ethiopia) Constitution**.

The system enables users to ask legal questions in **English** or **Amharic** and retrieves the most relevant constitutional articles with traceable source information.

It combines **multilingual E5 embeddings**, **template-based query alignment**, **semantic vector search using Qdrant**, **metadata filtering**, and **title-aware vector ranking** to improve retrieval accuracy.

The retrieved legal chunks are designed to serve as context for the **LLM-based response generation component (Task 9).**

---

# Objective

Build a semantic retrieval system that accepts legal questions and returns the most relevant constitutional provisions together with traceable metadata and citations.

---

# Features

## Multilingual Question Support

- Supports English and Amharic legal questions.
- Automatically detects the query language.
- Generates English and Amharic search queries.
- Translates retrieved content back to English when required.

---

## Semantic Vector Search

The system performs dense semantic retrieval using multilingual embeddings stored in Qdrant.

Embedding Model:

```text
intfloat/multilingual-e5-base
```

The same embedding model is used during document indexing and query embedding to ensure consistent semantic matching.

---

## Template-Based Query Alignment

To improve retrieval quality, user questions are converted into the same structure used by indexed legal documents.

Example query template:

```text
Article:
Title: {query}
Topic:
Content: {query}
```

This alignment significantly improves semantic retrieval accuracy without relying on manually created keyword rules.

---

## Metadata Filtering

The retrieval system supports metadata filtering using:

- Article Number
- Document Name
- Language

Example:

```text
What is Article 25?
```

The system filters the search to retrieve only chunks belonging to **Article 25**.

---

## Dual Vector Search

For multilingual retrieval, the system generates both English and Amharic query embeddings.

Both embeddings are searched independently in Qdrant, and the highest similarity score is selected using **Max Score Fusion**.

This improves:

- English retrieval
- Amharic retrieval
- Cross-language retrieval

---

## Title-Aware Vector Ranking

After retrieving candidate chunks from Qdrant, the system compares the semantic similarity between the query and article titles.

Title similarity is used as an additional ranking signal to improve retrieval quality.

Benefits include:

- Better legal concept matching
- Improved retrieval precision
- Reduced translation mismatch

---

## Safe No-Result Handling

Unsupported legal questions are rejected safely.

Example:

```text
How do I file for divorce?
```

Output:

```text
No relevant legal information found in the FDRE Constitution.
```

This prevents hallucinated legal responses.

---

## Structured Retrieval Output

Results are returned as structured JSON suitable for downstream LLM generation.

Example:

```json
{
  "document": "FDRE Constitution",
  "article": "Article 25",
  "title": "Right to Equality",
  "content": "...",
  "pages": "8-8",
  "similarity_score": 0.92,
  "ranking_score": 1.42
}
```

---

# System Workflow

```text
User Question
        │
        ▼
Input Validation & Safe Fallback
        │
        ▼
Language Detection
        │
        ▼
Metadata Extraction
        │
        ▼
English / Amharic Query Generation
        │
        ▼
Template-Based Query Alignment
        │
        ▼
E5 Embedding Generation (768 Dimensions)
        │
        ▼
Qdrant Dual Vector Search
        │
        ▼
Max Score Fusion
        │
        ▼
Top Candidate Retrieval
        │
        ▼
Title-Aware Vector Ranking
        │
        ▼
Top-K Result Selection
        │
        ▼
Translate Output (if required)
        │
        ▼
Structured JSON Response
        │
        ▼
Retrieval Logging
```

---

# Technologies Used

- Python 3.10+
- Sentence Transformers
- intfloat/multilingual-e5-base
- Qdrant Vector Database
- Deep Translator
- NumPy
- Python Dotenv

---

# Project Structure

```text
backend/

├── data/
│   └── chunks/
│       ├── article_chunks.json
│       └── article_chunks_metadata.json
│
├── output/
│   ├── retrieval_logs.jsonl
│   └── rag_logs.jsonl
│
├── scripts/
│   ├── retrieval.py
│   ├── embedding_e5.py
│   ├── rag_pipeline.py
│   ├── llm_service.py
│   └── test_evaluation.py
│
├── tests/
│   └── evaluation_results.json
│
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AILegalAssistant.git

cd AILegalAssistant/backend
```

---

## 2. Create a Virtual Environment

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

Example dependencies:

```text
sentence-transformers
qdrant-client
deep-translator
python-dotenv
numpy
google-generativeai
fastapi
uvicorn
```

---

## 4. Configure Environment Variables

Create a `.env` file.

```env
TOP_K=3

EMBEDDING_MODEL=intfloat/multilingual-e5-base

GEMINI_API_KEY=your_api_key

LLM_MODEL=gemini-1.5-flash

LLM_TEMPERATURE=0.1
```

---

## 5. Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Ensure the **legal_documents** collection has already been populated using **embedding_e5.py**.

---

# Running the Retrieval System

Run the retrieval application.

```bash
python scripts/retrieval.py
```

Example:

```text
Enter your legal question:

What does Ethiopian law say about equality?
```

---

# Example Retrieval Output

```text
Question:
What does Ethiopian law say about equality before the law?

Article:
Article 25

Title:
Right to Equality

Source:
FDRE Constitution

Similarity Score:
0.92
```

---

# Automated Evaluation

Run the evaluation script.

```bash
cd tests

python test_evaluation.py
```

The evaluation measures:

- Hit Rate@K
- Mean Reciprocal Rank (MRR)
- Retrieval Accuracy
- Top-K Performance

using a predefined evaluation dataset.

---

# Future Improvements

- Hybrid BM25 + Dense Retrieval
- Cross-Encoder Re-ranking
- Fine-tuned Legal Embedding Model
- Support for Civil Code and Criminal Code
- FastAPI REST API
- Web-based Legal Chatbot
- Larger Legal Corpus
- Production Deployment

