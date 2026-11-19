# AUTO v3.0: Zero-Cost Implementation Plan

**Date:** 2026-11-19
**Status:** Proposed implementation plan, not a released runtime
**Scope:** Existing `codewithutkarsh12/auto-orchestrator`; retain all existing feature branches and preserve `main`
**Constraints:** ₹0 **additional** spending (existing ChatGPT Plus subscription excluded); low-end laptop; no model training; no mandatory paid API; approval before installs or external side effects; active skill library capped at 100, discovery unbounded.

## 1. Ground-truth audit (GitHub `main`, 68fef0b)

- Python modules exist at repository root: `cli.py`, `decomposer.py`, `router.py`, `registry.py`, `pipeline.py`, `orchestrator.py`, `token_optimizer.py`, and related tests.
- The README claims `src/auto_orchestrator/`, `pyproject.toml`, and a `.github/` layout, but these are not present on `main`. Its editable-install and `python -m auto_orchestrator.cli` instructions therefore require repair/verification.
- Router uses a simple capability-overlap score. Registry is in-memory. Skill runners are local callables; a missing runner returns a **plan-only** response. No production autonomous agent, LLM adapter, remote skill installer, or authenticated MCP bridge is proven.
- `feat/gitdiagram-mcp-integration` has draft PR #1; `feat/ui-ux-reference-library` has open PR #2; `feat/oss-contributor-discovery-mvp` exists as a separate branch. These should be independently audited and not bulk-merged.
- One historical GitHub Actions run succeeded on the OSS branch, but no `.github/workflows` exists on current `main`.
- Audit is based on repository API inspection, **not an end-to-end local test run**.

## 2. Intended system architecture

```text
User request: /AUTO ...      (CLI/workflow contract; not a new native ChatGPT command)
       |
   Intent + task breakdown
       |
   Discovery / inventory (local paths, approved GitHub sources, provider capabilities)
       |-- SQLite inventory + provenance + hash + permission metadata
       |-- states: discovered -> inspected -> validated -> approved -> installed -> enabled
       |
   Router -> up to 4 relevant compatible active skills
       |
   Risk / permission gate  ----> DENY / ASK APPROVAL / ALLOW
       |
   Executor (sequential by default; concurrent only if real support is verified)
       |-- pure Python deterministic adapters (default)
       |-- optional Codex-capable adapter (only with documented interface & quota)
       |-- optional external MCP/app adapters (only if explicitly connected and supported)
       |
   Verifier -> unit/integration/security/evaluation checks
       |
   Structured result + redacted trace + reproducibility notes
```

Separate **discovery** from **installation**: discovering a GitHub skill never authorizes downloading, executing, granting permissions, or writing outside the repository.

### Target code organization (migration target, not current layout)
```text
auto-orchestrator/
  AGENTS.md
  pyproject.toml
  src/auto_orchestrator/
    cli.py
    core/{models,decomposer,router,pipeline,orchestrator}.py
    ecosystem/{inventory,discovery,policy,provenance,compatibility}.py
    adapters/{base,local}.py
    verification/{evals,traces}.py
  tests/{unit,integration,fixtures}/
  docs/{ARCHITECTURE,SECURITY,AUTO_V3_EXECUTION_PLAN}.md
  .github/workflows/ci.yml
```
Introduce folders in small reviewed PRs; don't break existing imports all at once. Avoid a GUI and heavy agent frameworks until CLI behavior is proven.

## 3. Work allocation: Plus, Work, Codex, and GitHub

| Surface | Useful work | Limitation |
| --- | --- | --- |
| ChatGPT Plus chat | Requirements, design, threat review, task specs, evaluation criteria | Chat responses do not modify local Antigravity settings automatically |
| ChatGPT Work | Research skill sources, inspect site/repo content, produce audit reports, permitted multi-step actions | Availability, permissions, usage budget and connected apps vary |
| Codex (ChatGPT sign-in) | Code changes on a dedicated branch, running focused/full tests, PR-ready diffs | Included usage limited; not a free unlimited API for another process |
| GitHub public repo | Source of truth; PRs; standard-runner Actions test jobs | CI must not embed a paid inference call or unsafe untrusted-code execution |
| Python 3.11+ / SQLite / pytest | Small, local, deterministic control plane, tests and inventory | SQLite is local state, not cross-device automatic sync |

ChatGPT Plus/API billing are separate. Do not assume a subscription key can be embedded in AUTO to call hosted models for free. No dependencies on Claude Code, Antigravity, or other subscriptions.

## 4. Implementation milestones and acceptance gates

### M0 — Stabilize baseline (Days 1–3; ~3–6 focused hours)
- Create `pyproject.toml`, restore valid importable `auto_orchestrator` package, correct README, keep existing CLI features.
- Organize `tests/`; add `python -m pytest` checks and `.github/workflows/ci.yml` on pull requests.
- Add minimal `AGENTS.md`; require branch-based development.
- **Gate:** Fresh clone: isolated Python 3.11+, editable install works, `python -m auto_orchestrator.cli run "Summarize text"` exits 0, full unit tests pass. Document real command output and CI URL. Never claim this gate passed until executed.

### M1 — Ecosystem inventory (Days 4–9; ~5–8 hours)
- Read-only discover adapters: existing local skill manifests, configured Antigravity / Codex / Claude sources **if accessible**, GitHub catalog URLs and user-supplied repositories.
- SQLite inventory: canonical ID, origin, source URL, commit/version, content digest, license, permission requirements, runtime, status, last-verified timestamp, compatibility.
- Canonical status labels: `discovered`, `inspected`, `validated`, `approved`, `installed`, `enabled`, `quarantined`.
- Hard separation of all discovered entries from max 100 **enabled** trusted skills; deduplicate by source identity and semantic purpose.
- **Gate:** 20 offline fixtures load without executing them; malformed/malicious metadata is rejected; no external writes or process launches. Repeated scans produce deterministic inventory entries.

### M2 — Router + safety policy (Days 10–16; ~6–8 hours)
- Maintain current deterministic baseline. Add task categories: research, programming, data, design, content, operations.
- Recommend only enabled, compatible skills; default top 1–4. Report evidence and reason for selection, missing capability, and fallback.
- Use `ALLOW`, `ASK`, `DENY`; file changes, installs, GitHub writes, web actions, posting, credentials, and payments require explicit bounded approvals.
- Sequential specialist passes by default (planner → implementer → reviewer → verifier); use actual multi-agent execution only when supported and demonstrated.
- **Gate:** Gold fixture suite (at least 30 prompts) measures top-1 correct routing and top-4 coverage; publish baseline and improvement, not an unsupported accuracy claim. Tests prove permission denial and stop-on-failure behavior.

### M3 — Execution and proof (Days 17–24; ~6–10 hours)
- Provider-neutral `ModelAdapter` interface with pure-Python stub/offline fallback. External LLM usage stays disabled unless a documented existing plan-backed tool or separately permitted free tier is verified.
- Store structured, **secret-redacted** run history; record input ID, selected skills, approvals, failures, test evidence, output references. Never store raw tokens, passwords or API keys.
- Implement `/AUTO-PLAN`, `/AUTO-VERIFY`, `/AUTO-STATUS` in the documented CLI/workflow layer; adapters must not impersonate native ChatGPT slash commands.
- **Gate:** End-to-end local demonstration from task → plan → permission decision → deterministic execution → verification report; zero side effects in dry-run.

### M4 — Optional integration reviews (after M3, separate PRs)
- Audit PR #1 GitDiagram and PR #2 UI reference library for scope, dependencies, licensing, prompt injection, accessibility and testability. Each requires independent tests before merge.
- Inspect OSS-contributor discovery branch for reusable read-only scanning logic.
- Any MCP adapter must verify real tool protocol, auth, permissions, network behavior and rollback. Keep disabled unless available.

## 5. Verification matrix

| Test | Required behavior |
| --- | --- |
| Clean install | Editable installation succeeds on Python 3.11+ |
| CLI smoke | `run` and existing review commands return predictable JSON / exit statuses |
| Router | Unsupported task -> clear no-skill result, not fabricated success |
| Dependencies | Cycles, missing IDs, duplicate IDs rejected |
| Failures | Exception recorded; dependent action skipped, not silently marked complete |
| Skill trust | Unreviewed remote content not executed |
| Approval | Unknown/denied permission -> blocked before side effect |
| Provenance | Source URL, revision/hash and verification status stored |
| Privacy | Secret-like strings absent from traces and CI output |
| Budget | No OpenAI API key or billable API request required for default workflow |
| CI | Unit tests pass on main-targeting PR before merge |
| Compatibility | CLI tested on Windows and Linux, or remaining platform declared unverified |

**Definition of done:** Tested implementation + documentation aligned with repository contents + passing GitHub CI + reviewable PR + user-approved merge. A plan, passing mock, or generated code without execution evidence is not a completed feature.

## 6. Cost and limits

- **Incremental cash:** ₹0 target; ChatGPT Plus already paid, not counted as ₹0 total cost.
- **Compute:** lightweight laptop for Python; use included Codex cloud when available; public-repo standard GitHub Actions for tests.
- **Avoid:** model training, GPU hosting, paid databases, Docker requirement, hosted inference as default, auto-install of untrusted repos, scheduled broad GitHub crawling with high rate usage.
- **Usage policy:** one small acceptance-tested engineering task per Codex run; reserve Work for multi-source audits, use Chat for specs, avoid rerunning unchanged contexts. Check product Usage settings instead of assuming unlimited calls.
- **Free services can change:** verify current quotas and terms before depending on them.

## 7. Risk register

1. **README/runtime divergence** -> P0 fixes packaging and documentation before feature work.
2. **Prompt-injection / supply-chain attacks from skills** -> read-only ingestion, quarantine, provenance, permissions, sandbox testing and human review.
3. **False expectation of free hosted model API** -> strict offline default, optional documented adapters, real usage accounting.

## 8. First Codex task: only M0

> Open `codewithutkarsh12/auto-orchestrator`. Start a new `feat/packaging-ci-baseline` branch from latest main; do not edit main or merge unrelated PRs. Inspect the real file layout and README; reproduce the packaging/import failure before changes. Use test-driven development to fix packaging in the smallest coherent change; preserve existing CLI review commands and behavior. Add Python 3.11+ `pyproject.toml`, importable package layout, working editable install, corrected README, project `AGENTS.md` guidance, and non-inference GitHub Actions pytest CI. Run the focused tests and full suite on the branch. Report exact commands and outputs and open a draft PR. Do not install remote skills, use paid APIs, rewrite external Antigravity global workflows, or claim success without verification.

## 9. Decision boundaries

- Merge only after user review; preserve `main`.
- Approval required **before skill/plugin installs** and consequential changes.
- Discovery sources can be broad; the active trusted library stays at **100 or fewer** skills.
- Keep independent global Antigravity `/auto` workflow and Python repository distinct until a compatibility-tested bridge exists.
- No assumed cross-session, cross-app or cross-device automatic synchronization.
