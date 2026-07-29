# Task 5: Embedding Model Comparison
## Ethiopian Legal Semantic Retrieval System

## 1. Objective

The goal of this experiment was to compare different embedding models and select the best model for the Ethiopian Legal Retrieval-Augmented Generation (RAG) system.

The experiment focused on:

- Generating vector embeddings from Ethiopian legal document chunks.
- Testing multilingual retrieval performance.
- Comparing English, Amharic, and cross-language search.
- Selecting a scalable embedding model for legal semantic search.

The selected model should retrieve relevant legal articles based on meaning, not only exact keywords.

---

# 2. Embedding Generation Pipeline

The embedding pipeline converts legal text chunks into numerical vectors that can be searched using semantic similarity.


Legal Document Chunks
|
v
Chunk Loading
|
v
Embedding Model
|
v
Vector Generation
|
v
Embedding Validation
|
v
Qdrant Vector Database
|
v
Semantic Retrieval


---

# 3. Embedding Generation Module

## Implementation Files


scripts/
│
├── embedding.py
└── embedding_e5.py


## Responsibilities

The embedding modules:

- Load legal chunks from Task 4.
- Generate dense vector embeddings.
- Validate vector dimensions.
- Store embeddings in Qdrant.
- Keep metadata connection for citation generation.

## Input


data/chunks/article_chunks.json


Example:

```json
{
  "article": "Article 25",
  "title": "Right to Equality",
  "text": "All persons are equal before the law..."
}
Output

Generated vectors stored in Qdrant:

Collection	Dimension
legal_documents	768
legal_documents_test	384
4. Tested Embedding Models

Two multilingual embedding models were evaluated.

Model A
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
Purpose

A lightweight multilingual embedding model for semantic similarity search.

Results
Metric	Result
Chunks processed	95
Vector dimension	384
Generation time	~20.9 seconds
Language support	Multilingual
Database	Qdrant
Advantages
Fast embedding generation.
Small memory requirement.
Easy deployment.
Limitations
Weak pure semantic retrieval for legal concepts.
Amharic retrieval performance was lower.
Required additional methods:
Keyword mapping.
KeyBERT extraction.
Manual boosting rules.

Example:

Query:

የእኩልነት መብት ምንድነው?

Without additional rules:

Retrieved:
Article 89
Article 4
Article 91

Expected:

Article 25
Model B (Selected)
intfloat/multilingual-e5-base
Purpose

A multilingual embedding model designed specifically for semantic retrieval.

It supports asymmetric retrieval:

Short User Query
        |
        v
Long Legal Document Passage

which matches the RAG architecture.

Results
Metric	Result
Chunks processed	95
Vector dimension	768
Generation time	~46 seconds
Language support	Multilingual
Database	Qdrant
Advantages
Strong semantic understanding.
Better legal concept matching.
Excellent English-Amharic retrieval.
Works without hardcoded keyword rules.
More scalable for future documents.
Limitations
Larger model size.
Higher memory usage.
Slower embedding generation.
5. Embedding Model Comparison
Criterion	MiniLM-L12	multilingual-e5-base
Model Name	paraphrase-multilingual-MiniLM-L12-v2	intfloat/multilingual-e5-base
Language Support	Multilingual	Multilingual
Vector Dimension	384	768
Model Size	~120 MB	~2.2 GB
Processing Time	~20.9 seconds	~46 seconds
English Retrieval	Medium	Excellent
Amharic Retrieval	Low without rules	Very Good
Cross-language Retrieval	Medium	Excellent
Semantic Understanding	Limited	Strong
Memory Requirement	Low	Higher
Production Suitability	Medium	High
6. Embedding Validation Results

The generated embeddings were validated before retrieval testing.

Validation checks:

Embeddings generated successfully.
Vector count matched legal chunks.
Dimensions were correct.
Qdrant collections were created.
Metadata remained connected with vectors.
Selected Model Output
Vectors: 95

Dimension: 768

Model:
intfloat/multilingual-e5-base

Vector Database:
Qdrant
7. Retrieval Evaluation

The models were tested using a legal retrieval dataset containing:

15 Evaluation Questions

Test categories:

Direct legal questions.
Paraphrased questions.
Article number questions.
Broad legal topics.
Amharic questions.
Cross-language questions.
Unsupported questions.
8. Retrieval Results
English Retrieval

Query:

What does Ethiopian law say about equality before the law?

Expected:

Article 25

Results:

Model	Result
MiniLM-L12	Failed without keyword boosting
multilingual-e5-base	Correctly retrieved Article 25
Amharic Retrieval

Query:

የእኩልነት መብት ምንድነው?

Expected:

Article 25

Results:

Model	Result
MiniLM-L12	Required manual mapping
multilingual-e5-base	Retrieved Article 25 semantically
Cross-Language Retrieval

Query:

What does Ethiopian law say about ግል ሕይወት (privacy)?

Expected:

Article 26

Results:

Model	Result
MiniLM-L12	Failed due to translation mismatch
multilingual-e5-base	Successfully retrieved Article 26
9. Final Recommendation
Selected Model
intfloat/multilingual-e5-base
Reason for Selection

The multilingual-e5-base model was selected because it provides better semantic retrieval performance for Ethiopian legal documents.

Reasons:
1. Better Semantic Understanding

E5 achieved higher retrieval accuracy using pure vector similarity.

Model	Hit Rate
MiniLM-L12	20% without rules
multilingual-e5-base	73.33%
2. Better Scalability

MiniLM required:

Manual keyword dictionaries.
Article mappings.
Extra ranking rules.

E5 understands legal meaning directly and requires fewer manual updates.

3. Better Cross-Language Support

E5 successfully handled:

English queries.
Amharic queries.
Mixed English-Amharic queries.

Example:

privacy + ግል ሕይወት

Retrieved:

Article 26
4. Suitable for RAG Pipeline

The model fits the architecture:

User Question
       |
       v
Query Embedding
       |
       v
Vector Search
       |
       v
Relevant Legal Passage
       |
       v
LLM Answer Generation
10. Conclusion

The experiment showed that embedding model selection strongly affects legal retrieval quality.

The MiniLM model is faster and smaller but struggles with complex legal concepts, especially Amharic and cross-language retrieval.

The multilingual-e5-base model provides:

Better semantic understanding.
Higher retrieval accuracy.
Strong multilingual support.
Better production scalability.

