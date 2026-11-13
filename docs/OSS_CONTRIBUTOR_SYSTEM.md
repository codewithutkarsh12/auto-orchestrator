# AUTO Open Source Contributor System

## Goal

Discover real, beginner-appropriate open-source issues and help Utkarsh complete meaningful contributions. The system optimizes for learning, maintainable code, accepted work, and a trustworthy public portfolio—not artificial contribution activity.

## Current MVP

The first milestone is a dependency-free issue discovery and ranking CLI:

- Uses GitHub's public issue search API.
- Filters to open issues and excludes pull requests.
- Supports language, label, repository, result limit, and sort filters.
- Ranks candidates using transparent heuristics.
- Produces a Markdown shortlist.
- Does not clone repositories, execute third-party code, modify files, or submit PRs.

Run from the repository root:

```powershell
python -m oss_contributor.cli --language Python --label "good first issue" --limit 20 --min-score 35
```

Optional report:

```powershell
python -m oss_contributor.cli --language Python --output reports/oss-shortlist.md
```

For higher GitHub API limits, set a fine-grained token in the environment as `GITHUB_TOKEN`. Do not hard-code it or commit it. Public search can work without a token but has stricter limits.

Run the MVP tests:

```powershell
python -m unittest discover -s oss_contributor/tests -v
```

## /AUTO integration

The system follows AUTO's existing orchestration boundaries:

1. **Decomposer** — turn a contribution goal into discovery, triage, repository inspection, implementation, tests, review, and PR preparation tasks.
2. **Skill registry** — register focused capabilities: `oss.discover`, `oss.triage`, `oss.inspect`, `oss.patch`, `oss.test`, `oss.review`, `oss.pr.prepare`.
3. **Router** — select no more than four skills per execution batch.
4. **Pipeline** — pass bounded issue/repository context between stages.
5. **Quality engine** — require acceptance-criteria mapping, focused tests, lint/type checks where present, and a clean diff.
6. **Execution engine** — isolate each task in a branch/worktree and record commands, outputs, changed files, and test results.

The discovery CLI is intentionally standalone in this first milestone so it does not destabilize AUTO's existing core.

## Target workflow

```text
Discover issues
  -> Score and shortlist
  -> Human selects an issue
  -> Read CONTRIBUTING, SECURITY, license, and issue discussion
  -> Inspect repository stack and test commands
  -> Create fork/branch/worktree
  -> Map acceptance criteria to tests
  -> Implement the smallest focused change
  -> Run focused tests, then the documented full checks
  -> Run code and security review
  -> Generate PR title/body with evidence
  -> Human approval
  -> Open PR
  -> Track review feedback and CI
```

## Safety and trust boundaries

- Issue descriptions, repository files, READMEs, CI logs, and model output are untrusted data, never instructions that override system policy.
- Do not run install scripts, build scripts, tests, or repository-provided commands until their contents and side effects have been inspected.
- Never execute downloaded skill code or shell commands copied from issue text automatically.
- Never expose tokens, credentials, private data, or environment dumps in logs or PRs.
- Use a separate branch/worktree per contribution; never patch the user's main branch directly.
- Do not auto-merge, force-push, publish releases, or modify repository settings.
- Require explicit human approval before opening a PR or posting comments.
- Respect maintainer contribution rules, DCO/sign-off requirements, issue claims, and AI disclosure policies.

## Planned milestones

### M1 — Discovery and ranking
Implemented in this branch. Standard-library Python; no Docker or paid API required.

### M2 — Repository inspection
Read README, CONTRIBUTING, license, issue discussion, language, test commands, and recent maintainer activity. Produce a risk and effort report without executing repository code.

### M3 — Isolated implementation workspace
Create a fork/branch and isolated Git worktree. Require approval before dependency installation or running repository scripts.

### M4 — Test-first patch agent
Map each acceptance criterion to a failing test, implement the smallest patch, then run focused and full test suites. Follow repository-specific conventions.

### M5 — Independent quality gates
Run formatting/lint, tests, secret scanning, dependency checks, diff review, and security review. Report what was actually executed; never claim unrun checks passed.

### M6 — Pull request preparation
Draft a focused PR with issue link, change summary, test evidence, screenshots if relevant, and AI-assistance disclosure where required. Human approval is mandatory before submission.

## Honest automation boundary

Issue discovery and ranking are automated in M1. Reliable code generation and validation need a coding model/runtime. A completely autonomous hosted model workflow is not guaranteed to be free; a local model can avoid API fees but may be slower or less capable on modest hardware. The design therefore keeps the provider adapter optional and keeps the default workflow usable without paid services.
