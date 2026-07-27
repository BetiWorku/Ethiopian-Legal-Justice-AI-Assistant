# Task 3: Legal Metadata and Structured Chunk Preparation

## Objective

Prepared structured metadata for Ethiopian legal document chunks to support retrieval, filtering, citation generation, and traceability in the RAG pipeline.

---

## Metadata Added

Each legal chunk contains:

- Document ID
- Document title
- Document type
- Article number
- Article title
- Topic
- Language
- Jurisdiction
- Source information
- Page information
- Document status
- Chunk index

---

## Output

Generated file:


data/chunks/article_chunks_metadata.json


---

## Metadata Data Dictionary

| Field | Description |
|---|---|
| document_id | Unique identifier for the legal document |
| document_title | Name of the legal document |
| document_type | Type of document (constitution, law, regulation) |
| article | Legal article number |
| article_title | Title of the article |
| topic | Main legal topic |
| language | Document language (am/en) |
| jurisdiction | Legal authority level |
| page_start | Starting page number of the article |
| page_end | Ending page number of the article |
| source | Original document citation source |
| status | Current document status |
| chunk_index | Order of chunk inside the document |

---

## Example Metadata Record

```json
{
    "id": "fdre_constitution_article_1_chunk_001",
    "text": "አንቀጽ 1\nየኢትዮጵያ መንግሥት ስያሜ...",
    "metadata": {
        "document_id": "fdre_constitution_amharic_1995",
        "document_title": "FDRE Constitution",
        "document_type": "constitution",
        "article": "Article 1",
        "article_title": "የኢትዮጵያ መንግሥት ስያሜ",
        "topic": "የኢትዮጵያ መንግሥት ስያሜ",
        "language": "am",
        "jurisdiction": "Federal",
        "page_start": 2,
        "page_end": 2,
        "source": "FDRE Constitution, Article 1",
        "status": "active",
        "chunk_index": 1
    }
}
Page Information Handling

Page numbers are extracted from the original OCR document structure.

Example:

Article 1 starts on page 2
Article 3 starts on page 3
Article 4 starts on page 3

This allows future citation generation:

Example:

Source:
FDRE Constitution, Article 1, Page 2
Metadata Validation

Validation checks:

Required fields exist
Chunk IDs are unique
Document IDs are valid
Chunk text is not empty
Language values are controlled
Status values are valid
Source information exists
Page numbers are valid
Importance

Metadata allows the RAG system to:

Filter legal documents by article and language
Retrieve accurate legal context
Generate citations with document references
Track every answer back to the original legal source
Improve semantic search accuracy

### Conclusion

Structured metadata prepares Ethiopian legal documents for reliable retrieval. By storing article, page, language, and source information, the system can provide traceable and citation-based legal answers.