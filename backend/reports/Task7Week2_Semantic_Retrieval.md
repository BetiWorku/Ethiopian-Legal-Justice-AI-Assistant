# Ethiopian Legal Semantic Retrieval System (Task 7)

## Overview

The Ethiopian Legal Semantic Retrieval System is a semantic search application that retrieves relevant legal provisions from the **FDRE (Federal Democratic Republic of Ethiopia) Constitution**.

The system allows users to ask legal questions in **English or Amharic** and returns the most relevant constitutional articles together with traceable source information. It combines multilingual sentence embeddings, semantic vector search, keyword extraction, metadata filtering, and custom re-ranking to improve retrieval accuracy.

The retrieval output is designed to be passed directly into the LLM-based legal response generation component developed in **Task 9**.

---

# Objective

Build a semantic retrieval application that accepts a legal question and returns the most relevant legal chunks with traceable evidence and metadata.

---

# Features

## Multilingual Question Support

- Supports both English and Amharic legal questions.
- Automatically detects the query language.
- Translates English keywords into Amharic for accurate retrieval.
- Translates retrieved content back into English when necessary.

---

## Semantic Vector Search

- Uses multilingual sentence embeddings.
- Embeds user queries using the same embedding model used during document indexing.
- Performs similarity search on the Qdrant Vector Database.

Embedding Model:

```
paraphrase-multilingual-MiniLM-L12-v2
```

---

## Keyword Extraction

To improve retrieval quality, the system extracts only meaningful legal concepts by removing common stop words.

Extracted keywords include:

- Unigrams
- Bigrams

Example:

Input:

```
What does Ethiopian law say about equality before the law?
```

Extracted keywords:

```
equality
before law
```

This reduces embedding noise and improves semantic search accuracy.

---

## Semantic Keyword Mapping

Some legal concepts have direct constitutional articles.

Examples:

| Keyword | Article |
|----------|----------|
| Equality | Article 25 |
| Privacy | Article 26 |
| Freedom of Religion | Article 27 |
| Freedom of Expression | Article 29 |

The system intercepts these concepts and routes retrieval directly to the relevant article before semantic search.

---

## Metadata Filtering

Supports metadata filtering including:

- Language
- Article Number
- Document Name

Example:

```
Article 25
```

retrieves only chunks belonging to Article 25.

---

## Hybrid Re-ranking

After retrieving the Top-50 semantic matches from Qdrant, documents are re-ranked using keyword boosting.

Boost Rules

- Title match: +3.0
- Content match: +1.0

Final ranking combines:

- Vector similarity score
- Keyword boost score

This significantly improves retrieval precision.

---

## Safe No-Result Handling

Unsupported legal questions are safely rejected.

Example:

```
How do I file for divorce?
```

Output:

```
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
  "source": "FDRE Constitution",
  "pages": "8-8",
  "similarity_score": 0.92,
  "ranking_score": 5.92
}
```

---

# System Workflow

```
User Question
      │
      ▼
Input Validation
      │
      ▼
Language Detection
      │
      ▼
Metadata Extraction
      │
      ▼
Semantic Keyword Mapping
      │
      ▼
Keyword Extraction
      │
      ▼
English → Amharic Translation
      │
      ▼
Sentence Embedding
      │
      ▼
Qdrant Vector Search
      │
      ▼
Top-50 Candidate Retrieval
      │
      ▼
Keyword Re-ranking
      │
      ▼
Top-K Results
      │
      ▼
Translate Output (if English)
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
- Qdrant Vector Database
- Deep Translator
- NumPy
- Python Dotenv

---

# Project Structure

```
backend/

│
├── data/
│   ├── chunks/
        article_chunks.json
        article_chunks_metadata.json
│
├── output/
│   └── retrieval_logs.jsonl
│
├── scripts/
│   ├── retrieval.py
│   ├── qdrant_insert.py
│   ├── qdrant_setup.py
│   ├── qdrant_test.py
│   └── test_evaluation.py
│
├── .env
├──  evaluation_results.json
├── requirements.txt
└── README.md
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

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

Install required packages.

```bash
pip install -r requirements.txt
```

Example requirements.txt

```text
sentence-transformers
qdrant-client
deep-translator
python-dotenv
numpy
```

---

## 4. Configure Environment Variables

Create a `.env` file.

```env
TOP_K=3

EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

---

## 5. Start Qdrant

Using Docker

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Ensure the `legal_documents` collection has already been populated with the processed FDRE Constitution vectors.

---

# Running the Retrieval System

Run the CLI application.

```bash
python scripts/retrieval.py
```

Example

```
Enter your legal question:

What does Ethiopian law say about equality?
```

---

# Example Retrieval Output

```
Search Question

What does Ethiopian law say about equality before the law?
```

Result 1

```
Document:
FDRE Constitution

Article:
Article 25

Title:
Right to Equality

Content:
All persons are equal before the law...

Source:
FDRE Constitution

Pages:
8-8

Similarity Score:
0.92

Ranking Score:
5.92
```

---

# Automated Evaluation

Run the evaluation script.

```bash
python scripts/test_evaluation.py
```

The evaluation measures:

- Hit Rate@K
- Mean Reciprocal Rank (MRR)
- Retrieval Accuracy

using a predefined set of legal questions.

---

# Retrieval Output Format

Each search returns:

- Document Name
- Article Number
- Article Title
- Chunk Content
- Source
- Page Number(s)
- Similarity Score
- Ranking Score

The output is also returned as structured JSON for integration with the LLM generation component.

---

# Deliverables

- Semantic legal retrieval system
- Multilingual search support
- Processed legal document chunks
- Populated Qdrant vector database
- Hybrid semantic retrieval with re-ranking
- Retrieval logging
- Structured JSON output for Task 9
- Evaluation script with Hit Rate and MRR
- README with installation and execution instructions

---

# Future Improvements

- BM25 + Dense Retrieval Hybrid Search
- Cross-Encoder Re-ranking
- Multi-document legal retrieval
- Retrieval-Augmented Generation (RAG)
- Support for Ethiopian Civil Code and Criminal Code
- FastAPI REST API integration
- Web-based legal search interface

---

