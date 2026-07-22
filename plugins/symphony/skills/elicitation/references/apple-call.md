# Apple Call Recording Acquisition

For phone/FaceTime calls recorded with Apple's built-in call recording. macOS
surfaces these in the Notes app, but the audio lives on disk in the Notes group
container — read it from the filesystem; do not drive the Notes UI.

## Where the audio lives

```text
~/Library/Group Containers/group.com.apple.notes/Accounts/<ACCOUNT_UUID>/Media/<MEDIA_UUID>/1_<UUID>/Call with <Contact>.m4a
```

Find recent recordings by name and modification time:

```bash
find ~/Library/Group\ Containers/group.com.apple.notes/Accounts \
  -iname 'call with*.m4a' -newermt '-14 days' 2>/dev/null
```

- The filename carries the contact name; file modification time approximates
  the call date. `NoteStore.sqlite` in the container root has richer metadata
  but is rarely needed.
- The same call can appear under several `Media/` UUID folders (sync copies);
  pick the newest and note the duplication only if sizes differ.

## Handling

1. Copy the `.m4a` out to the session scratchpad before doing anything with
   it. Never modify or delete files inside the Notes container.
2. Upload the copy to the private Drive evidence folder (shared pipeline step
   2), then transcribe with Scribe using diarization — calls are two-speaker
   by nature and Apple's own transcript, when one exists in the note, is not
   exported here.
3. Record the original container path as the source pointer in metadata.

## Blockers

- If the container is unreadable (Full Disk Access not granted to the
  terminal), report that exact blocker and ask Pedro to share the recording
  from Notes (share sheet → save audio) instead. Do not silently fall back.
