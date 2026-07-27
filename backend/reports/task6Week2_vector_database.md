# Task 6: Vector Database Implementation

## Objective

The goal of this task was to store Ethiopian legal document embeddings, text chunks, and metadata in a vector database to support semantic search and RAG retrieval.

## Vector Database

Selected Database:

**Qdrant**

Reasons:

- Open-source vector database.
- Supports semantic similarity search.
- Supports metadata filtering.
- Suitable for RAG applications.

---

## Setup

Run Qdrant with Docker:

```bash
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant

Dashboard:

http://localhost:6333/dashboard
Collection Configuration

Collection Name:

legal_documents

Embedding Model:

intfloat/multilingual-e5-base

Vector Dimension:

768

Similarity Metric:

Cosine Similarity
Implementation Files
1. Collection Setup

File:

scripts/qdrant_setup.py

Functions:

Connect to Qdrant.
Create collection.
Configure vector size and distance.
Display collection statistics.
2. Vector Insertion

File:

scripts/qdrant_insert.py

Process:

Load FAISS embeddings.
Load legal metadata.
Convert chunks into Qdrant points.
Insert vectors and payload.

Stored data:

Chunk ID
Document information
Article number
Language
Source
Legal text
Metadata
Insertion Result

Command:

python scripts/qdrant_insert.py

Output:

Vectors count: 95
Vector dimension: 768
Distance: Cosine
Testing and Filtering

File:

scripts/qdrant_test.py

Tested features:

Retrieve record by ID.
Language filtering.
Article filtering.

Example:

Language filter:

language = "am"

Article filter:

article = "Article 25"
Duplicate Handling

Handled using Qdrant upsert() operation.

Prevents duplicate vector IDs.
Updates existing records when ID already exists.
Error Handling

Implemented:

Qdrant connection checking.
Collection validation.
Vector dimension checking.
File loading error handling.
Final Statistics
Item	Value
Collection	legal_documents
Vectors	95
Dimension	768
Similarity	Cosine
Status	Active
Importance for RAG

Qdrant enables:

Semantic legal search.
Fast retrieval of legal articles.
Metadata filtering.
Citation generation.
Multilingual legal question answering.
Conclusion

Qdrant was successfully integrated into the Ethiopian Legal AI Assistant system and provides the vector storage foundation required for the RAG pipeline.