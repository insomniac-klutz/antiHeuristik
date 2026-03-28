# loudMouth

> speak. think. answer. under 2 seconds.

voice-first agent: user speaks, system understands, takes action, speaks back. real-time, conversational, low-latency. three models in series and the clock is ticking.

## what you're building

- speech-to-text → LLM reasoning → text-to-speech pipeline
- end-to-end latency target: <2s
- handle interruptions (user speaks while agent is talking)
- handle unclear speech, background noise, accents
- integrate with at least one tool (lookup, booking, etc.)

## what will break you

- **latency stacking**: three models in series — each adds 200-600ms and it compounds
- **streaming**: you can't wait for full transcription before reasoning starts
- **turn-taking**: interruption handling is an unsolved UX problem
- **VAD**: voice activity detection — knowing when the user stopped talking
- **audio preprocessing**: garbage in, garbage out applies to audio too

## why this matters

real-time multi-model pipelines force you to think about latency, streaming, and failure differently than any text-only system. the constraints are physical — speed of sound, human patience — and they don't negotiate.

## stretch

- emotion detection (frustrated caller → escalate)
- multi-language with auto language detection
- conversation analytics (topic extraction, sentiment over time)
