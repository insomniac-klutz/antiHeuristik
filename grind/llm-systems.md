# LLM Systems Architecture

The core. 80% of Applied AI work lives here.

## RAG
- [ ] Chunking strategies — semantic vs fixed vs recursive
- [ ] Embedding model selection and benchmarking
- [ ] Reranking — cross-encoders vs ColBERT, when each wins
- [ ] Hybrid search — dense + sparse (BM25 + embeddings)
- [ ] Metadata filtering in vector search
- [ ] Citation / grounding — proving where an answer came from
- [ ] When RAG fails and why (garbage in, wrong chunks, lost-in-middle)
- [ ] Multi-hop RAG — chaining retrievals

## Agents
- [ ] ReAct loop — observe, think, act, repeat
- [ ] Tool use / function calling — design and implementation
- [ ] Planning loops — task decomposition, replanning on failure
- [ ] Memory architectures — short-term (session), long-term (knowledge)
- [ ] Multi-agent orchestration — when and how
- [ ] Human-in-the-loop design — escalation, approval gates
- [ ] When agents are overkill vs necessary

## Prompt Engineering
- [ ] System prompt design at scale
- [ ] Few-shot selection strategies — static vs dynamic vs similarity-based
- [ ] Structured outputs — JSON mode, constrained decoding, grammar enforcement
- [ ] Prompt versioning and management in production
- [ ] Prompt compression / optimization for cost

## Eval & Guardrails
- [ ] LLM-as-judge — criteria, rubrics, calibration
- [ ] Reference-free evaluation — when you don't have ground truth
- [ ] Hallucination detection techniques
- [ ] Input guardrails — content filtering, injection detection
- [ ] Output guardrails — format validation, safety filtering
- [ ] Red-teaming frameworks
- [ ] Eval dataset construction — what makes a good eval set
- [ ] A/B testing LLM outputs with statistical rigor

## Fine-Tuning
- [ ] Decision tree: when to fine-tune vs prompt vs RAG
- [ ] LoRA / QLoRA mechanics — what's happening, why it works
- [ ] Data curation for fine-tuning — quality over quantity
- [ ] Evaluating fine-tuned models against base
- [ ] Cost-benefit framing — compute cost vs inference savings

## NLP Fundamentals (Applied)
- [ ] Tokenization — BPE, SentencePiece, tiktoken, why token counts matter for cost/context
- [ ] Embedding spaces — word2vec intuition, sentence embeddings
- [ ] Cross-encoder vs bi-encoder tradeoffs
- [ ] Transformer architecture — attention, positional encoding, KV cache, context windows
- [ ] Why long-context models behave differently
- [ ] Why retrieval beats context stuffing
- [ ] Lost-in-the-middle effect
- [ ] Text preprocessing at scale — NER, regex extraction, normalization, language detection
- [ ] Sequence labeling vs classification vs generation — which framing for which problem
