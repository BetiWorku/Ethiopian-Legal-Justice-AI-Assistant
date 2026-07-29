# Task 0: OCR, PDF Processing, Embeddings, and Vector Database Review

## Objective

The objective of this task was to understand the technologies required to convert Ethiopian legal PDF documents into searchable, traceable, and retrieval-ready vector data for the Legal AI Assistant.

---

# 1. PDF Fundamentals

PDF documents can be classified into three types:

### Digital PDF
- Contains a machine-readable text layer.
- Text can be extracted directly using tools like PyMuPDF.
- Example: English Constitution PDF.

### Scanned PDF
- Contains only page images.
- No selectable text layer.
- Requires OCR to extract text.
- Example: Scanned Amharic legal documents.

### Mixed PDF
- Contains both selectable text and scanned images.
- Requires both direct extraction and OCR fallback.

### PDF Challenges
- Complex layouts
- Headers and footers
- Tables
- Columns
- Stamps and signatures
- Page numbering issues

---

# 2. OCR Fundamentals

OCR (Optical Character Recognition) converts document images into machine-readable text.

OCR Pipeline:


PDF Page
|
▼
Image Rendering
|
▼
Image Preprocessing
(Grayscale, Thresholding, Resize, Deskew)
|
▼
OCR Engine
(Tesseract)
|
▼
Recognized Text
|
▼
Post Correction


### OCR Components

- Page rendering: Converts PDF pages into images.
- Image preprocessing: Improves image quality before recognition.
- Language selection: Uses language models such as `amh` and `eng`.
- Character recognition: Detects characters from images.
- Confidence: Measures OCR prediction accuracy.
- Post-correction: Removes OCR errors.

---

# 3. Amharic OCR Challenges

Amharic OCR has additional difficulties:

- Similar-looking characters
- Poor scan quality
- Low resolution images
- Different fonts
- Skewed pages
- Mixed Amharic and English content
- Incorrect punctuation recognition

Therefore, preprocessing and validation are important for legal documents.

---

# 4. Legal Document Cleaning Risks

Legal document cleaning must preserve:

- Article numbers
- Sections and subsections
- Conditions
- Exceptions
- Dates
- Legal references

Incorrect cleaning may change the legal meaning.

Example:

Before:

Article 25(1)
All persons are equal before the law.


After incorrect cleaning:

All persons are equal.


Important legal information may be lost.

---

# 5. Embedding Fundamentals

Embeddings convert text into numerical vectors.

Example:


Legal Text
|
▼
Embedding Model
|
▼
[0.23, 0.56, 0.91, ...]


### Concepts

- Vector: Numerical representation of text.
- Dimension: Number of values inside a vector.
- Document embedding: Vector representation of stored legal documents.
- Query embedding: Vector representation of user questions.
- Semantic similarity: Measures meaning similarity between vectors.

---

# 6. Vector Database Fundamentals

A vector database stores embeddings and enables semantic search.

Important components:

- Collection: Group of stored vectors.
- Vector dimension: Size of embeddings.
- Similarity metric: Measures closeness between vectors.
- ID: Unique identifier.
- Payload/Metadata: Additional information such as article number and source.
- Top-K Search: Returns the most relevant documents.

Example:


User Question
|
▼
Query Embedding
|
▼
Vector Search
|
▼
Top-K Legal Articles


---

# 7. Keyword Search vs Semantic Search

| Keyword Search | Semantic Search |
|---|---|
| Matches exact words | Understands meaning |
| Requires same terms | Finds related concepts |
| Less flexible | More accurate |
| Example: "Article 25" | Example: "right to equality" |

---

# 8. Technology Selection and Justification

## PDF/OCR Method

Selected Method:

**Hybrid Approach**
(PyMuPDF + Tesseract OCR)

Reason:

- PyMuPDF handles digital PDFs.
- Tesseract handles scanned Amharic PDFs.
- Supports both English and Amharic documents.

---

## Embedding Model Comparison


Model	                                    Purpose	                                 Advantage
all-MiniLM-L6-v2	                     General text embeddings	           Fast and lightweight
paraphrase-multilingual-MiniLM-L12-v2	Multilingual semantic search	     Better Amharic support
Selected Model:
paraphrase-multilingual-MiniLM-L12-v2 (Sentence Transformer)

Reason:

Supports Amharic and English legal documents.
Provides multilingual semantic search capability.
Suitable for legal question retrieval.
Uses 384 dimensions, making it fast and efficient for local Qdrant deployment.
---

## Vector Database Selection

Selected: Qdrant
Reason:
   Fast similarity search and advanced metadata filtering.
   Easy local deployment (via Docker or local instance).
   Highly scalable and production-ready.
   Excellent payload (metadata) support, which is critical for storing legal citations (Article, Page, Document Title).

---

# 9. Individual Experiment Plan

Experiment:

1. Extract Ethiopian legal PDF text.
2. Generate embeddings using selected model.
3. Store embeddings in qdrant.
4. Test legal questions.
5. Measure:
   - Retrieval accuracy
   - Article matching
   - Response quality

---

# 10. Mini Architecture Diagram


Legal PDF Documents
|
▼
PDF Processing / OCR
(PyMuPDF + Tesseract)
|
▼
Clean Legal Text
|
▼
Article-level Chunks
|
▼
Embedding Model
|
▼
qdrant Vector Index
|
▼
Semantic Search
|
▼
Retrieved Legal Context
|
▼
Gemini LLM
|
▼
Legal Answer with Citation

base
---

# Conclusion
The reviewed technologies provide the foundation for building the Ethiopian Legal & Justice AI Assistant. A hybrid PDF extraction approach, multilingual embeddings, and qdrant vector search were selected to support accurate legal document retrieval and RAG-based question answering.