---
name: oracle
description: Ask the user's logged-in ChatGPT Pro model, currently GPT-5.5 Pro, through Chrome using Computer Use, wait for the answer, and bring the useful guidance back into the current Codex thread.
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

- Use Computer Use to operate the local Chrome app directly.
- Navigate Chrome to ChatGPT.
- Select Pro (GPT-5.5 Pro) before sending.
- Send one focused prompt.
- Wait for the answer to finish.
- Summarize the useful guidance back in the Codex thread.

Do not use the Codex in-app Browser for Oracle. The in-app Browser cannot rely
on the user's logged-in ChatGPT session.

Do not use the Chrome plugin as the default Oracle path. It can time out on long
Pro runs. Use it only if the user explicitly asks for that plugin or Computer
Use is unavailable and the user approves the fallback.

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

## Computer Use Workflow

1. If the Oracle question is unclear, ask one short clarifying question. If the
   current thread already makes the question clear, proceed.
2. Build the prompt from verified local context and the user's actual goal.
3. Use Computer Use to open or focus Google Chrome.
4. Navigate to `https://chatgpt.com/`.
5. Verify that the page is logged in to the user's ChatGPT account. If it is not
   logged in and no saved session is available, stop and report that Oracle is
   unavailable until the user logs in.
6. Start a new ChatGPT conversation unless continuing an existing Oracle thread
   is clearly required by the user's request.
7. Open the model selector and choose Pro (GPT-5.5 Pro).
   If the selector does not expose a Pro model, stop and report that the Oracle
   surface is unavailable.
8. Paste/send the prompt.
9. Wait patiently. Pro can take several minutes. Observe the page periodically
   with Computer Use until the response is complete.
10. Extract the final answer. Do not invent the answer while ChatGPT is still
    thinking.
11. Return a concise Codex summary with the direct verdict first, then the
    actionable steps and local verification still needed.

## Browser Rules

- Default: Computer Use controlling Chrome.
- Do not use the in-app Browser.
- Do not use the Chrome plugin by default.
- Do not use a logged-out, free, or non-Pro ChatGPT surface as the Oracle.
- Do not bypass browser safety barriers, solve CAPTCHAs, or handle login
  challenges automatically. Ask the user to take over for those steps.
- If ChatGPT asks to save credentials, payment details, or persistent account
  permissions, stop and ask the user.
- If the prompt would transmit sensitive private data to ChatGPT and the user
  has not clearly approved that specific transmission, confirm immediately
  before sending.

## Waiting And Extraction

- Pro answers can run long. Keep waiting unless the user asks to stop or the UI
  clearly errors.
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
selector, Pro availability, page error, or Computer Use access.
