# SWE Stack ElevenLabs Plugin

Use ElevenLabs audio and speech tooling from Codex or Claude Code.

The current bundled workflow focuses on ElevenLabs Scribe transcription with language hints, diarization, speaker-count hints, keyterms, and multiple output formats.

This project is unofficial and is not affiliated with ElevenLabs.

## Requirements

- Python 3
- `requests`
- `ELEVENLABS_API_KEY` set in the shell environment for live API calls

## Start

```bash
python3 scripts/transcribe_elevenlabs.py meeting.mp4 --language es --diarize --num-speakers 2 --response-format diarized_text --out transcript.txt
```

Use the `elevenlabs` skill for the documented Scribe options and safety rules.
