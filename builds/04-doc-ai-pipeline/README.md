# paperShredder

> PDFs, scans, garbage formatting. structure it all.

pipeline that ingests messy documents, extracts structured data, and makes everything searchable via natural language. the real world doesn't hand you clean JSON.

## what you're building

- handle PDFs (text + scanned), images with text, tables in documents
- extract structured fields (dates, amounts, names, entities)
- make extracted content searchable via embeddings
- handle failures gracefully (corrupt files, unreadable scans)
- confidence scores for every extraction

## what will break you

- **multimodal models**: knowing when to use vision-language vs OCR vs both
- **table extraction**: tables in PDFs are crimes against structure
- **the 5% that fail**: corrupt files, weird encodings, rotated scans — you need a plan
- **quality metrics**: how do you measure extraction accuracy without labeled data?
- **heterogeneous embeddings**: text chunks and image descriptions in one search space

## why this matters

every company has messy documents. the hard part isn't extracting data from clean PDFs — it's the 5% that fail and the pipeline that has to keep running anyway. multimodal + error handling at scale is where the real skill lives.

## stretch

- human review queue for low-confidence extractions
- multi-language support
- diff/comparison view for contract versions
