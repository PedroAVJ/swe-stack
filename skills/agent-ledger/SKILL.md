---
name: agent-ledger
description: Manage agent-owned operational state in a local SQLite ledger through the installed `agent-ledger` CLI. Use when an agent needs to remember, inspect, update, settle, or close mutable agent-side facts such as IOUs, obligations, follow-up state, personal coordination notes, agent todos, or reminders that are for the agent to consult rather than for Pedro to see in Google Tasks, Apple Reminders, Calendar, Linear, or a repo.
---

# Agent Ledger

Use `agent-ledger` for mutable operational context that belongs to the agent. This is not Pedro's task system and not repo canon. It is a small local SQLite database for facts the agent should consult and update later.

## Start

Verify the command and database first:

```bash
command -v agent-ledger
agent-ledger --json doctor
```

The database lives at:

```bash
~/.local/share/codex-agent-ledger/ledger.sqlite3
```

No auth or network is required.

## Decide Whether To Use It

Use the ledger when the information is:

- Agent-owned: future agents should remember or act on it.
- Mutable: status can become `settled`, `waived`, `stale`, or `closed`.
- Operational: useful for coordination, not a polished human-facing note.
- Personal/private enough that it should stay local unless Pedro asks otherwise.

Do not use the ledger when Pedro asks for a consumer-facing reminder, notification, calendar event, Google Task, Apple Reminder, Linear issue, repo doc, or finance-registry update. Use the actual requested surface for those.

## Read Existing State

List open items:

```bash
agent-ledger list
```

Filter by kind or person:

```bash
agent-ledger list --kind obligation
agent-ledger list --person Diana
```

Inspect one item with events:

```bash
agent-ledger --json show obligation_diana_amazon_book_20260518
```

## Add Items

Preview first when the wording, amount, person, or source is uncertain:

```bash
agent-ledger --json add \
  --kind obligation \
  --title "Diana owes $279 MXN for Amazon book" \
  --person "Sam / Roommate" \
  --amount 279 \
  --currency MXN \
  --source "whatsapp+amazon" \
  --source-ref "WhatsApp message id or other compact source pointer" \
  --body "Short factual summary." \
  --dry-run
```

Create once grounded:

```bash
agent-ledger --json add \
  --kind obligation \
  --title "Diana owes $279 MXN for Amazon book" \
  --person "Sam / Roommate" \
  --amount 279 \
  --currency MXN \
  --source "whatsapp+amazon" \
  --source-ref "WhatsApp request and confirmation message ids" \
  --body "Diana asked Pedro to order the physical paperback and said she would deposit it."
```

Use `kind=obligation` for IOUs and money owed, `note` for durable facts, `todo` for agent-owned follow-up work, `reminder` for agent-side future checks, and `state` for small current-state records.

## Update Status

Preview status changes first unless Pedro has explicitly confirmed the exact change:

```bash
agent-ledger --json status obligation_diana_amazon_book_20260518 settled \
  --note "Diana paid" \
  --dry-run
```

Apply the change:

```bash
agent-ledger --json status obligation_diana_amazon_book_20260518 settled \
  --note "Diana paid"
```

Status values are `open`, `settled`, `waived`, `stale`, and `closed`.

## Safety

- Ground money, WhatsApp, email, purchase, and payment facts in their source before adding or settling ledger items.
- Keep `source_ref` compact but useful: message id, chat label, order id, receipt pointer, or local artifact path.
- Do not store secrets, card numbers, full addresses, tokens, or unnecessary raw message bodies.
- Do not treat an open ledger item as proof that money is still owed after Pedro says it was paid; verify if cheap, then settle or mark stale.
- Do not create a duplicate if an open item for the same person/reason already exists. Search first.
