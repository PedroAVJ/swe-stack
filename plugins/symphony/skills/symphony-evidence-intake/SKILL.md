---
name: symphony-evidence-intake
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
2. Preserve the raw source or a stable reference in the repo/workspace when
   there is a clear canonical home.
3. If no transcript exists, transcribe the recording with the available
   transcription workflow.
   - Use Spanish (`--language es`) when the source is Spanish.
   - Enable diarization for calls or multi-speaker notes when speaker identity
     matters.
4. Store the canonical transcript and metadata in a predictable location.
5. Upload source media and transcript to Drive only when that is the intended
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
with `symphony-issue-intake` or `symphony-coverage-pass`.

## Preferred Output

Return a short evidence bundle:

```markdown
Evidence ready:
- Transcript: PATH_OR_LINK
- Recording/source media: PATH_OR_LINK
- Chat transcript: PATH_OR_LINK_OR_NOT_AVAILABLE
- Metadata: PATH_OR_LINK
```
