---
name: "symphony-azure-merge"
description: "Run the Azure DevOps Symphony merge lane: publish or reuse an Azure DevOps PR, merge it, babysit relevant rollout proof, verify live behavior when scoped, and reconcile the tracker after proof is satisfied."
---

# Symphony Azure Merge

Use this skill when Pedro wants the full Azure DevOps ship flow for a repo:
branch, publish, PR, merge, rollout proof when relevant, tracker
reconciliation, and worktree cleanup.

This is the generic Azure DevOps lane. If the current repo has repo-local
`merge`, `publish-changes`, release, or deployment skills, prefer those local
rules for project-specific facts and then use this skill as the lifecycle
shape.

## Required Repo Facts

Derive these before mutating anything:

- Azure DevOps organization URL from `git remote get-url origin`.
- Project name from the remote URL or repo docs.
- Repository name from the remote URL or repo docs.
- Target branch from the remote default branch or repo docs.
- Relevant pipeline names from `azure-pipelines.yml`, repo docs, or Azure CLI.
- Relevant production/preview endpoints from repo docs or deployment config.
- Tracker issue and terminal/review states when a tracker is involved.

Do not hardcode facts from a different client or repo.

## Branch And Publish Policy

- Always branch local work before publishing.
- If local changes exist on the target branch, create `codex/{description}`.
- If already on a feature branch, stay there unless Pedro asks otherwise.
- Never commit directly to the target branch unless Pedro explicitly asks.
- If the worktree is mixed, stage only intended files and ask when scope is
  ambiguous.
- Use repo-local publish guidance when present. Otherwise use
  `symphony-azure-publish-changes`.

## Quick Start

1. Run `git status -sb`, `git branch --show-current`, `git remote get-url origin`,
   and `git worktree list`.
2. Confirm the remote is Azure DevOps/Azure Repos.
3. If local changes need publishing, run the publish phase.
4. Confirm PR, target branch, mergeability, and local worktree safety.
5. Complete the Azure DevOps PR non-interactively.
6. Record merged commit SHA and merge timestamp.
7. Determine which runtime surfaces are relevant from changed paths.
8. Watch only relevant Azure Pipelines, App Service/Kudu, preview, job, or live
   behavior signals.
9. Reconcile tracker state only after the applicable proof is satisfied.
10. Realign worktrees when safe.

## Merge The Azure DevOps PR

Show the PR first:

```bash
az repos pr show \
  --organization ORG_URL \
  --project PROJECT_NAME \
  --id PR_ID
```

Complete it non-interactively:

```bash
az repos pr update \
  --organization ORG_URL \
  --project PROJECT_NAME \
  --id PR_ID \
  --status completed
```

If Azure DevOps reports conflicts or the PR is not mergeable, stop immediately.
Do not continue to rollout babysitting until conflicts are resolved.

## Rollout Relevance Gate

Before watching anything, inspect changed paths from the local diff or PR file
list.

- Runtime proof is relevant for backend, frontend, jobs, database, deployment
  scripts, pipelines, infrastructure, configuration, native/mobile artifacts, or
  anything that affects a live execution surface.
- Docs-only, skill-only, README-only, or internal workflow-note changes may have
  no runtime surface. In that case, merge plus required checks is terminal.
- Watch only the surfaces the changed paths can affect.
- Do not treat a PR preview as production proof unless the repo explicitly uses
  that preview as the release surface.

Report skipped surfaces as `not relevant to changed paths`.

## Prove Rollout Completion

Use the most direct applicable evidence:

1. Azure Pipelines when visible through CLI/API.

```bash
az pipelines runs list \
  --organization ORG_URL \
  --project PROJECT_NAME \
  --branch TARGET_BRANCH
```

```bash
az pipelines runs show \
  --organization ORG_URL \
  --project PROJECT_NAME \
  --id RUN_ID
```

2. App Service/Kudu deployment records when pipeline visibility is blocked and
   credentials are available.

3. Exact live behavior probes for small backend/API/UI changes where the new
   behavior can be observed directly.

4. Health probes only as supplemental evidence. Health alone is not deployment
   proof unless paired with pipeline, Kudu, deployment, or exact behavior
   evidence.

If Azure CLI/API visibility is blocked, report the permission boundary and use
other non-browser proof only when available. Do not open Azure Portal or other
interactive UIs unless Pedro explicitly asks.

## Tracker Reconciliation

- Identify linked Linear or tracker issue before merge when possible.
- Move it to completed only after relevant proof is satisfied.
- Leave it open and report the boundary if merge succeeded but rollout proof
  failed or could not be verified.

## Worktree Cleanup

After rollout reaches a terminal state, leave worktrees useful when safe:

```bash
git fetch origin
git switch TARGET_BRANCH
git pull --ff-only origin TARGET_BRANCH
```

If another worktree owns the target branch:

```bash
git fetch origin
git switch --detach origin/TARGET_BRANCH
```

Never stash, reset, delete, or force-switch unrelated local work.

## Final Report

Include:

- branch and commit
- PR number/title/URL
- merged commit SHA and timestamp
- rollout evidence used, or `not relevant to changed paths`
- direct probes used, if any
- tracker issue action and final state
- final local branch or detached-`HEAD` state
- remaining manual boundary, if any
