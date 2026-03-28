# antiHeuristik

***pathei mathos ara prōtai archai*** — learn through suffering, then find first principles

`cargo cult engineering  ×  return to monke`

theory, minus the parts that exist to justify someone's thesis -- learn what to do with it. then ask why and how. that's antiHeuristik.

**[skip the vibes, read the book →](meta/anti-bk.pdf)**

12 applied AI builds. each one compresses months of on-the-job learning into days. no toy demos. no tutorial hell. you build the thing, hit the wall, learn only what unblocks you, and build again.

## the builds

| # | codename | what it actually is | the wall you'll hit |
|---|----------|--------------------|--------------------|
| 01 | [**needleStack**](builds/01-patent-search/) | RAG prior-art search over 10K patents | chunking strategy will make or break recall |
| 02 | [**noLeaks**](builds/02-multitenant-bot/) | multi-tenant support agent with strict isolation | one prompt injection away from a data breach |
| 03 | [**sqlMePlz**](builds/03-nl2sql-dashboard/) | beg the database in english, get SQL back | ambiguous questions expose every shortcut you took |
| 04 | [**paperShredder**](builds/04-doc-ai-pipeline/) | doc AI pipeline for PDFs, scans, and chaos | 5% of your docs will fail and you'll learn why that matters |
| 05 | [**diffWhisperer**](builds/05-code-review-agent/) | code review agent that reads diffs, not vibes | false positives get you muted faster than missed bugs |
| 06 | [**loudMouth**](builds/06-voice-agent/) | voice-first agent — speak, think, answer, under 2s | latency compounds across three models in series |
| 07 | [**cageMatch**](builds/07-framework-shootout/) | same agent, three frameworks, one winner | the framework you love will lose on something |
| 08 | [**elephantBrain**](builds/08-long-conversation-agent/) | long-conversation agent — coherent at turn 80+ | lost-in-the-middle will personally betray you |
| 09 | [**overHyped**](builds/09-llm-vs-classical-bakeoff/) | LLM vs XGBoost on tabular data, place your bets | spoiler: the LLM loses and costs 1000x more |
| 10 | [**whoDidThat**](builds/10-video-incident-analyzer/) | multimodal snitch for meetings and security cams | fusing audio + vision without drowning in context |
| 11 | [**routeOrDie**](builds/11-ai-gateway-compliance/) | classify, route, redact, log — or explain to legal | compliance is the feature, not the afterthought |
| 12 | [**scopeCreep**](builds/12-greenfield-scoping-sim/) | 5 companies want AI — maybe 2 should get it | saying "don't use AI" is the hardest rec to make |

## how it works

each build follows the same loop:

```
brief → whiteboard → prototype → hit wall → learn what unblocked you → repeat
```

then four layers deep:

1. **EVAL** — measure your baseline. no vibes-based "it works"
2. **COST-KILLER** — cut cost 70%, hold quality. the real engineering starts here
3. **FEEDBACK** — make it learn. human-in-the-loop, online eval, active learning
4. **CATASTROPHE** — break it. debug it. harden it. sleep well at night

## pick order

don't go 01 → 02 → 03. pick the build where you have the biggest gap between "I've read about this" and "I've built this."

## when you're done

you can draw the architecture from memory in 5 minutes. you can explain every decision and its tradeoff. you can name 5 things that would break it and how you'd fix each one. that's the bar.

## repo structure

```
builds/
  NN-slug/
    brief.md        # the assignment
    musings.md       # append-only decision log
    prototype/       # your code
    layers/          # L1-L4 progression
    theory/          # concepts learned during the build
clients/             # shared reusable clients
```
