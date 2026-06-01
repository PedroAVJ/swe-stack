---
name: google-tasks
description: Manage Google Tasks through the authenticated Google Workspace CLI. Use for task list discovery, task reads, task creation, updates, completion, reopening, deletion, movement, and Google Tasks API limitation questions.
---

# Google Tasks (CLI)

Use this plugin when the user wants to inspect or manage Google Tasks.

Use the installed `gws` CLI for Google Tasks operations. This plugin is the product shell and operating manual around `gws tasks ...`; keep the curated Google plugins available as fallbacks when their connector-shaped views are more useful.

## Start

```bash
command -v gws
gws auth status
gws tasks tasklists list
```

Resolve the target task list before mutating anything:

```bash
gws tasks tasklists list --params '{"maxResults":100}'
gws tasks tasks list --params '{"tasklist":"@default","maxResults":50}'
```

## Safe Reads

```bash
gws tasks tasks list --params '{"tasklist":"@default","maxResults":50}'
gws tasks tasks list --params '{"tasklist":"@default","showCompleted":true,"showHidden":true,"maxResults":100}'
gws tasks tasks get --params '{"tasklist":"@default","task":"TASK_ID"}'
```

Use `--page-all --page-limit N` when a bounded multi-page read is needed.

## Writes

Prefer `--dry-run` before writes when the user has not given exact task IDs or exact text. Ask before creating, deleting, completing, reopening, moving, or materially editing tasks unless the user already made that action explicit.

```bash
gws tasks tasks insert --params '{"tasklist":"@default"}' --json '{"title":"Call accountant","notes":"Ask about ISR and IVA filing"}' --dry-run
gws tasks tasks patch --params '{"tasklist":"@default","task":"TASK_ID"}' --json '{"status":"completed"}' --dry-run
gws tasks tasks patch --params '{"tasklist":"@default","task":"TASK_ID"}' --json '{"title":"New title"}' --dry-run
gws tasks tasks move --params '{"tasklist":"@default","task":"TASK_ID","previous":"PREVIOUS_TASK_ID"}' --dry-run
```

After an approved mutation, read the task or list again and report the confirmed state.

## Raw API Help

Use schema discovery before unfamiliar fields or methods:

```bash
gws schema tasks.tasklists.list --resolve-refs
gws schema tasks.tasks.insert --resolve-refs
gws schema tasks.tasks.patch --resolve-refs
```

## Rules

- Prefer task IDs for mutations; task titles are not unique.
- Run `tasks get` before update, move, complete, reopen, or delete when the ID came from stale context.
- Keep due dates date-level unless the user specifically asks about due-time workarounds.
- Treat recurring-task editing, reminders, Docs assigned tasks, and Chat assigned tasks as Google Tasks API limitation zones.
- Read `references/limitations.md` when recurring tasks, reminders, due times, Docs or Chat assigned tasks, or sync design matter.
