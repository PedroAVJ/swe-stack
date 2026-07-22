# Google Meet Acquisition

For sessions held on Google Meet with recording enabled. Everything is already
durable in Google Workspace; this flow locates the artifacts and points at
them — do not re-upload to Drive.

## Source order

1. User-provided recording link, transcript link, or Drive folder.
2. Gmail "recording is ready" / "transcript is ready" notification from Google
   Meet (search Gmail for recent Meet notifications naming the meeting).
3. The Drive "Meet Recordings" folder, or the calendar event's attached
   artifacts.

## Artifacts to collect

- Recording video (Drive file).
- Transcript Google Doc, when Meet generated one. Export/read its text; this
  usually removes the need for Scribe transcription.
- Chat transcript file, when present alongside the recording.
- Meeting date, title, and attendee list from the calendar event or the Gmail
  notification.

## Notes

- Use the Drive/Gmail connectors first; fall back to the `gws drive` CLI for
  downloads or metadata the curated connector cannot reach.
- If Meet produced no transcript, download the recording audio and run the
  shared pipeline's Scribe transcription with diarization.
- Meet transcripts attribute speakers by account, but a shared physical
  microphone collapses everyone in the room into one speaker. Record that
  provenance limit in metadata when it applies.
