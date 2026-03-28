# Build 04: NL2SQL Analytics Dashboard

## The Ask
Build a system where users type natural language questions and get SQL queries, results, and auto-generated visualizations. This is YOUR domain — treat this build as polishing your sharpest weapon.

## Constraints
- Multi-table schema (5+ tables with joins)
- Must handle ambiguous questions ("show me top customers" — by revenue? by orders? by recency?)
- Must validate generated SQL before execution
- Must handle errors gracefully (bad SQL, no results, timeout)
- Show the SQL to the user (transparency)

## What This Forces You to Learn
- Schema linking (mapping NL terms to table/column names)
- Query validation and safety (prevent DROP TABLE, injection)
- Error recovery (bad SQL → diagnose → retry with feedback)
- Disambiguation strategies (ask user vs best-guess)
- Complex SQL: window functions, CTEs, self-joins, subqueries
- Result presentation (when to chart, when to table, when to summarize)
- Prompt engineering for structured output (SQL is unforgiving)

## The Real Lesson
NL2SQL looks simple in demos and breaks in every non-trivial case. Ambiguity, safety, error recovery, complex joins — the gap between "it works on happy path" and "someone can trust this with real data" is where all the learning lives.

## Stretch
- Add query caching (same question, same result without re-running)
- Support "follow-up" queries ("now filter that by last quarter")
- Add query explanation ("here's what this SQL does in plain English")
