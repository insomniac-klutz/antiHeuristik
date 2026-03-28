# whoDidThat

> multimodal snitch for meetings and security cams.

system that ingests video, samples frames, transcribes audio, fuses both modalities, and answers natural language questions about what happened. "summarize the key decisions" or "did anyone enter after 3pm?" — it saw everything.

## what you're building

- process video files (5-15 min clips to start)
- extract both visual and audio information
- fuse modalities — answers reference what was seen AND heard
- handle temporal queries ("what happened at the 5 minute mark?")
- processing can be offline, but query answering must be interactive

## what will break you

- **frame sampling**: every N frames? scene change detection? keyframes? wrong choice = missed events or blown context
- **multimodal fusion**: combining transcript + visual frames into one coherent representation
- **temporal reasoning**: mapping events to timestamps across modalities
- **context explosion**: a 15-min video generates a LOT of tokens
- **speaker diarization**: knowing who said what, not just what was said

## why this matters

most AI work is text-only. video forces you to think across modalities — vision, audio, time. the fusion problem alone teaches more about representation than any NLP-only project will.

## stretch

- real-time processing (live stream, not just recordings)
- emotion/sentiment from facial expressions + voice tone
- auto-generated highlight reel of most important moments
