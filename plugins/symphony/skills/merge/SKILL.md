---
name: merge
description: "Run the explicit Symphony publish/merge/release-proof lifecycle: branch, PR, merge, rollout babysitting, tracker reconciliation, and worktree cleanup across GitHub, Azure DevOps, or another repo host."
---

# Symphony Merge

## Overview

Use this skill for the whole "get it into the real target and prove the relevant release settled" lifecycle.

When work was started through `implementation-dispatch`, the dispatched worker
thread owns this lifecycle by default. The parent/operator thread routes Pedro's
merge approval back to that same worker thread; it does not execute the merge
itself unless no worker thread exists or Pedro explicitly asks this thread to
take over.

This skill supersedes the old `merge-and-babysit` name. It also incorporates the publish step: if the work is local, first publish it on a branch and create a PR; then merge; then babysit the relevant rollout, deployment, preview, release, tracker, and worktree state.

Use underlying skills as implementation modules when they fit:

- For GitHub publishing, follow the installed `github:yeet` skill when available.
- For legacy prompts or detailed rollout heuristics, the old `merge-and-babysit` path may redirect here.
- For repo-local workflows, prefer a repo-local `merge` skill over this global skill when present.
- For Azure DevOps repos, prefer `azure-publish-changes` and
  `azure-merge` when the repo matches their facts or has equivalent
  Azure DevOps conventions.

## Thread Ownership

Use this routing before touching Git, GitHub, Linear, or deployment state:

- If you are the parent/operator thread and the work has an implementation
  thread, PR, branch, or Linear issue produced by `implementation-dispatch`,
  find that worker thread with `list_threads`/`read_thread` and send it a merge
  prompt with `send_message_to_thread`.
- The merge prompt should name the Linear issue, PR/branch, Pedro's approval,
  and ask the worker to run this `merge` skill through merge, rollout proof,
  tracker reconciliation, and local cleanup.
- Do not start a second worker or merge locally from the parent just because
  the PR is ready. Report the worker thread that now owns the merge.
- If you are the worker thread that receives Pedro's merge approval, run the
  lifecycle in this skill end-to-end and report the merge/release result in the
  worker thread.
- If no worker thread exists, or the worker is unavailable/blocked, the parent
  may run this skill directly after saying why it is taking over.
- If Pedro explicitly asks the current thread to merge, this thread may execute
  the merge directly, but still preserve the same merge/release/tracker proof
  contract.

## Default Meaning

When the user says "merge", assume they want:

1. A branch, never direct commits to the default branch.
2. A scoped commit and PR if the change is local.
3. A host-native merge once the PR is ready.
4. Active babysitting of the release signals that matter for this specific change.
5. Tracker reconciliation when applicable.
6. Local worktree realignment when safe.

Do not stop at "PR opened" unless the user explicitly asks only for a PR.
Do not stop at "merged" when there are rollout signals to watch.
Do not claim a release is done when the remaining boundary is manual.
In an operator thread, "merge" usually means "tell the issue's worker thread to
run the merge lane"; in a worker thread, it means "execute the merge lane here."

## Branch And Publish Policy

Always branch local work before publishing.

- If local changes exist on `main`, `master`, or the remote default branch, create `codex/{description}` first.
- If local changes exist on a feature branch, usually keep that branch.
- If the user asks to merge an existing PR from a clean checkout, do not create a new branch.
- Never commit directly to the default branch unless the user explicitly asks for direct-to-main and the repo policy allows it.
- If the worktree contains unrelated changes, inspect the diff and stage only the intended files. Ask the user when scope is ambiguous.
- Default PR state is draft unless the user explicitly asks for ready-for-review or the repo workflow requires ready PRs for merge.

## Quick Start

1. Orient:

```bash
git status -sb
git branch --show-current
git remote get-url origin
git worktree list
```

2. Detect the repo host and existing PR state.
3. If local changes need publishing, run the publish phase.
4. If a PR exists or was created, run the merge phase.
5. Babysit every release signal relevant to the changed paths until success, failure, no-runtime-change, or documented manual handoff.
6. Reconcile linked tracker issues and worktrees.

## Publish Phase

### GitHub

Use `github:yeet` for the GitHub publish flow. It owns:

- branch creation from default branch
- scope confirmation
- explicit staging
- commit
- push with upstream tracking
- draft PR creation

After using it, record the branch, commit SHA, PR number, PR URL, and checks run.

### Azure DevOps

Use repo-local publish guidance when present, such as `.agents/skills/publish-changes/SKILL.md`.

If no repo-local publish skill exists, use host-native Azure DevOps commands:

- create or keep a branch
- commit scoped changes
- push the branch
- create a PR with `az repos pr create`

Do not pretend GitHub auth is broken when the repo remote is Azure DevOps.

### Other Hosts

Use the documented host-native publish path. If there is no documented safe path, stop and report the host and missing publish boundary.

## Merge Phase

Detect the host before merging.

### GitHub

Use `gh pr view` or GitHub tools to confirm:

- PR number/title
- base and head branch
- mergeability
- required checks or branch protection state
- whether the PR is draft

Merge non-interactively with explicit strategy flags. If the merge command reports conflicts, stop immediately. Do not retry with another strategy or continue rollout babysitting.

### Azure DevOps

Use Azure DevOps CLI or repo-local guidance. Confirm the PR is not draft, is mergeable, and targets the intended branch. Complete it non-interactively with explicit options. Stop on conflicts.

### Other Hosts

Use host-native merge commands only when documented and safe. Otherwise stop at a clear manual boundary.

## Babysitting Scope

Before watching anything, determine the changed-path scope from the local diff, PR file list, and repo docs. Babysit only the CI, preview, deployment, release, job, or live-behavior surfaces that could actually be affected by those changes.

Documentation-only, skill-only, workflow-note-only, and other non-runtime changes may have no production surface to watch. In that case, treat "no runtime rollout relevant to these changed paths" as a valid terminal state after merge and any required merge-gating checks settle. Do not arbitrarily wait for production to deploy just to have a deployment to report.

Runtime production rollout proof is relevant when the changed files affect deployed app code, backend code, job code, infrastructure, runtime configuration, schema, native app release contents, or another user-facing/execution surface. Preview or non-production signals matter when:

- the user explicitly asks for preview verification
- the PR has not merged yet and preview is the requested review surface
- repo docs say preview is the release surface
- preview checks block merge
- the change is a mobile/internal-testing release, desktop artifact, background job, or other non-web surface

Do not treat a PR preview as production proof unless the repo really uses that preview as the production/release surface.
Do not probe unrelated live endpoints, dashboards, jobs, or apps merely because they exist in the repo.

Separate the final report by surface:

- merge state
- production web/backend deployment
- background jobs
- mobile build/update/internal-testing release
- preview or branch deployment when relevant
- direct live probes
- tracker state
- local worktree state

## Discover Release Signals

Start from the merged commit SHA or the exact build/release artifact ID.

For GitHub repos:

```bash
gh api repos/OWNER/REPO/commits/SHA/status
gh api repos/OWNER/REPO/commits/SHA/check-runs
gh run view RUN_ID --json name,workflowName,status,conclusion,jobs,url
```

Use the bundled watcher when GitHub statuses/check-runs are the right signal:

```bash
python3 ~/.codex/skills/merge/scripts/watch_github_rollout.py \
  --repo OWNER/REPO \
  --sha MERGED_SHA
```

For Azure DevOps repos:

```bash
az pipelines runs list --organization ORG_URL --project PROJECT --branch TARGET_BRANCH
az pipelines runs show --organization ORG_URL --project PROJECT --id RUN_ID
```

Read `references/release-signals.md` when the repo has multiple possible rollout surfaces or the right proof is unclear.

## Poll Until Terminal

Watch the relevant signals until:

- success
- failure
- no deployment needed for the changed paths
- a documented manual boundary
- an auth/observability boundary that cannot be resolved safely

If a release fails, pull the first useful failing status, check-run, pipeline, deployment, or live-probe detail. Include URLs when available.

## Tracker Reconciliation

If the work is tied to Linear or another tracker:

- identify the issue before merge when possible
- move it to completed only after the relevant rollout proof is satisfied
- leave it open or report the boundary if merge succeeded but rollout failed or could not be verified

Use native tracker tools when available.

## Worktree Realignment

After rollout settles, leave worktrees in a useful state when safe.

- If this worktree is clean and can own the target branch:

```bash
git fetch origin
git switch TARGET_BRANCH
git pull --ff-only origin TARGET_BRANCH
```

- If another worktree owns the target branch:

```bash
git fetch origin
git switch --detach origin/TARGET_BRANCH
```

- If this is a linked worktree, also fast-forward the main worktree when it is clean and already on the target branch.
- Never stash, reset, delete, or force-switch unrelated local work.

## Guardrails

- Always branch local work.
- Never stage unrelated changes silently.
- Never assume "merged" means "deployed."
- Never assume one release surface proves all release surfaces.
- Never confuse PR preview proof with production proof.
- Never continue after merge conflicts.
- Never mark tracker work complete before release proof settles.
- Never force local worktree cleanup.
- Do not log into external dashboards or click externally visible actions unless the user asked for that surface or the release workflow requires it.
- Stop before destructive or externally visible manual actions when user confirmation is required.

## Final Report

Include:

- branch name
- commit SHA
- PR number/title/URL
- merge commit SHA and timestamp
- checks run
- rollout/release signals watched and final state
- direct probes used, if any
- tracker updates
- final local worktree state
- any remaining manual boundary or follow-up release skill to run
