# Layer 1: Eval

**Apply after**: MVP works.
**Apply before**: any optimization — you can't improve what you can't measure.

---

## The Ask
Build a reusable evaluation system for this build's MVP. Not a toy — something you'd actually use in production to catch regressions.

## What You Must Produce
- Eval dataset — curated inputs with expected behavior (not necessarily exact outputs)
- Metric suite — what numbers define "good" for THIS specific system
- Baseline measurement — the MVP's current quality, quantified
- Automated runner — re-run eval after any change, compare against baseline
- Failure analysis — categorize where and why the system fails

## What This Forces You to Learn
- LLM-as-judge design (criteria, rubrics, calibration)
- Reference-free evaluation (when you don't have ground truth)
- Eval dataset construction and curation
- Hallucination detection techniques
- Statistical significance in small-sample eval
- Metric design — what to measure varies per system:
  - RAG → retrieval precision, answer faithfulness, citation accuracy
  - Agent → task completion rate, tool use accuracy, loop rate
  - NL2SQL → query correctness, execution success, result accuracy
  - Voice → transcription accuracy, end-to-end latency, task completion
  - Code review → precision, recall, false positive rate
  - Doc AI → extraction accuracy, field-level F1, confidence calibration
- CI integration for LLM quality gates

## Interview Translation
"How do you know your LLM system is working?" — asked in every serious interview. Most candidates mumble about BLEU scores. You'll whiteboard an eval architecture specific to the system type.

## Stretch
- A/B testing framework for prompt variants
- Automatic adversarial test generation (red-teaming the eval itself)
- Eval dashboard with drill-down into failure categories
