---
name: swe-stack-plugin-release
description: Release and upgrade SWE Stack plugins across both Codex and Claude Code. Use when changing a plugin in PedroAVJ/swe-stack, bumping plugin versions, publishing to the marketplace, or verifying that Codex and Claude installed caches both see the same plugin version.
---

# SWE Stack Plugin Release

Use this skill when a SWE Stack plugin changes and needs to be available in
both Codex and Claude Code.

## Model

SWE Stack uses one source directory per plugin and client-specific manifests:

- Shared plugin source: `plugins/<plugin>/`
- Codex manifest: `plugins/<plugin>/.codex-plugin/plugin.json`
- Claude manifest: `plugins/<plugin>/.claude-plugin/plugin.json`

Do not fork the implementation just because both clients use the plugin. Add a
Claude-specific source path only when the runtime behavior truly differs. Most
plugins should share skills, scripts, CLIs, assets, docs, and tests.

## Before Editing

Start from the marketplace checkout:

```bash
cd ~/.codex/.tmp/marketplaces/swe-stack
git status --short --branch
git fetch origin main
```

If another checkout is in use, verify its remote is
`https://github.com/PedroAVJ/swe-stack.git`.

Leave unrelated untracked installer files alone, such as
`.codex-marketplace-install.json`.

## Change Checklist

1. Patch the plugin source under `plugins/<plugin>/`.
2. If the plugin version should change, bump every relevant version:
   - `plugins/<plugin>/package.json`, when present.
   - `plugins/<plugin>/.codex-plugin/plugin.json`.
   - `plugins/<plugin>/.claude-plugin/plugin.json`, when present.
3. If a plugin is intended to work in both clients, ensure both manifests exist.
4. Update the plugin skill/docs when agent behavior changes.
5. Add or update tests that guard the behavior and manifest shape.

Useful manifest audit:

```bash
find plugins -maxdepth 3 \( -path '*/.codex-plugin/plugin.json' -o -path '*/.claude-plugin/plugin.json' -o -name package.json \) -print
```

## Validate

Run focused tests for the changed plugin. Examples:

```bash
pnpm --dir plugins/whatsapp test
python3 -m py_compile plugins/whatsapp/cli/whatsapp_cli.py
```

Validate manifests when Claude-specific metadata changed:

```bash
claude plugins validate plugins/<plugin>
```

Use `git diff --check` before committing.

## Commit And Push

Stage only related plugin files:

```bash
git add plugins/<plugin> ...
git commit -m "Short plugin release summary"
git push origin main
```

After pushing, verify local and remote `main` agree:

```bash
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

## Upgrade Codex

Codex has its own marketplace checkout and plugin cache under:

```text
~/.codex/.tmp/marketplaces/swe-stack
~/.codex/plugins/cache/swe-stack/<plugin>/<version>
```

Upgrade:

```bash
codex plugin marketplace upgrade
```

If the installed Codex CLI cannot parse the user's config because
`service_tier = "default"` is too new/old for that CLI, use a one-command
override instead of editing the user's config:

```bash
codex -c 'service_tier="fast"' plugin marketplace upgrade
```

Verify the installed cache:

```bash
find ~/.codex/plugins/cache/swe-stack/<plugin> -maxdepth 2 -name package.json -print -exec cat {} \;
```

For CLI plugins, verify the new command surface through the installed command
or cache path.

## Upgrade Claude Code

Claude Code has a separate marketplace checkout, install manifest, and cache:

```text
~/.claude/plugins/marketplaces/swe-stack
~/.claude/plugins/installed_plugins.json
~/.claude/plugins/cache/swe-stack/<plugin>/<version>
```

Update the marketplace, then update the installed plugin:

```bash
claude plugins marketplace update swe-stack
claude plugins update <plugin>@swe-stack
```

Verify:

```bash
claude plugins list
cat ~/.claude/plugins/installed_plugins.json
cat ~/.claude/plugins/cache/swe-stack/<plugin>/<version>/.claude-plugin/plugin.json
```

Claude reports "restart required to apply changes"; mention this if any Claude
session may already be running.

If Claude's marketplace checkout reports stale `origin/main`, refresh it:

```bash
git -C ~/.claude/plugins/marketplaces/swe-stack fetch origin main
git -C ~/.claude/plugins/marketplaces/swe-stack status --short --branch
```

## Closeout

Report:

- Commit SHA pushed.
- Tests/validation run.
- Codex installed version and cache path.
- Claude installed version and cache path.
- Any client restart needed.

Do not claim both clients are upgraded until both caches or install manifests
have been read back.
