# nlp — Theo Index

## Files
- evaluation.md — LLM evaluation methods, recall patterns, and behavioral failure modes

## evaluation.md
- Methods & Frameworks — tools and protocols for testing LLM context handling
  - Needle in a Haystack (NIAH) — standard buried-fact retrieval benchmark and its limitations
  - Scripted Dialogue Evaluation — deterministic conversation scripts for reproducible testing
  - Probe Design — injected recall questions at fixed intervals with four probe types
  - Scoring Categories — pass/hedge/fail/confabulate taxonomy for probe responses
  - Ground Truth Control — mixing real and fabricated facts to detect training data leakage
  - Run-Until-Failure vs Fixed Turn Count — finding natural breaking points instead of arbitrary cutoffs
- Behavioral Patterns — observed LLM failure modes in extended conversations
  - Sycophancy at Long Context — models increasingly agree with users as context grows
  - Schema-Consistent vs Schema-Inconsistent Retrieval — narrative-supported vs isolated fact recall and where confabulation hides
