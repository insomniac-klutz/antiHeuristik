# Build 09: LLM vs Classical ML Bake-off

## The Ask
Take a tabular prediction problem (churn, fraud, lead scoring — pick one with available data). Build two systems: one with feature engineering + XGBoost/logistic regression, one with LLM embeddings + classification. Compare on accuracy, latency, cost, and explainability. Then build an ensemble router that picks the best model per input.

## Constraints
- Use a real dataset (Kaggle is fine — telco churn, credit fraud, etc.)
- Classical pipeline: proper feature engineering, train/test split, hyperparameter tuning
- LLM pipeline: embed each row's features as text, classify with LLM or use embeddings + classifier
- Benchmark on: accuracy, latency per prediction, cost per 1000 predictions, explainability
- Write a clear recommendation: "for this type of problem, use X because Y"

## What This Forces You to Learn
- When XGBoost beats an LLM — and it will, on this task
- When logistic regression is enough — and why that's fine
- Feature engineering vs embeddings — which problems favor which
- Ensemble basics — routing to whichever model is better per input
- Sequence labeling vs classification vs generation — choosing the right framing
- pandas/polars — data loading, groupby, merge, pivot, window functions for feature engineering
- CSV/Parquet format tradeoffs — chunked reading for large datasets
- Cost modeling — LLM cost per prediction vs classical ML cost (essentially free)

## The Real Lesson
The instinct to throw an LLM at everything is expensive and often wrong. This build gives you the numbers and discipline to know when classical ML wins — the kind of judgement that normally takes years of shipping the wrong solution first.

## Stretch
- Add a polars implementation alongside pandas and benchmark data processing speed
- Test with a problem where the LLM actually wins (e.g., unstructured text classification)
- Build a decision flowchart: "given problem characteristics X, use approach Y"
