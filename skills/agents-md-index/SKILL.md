---
name: agents-md-index
description: AGENTS.md is an index, not a manual. At small scales it can hold everything; at scale it must be paragraph + index of things and labels — nothing else. Instructions, commands, rules, and context belong in docs, skills, lint rules, or colocated about.md files. This skill teaches the index pattern and walks through migrating an AGENTS.md that has grown into a garbage dump back to its proper shape. Use when AGENTS.md has bloated past pure index, when READMEs are sprawling without clear ownership, when the user references OpenAI's harness engineering pattern, or when adding new content to AGENTS.md and questioning whether it belongs there.
---

# AGENTS.md is an index

Like a book.

At small scales, a book is a single page — the whole story fits there. A repo with one app and three rules can have an AGENTS.md that contains everything: intent, commands, rules, naming context. That's fine while it stays readable.

At scale, a book has a paragraph (condensed info about the whole thing) and a big-ass index (things and labels pointing at where the actual content lives). Not chapters glued onto the front. Not a wall of rules. Just paragraph + index.

The OpenAI harness engineering post (Feb 2026) names the failure mode of mixing: *"context is a scarce resource — a giant instruction file crowds out the task. When everything is important, nothing is. It rots instantly."*

Once an AGENTS.md grows past pure index, it stays bloated unless someone migrates it back. This skill is for that migration, and for maintaining the shape afterward.

# What goes in AGENTS.md vs elsewhere

**In AGENTS.md (at scale):**

- One paragraph: what the project is, who steers, what's the system of record. Three to six sentences.
- The map: a tree of top-level units (apps, packages, hardware) and cross-cutting docs/ subdirectories. Each entry gets a one-line label.

**Not in AGENTS.md:**

- Commands → `docs/workflows/development.md` or wherever workflow docs live.
- Lint / code style rules → ideally promoted into Biome / lint custom rules (the harness post: *"when documentation falls short, promote into code"*). What can't be promoted goes to `docs/code-style.md`.
- Architecture / how features fit together → `docs/architecture/`.
- Tech stack listing → `docs/tech-stack.md`.
- Per-unit setup, commands, constraints → that unit's colocated `about.md`.
- Naming context, glossary → `docs/strategy/` or `docs/glossary.md`.
- Ritual workflows ("when user says X, do Y") → a skill, not prose in AGENTS.md.

**The check:** if you're adding a sentence to AGENTS.md that tells the agent to *do* something, you're adding the wrong thing. The index points at where instructions live; it doesn't contain them.

# Hybrid colocation

Two doc locations, one rule each:

- **Unit-specific docs** colocated with the unit, as `<unit>/about.md`. When working on `apps/mobile/`, you see `about.md` in the tree. Delete the app, the docs go with it.
- **Cross-cutting docs** in `docs/`. Architecture, workflows, code style, strategy, research — anything that spans units or doesn't belong to one.

The `about.md` filename is intentional. README is for humans; about is for "what this is and how it works."

# No nested AGENTS.md

Both Codex and Claude Code walk *up* from the working directory looking for AGENTS.md, never down. If the user always invokes from the repo root, a nested `apps/web/AGENTS.md` is dead weight — the agent never sees it unless something explicitly tells it to read the file. Use `about.md` instead.

The exception: if the user actually runs agents from inside a subtree (e.g. `cd apps/web && claude`). Confirm before keeping nested AGENTS.md. Default: no.

# No README files

In an agent-first repo, README is an anachronism. Humans aren't the audience. The two places README matters (GitHub repo home page, npm package page) are edge cases — if they matter, accept the cost. Otherwise, delete or rename to `about.md`.

# CLAUDE.md → AGENTS.md as a symlink

If the user uses both Claude Code and Codex, symlink `CLAUDE.md → AGENTS.md`. One source of truth, both tools find it. Not a duplicate file (which guarantees drift).

# Migration procedure (when AGENTS.md is already bloated)

## 1. Audit

Read the existing AGENTS.md cover to cover. Then find every README and AGENTS.md in the repo:

```bash
find . -maxdepth 5 -type f \( -name "README.md" -o -name "AGENTS.md" \) -not -path "*/node_modules/*" -not -path "*/.git/*"
```

Read all of them. Don't summarize — read. The whole point is that lazy reading is the failure this skill fixes; don't replicate the failure.

For each file, decide its category:

- **Index** — pure list of "what's here." Becomes redundant once AGENTS.md has the map. Tag for deletion.
- **Real content** — framing, conclusions, rules with reasoning, operational steps. Keep. Migrate.
- **Mixed** — index plus some real content. Most "README" files are this. Extract the real content.
- **Stale or wrong** — files referencing apps that no longer exist, commands that don't run. (Don't fix content during this skill — that's a separate pass.)

For the existing AGENTS.md, categorize section by section against the "what goes where" list above.

## 2. Confirm scope with the user

Before moving files:

- Structural migration only? **Default: yes.** Content rewriting is a separate pass — mixing the two risks losing content while reorganizing it.
- Cross-cutting docs go under `docs/`? Yes. Unit-specific stays colocated as `about.md`.
- Keep or delete root `README.md`? Usually delete or migrate to `docs/<product>-product.md`. (GitHub falls back to AGENTS.md as the rendered landing page.)

Show the user a draft AGENTS.md and target tree *before* executing. Don't migrate first and ask after.

## 3. Migrate (use git mv)

Always use `git mv` so history is preserved. Order matters:

1. Create the new structure: `mkdir -p docs/architecture docs/workflows`.
2. Move whole trees: `git mv strategy docs/strategy`, `git mv research docs/research`.
3. Inside moved trees, rename meaningful README files (e.g. `docs/strategy/focus/README.md` → `docs/strategy/focus/superseded-framing.md` if it has real content beyond an index).
4. Rename per-unit READMEs to `about.md`: `git mv apps/mobile/README.md apps/mobile/about.md`.
5. Consolidate where multiple files merge into one (folder with both `README.md` and nested `AGENTS.md` → write the merged `about.md`, then `git rm` the originals).
6. Migrate root `README.md` to `docs/<product>-product.md`, then `git rm README.md`.
7. Extract sections from the old AGENTS.md into target docs.
8. Write the new AGENTS.md (paragraph + map).

## 4. Recover from over-deletion

A real failure mode: marking a README "pure index" and deleting it, but it actually had a framing paragraph or a conclusions section. After deleting, scan what was lost:

```bash
git show HEAD:<old-path> > /tmp/recovered.md
```

If the recovered content has anything beyond the index, write it as `<dir>/about.md`.

Better: don't delete on first pass. Rename to `about.md` instead, then trim later if it really was just an index.

## 5. Fix path references

Moves break path references. After all moves:

```bash
grep -rn "old-path/" --include="*.md" --include="*.ts" --include="*.tsx" --include="*.json" --include="*.yaml" -- . 2>/dev/null | grep -v node_modules | grep -v ".git"
```

Common refs to fix:

- "Canonical path" lines inside migrated files (point at their old location).
- Migration manifests (e.g. `notion-migration.md` table).
- Cross-references between docs (relative refs survive whole-tree moves; absolute refs always break).
- Skill files referencing repo paths.

Use `sed -i ''` for bulk replacement on macOS, `sed -i` on Linux.

## 6. Verify

- `git status --short` shows the full set of moves and renames.
- `find . -name "README.md" ...` returns zero results (or only explicitly kept exceptions).
- `find . -name "AGENTS.md" ...` returns one result (the root).
- `wc -l AGENTS.md` is small. ~40 lines for a multi-app monorepo. 60 is high. 100 is bloat.
- No stale path references remain.

## 7. Hand off

Show the user the final AGENTS.md, the docs/ tree, the staged file list. Don't commit unless asked. Let them skim and react before the change hits main.

# Failure modes

## Smuggling complexity past the index principle

When you can't fit a rule cleanly elsewhere, the temptation is to keep it inline in AGENTS.md as a "small exception." Don't. The harness post: *"if everything is important, nothing is."* The cost of one inline rule is small. The cost of normalizing inline rules is that AGENTS.md slowly grows back to what it was. Promote rules into code (lint, hook, test) when possible, into docs when not.

## Calling something a bug without checking the filesystem

If `CLAUDE.md` and `AGENTS.md` have identical content, check `ls -la` before claiming duplication. They might already be a symlink. Same applies to anything that "looks wrong" — verify before declaring.

## Creating a `docs/README.md`

The "no READMEs" rule applies to `docs/` too. AGENTS.md is the docs index. A `docs/README.md` recreates the indexing layer the AGENTS.md map already provides; the two will drift.

## Per-app `AGENTS.md` files

Tempting because vLLM does it. But vLLM's per-package AGENTS.md files are in *hotspot directories where agents run from*. If the user always runs from the repo root, those nested files never load. Use `about.md` instead.

## Lazy auditing

Reading three READMEs and projecting the rest is the exact failure pattern this skill fixes. Read all of them. Use parallel tool calls to make it cheap. The visible cost is a few extra reads; the invisible cost of skipping is missed content during deletion.

## Misnaming this skill / placing it locally

The principle is generic across repos. The skill belongs at user level (`~/.agents/skills/`), not inside one repo's local skills directory. The name should reflect the principle (index pattern), not the one-time action of restructuring.

# After the migration

The first AGENTS.md is rarely the last. The skill is structural; content quality is a separate pass. Common follow-ups:

- Promote prose rules into Biome / lint custom rules ("when documentation falls short, promote into code" — harness post).
- Tighten or rename verbose docs.
- Audit cross-references after the dust settles.
- Pull skill paths into a single naming convention if multiple agent tools (Codex + Claude) maintain parallel skill trees.

These are not part of the structural migration. They come later.
