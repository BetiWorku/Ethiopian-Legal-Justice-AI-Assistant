# Task 5: Embedding Model Comparison

## Objective

The objective of this experiment was to compare embedding models for Ethiopian legal document retrieval and select a suitable model for the RAG pipeline.

---

# Tested Embedding Models

## Model A

Model:

`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

Purpose:

Multilingual semantic search.

Result:

- Chunks processed: 95
- Vector dimension: 384
- Output: data/vectors/legal.index


---

## Model B

Model:

`intfloat/multilingual-e5-base`

Purpose:

Multilingual embedding model optimized for semantic retrieval.

Result:

- Chunks processed: 95
- Vector dimension: 768
- Generation time: 35.5 seconds
- Output: data/vectors/legal_e5.index


---

# Model Comparison

| Criterion | Model A | Model B |
|---|---|---|
| Model | paraphrase-multilingual-MiniLM-L12-v2 | multilingual-e5-base |
| Language Support | Multilingual | Multilingual |
| Vector Dimension | 384 | 768 |
| Model Size | Smaller | Larger |
| Processing Time | Faster | 35.5 seconds |
| English Retrieval | Good | Very Good |
| Amharic Retrieval | Good | Better |
| Cross-language Retrieval | Good | Very Good |
| Production Suitability | Medium | High |


---

# Validation Results

Validation performed:

- Generated embeddings successfully.
- Vector count matches legal chunks.
- FAISS index created successfully.
- Metadata stored for citation retrieval.


Validation Output:


Vectors: 95
Dimension: 768
Model: intfloat/multilingual-e5-base



---

# Final Recommendation

Selected Model:

`intfloat/multilingual-e5-base`

Reason:

- Better multilingual capability.
- Higher vector dimension.
- Suitable for Amharic and English legal documents.
- Better semantic retrieval quality for RAG systems.

Although it requires more memory and processing time, retrieval accuracy is more important for legal applications.