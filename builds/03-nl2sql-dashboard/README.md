# sqlMePlz

> beg the database in english, get SQL back.

users type natural language questions, get SQL queries, results, and auto-generated visualizations. this is your domain — make it your sharpest weapon.

## what you're building

- multi-table schema (5+ tables with joins)
- handle ambiguous questions ("show me top customers" — by revenue? orders? recency?)
- validate generated SQL before execution (no DROP TABLE surprises)
- show the SQL to the user — transparency, not magic
- error recovery: bad SQL → diagnose → retry with feedback

## what will break you

- **schema linking**: mapping "top customers" to the right table and column
- **disambiguation**: when to ask the user vs best-guess
- **complex SQL**: window functions, CTEs, self-joins — the LLM will fumble these
- **injection safety**: user input → SQL is a minefield
- **result presentation**: when to chart, when to table, when to summarize

## why this matters

NL2SQL is deceptively hard — ambiguity, safety, error recovery. the gap between a demo and a system someone can trust with real data is where the learning lives.

## stretch

- query caching for repeated patterns
- follow-up queries ("now filter that by Q4")
- query explanation in plain english
