---
name: evidence-intake
description: Preserve meeting, call, audio-note, transcript, Drive, Gmail, or local media evidence before Symphony issue intake, coverage passes, review artifacts, or Linear extraction. Do not create Linear issues by default.
---

# Symphony Evidence Intake

Use this skill when raw evidence needs to become stable before Symphony turns it
into issues, coverage notes, review artifacts, replies, or implementation
briefs.

This skill combines the prior meeting and audio-note intake lanes:

- Google Meet recordings, transcripts, chat transcripts, Gmail recording
  notifications, Drive artifacts, and local meeting media.
- Local call recordings, voice memos, audio notes, or short audio/video
  artifacts.

## Contract

Produce durable pointers to the source evidence:

- transcript
- recording or source media, when available
- chat transcript, when available
- Drive links, when uploaded or already canonical
- repo/workspace transcript and metadata paths when a repo is the right home
- metadata that identifies the original source artifact

This skill prepares evidence only. It does not create Linear issues unless Pedro
explicitly asks for Linear capture in the same turn.

## Tool Routing

- For local recording, voice memo, AirDrop, Downloads, or other raw audio/video
  evidence, use Google Drive as the durable source-media home. Upload the
  original media to a private Drive folder first when the source is not already
  in Drive, then store repo/workspace metadata that points to the Drive files.
- For Drive uploads, folder creation, metadata reads, or raw media files that
  the curated Drive connector cannot upload directly, use the authenticated
  Google Drive CLI workflow (`gws drive ...`) from the Google Drive CLI plugin.
- For audio/video transcription, prefer ElevenLabs Scribe when the ElevenLabs
  plugin is available and `ELEVENLABS_API_KEY` is set. Use Spanish
  (`--language es`) when the source is Spanish, diarization for multi-speaker
  conversations, and `--response-format diarized_text` for readable evidence.
- If ElevenLabs is unavailable or lacks credentials, say that explicitly before
  choosing a fallback transcription path. Do not silently pivot to a generic
  local or OpenAI transcription workflow.

## Source Order

1. User-provided recording, transcript, local path, or Drive link.
2. Gmail recording notification from Google Meet.
3. Google Drive meeting folder, Meet Recordings folder, or relevant evidence
   folder.
4. Local audio/video files from Documents, Downloads, Voice Memos exports, or a
   repo/workspace evidence folder.

If no source artifact can be found, stop and say the evidence is not grounded.

## Workflow

1. Find the source artifacts:
   - recording or source media
   - transcript or Google Doc transcript
   - chat transcript
   - Drive/Gmail/local metadata
2. For local audio/video evidence, create or find the intended private Drive
   evidence folder and upload the original source media before transcription.
   For non-media or already-canonical evidence, preserve the raw source or a
   stable reference in the repo/workspace when there is a clear canonical home.
3. If no transcript exists, transcribe the recording with ElevenLabs Scribe
   when available.
   - Use Spanish (`--language es`) when the source is Spanish.
   - Enable diarization for calls or multi-speaker notes when speaker identity
     matters.
   - If ElevenLabs cannot run, report the exact blocker before using another
     transcription workflow.
4. Store the canonical transcript and metadata in a predictable location.
5. Upload transcripts to the same Drive evidence folder when Drive is the
   durable evidence home, and do not change sharing/permissions without explicit
   approval.
6. Verify the bundle:
   - read first and last transcript lines
   - check recording metadata or file presence
   - check uploaded Drive metadata or folder listing when Drive was used
   - check repo diff/status when repo files were added
7. Return exact artifact pointers.

## Preferred Repo Shape

Use a dated slug under the relevant repo when there is a clear source repo:

```text
docs/meetings/YYYY-MM-DD-short-topic/
  metadata.md
  transcript.es.txt
```

For audio that is not a meeting but still evidence, use the same shape unless
the repo already has a better evidence folder convention.

## Preferred Metadata Shape

```markdown
# SHORT_TITLE

Date: YYYY-MM-DD

Topic: SHORT_TOPIC

Transcript:
`RELATIVE/PATH/transcript.es.txt`

Recording:
DRIVE_OR_LOCAL_AUDIO_POINTER

Drive folder:
DRIVE_FOLDER_LINK_OR_NOT_USED

Source:
SOURCE_POINTER

Notes:
- Transcribed from SOURCE with TOOL.
```

## Boundaries

Do not:

- create Linear issues unless Pedro explicitly asks
- invent action items or specifications from the transcript
- treat transcript snippets as a replacement for the recording when the audio
  is available
- change Drive permissions or public sharing without explicit approval
- delete source files

If Pedro asks for Linear follow-up after this intake, use the evidence pointers
with `issue-intake` or `coverage-pass`.

## Preferred Output

Return a short evidence bundle:

```markdown
Evidence ready:
- Transcript: PATH_OR_LINK
- Recording/source media: PATH_OR_LINK
- Chat transcript: PATH_OR_LINK_OR_NOT_AVAILABLE
- Metadata: PATH_OR_LINK
```
