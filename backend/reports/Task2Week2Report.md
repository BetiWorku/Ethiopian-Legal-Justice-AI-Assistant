# Task 2: Document Cleaning and Legal Structure Preservation

## Objective

The goal of this task was to transform raw OCR-extracted Ethiopian legal text into clean, structured, and machine-readable content while preserving the original legal meaning. The cleaned text is used as the input for metadata creation, article chunking, embedding generation, semantic retrieval, and Retrieval-Augmented Generation (RAG).

---

## Cleaning Process

**Input**

```text
data/raw/extracted_pages.txt
```

**Cleaning Script**

```text
scripts/clean_text.py
```
**Output**

```text
output/constitution_full.txt
```
---
## Cleaning Workflow

```text
Raw OCR Text
      │
      ▼
Remove Headers & Footers
      │
      ▼
Remove Page Numbers
      │
      ▼
Normalize Unicode
      │
      ▼
Remove OCR Noise
      │
      ▼
Fix Broken Lines & Spaces
      │
      ▼
Preserve Legal Structure
      │
      ▼
Clean Legal Text
```

---

## Cleaning Operations

The following operations were performed:

- Removed repeated page headers and footers.
- Removed standalone page numbers.
- Removed OCR-generated symbols (e.g., `======`).
- Removed unnecessary blank lines.
- Fixed broken line endings.
- Joined wrapped sentences.
- Removed extra whitespace.
- Normalized Unicode characters.
- Removed invalid OCR control characters.
- Preserved article numbers and article titles.
- Preserved chapters, sections, and subsection numbering.
- Preserved legal references, conditions, and exceptions.
- Preserved Amharic and English text.
- Preserved page source information for future citation generation.

---

## Cleaning Rules

| Rule | Purpose |
|------|---------|
| Remove repeated headers | Eliminate duplicated page titles |
| Remove repeated footers | Remove footer noise |
| Remove standalone page numbers | Reduce OCR artifacts |
| Remove OCR symbols | Clean unnecessary characters |
| Normalize whitespace | Improve readability |
| Join broken lines | Restore complete legal sentences |
| Preserve article numbers | Maintain legal references |
| Preserve headings | Preserve document hierarchy |
| Normalize Unicode | Improve retrieval consistency |

---

## Unicode Normalization

Unicode normalization was applied to remove inconsistent Amharic character encoding and invisible control characters without changing the legal meaning.

Benefits include:

- Better text consistency
- Improved embedding quality
- Better semantic retrieval
- Consistent multilingual processing

---

## Before and After Examples

### Example 1 – Remove Page Number

**Before**

```text
PAGE: 12

አንቀጽ 25
የእኩልነት መብት
```

**After**

```text
አንቀጽ 25
የእኩልነት መብት
```

---

### Example 2 – Remove Header

**Before**

```text
SOURCE: Ethiopia_Constitution_Amharic.pdf

አንቀጽ 34
```

**After**

```text
አንቀጽ 34
```

---

### Example 3 – Remove OCR Symbols

**Before**

```text
========

አንቀጽ 37

========
```

**After**

```text
አንቀጽ 37
```

---

### Example 4 – Fix Broken Lines

**Before**

```text
ማንኛውም ሰው በሕግ
ፊት እኩል ነው።
```

**After**

```text
ማንኛውም ሰው በሕግ ፊት እኩል ነው።
```

---

### Example 5 – Preserve Legal Structure

**Before**

```text
አንቀጽ 34

1.
በሕግ ከተወሰነው...
```

**After**

```text
አንቀጽ 34

1.
በሕግ ከተወሰነው...
```

---

## Execution Result

```bash
python scripts/clean_text.py
```

```
Original characters : 710277
Cleaned characters  : 629762
Saved to            : output/constitution_full.txt
```

---

## Legal Structure Preservation

During cleaning, the following legal elements were intentionally preserved:

- Constitution title
- Preamble
- Chapters and parts
- Article numbers
- Article titles
- Sections and subsections
- Paragraph numbering
- Enumerated lists
- Legal references
- Conditions and exceptions
- Dates
- Source page information

No legal provisions were modified during the cleaning process.

---

## Quality Verification

The cleaned document was manually reviewed to confirm that:

- Article numbers remained correct.
- Article titles were unchanged.
- Paragraph order was preserved.
- OCR artifacts were removed.
- Legal clauses remained intact.
- Constitutional structure was maintained.

---

## Cleaning Risks

Some OCR-related challenges may still remain:

- Similar Amharic characters can be misrecognized.
- Low-quality scans may contain missing characters.
- Over-aggressive cleaning rules could remove legal information.

To minimize these risks, only formatting noise was removed, while all legal content was preserved.

---

## Importance for the RAG Pipeline

The cleaned text is used throughout the retrieval pipeline:

```text
Clean Legal Text
      │
      ▼
Metadata Creation
      │
      ▼
Article Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Qdrant Vector Database
      │
      ▼
Semantic Retrieval
      │
      ▼
Retrieved Legal Context
      │
      ▼
Gemini LLM
      │
      ▼
Grounded Legal Response
```

A high-quality cleaning process improves embedding quality, retrieval accuracy, citation reliability, and reduces hallucinations during response generation.

---

## Deliverables

- ✅ `scripts/clean_text.py`
- ✅ Raw extracted text (`data/raw/extracted_pages.txt`)
- ✅ Cleaned text (`output/constitution_full.txt`)
- ✅ Cleaning rules documentation
- ✅ Five before-and-after examples
- ✅ Legal structure preservation explanation
- ✅ Cleaning risks documentation

---

## Conclusion

The document cleaning pipeline successfully converted noisy OCR output into clean, structured legal text while preserving the constitutional hierarchy and legal meaning. Removing headers, footers, page numbers, OCR artifacts, and formatting inconsistencies improved text quality without affecting legal provisions. The cleaned document now provides reliable input for metadata generation, article chunking, embedding generation, Qdrant vector storage, semantic retrieval, and Retrieval-Augmented Generation (RAG) in the Ethiopian Legal & Justice AI Assistant.