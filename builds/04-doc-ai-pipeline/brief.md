# Build 05: Document AI Pipeline

## The Ask
Build a pipeline that ingests messy documents (PDFs, scanned images, mixed-format), extracts structured data, and makes everything searchable via natural language.

## Constraints
- Handle at least: PDFs (text + scanned), images with text, tables in documents
- Extract structured fields (dates, amounts, names, entities)
- Make extracted content searchable via embeddings
- Pipeline must handle failures gracefully (corrupt files, unreadable scans)
- Show confidence scores for extractions

## What This Forces You to Learn
- Multimodal models — vision-language for document understanding
- OCR + LLM pipelines (when to use each, how to combine)
- Document parsing strategies (layout detection, table extraction)
- Structured data extraction from unstructured text (NER, regex, LLM extraction)
- Embedding pipeline design for heterogeneous content
- Error handling at scale (what do you do with 5% of docs that fail?)
- Quality metrics for extraction accuracy

## The Real Lesson
Every company has messy documents. The hard part isn't the happy path — it's the 5% that fail and the pipeline that has to keep running. Multimodal processing + error handling at scale is where the real understanding develops.

## Stretch
- Add a human review queue for low-confidence extractions
- Handle multi-language documents
- Build a comparison view (diff two versions of a contract)
