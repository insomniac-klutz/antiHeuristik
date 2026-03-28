# overHyped

> XGBoost vs GPT-4. tabular data. place your bets.

take a real tabular prediction problem — churn, fraud, lead scoring. build it twice: classical ML with proper feature engineering, and LLM with embeddings. compare on accuracy, latency, cost, explainability. then build a router that picks the best model per input.

## what you're building

- real dataset (telco churn, credit fraud, etc.)
- classical pipeline: feature engineering, train/test split, hyperparameter tuning
- LLM pipeline: embed row features as text, classify with LLM or embeddings + classifier
- benchmark on: accuracy, latency per prediction, cost per 1000 predictions, explainability
- clear recommendation: "for this type of problem, use X because Y"

## what will break you

- **the LLM will lose**: on tabular data, XGBoost wins. accepting this is the point
- **cost modeling**: LLM cost per prediction vs classical ML (essentially free at inference)
- **feature engineering vs embeddings**: knowing which problems favor which approach
- **ensemble routing**: picking the right model per input without adding latency
- **explainability gap**: SHAP values vs "the model said so"

## why this matters

the instinct to throw an LLM at everything is expensive and often wrong. this build gives you the numbers to know when classical ML wins — and the discipline to pick the right tool, not the shiniest one.

## stretch

- polars implementation alongside pandas
- find a problem where the LLM actually wins (unstructured text classification)
- decision flowchart: "given problem characteristics X, use approach Y"
