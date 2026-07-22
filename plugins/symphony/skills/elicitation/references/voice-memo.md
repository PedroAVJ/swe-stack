# Voice Memo / Local Media Acquisition

For dictated audio notes and any loose local audio/video evidence. Voice Memos
has its own on-disk store — read recordings from it directly; AirDrop-to-self
is a fallback, not the flow.

## Where Voice Memos live

```text
~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/
```

- Recordings are `.m4a` files named `YYYYMMDD HHMMSS-<HEX>.m4a` — the filename
  itself gives the recording timestamp. Ignore the `.waveform` sidecar files.
- User-assigned titles are not in the filename; they live in
  `CloudRecordings.db` (SQLite) in the same folder. Query it only when the
  timestamp is not enough to identify the right memo.

Find recent memos:

```bash
ls -t ~/Library/Group\ Containers/group.com.apple.VoiceMemos.shared/Recordings/*.m4a | head -5
```

## Other local media

- AirDropped or exported files land in `~/Downloads`; also check paths Pedro
  gives directly. Treat these the same once located.

## Handling

1. Copy the file out to the session scratchpad. Never modify or delete files
   inside the Voice Memos container.
2. Upload the copy to the private Drive evidence folder (shared pipeline step
   2), then transcribe with Scribe. Voice memos are usually single-speaker
   Spanish or English dictation — diarization only when the memo captured a
   live conversation.
3. Record the original store path (or the AirDrop/Downloads path) as the
   source pointer in metadata.

## Blockers

- If the Voice Memos store is unreadable (Full Disk Access not granted),
  report that exact blocker and ask Pedro to share the memo from the app
  instead. Do not silently fall back.
