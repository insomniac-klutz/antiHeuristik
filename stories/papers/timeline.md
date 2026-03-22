# The Timeline — From Word2Vec to DeepSeek V3

Not derivations. For each: what it changed, why it matters now, 2-min explanation.
Read in order — each paper is a response to what came before.

---

## Era 1: Learning to Represent Words (2013-2017)

- [ ] **Word2Vec** (Mikolov et al., 2013)
  - What: Learned dense vector representations of words from co-occurrence
  - Shift: Words became math. "king - man + woman = queen" showed embeddings capture meaning
  - Why it still matters: Embedding intuition. Every sentence-embedding and retrieval system descends from this idea
  - Limitation: One vector per word — "bank" (river) = "bank" (finance)

- [ ] **GloVe** (Pennington et al., 2014)
  - What: Global matrix factorization approach to word vectors
  - Shift: Combined global statistics with local context (bridged count-based and prediction-based)
  - Why it still matters: Still used as baseline. Understanding GloVe vs Word2Vec tradeoff helps explain embedding model selection
  - Limitation: Still static — same word, same vector regardless of context

## Era 2: Context Changes Everything (2017-2019)

- [ ] **Attention Is All You Need** (Vaswani et al., 2017)
  - What: Transformer architecture — self-attention replacing RNNs/LSTMs entirely
  - Shift: Parallelizable training, long-range dependencies without vanishing gradients
  - Why it still matters: Everything runs on this. Understanding attention, positional encoding, KV cache explains every model's behavior and limitation
  - Limitation: Quadratic attention cost with sequence length (the reason context windows are expensive)

- [ ] **ELMo** (Peters et al., 2018)
  - What: Contextualized word embeddings — same word, different vectors based on context
  - Shift: Killed static embeddings. "Bank" in "river bank" ≠ "bank" in "bank account"
  - Why it still matters: Bridge between Word2Vec thinking and BERT thinking. Explains why context matters for embeddings
  - Limitation: BiLSTM-based, not transformer. Slower, less scalable

- [ ] **BERT** (Devlin et al., 2018)
  - What: Bidirectional transformer encoder, pre-trained with masked language modeling
  - Shift: Pre-train once, fine-tune for anything. Transfer learning for NLP at scale
  - Why it still matters: Cross-encoders for reranking, sentence-BERT for embeddings, NER, classification. BERT descendants power most retrieval systems today
  - Limitation: Encoder-only — can't generate text. Not useful for chatbots or generation

- [ ] **GPT** (Radford et al., 2018)
  - What: Decoder-only transformer, autoregressive language model
  - Shift: Showed that unsupervised pre-training + supervised fine-tuning works. Language modeling as foundation
  - Why it still matters: The architecture that became ChatGPT. Autoregressive generation is how every LLM produces text
  - Limitation: Small (117M params). Needed scale to become useful

- [ ] **GPT-2** (Radford et al., 2019)
  - What: Scaled GPT to 1.5B params. "Too dangerous to release" (they released it)
  - Shift: Proved the scaling hypothesis — more data + more params = emergent abilities. Zero-shot task performance without fine-tuning
  - Why it still matters: First proof that scale is a strategy. The "just make it bigger" insight that led to GPT-3/4
  - Limitation: No instruction following. Generates fluent text but doesn't "listen"

## Era 3: Scale and Instruction (2020-2022)

- [ ] **GPT-3** (Brown et al., 2020)
  - What: 175B params. Few-shot learning via in-context examples
  - Shift: No fine-tuning needed for many tasks. Prompt engineering is born
  - Why it still matters: The paper that launched the current era. Few-shot prompting, in-context learning, prompt design all start here
  - Limitation: Expensive, hallucinates, doesn't follow instructions reliably

- [ ] **InstructGPT / RLHF** (Ouyang et al., 2022)
  - What: Fine-tuning GPT-3 with human feedback to follow instructions
  - Shift: Alignment. Models that do what you ask, not just what's statistically likely
  - Why it still matters: Every chat model uses RLHF or its descendants (DPO, RLAIF). Understanding this explains why ChatGPT feels different from base GPT-3
  - Limitation: Reward hacking, sycophancy, alignment tax on capabilities

- [ ] **Chain-of-Thought** (Wei et al., 2022)
  - What: "Let's think step by step" dramatically improves reasoning
  - Shift: Prompting technique that unlocks capabilities already in the model
  - Why it still matters: Foundation of all reasoning-heavy prompting. Every agent loop, every complex query uses CoT
  - Limitation: Longer outputs = more tokens = more cost. Sometimes the reasoning is wrong but convincing

## Era 4: Retrieval, Efficiency, and Agents (2020-2024)

- [ ] **ColBERT** (Khattab & Zaharia, 2020)
  - What: Late interaction — encode query and document separately, compare token-level
  - Shift: Best of both worlds — bi-encoder speed with cross-encoder quality
  - Why it still matters: Powers high-quality retrieval at scale. Key tradeoff to know for RAG system design
  - Limitation: Larger index size than single-vector approaches

- [ ] **RAG** (Lewis et al., 2020)
  - What: Retrieve relevant documents, condition generation on them
  - Shift: External knowledge without retraining. Grounded generation
  - Why it still matters: The dominant pattern for knowledge-grounded AI systems. You build this constantly
  - Limitation: Garbage in = garbage out. Retrieval quality caps generation quality

- [ ] **LoRA** (Hu et al., 2021)
  - What: Low-rank adaptation — fine-tune a tiny fraction of model weights
  - Shift: Fine-tuning goes from "needs a cluster" to "needs a single GPU"
  - Why it still matters: Makes fine-tuning accessible. The decision tree of "when to fine-tune" depends on LoRA making it cheap
  - Limitation: Less expressive than full fine-tuning. Not always sufficient for large distribution shifts

- [ ] **ReAct** (Yao et al., 2022)
  - What: Interleave reasoning traces with tool-use actions
  - Shift: LLMs can use tools, search the web, call APIs — not just generate text
  - Why it still matters: The architecture behind every agent system. Tool use, planning loops, all descend from ReAct
  - Limitation: Prone to loops, hallucinated tool calls, brittle error recovery

- [ ] **DPO** (Rafailov et al., 2023)
  - What: Direct preference optimization — skip the reward model, optimize preferences directly
  - Shift: Simpler alignment pipeline. No separate reward model training needed
  - Why it still matters: Increasingly preferred over RLHF. Understanding DPO vs RLHF tradeoff matters for fine-tuning decisions
  - Limitation: Needs high-quality preference pairs. Sensitive to data distribution

- [ ] **Constitutional AI** (Bai et al., 2022)
  - What: Self-critique and revision guided by principles, not human labels
  - Shift: Scalable safety without massive human annotation
  - Why it still matters: The pattern behind self-correction, safety layers, and output filtering in production systems
  - Limitation: Model can learn to game its own constitution. Principles need careful design

## Era 5: Frontier and Open-Source (2023-2026)

- [ ] **Lost in the Middle** (Liu et al., 2023)
  - What: LLMs perform worst on information placed in the middle of long contexts
  - Shift: Context position matters. Not all tokens are equal
  - Why it still matters: Directly affects RAG design — where you place retrieved chunks changes answer quality. Explains why retrieval beats stuffing
  - Limitation: Varies by model and fine-tuning. Some newer models mitigate it

- [ ] **RAFT** (Zhang et al., 2024)
  - What: Retrieval-aware fine-tuning — train the model to reason over retrieved (and distractor) documents
  - Shift: RAG + fine-tuning > either alone. The model learns to ignore bad retrievals
  - Why it still matters: The next step after basic RAG. When RAG quality plateaus, RAFT is the upgrade path
  - Limitation: Requires domain-specific training data paired with retrievals

- [ ] **Mixture of Experts / DeepSeek V3** (DeepSeek, 2024-2025)
  - What: 671B total params, 37B active per token via mixture-of-experts routing
  - Shift: MoE makes massive models economically viable — you don't activate every parameter for every token
  - Why it still matters: Economics of inference. Understanding MoE explains why some models are cheap despite being "huge." Cost modeling requires knowing this architecture
  - Limitation: Routing instability, expert collapse, harder to fine-tune (LoRA on which experts?)
  - Also know: Multi-head latent attention (MLA) for KV cache compression, FP8 mixed-precision training

---

## How to Use This Timeline

1. Read in order — each paper makes more sense after the one before it
2. For each, practice the 2-minute version: "what it is, what it changed, why I care in production"
3. Mark `[x]` when you can explain it cold without looking at notes
4. The connections matter more than the individual papers — trace the lineage:
   - Word2Vec → GloVe → ELMo → BERT → Sentence-BERT → bi-encoder retrieval
   - Attention → GPT → GPT-2 → GPT-3 → InstructGPT → ChatGPT
   - RAG → RAFT → ColBERT → hybrid retrieval
   - RLHF → DPO → Constitutional AI
   - Scale hypothesis → MoE → DeepSeek V3
