# Task 0: OCR, PDF Processing, Embeddings, and Vector Database Review

## 1. Introduction

The Ethiopian Legal & Justice AI Assistant requires converting Ethiopian legal documents into searchable and traceable digital knowledge. This process includes PDF inspection, text extraction, Optical Character Recognition (OCR), document cleaning, text chunking, embeddings generation, and vector database storage.
The goal of this task is to understand the technologies required for building a Retrieval-Augmented Generation (RAG) system for Ethiopian legal documents.

---

# 2. PDF Fundamentals

## Digital PDF

A digital PDF contains an embedded text layer. Text can be selected, searched, and extracted directly using tools such as PyMuPDF or pdfplumber.

Advantages:

* Fast extraction
* High accuracy
* Preserves original text

Limitation:

* Some PDFs contain formatting problems such as columns, tables, and incorrect reading order.

## Scanned PDF

A scanned PDF contains only page images without a text layer. OCR is required to convert images into machine-readable text.

Challenges:

* Low image quality
* Noise
* Skewed pages
* Character recognition errors

## Mixed PDF

A mixed PDF contains both selectable text and scanned images. A hybrid extraction approach is required.

---

# 3. OCR Fundamentals

OCR (Optical Character Recognition) converts document images into editable text.

Main OCR steps:

1. Page Rendering

* Convert PDF pages into images.

2. Image Preprocessing

* Grayscale conversion
* Thresholding
* Noise removal
* Image resizing
* Deskewing

3. Language Selection
   OCR requires proper language models.

For Ethiopian legal documents:

* Amharic language model (`amh`)
* English language model (`eng`)

4. Character Recognition

OCR identifies characters from images and produces text output.

5. Confidence and Post Correction

OCR systems provide confidence scores. Legal documents require manual validation because incorrect article numbers or legal terms can affect meaning.

---

# 4. Amharic OCR Challenges

Amharic OCR has several difficulties:

* Similar looking Ge'ez characters can be confused.
* Poor scan quality reduces recognition accuracy.
* Old legal documents may use low-quality fonts.
* Skewed pages affect character detection.
* Mixed Amharic and English pages require multiple language models.

---

# 5. Document Cleaning Risks in Legal Systems

Legal documents require careful preprocessing.

Important information must be preserved:

* Article numbers
* Sections
* Exceptions
* Conditions
* Dates
* Legal references

Incorrect cleaning may change legal meaning.

---

# 6. Embedding Fundamentals

Embeddings convert text into numerical vectors.

A vector represents the semantic meaning of a document.

Important concepts:

## Document Embedding

Represents the meaning of stored legal documents.

## Query Embedding

Represents the meaning of a user's question.

## Semantic Similarity

Measures how close two vectors are. Similar legal concepts have similar vector representations.

---

# 7. Vector Database Fundamentals

A vector database stores and searches embeddings.

Main components:

* Collection: group of stored vectors
* Vector dimension: size of embedding representation
* Similarity metric: cosine similarity or other distance methods
* ID: unique identifier
* Payload: stored information
* Metadata filters: filtering by article, document type, or year
* Top-k search: returning the most similar results

---

# 8. Keyword Search vs Semantic Search

| Keyword Search            | Semantic Search            |
| ------------------------- | -------------------------- |
| Matches exact words       | Understands meaning        |
| Requires same terminology | Finds related concepts     |
| Less flexible             | Better for legal questions |

Example:

Keyword search:
"Article 25"

Semantic search:
"Right to equality"

Both can retrieve the same legal information.

---

# 9. Technology Selection

## OCR/PDF Method

Selected method:

Hybrid PDF extraction approach.

Tools:

Primary:

* PyMuPDF for digital PDF extraction and rendering
* Tesseract OCR with Amharic and English models for scanned pages

Reason:

* Supports Ethiopian legal PDFs
* Local processing
* Open source
* Good Amharic support with language data

---

# 10. Embedding Model Comparison Plan

Models to evaluate:

## Sentence Transformers

Advantages:

* Good semantic search performance
* Easy integration with Python

## Google Gemini Embedding Model

Advantages:

* Strong multilingual capability
* Suitable for legal question understanding

Evaluation criteria:

* Retrieval accuracy
* Amharic support
* Processing speed
* Vector quality

---

# 11. Vector Database Selection and Justification

## Vector Database Comparison

| Vector Database | Advantages | Limitations | Suitability for Legal RAG |
|---|---|---|---|
| Qdrant | Open source, fast similarity search, metadata filtering, easy Python integration | Requires self-hosting or deployment setup | Excellent for legal document retrieval |
| ChromaDB | Simple setup, developer friendly, good for prototypes | Less optimized for large-scale production workloads | Good for small experiments |
| Pinecone | Fully managed cloud service, scalable, high performance | Paid service, requires external cloud dependency | Good for enterprise applications |
| Weaviate | Supports hybrid search, GraphQL API, scalable | More complex architecture | Good for large knowledge systems |
| FAISS | Very fast vector similarity library, open source | No built-in metadata filtering or database features | Good for local experiments |

---

## Selected Vector Database: Qdrant

Qdrant is selected as the primary vector database for the Ethiopian Legal & Justice AI Assistant.

### Reasons:

### 1. Open Source
Qdrant can be self-hosted locally, reducing dependency on external cloud services.

### 2. Metadata Filtering
Legal documents require filtering by:
- Article number
- Document type
- Language
- Source
- Publication year

Qdrant supports payload metadata filtering.

### 3. Efficient Similarity Search
Qdrant provides fast vector similarity search using embeddings, allowing retrieval of relevant legal sections based on user questions.

### 4. Suitable for RAG Architecture
Qdrant integrates well with:
- Embedding models
- Retrieval pipelines
- LLM-based answer generation

### 5. Python Integration
Qdrant provides a Python client that can easily integrate with the backend RAG pipeline.

---

## Final Decision

For this project, Qdrant is preferred because it provides a balance between performance, flexibility, cost, and RAG compatibility. It is more suitable than simple local libraries such as FAISS and avoids the cost dependency of managed services such as Pinecone.
---

# 12. Mini Architecture

PDF Documents

↓

PDF Extraction / OCR

↓

Text Cleaning

↓

Chunking

↓

Embedding Generation

↓

Qdrant Vector Database

↓

Retriever

↓

LLM Answer Generation

---

# 13. Conclusion

OCR, embeddings, and vector databases are essential components for transforming Ethiopian legal PDFs into searchable AI knowledge. A hybrid PDF extraction approach using PyMuPDF and Tesseract provides reliable processing for both digital and scanned legal documents.
