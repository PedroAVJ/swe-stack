---
name: codex-app-hacking
description: Inspect, patch, restore, or reason about the local macOS Codex desktop app bundle. Use when working with /Applications/Codex.app, Electron ASAR files, Info.plist ElectronAsarIntegrity, ad-hoc codesigning, Codex Safe Storage Keychain prompts, or local desktop feature experiments.
---

# Codex App Hacking

Use this skill for local Codex desktop app surgery. Treat it as a careful
forensics and patch workflow, not a general app-development guide.

## Operating Rules

- Prefer official app updates and supported configuration before patching the
  app bundle.
- Before touching `/Applications/Codex.app`, identify the exact app version and
  make fresh backups of `app.asar`, `app.asar.unpacked`, and `Info.plist`.
- Patch the smallest possible expression in an extracted ASAR. Minified
  function names and hashed bundle names change by release.
- After repacking `app.asar`, update `Info.plist`
  `ElectronAsarIntegrity:Resources/app.asar:hash` with the ASAR header hash,
  not the whole-file hash.
- Re-sign after bundle changes with `codesign --force --deep --sign -`.
- Explain that macOS Keychain prompts for `Codex Safe Storage` are expected
  after ad-hoc re-signing; that item is Electron safe-storage material, not the
  user's OpenAI password.
- Do not replay old patch binaries against a newer Codex version. Re-locate the
  behavior in the current extracted bundle.

## Workflow

Read `references/asar-workflow.md` before making or restoring a Codex app patch.

For Browser-pane work specifically, first verify whether the current official
Codex app already exposes the feature. The old local Browser-pane patch was a
historical workaround; it is not a reason to preserve stale binary backups if
the feature has shipped.

## Output

When reporting results, include:

- app version and bundle path inspected
- files backed up or changed
- ASAR header hash update status
- signing verification result
- whether the app was launched or left untouched
