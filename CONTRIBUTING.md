# Contributing to AUTO

Thanks for helping make AUTO safer and more useful! 🎉

## Before you start

1. Check existing issues and discussions before opening a new one.
2. For substantial changes, open an issue describing the problem and proposed approach.
3. Keep pull requests focused; avoid bundling unrelated refactors.

## Development setup

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Pull request checklist

- [ ] Tests added or updated
- [ ] `pytest` passes
- [ ] `ruff check .` passes
- [ ] Docs and examples updated where needed
- [ ] New permissions and external effects are documented
- [ ] No credentials, personal data, or private user content included
- [ ] Skill behavior is deterministic or randomness is controlled in tests

## Adding a skill

Prefer declarative metadata under `skills/` first. Include a unique name, version,
description, capabilities, dependencies, permissions, risk level, and input/output
contract. Do not add arbitrary code execution to the core registry.

## Style

- Python 3.11+
- Type hints for public interfaces
- Small functions and explicit errors
- Tests for happy paths, invalid inputs, and permission boundaries
- Keep dependencies minimal

## Community expectations

Be respectful and constructive. Maintainers may request changes, close unsafe
contributions, or defer proposals that do not fit the project scope.
