---
name: google-drive-cli
description: Use Google Drive through the authenticated Google Workspace CLI. Use for Drive file search, metadata inspection, downloads, uploads, exports, folder creation, permissions, Meet recording files, and source-of-truth Drive artifacts when a CLI path is preferable to the curated connector.
---

# Google Drive (CLI)

Use this plugin when the user wants Google Drive access through `gws`, especially when the curated Drive connector cannot download, upload, export, or update the exact artifact needed.

This is a product plugin backed by the installed `gws` CLI. Keep `google-drive@openai-curated` available for connector-native Docs, Sheets, Slides, comments, and visual workflows when that plugin is more ergonomic.

## Start

```bash
command -v gws
gws auth status
gws drive files list --params '{"pageSize":10,"fields":"files(id,name,mimeType,modifiedTime,webViewLink),nextPageToken"}'
```

## Search And Inspect

Search by name or folder:

```bash
gws drive files list --params '{"q":"name contains \"recording\" and trashed=false","pageSize":10,"fields":"files(id,name,mimeType,size,modifiedTime,webViewLink),nextPageToken"}'
gws drive files list --params '{"q":"\"FOLDER_ID\" in parents and trashed=false","pageSize":50,"fields":"files(id,name,mimeType,size,modifiedTime,webViewLink),nextPageToken"}'
```

Get metadata:

```bash
gws drive files get --params '{"fileId":"FILE_ID","fields":"id,name,mimeType,size,modifiedTime,parents,webViewLink,webContentLink"}'
```

Use `--page-all --page-limit N` for bounded broad reads.

## Download Files

Download normal binary files, including Meet recording MP4 files:

```bash
gws drive files get --params '{"fileId":"FILE_ID","alt":"media"}' --output ./recording.mp4
```

Verify downloaded artifacts before handing them to another tool:

```bash
ls -lh ./recording.mp4
file ./recording.mp4
```

`gws` validates `--output` paths against the current working directory. Use a relative path such as `./recording.mp4` or run from the directory where the artifact should land.

For Google Workspace files, export instead of `alt=media`:

```bash
gws drive files export --params '{"fileId":"DOC_OR_SHEET_OR_SLIDE_ID","mimeType":"application/pdf"}' --output ./export.pdf
gws drive files export --params '{"fileId":"DOC_ID","mimeType":"text/plain"}' --output ./document.txt
```

## Upload And Create

Upload a local file:

```bash
gws drive +upload ./report.pdf
gws drive +upload ./report.pdf --parent FOLDER_ID --name "Report.pdf"
```

Create a folder:

```bash
gws drive files create --json '{"name":"Folder name","mimeType":"application/vnd.google-apps.folder"}'
```

Create Google-native files through Drive metadata only when that is the right API surface; for rich Docs edits, use `gws docs ...`.

## Permissions

Ask before sharing, unsharing, publishing, or changing permissions. Always read current permissions first.

```bash
gws drive permissions list --params '{"fileId":"FILE_ID","fields":"permissions(id,type,role,emailAddress,domain,allowFileDiscovery)"}'
gws drive permissions create --params '{"fileId":"FILE_ID"}' --json '{"role":"reader","type":"user","emailAddress":"person@example.com"}' --dry-run
gws drive permissions delete --params '{"fileId":"FILE_ID","permissionId":"PERMISSION_ID"}' --dry-run
```

## Raw API Help

Use schema discovery before unfamiliar fields or methods:

```bash
gws schema drive.files.list --resolve-refs
gws schema drive.files.get --resolve-refs
gws schema drive.files.create --resolve-refs
gws schema drive.permissions.create --resolve-refs
```

## Rules

- Prefer Drive file IDs over names; names are not unique.
- Read metadata before downloading, exporting, moving, deleting, or sharing.
- Ask before deletes, permission changes, public sharing, moves, ownership transfers, or uploads into shared/customer folders unless the user already approved the exact action.
- Use `--output` for binary responses, keep the output path under the current directory, and verify the file exists afterward.
- Use `alt=media` for binary Drive files and `files export` for Google-native Docs, Sheets, and Slides.
- Keep the curated Google Drive plugin as a fallback for connector-native workflows; this plugin is the reliable CLI path.
