---
name: elevenlabs
description: Use ElevenLabs audio and speech tooling. Documented use cases include Scribe transcription, diarization, language hints, and keyterm biasing.
---

# ElevenLabs

Use this plugin when the user explicitly asks for ElevenLabs or when audio/speech quality matters enough to choose ElevenLabs.

Do not title the workflow as generic transcription. The product surface is ElevenLabs; transcription is one documented use case through Scribe.

## Scribe Use Case

Use the bundled CLI:

```bash
python3 scripts/transcribe_elevenlabs.py \
  meeting.mp4 \
  --language es \
  --diarize \
  --num-speakers 2 \
  --response-format diarized_text \
  --out output/elevenlabs/meeting/transcript.txt
```

Resolve `scripts/transcribe_elevenlabs.py` relative to the ElevenLabs plugin root. If you are reading this skill from a plugin cache path, the helper is two directories above this skill file at `../../scripts/transcribe_elevenlabs.py`.

## Decision Rules

- Default to `scribe_v2` for Scribe.
- For meetings, prefer `--diarize --num-speakers 2` when the user knows it is a two-speaker conversation.
- Use `--response-format diarized_text` when the goal is a readable speaker transcript.
- Use `--response-format json` when raw API evidence matters.
- Add `--language es` when the recording is known to be Spanish.
- Add `--keyterm` for domain jargon the model is likely to miss.
- Leave verbatim mode on unless the user wants filler words and false starts removed.

## Environment

- `ELEVENLABS_API_KEY` must be set for live API calls.
- Never ask the user to paste the full key in chat.

## Reference Map

- `references/api.md`: Scribe request knobs, limits, and diarization tradeoffs.
