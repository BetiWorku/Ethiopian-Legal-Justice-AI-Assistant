# Task 6: Vector Database Implementation

## Objective

The objective of this task was to store Ethiopian legal document embeddings, text chunks, and metadata in a vector database to support semantic search and Retrieval-Augmented Generation (RAG).

The vector database stores:

- Legal chunk embeddings
- Original legal text
- Document metadata
- Article information
- Language information
- Source information

This enables accurate legal retrieval with traceable citations.

---

# Vector Database Selection

## Selected Database

**Qdrant**

## Reasons for Selecting Qdrant

Qdrant was selected because:

- Open-source and optimized for vector similarity search.
- Supports metadata filtering through payloads.
- Provides fast semantic retrieval.
- Supports multilingual RAG applications.
- Supports upsert operations for duplicate handling.
- Easy local deployment using Docker.
- Suitable for production retrieval systems.

---

# Setup Instructions

## Run Qdrant Using Docker

Run the following command:

```bash
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant
```

## Access Qdrant Dashboard

```
http://localhost:6333/dashboard
```

The dashboard was used to verify:

- Collection creation
- Stored vectors
- Collection statistics
- Payload metadata

---

# Collection Configuration

## Collection Name

```
legal_documents
```

## Embedding Model

```
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

## Vector Configuration

| Configuration | Value |
|---|---|
| Vector Dimension | 384 |
| Similarity Metric | Cosine Similarity |
| Total Vectors | 95 |

---

# Similarity Metric Selection

The system uses:

```
Cosine Similarity
```

## Reason

Cosine similarity measures the semantic similarity between text embeddings by comparing the angle between vectors.

It is suitable for legal document retrieval because:

- Similar meanings produce closer vector representations.
- Document length has less influence.
- It is widely used in semantic search systems.

---

# Implementation Files

## 1. Collection Setup and Vector Insertion

File:

```
scripts/embedding.py
```

## Responsibilities

The script performs:

- Connection to Qdrant.
- Collection creation.
- Vector dimension validation.
- Embedding generation.
- Vector insertion.
- Payload storage.
- Error handling.

---

# Collection Creation Process

The script:

1. Connects to Qdrant server.
2. Checks whether the collection exists.
3. Validates vector dimension.
4. Deletes and recreates collection if dimensions mismatch.
5. Creates a collection with 384 dimensions.
6. Uploads vectors in batches.

Example:

```python
client.create_collection(
    collection_name="legal_documents",
    vectors_config=models.VectorParams(
        size=384,
        distance=models.Distance.COSINE
    )
)
```

---

# Vector Insertion Process

Legal chunks are converted into Qdrant points containing:

- Vector embeddings
- Chunk ID
- Legal text
- Metadata payload

## Stored Information

Each vector stores:

- Document title
- Article number
- Article title
- Language
- Page information
- Source
- Original legal text

---

# Example Vector Record

```json
{
  "id": "fdre_article_25_chunk_001",
  "vector": [
    0.012,
    -0.023,
    0.108
  ],
  "payload": {
    "document_title": "FDRE Constitution",
    "article": "Article 25",
    "title": "Right to Equality",
    "language": "am",
    "page_start": 9,
    "page_end": 9,
    "source": "FDRE Constitution, Article 25",
    "text": "All persons are equal before the law..."
  }
}
```

---

# Duplicate Chunk ID Handling

Duplicate handling is implemented using Qdrant:

```
upsert()
```

## Behavior

- If a chunk ID does not exist → creates a new vector.
- If a chunk ID already exists → updates the existing record.
- Prevents duplicate legal chunks.

Example:

```python
client.upsert(
    collection_name="legal_documents",
    points=points
)
```

## Testing

Running:

```bash
python scripts/embedding.py
```

multiple times safely updates the existing 95 records without creating duplicates.

---

# Record Retrieval by ID

File:

```
scripts/retrieval.py
```

The system can retrieve stored legal chunks using Qdrant queries.

Example:

```python
client.scroll(
    collection_name="legal_documents",
    scroll_filter=filter
)
```

Retrieved information includes:

- Article number
- Language
- Source
- Legal text
- Metadata

---

# Metadata Filtering

The system supports metadata-based filtering.

## 1. Language Filter

### Purpose

Retrieve documents based on language.

Example:

```python
language = "am"
```

Use case:

Retrieve only Amharic constitutional articles.

---

## 2. Article Filter

### Purpose

Retrieve specific constitutional articles.

Example:

User Query:

```
What is Article 25 about?
```

The system extracts:

```
Article 25
```

and applies:

```python
search_filter = models.Filter(
    must=[
        models.FieldCondition(
            key="article",
            match=models.MatchValue(
                value="Article 25"
            )
        )
    ]
)
```

Result:

Only Article 25 chunks are retrieved.

---

# Error Handling

The implementation includes several error-handling mechanisms.

## 1. Connection Error Handling

If Qdrant is unavailable:

```
Qdrant connection failed
```

The system returns a safe error message instead of crashing.

---

## 2. Dimension Validation Error

### Problem

Existing collection dimension does not match embedding dimension.

### Solution

The system:

1. Detects dimension mismatch.
2. Deletes incorrect collection.
3. Creates a new collection with the correct dimension.

---

## 3. File Loading Errors

Handled cases:

- Missing chunk files.
- Missing metadata files.
- Invalid embedding files.

---

# Collection Statistics

| Item | Value |
|---|---|
| Collection Name | legal_documents |
| Total Vectors | 95 |
| Vector Dimension | 384 |
| Similarity Metric | Cosine |
| Embedding Model | paraphrase-multilingual-MiniLM-L12-v2 |
| Status | Active |

---

# Populated Vector Collection

The Qdrant collection contains:

```
95 legal document vectors
```

Each vector contains:

- Semantic embedding
- Legal article metadata
- Source information
- Original legal text

The collection is ready for semantic retrieval.

---

# Importance for RAG Pipeline

Qdrant provides the retrieval layer of the Ethiopian Legal AI Assistant.

It enables:

## Semantic Legal Search

Retrieves relevant legal articles even when user questions are paraphrased.

Example:

Question:

```
What protects equal treatment before the law?
```

Retrieved:

```
Article 25 - Right to Equality
```

---

## Fast Retrieval

Qdrant returns Top-K relevant legal chunks efficiently.

---

## Citation Generation

Payload metadata provides:

- Article number
- Source document
- Page information
- Original legal text

This allows generated answers to include traceable legal citations.

---

## Multilingual Retrieval

Supports:

- English queries
- Amharic queries
- Cross-language retrieval

Example:

English Question:

```
What is freedom of expression?
```

Can retrieve:

```
Amharic constitutional text
```

---

# Conclusion

Qdrant was successfully integrated into the Ethiopian Legal AI Assistant system.

The implementation provides:

- Vector storage
- Semantic search
- Metadata filtering
- Duplicate prevention
- Error handling
- Citation-ready retrieval

The Qdrant vector database completes the retrieval foundation required for the RAG pipeline:

```
User Question
       |
       ↓
Embedding Generation
       |
       ↓
Qdrant Semantic Search
       |
       ↓
Relevant Legal Chunks
       |
       ↓
LLM Response with Citation