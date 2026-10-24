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
- Tests and GitHub contribution/security templates.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

Run the example:

```bash
python -m auto_orchestrator.cli "Research competitors and prepare a concise comparison"
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

The starter registry ships with safe demonstration skills. These produce planning artifacts, not real web research or external actions.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Main flow:

1. `PromptDecomposer` turns the request into tasks.
2. `SkillRouter` ranks registered skills by capability and limits each batch.
3. `ExecutionPipeline` runs tasks in dependency order and passes bounded context.
4. `TokenOptimizer` trims context to the configured budget.
5. `AutoOrchestrator` returns a structured result and execution trace.

## Safety model

- Skills are untrusted extensions; metadata is not proof of safety.
- The core does not execute arbitrary skill code, shell commands, network calls, or MCP actions.
- Permission declarations are checked before execution.
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
├── skills/                    # declarative sample skill catalog
├── tests/
├── docs/
├── .github/                   # issue/PR templates and CI
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
