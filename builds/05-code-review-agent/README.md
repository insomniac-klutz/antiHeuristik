# diffWhisperer

> read the diff. find the bug. skip the nitpick.

agent that reads pull requests, identifies real issues — bugs, security holes, perf traps — and suggests fixes with explanations. noisy reviewers get muted. this one earns trust.

## what you're building

- read actual diffs (not full files — context-window efficient)
- categorize findings: bug, style, security, perf, nitpick
- suggest fixes, not just flag problems
- handle multi-file PRs
- false positive rate matters more than recall

## what will break you

- **code representation**: diffs vs ASTs vs full files — each has tradeoffs for LLM comprehension
- **precision/recall**: flag everything and developers ignore you. miss a bug and why do you exist?
- **structured output**: findings as structured data, not prose blobs
- **context gathering**: which files to read beyond the diff, and when to stop
- **tool use**: git operations, file reading, linting — the agent needs to explore

## why this matters

code review agents are the testbed for precision vs recall in LLM systems. building one teaches you how to make an AI tool that people actually keep turned on instead of muting after day two.

## stretch

- auto-fix capability (generate corrected code)
- learning from past human reviews
- security-focused mode (OWASP top 10 detection)
