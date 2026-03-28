# Layer 3: Feedback Flywheel

**Apply after**: Cost Killer — the system should be measured and optimized before adding learning.
**Apply before**: Catastrophe — the feedback loop should be running when you stress-test.

---

## The Ask
Add a feedback loop that makes this build's system improve over time from user interactions. Not fine-tuning as a one-shot — a continuous improvement pipeline.

## What You Must Produce
- Feedback collection mechanism (explicit thumbs up/down + implicit signals)
- Feedback → action pipeline (how feedback becomes prompt updates, retrieval tuning, or fine-tuning data)
- Before/after measurement using your eval layer — prove the system actually improved
- Noise handling — users are wrong sometimes, system should be robust to bad feedback

## What This Forces You to Learn
- RLHF concepts at an applied level (not the math — the pipeline)
- Preference data collection and curation
- Active learning (which examples to label next for maximum impact)
- Annotation pipeline design
- Fine-tuning decision tree (when feedback means fine-tune vs fix the prompt vs fix retrieval)
- Fine-tuning mechanics: LoRA/QLoRA, data curation, evaluation of fine-tuned vs base
- Continuous eval (measuring improvement over time, not just point-in-time)
- Data flywheel economics (when more data helps vs when it doesn't)

## The Real Lesson
Shipping v1 is table stakes. Owning a system means making it improve over time from real usage. This layer is the difference between "I built it" and "I made it learn."

## Stretch
- Implement a preference model that learns from feedback
- Add automatic prompt optimization based on failure patterns
- Build a labeling interface for human annotators
- Actually fine-tune a small model on collected preferences, compare against prompt-only baseline
- Cost-benefit: "fine-tuning saved X% on inference but cost Y in compute and Z in pipeline complexity"
