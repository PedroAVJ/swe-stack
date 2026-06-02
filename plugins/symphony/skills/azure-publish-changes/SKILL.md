---
name: "azure-publish-changes"
description: "Publish local changes for an Azure DevOps-hosted Symphony lane: confirm scope, stage intended files, commit, push, and create or update an Azure DevOps pull request."
---

# Symphony Azure Publish Changes

Use this skill when Pedro wants the publish half of an Azure DevOps repo
lifecycle: scope confirmation, branch, commit, push, and pull request creation
or update.

This is the generic Azure DevOps lane. If the current repo has a repo-local
publish skill, use that local skill first because it may know project-specific
validation, branch, and PR conventions.

## Required Repo Facts

Derive these from the repo before mutating anything:

- Azure DevOps organization URL from `git remote get-url origin`.
- Project name from the remote URL or repo docs.
- Repository name from the remote URL or repo docs.
- Target branch from the remote default branch or repo docs.
- Existing repo-local publish skill, if any.

Do not hardcode client/project names from another repo.

## Quick Start

1. Run `git status -sb`, `git branch --show-current`, `git remote get-url origin`,
   and `git worktree list`.
2. Confirm the remote is Azure DevOps/Azure Repos.
3. Inspect `git diff --stat` and `git diff --name-only`.
4. If the worktree is mixed, ask which files belong in scope.
5. If on the target branch, create `codex/{description}`.
6. Stage only intended files.
7. Commit with a terse message.
8. Run focused validation appropriate to the changed paths.
9. Push with upstream tracking.
10. Reuse an active Azure DevOps PR for the branch, or create a draft PR.
11. Summarize branch, commit, PR URL, and validation.

## Azure DevOps PR Commands

Detect values first:

```bash
origin_url=$(git remote get-url origin)
branch=$(git branch --show-current)
```

Find an active PR for the branch:

```bash
az repos pr list \
  --organization ORG_URL \
  --project PROJECT_NAME \
  --repository REPOSITORY_NAME \
  --source-branch "$branch" \
  --status active
```

Create a draft PR when none exists:

```bash
az repos pr create \
  --organization ORG_URL \
  --project PROJECT_NAME \
  --repository REPOSITORY_NAME \
  --source-branch "$branch" \
  --target-branch TARGET_BRANCH \
  --title "[codex] SHORT_DESCRIPTION" \
  --description "what changed" "why it changed" "validation" \
  --draft true
```

When using `--description`, pass each paragraph or bullet line as a separate
argument so Azure DevOps renders markdown with real newlines.

## Guardrails

- Never stage unrelated user changes silently.
- Never push a mixed worktree without confirming scope.
- Default new PRs to draft unless Pedro explicitly asks for ready-for-review.
- If Azure DevOps auth is missing, report that blocker instead of switching to
  GitHub tooling.
- If an active PR already exists for the branch, update or reuse it instead of
  creating a duplicate PR.

## Final Report

Include:

- branch name
- commit SHA
- PR ID and URL
- target branch
- validation commands run
- any remaining manual follow-up
