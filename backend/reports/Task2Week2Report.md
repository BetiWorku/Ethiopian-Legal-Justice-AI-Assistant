# Task 2: Document Cleaning and Legal Structure Preservation

## Objective
Clean raw OCR extracted legal text while preserving important legal structures such as articles, titles, sections, references, and page information.

## Cleaning Process

Input:

data/raw/extracted_pages.txt


Cleaning Script:

scripts/clean_text.py


Output:

output/constitution_full.txt


## Cleaning Operations Applied

- Removed repeated page headers and footers.
- Removed standalone page numbers and OCR symbols.
- Fixed extra spaces and broken line endings.
- Preserved article numbers and legal headings.
- Removed invalid OCR characters.
- Maintained Amharic and English text structure.

# Before and After Cleaning Examples

## Example 1: Page Number Removal

Before:

PAGE: 12

አንቀጽ 25
የእኩልነት መብት


Cleaning Rule:

Remove standalone page numbers.


After:

አንቀጽ 25
የእኩልነት መብት


---

## Example 2: Header Removal

Before:

SOURCE: Ethiopia_Constitution_Amharic.pdf

አንቀጽ 34
የጋብቻ፣ የግልና የቤተሰብ መብቶች


Cleaning Rule:

Remove repeated document headers while keeping article content.


After:

አንቀጽ 34
የጋብቻ፣ የግልና የቤተሰብ መብቶች


---

## Example 3: Extra OCR Symbols Removal

Before:

========

አንቀጽ 37

========


Cleaning Rule:

Remove OCR-generated separator symbols.


After:

አንቀጽ 37


---

## Example 4: Extra Line Break Cleaning

Before:

ማንኛውም ሰው በሕግ  
ፊት እኩል ነው።


Cleaning Rule:

Join broken lines without changing legal meaning.


After:

ማንኛውም ሰው በሕግ ፊት እኩል ነው።


---

## Example 5: Preserve Legal Structure

Before:

አንቀጽ 34

1.
በሕግ ከተወሰነው የጋብቻ ዕድሜ...


Cleaning Rule:

Preserve article number and subsection numbering.


After:

አንቀጽ 34

1.
በሕግ ከተወሰነው የጋብቻ ዕድሜ...

## Execution Result

Command:

python scripts/clean_text.py


Result:

Original characters: 710277
Cleaned characters: 629762
Saved: output/constitution_full.txt


## Legal Information Preservation

The cleaning process preserves:

- Article numbers
- Article titles
- Sections and subsections
- Legal conditions and exceptions
- Source information for citation

## Cleaning Risks

- OCR may confuse similar Amharic characters.
- Removing text automatically can affect legal meaning.
- Legal numbers and references require verification.