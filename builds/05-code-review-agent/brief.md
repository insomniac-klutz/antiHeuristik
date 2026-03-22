# Build 06: Code Review Agent

## The Ask
Build an agent that reads pull requests, identifies issues (bugs, style, security, performance), and suggests fixes with explanations. You've built production code-review tooling before — sharpen it.

## Constraints
- Must read actual diffs (not full files — context-window efficient)
- Must categorize findings (bug, style, security, perf, nitpick)
- Must suggest fixes, not just flag problems
- Must handle multi-file PRs
- False positive rate matters — noisy reviewers get ignored

## What This Forces You to Learn
- Code representation for LLMs (diffs, AST, context windows)
- Agentic planning (which files to read, what context to gather)
- Structured output (findings as structured data, not prose)
- Prompt engineering for code understanding
- Precision/recall tradeoffs in classification
- Tool use (git operations, file reading, linting)

## Interview Translation
"You've built code review tooling — go deeper." This build gives you a whiteboard-ready architecture for that conversation.

## Stretch
- Add auto-fix capability (generate the corrected code)
- Add learning from past reviews (what did human reviewers flag?)
- Security-focused mode (OWASP top 10 detection)
