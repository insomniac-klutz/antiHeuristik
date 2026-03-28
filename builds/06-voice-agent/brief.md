# Build 07: Voice-First Support Agent

## The Ask
Build a voice agent: user speaks, system understands, takes action, speaks back. Real-time, conversational, low-latency.

## Constraints
- Speech-to-text → LLM reasoning → text-to-speech pipeline
- Latency target: <2s end-to-end response time
- Must handle interruptions (user speaks while agent is talking)
- Must handle: unclear speech, background noise, accented speech
- Must integrate with at least one tool (lookup, booking, etc.)

## What This Forces You to Learn
- Whisper / speech-to-text models and tradeoffs
- TTS models and streaming synthesis
- Real-time streaming architecture (WebSockets, chunked responses)
- Latency optimization across a multi-model pipeline
- Turn-taking and interruption handling
- Audio preprocessing and VAD (voice activity detection)
- End-to-end latency profiling

## The Real Lesson
Real-time multi-model pipelines force you to think about latency, streaming, and failure in ways text-only systems never will. The constraints are physical — speed of sound, human patience — and they teach you system design under pressure.

## Stretch
- Add emotion detection (frustrated caller → escalate)
- Multi-language support with language detection
- Add conversation analytics (topic extraction, sentiment over time)
