---
name: implementation-dispatch
description: "Use when Pedro has approved a Linear work packet and wants Symphony to create a fresh Codex thread/agent to implement it. This skill takes the approved Linear issue plus source pointers, creates a separate implementation thread, sends a bounded prompt, and reports the new thread back without implementing in the current thread."
---

# Symphony Implementation Dispatch

Use this as Symphony's second lane: approved Linear work packet in, fresh
implementation thread out.

## Contract

- Dispatch only after the requirement is approved and represented in Linear, or
  Pedro explicitly asks to create the issue and dispatch in the same step.
- Do not implement product code in the current thread.
- Create a new Codex thread so the implementation agent has fresh context and
  Pedro can follow up there.
- The Linear issue is the implementation source of truth; source messages and
  docs are pointers the implementation agent must reread.

## Preconditions

Before dispatching:

1. Verify the Linear issue title, state, URL/ID, and scope.
2. Verify the target repo/worktree path and branch expectations when available.
3. Check whether an active worker, branch, PR, or thread already exists for that
   issue. If one exists, report it instead of starting a duplicate unless Pedro
   asks for a restart.
4. If the issue was materially rewritten after work started, make the restart
   boundary explicit.

## Thread Tools

When running inside Codex, search for the thread-management tool before
dispatching:

- `create_thread`
- `send_message_to_thread`
- `set_thread_title`
- `read_thread` or `list_threads` when checking for existing work

Use the available thread tool schema. Do not invent raw thread directives. If
thread tools are unavailable, produce the exact handoff prompt and say dispatch
could not be completed from this environment.

## Implementation Prompt Shape

Send the new thread a concise prompt with:

- plain-English issue name first, Linear ID secondary;
- Linear URL/ID and current state;
- repo path and branch expectations;
- source pointers the agent must reread;
- scope and out-of-scope;
- verification expectations and expensive-check boundaries;
- instruction to follow the repo's `AGENTS.md`/`CLAUDE.md`;
- instruction to work end-to-end in that thread and report back there.

Template:

```markdown
Implement ISSUE_TITLE (ISSUE_ID).

Linear: ISSUE_URL
Repo: ABSOLUTE_REPO_PATH

Source pointers to reread:
- SOURCE_POINTERS

Scope:
- APPROVED_SCOPE

Out of scope:
- EXPLICIT_NON_GOALS

Verification:
- EXPECTED_TESTS_OR_CHECKS
- EXPENSIVE_CHECK_BOUNDARIES

Follow the repo instructions, keep the change narrowly scoped, and report the
result in this thread.
```

## Reporting Back

Return to Pedro with:

- new thread title/link or identifier;
- Linear issue name and ID;
- whether a duplicate worker/PR/thread was found;
- any dispatch caveats.

Do not claim the implementation is done. The new thread owns implementation and
verification.
