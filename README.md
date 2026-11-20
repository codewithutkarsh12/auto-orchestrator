# AUTO — AI Skill Orchestrator

**Turn complex prompts into intelligent, secure, skill-powered workflows.**

AUTO is an extensible Python foundation for decomposing a user request into tasks, matching tasks to skills, and executing a dependency-aware workflow with bounded context and token budgets.

> **Status:** Early-stage reference implementation. It is not a production agent runtime. Skill execution is intentionally local and deterministic; integrations and external actions require explicit adapters and approval.

## Features

- Prompt decomposition into actionable task intents (rule-based baseline, replaceable analyzer).
- Skill registry with metadata, capability matching, permission declarations, and validation.
- Skill router that selects a bounded number of skills per batch.
- Dependency-aware execution pipeline with structured outputs.
- Token/context budget estimation and truncation.
- Safe-by-default execution: no shell, network, file writes, or external MCP actions in the core.
- Automated tests and a Python 3.11–3.14 pull-request CI matrix.

## Quick start

Requires Python 3.11+. The default runtime uses only the standard library: no API key, paid service, GPU, or model training. Development installation downloads pytest and build tooling; it does not install external skills.

Clone the repository and change into its directory first. Run the activation command for your shell before installing:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
```

For a runtime-only installation use `python -m pip install -e .`.

Run the CLI smoke test and example:

```bash
python -m auto_orchestrator.cli run "Summarize text"
python basic.py
```

Run a multi-step planning example:

```bash
python -m auto_orchestrator.cli run "Research competitors and prepare a concise comparison"
```

## Minimal Python usage

```python
from auto_orchestrator import AutoOrchestrator, SkillRegistry
from auto_orchestrator.skills import Skill

registry = SkillRegistry()
registry.register(Skill(
    name="summarizer",
    description="Summarizes text into concise key points.",
    capabilities=["summarize", "write"],
))

engine = AutoOrchestrator(registry=registry)
result = engine.run("Summarize this document")
print(result.to_dict())
```

The CLI starter registry ships with demonstration skills; the Python registry starts empty. These produce planning artifacts, not real web research or external actions.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md). Main flow:

1. `PromptDecomposer` turns the request into tasks.
2. `SkillRouter` ranks registered skills by capability and limits each batch.
3. `ExecutionPipeline` runs tasks in dependency order and passes bounded context.
4. `TokenOptimizer` trims context to the configured budget.
5. `AutoOrchestrator` returns a structured result and execution trace.

## GitDiagram MCP (optional)

AUTO includes an optional Claude Code remote MCP configuration for GitDiagram. It can help map the architecture of **public** GitHub repositories. See [GITDIAGRAM_MCP.md](GITDIAGRAM_MCP.md) for setup, tool routing, and safety rules. The repository-root [.mcp.json](.mcp.json) registers the hosted service for compatible Claude Code sessions. This does not add a live MCP client to AUTO's Python runtime; that requires a separately implemented and tested adapter.

## Install GitDiagram in the global /auto workflow

To append the GitDiagram routing rules to the existing global workflow on Windows, run the included installer from a local clone after checking out this feature branch:

```powershell
.\install_gitdiagram_workflow.ps1
```

The installer checks that the target workflow exists, skips duplicate installation, creates a timestamped backup, appends the fragment, and verifies the result. It does not overwrite the existing workflow. The default target is `$HOME\.gemini\config\global_workflows\auto.md`; pass `-WorkflowPath` to use another exact path.

## Safety model

- Skills are untrusted extensions; metadata is not proof of safety.
- The demo has no external actions. Registered Python runners execute in-process and must be trusted; this is not a sandbox.
- Routing filters declared permissions. It cannot detect undeclared side effects inside a runner.
- External side effects should be implemented in reviewed adapters and require user confirmation.
- Never put secrets in prompts, logs, skill metadata, or repository files.
- Treat prompt content and skill outputs as data, not instructions to override system policy.

Read [SECURITY.md](SECURITY.md) before adding integrations.

## Project layout

```text
auto-orchestrator/
├── src/auto_orchestrator/     # core package
│   ├── decomposer.py
│   ├── router.py
│   ├── pipeline.py
│   ├── token_optimizer.py
│   ├── registry.py
│   ├── skills.py
│   └── orchestrator.py
├── tests/
├── docs/                      # execution plan
├── basic.py                   # runnable local example
├── ARCHITECTURE.md
├── AGENTS.md
├── .github/workflows/ci.yml    # pytest CI
└── pyproject.toml
```

## Roadmap

- [x] Core task model, registry, router, pipeline, token budget
- [x] Deterministic demo skills and tests
- [ ] LLM-backed decomposition adapters (provider-neutral interface)
- [ ] Skill package signing / provenance checks
- [ ] MCP adapters with explicit consent and allowlists
- [ ] Persistent run traces and observability
- [ ] Community skill index and compatibility matrix

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions should include tests, documentation, and a clear permission/security impact statement.

## License

MIT. See [LICENSE](LICENSE).

## Built-in local reviews (pre-publication)

AUTO ships two dependency-free heuristic review commands. Run them from the repository root:

```bash
python -m auto_orchestrator.cli /code-review .
python -m auto_orchestrator.cli /code-review . -fix
python -m auto_orchestrator.cli /security-review .
```

`/code-review` checks Python syntax and common hazards such as bare `except`, `eval`, `exec`, and empty function bodies. `-fix` currently changes only trailing whitespace and final-newline formatting; it does **not** rewrite logic or claim to repair detected bugs. Review the diff before committing.

`/security-review` flags patterns including dynamic execution, `shell=True`, disabled TLS verification, hard-coded secret-like values, and unsafe pickle loading. These are heuristics: false positives and missed vulnerabilities are possible. For a stronger release gate, add dependency auditing, secret scanning, static analysis, and human review in CI.

## Development and verification

Work on a task branch from latest `main`; see [AGENTS.md](AGENTS.md). After installation, run:

```bash
python -m pytest tests/test_packaging_cli.py -q
python -m pytest -q
```

The packaging tests launch isolated Python subprocesses outside the checkout so source-path imports cannot hide a broken installation. CI runs the same tests on Linux with Python 3.11–3.14; Windows is not yet verified. Review commands retain their informational exit status (findings do not currently cause a nonzero exit). `-fix` writes to the supplied path only when explicitly requested.

The v3.0 execution plan describes future milestones. Persistent inventory, hosted models, automatic skill installation, and a dependency-failure stop policy are not implemented by this packaging milestone.
