---
name: oracle
description: Ask the user's logged-in ChatGPT Pro model, currently GPT-5.5 Pro, through Chrome using the Chrome plugin, wait for the answer, and bring the useful guidance back into the current Codex thread.
metadata:
  author: Pedro
  origin: swe-stack-plugin
  source: hand-written
  provenance: unofficial-not-openai-curated
---

# Oracle

## Overview

Use the user's logged-in ChatGPT session in Chrome as the Oracle. This is the
single Oracle skill. The intended model is ChatGPT Pro's Pro option, currently
GPT-5.5 Pro.

The default Oracle flow is live and interactive:

- Use the Chrome plugin / Codex Chrome Extension against the user's logged-in
  Chrome ChatGPT session.
- Open a fresh ChatGPT conversation unless the user explicitly asks to continue
  an existing one.
- Select Pro (GPT-5.5 Pro / Extended Pro) before sending.
- Verify the visible model control says `Extended Pro` or an equivalent Pro
  label before sending. If the model control still says `Instant`, abort.
- Send one focused prompt.
- Wait for the answer to finish, even if it takes many minutes.
- Summarize the useful guidance back in the Codex thread.

Do not use the Codex in-app Browser for Oracle. The in-app Browser cannot rely
on the user's logged-in ChatGPT session.

Use Computer Use only as a fallback if the Chrome plugin is unavailable,
cannot communicate with Chrome after the standard retry/recovery checks, or the
user explicitly asks for Computer Use.

The old static dossier/zip workflow is no longer the Oracle default. The helper
scripts under this skill directory are legacy utilities, not the primary skill
behavior.

## When To Use

Use this skill when the user says things like:

- "ask Pro"
- "ask the Oracle"
- "use Oracle"
- "get a second opinion from Pro"
- "ask ChatGPT Pro"
- "ask GPT-5.5 Pro"
- "use the stronger model"
- "run this by Pro Mode"

If the user explicitly asks for a static uploadable zip, say that the old
dossier helper still exists locally, then use it only for that request. Do not
silently switch normal Oracle requests into bundle-building.

## Source-Of-Truth Discipline

Before asking Pro, gather the facts Codex can verify locally.

- For repo work, inspect the relevant files, diffs, tests, logs, issue text, and
  deployment state first.
- For messages, tickets, docs, emails, calendars, Sentry, Linear, or other
  external state, use the relevant source-of-truth connector or local artifact
  first when available.
- Distinguish verified facts from guesses in the prompt.
- Do not ask Pro to fetch data from tools it cannot access.

Oracle is a second-opinion reasoning surface, not a replacement for Codex's
local source checks.

## Prompt Shape

Write one concise prompt for Pro. Include only what matters.

Strong Oracle prompts look like this:

```text
I need a second-opinion answer from a senior <domain> engineer.

Context:
- <verified fact>
- <verified command/log/result>
- <current implementation detail>
- <constraint that matters>

Question:
1. <core decision>
2. <specific failure mode>
3. <practical implementation path>

Please be blunt. Separate verified platform behavior from guesses. Prefer a
concrete next step over generic advice.
```

For code or repo problems, include relevant file paths and short excerpts or
summaries. If the context is too large to paste safely, reduce it to the
decision-critical facts before using Oracle.

## Chrome Plugin Workflow

1. If the Oracle question is unclear, ask one short clarifying question. If the
   current thread already makes the question clear, proceed.
2. Build the prompt from verified local context and the user's actual goal.
3. Use the Chrome plugin with the Codex Chrome Extension. Start with a
   lightweight connection check such as listing open tabs.
4. Open a fresh ChatGPT tab at `https://chatgpt.com/`, unless the user
   explicitly asks to continue an existing Oracle thread.
5. Verify that the page is logged in to the user's ChatGPT account. If it is not
   logged in and no saved session is available, stop and report that Oracle is
   unavailable until the user logs in.
6. Open the model selector and choose Pro (GPT-5.5 Pro / Extended Pro).
   If the selector does not expose a Pro model, stop and report that the Oracle
   surface is unavailable.
7. Verify the visible model control after selection. It must say `Extended Pro`
   or an equivalent Pro label before the prompt is sent. If it says `Instant`,
   do not send.
8. Paste/send the prompt only after the Pro verification succeeds.
9. Wait patiently. Pro can take many minutes. Poll in short chunks and recover
   the Chrome plugin session if the socket stalls, then re-claim the same
   ChatGPT tab. Never cancel a Pro run merely because it is taking a long time.
10. If the tab can be listed or claimed but page body, DOM, or screenshot reads
    keep timing out, treat the live tab as wedged rather than treating the
    Oracle run as lost. Recover the saved conversation URL from the tab list or
    Chrome history, open that `https://chatgpt.com/c/...` URL in a fresh tab,
    and extract the answer there.
11. Extract the final answer only after the page no longer shows that ChatGPT is
    thinking.
12. Return a concise Codex summary with the direct verdict first, then the
    actionable steps and local verification still needed.

## Browser Rules

- Default: Chrome plugin controlling the user's logged-in Chrome session through
  the Codex Chrome Extension.
- Do not use the in-app Browser.
- Do not use Computer Use by default.
- Do not use a logged-out, free, or non-Pro ChatGPT surface as the Oracle.
- Do not bypass browser safety barriers, solve CAPTCHAs, or handle login
  challenges automatically. Ask the user to take over for those steps.
- If ChatGPT asks to save credentials, payment details, or persistent account
  permissions, stop and ask the user.
- If the prompt would transmit sensitive private data to ChatGPT and the user
  has not clearly approved that specific transmission, confirm immediately
  before sending.

## Waiting And Extraction

- Pro answers can run long. Keep waiting unless the user explicitly asks to
  stop or the UI clearly errors.
- Never click `Stop answering` or otherwise cancel a Pro run for duration alone.
- If a Chrome plugin call times out or the socket stalls, reset/reconnect the
  browser runtime and re-claim the existing ChatGPT tab before deciding the run
  failed.
- If Chrome can still list or claim the ChatGPT tab but body, DOM, or screenshot
  reads keep timing out, use saved-history recovery before starting over:
  recover the current `https://chatgpt.com/c/...` URL from open tabs or Chrome
  history, open it in a fresh tab, wait for the saved conversation to load, and
  extract the completed answer from the fresh tab.
- Do not start a duplicate Oracle run until the fresh-tab history recovery path
  has been tried. If it succeeds, summarize that answer and mention that the
  original live tab's extraction path wedged.
- Use screen observation or screenshots sparingly to determine whether the
  answer is still generating.
- Avoid dumping large transcripts back into Codex. Summarize the relevant
  answer.
- If the user asks for status while Pro is still thinking, say so plainly and
  continue waiting.
- If the response fails, times out, or the page becomes unusable, report the
  failure and what was already sent.

## Output Contract

Return a concise summary, not a transcript dump.

Include:

- Pro's direct answer.
- What changed in our understanding.
- Concrete next implementation or decision steps.
- Caveats, assumptions, or facts Pro said should be locally verified.

If Pro was unavailable, say exactly which surface failed: Chrome login, model
selector, Pro verification, page error, Chrome plugin access, or Computer Use
fallback access.
