# Build 12: Greenfield AI Scoping Simulator

## The Ask
This is not a codebase — it's a structured decision exercise. Take 5 real-world company scenarios and produce a 1-page scoping doc for each. Then build the ONE that actually makes sense.

## The 5 Scenarios

### Scenario A: "We're a logistics company. Our competitors have AI-powered route optimization. We need AI too."
- Is AI actually the gap, or is it better data/UX?
- Classical optimization might beat LLMs here — prove it or disprove it

### Scenario B: "We're a legal tech startup. We want an AI that reads contracts and flags risky clauses."
- This is a real AI problem. Scope the MVP.
- What's the simplest version that proves value? What do you cut?

### Scenario C: "We're an e-commerce platform. Add AI to increase conversion."
- Ambiguous. 50 possible AI features. Which ONE do you build first?
- How do you prioritize with incomplete data?

### Scenario D: "We want a chatbot for our internal knowledge base."
- Everyone wants this. Most implementations suck. Why?
- When is RAG enough? When do you need agents? When is search enough without AI?

### Scenario E: "Our customer support costs $2M/year. Use AI to cut it in half."
- Clear business objective. Multiple AI approaches.
- When should you say "AI won't do this" vs "AI can do part of this"?

## What Each Scoping Doc Must Contain
1. Problem definition (what's actually being solved, not what was asked)
2. Proposed approach (including "don't use AI" if that's the answer)
3. Why this approach over alternatives
4. MVP definition (smallest thing that proves value)
5. What you're explicitly cutting and why
6. Cost estimate (build + run)
7. Risk assessment (what could go wrong, what's the blast radius)
8. Success metrics (before writing a line of code)

## What This Forces You to Learn
- Ambiguity navigation — scoping from a vague stakeholder request
- Saying no — when AI isn't the right solution (Scenario A might be this)
- Prioritization under uncertainty — which of 50 features to build first
- "Our competitors have AI" — is the AI actually their advantage?
- When classical ML wins — route optimization, churn, tabular prediction
- Cost modeling from scratch — not optimizing an existing system, estimating a new one
- Stakeholder communication — explaining technical decisions to non-technical people

## Interview Translation
"How would you add AI to our product?" — the most common open-ended question at Series B-D startups. This exercise trains the muscle for that exact conversation.

## The Build Phase
Pick the one scenario where AI genuinely makes sense. Build it. Apply all 4 layers. This is where the exercise becomes antiHeuristic — the scoping forces strategic thinking, then you build the thing you scoped.

## Stretch
- Present each scoping doc to someone and get pushback. Revise.
- Add a "6 months later" retrospective for each: what would you have learned by now?
- For the "don't use AI" scenarios, propose the non-AI solution and estimate its impact