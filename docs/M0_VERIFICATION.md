# M0 verification evidence

Status: implementation prepared; installation/full-suite verification blocked.

Base: `d7f9401` (latest fetched main on 2026-11-19).
Branch: `feat/packaging-ci-baseline`.
Local Python: 3.12.14, Linux.

## Red phase (before implementation)

- `python -m pip install -e . --no-build-isolation`: exit 1; neither setup.py nor pyproject.toml found.
- `python -m auto_orchestrator.cli run 'Summarize text'`: exit 1; ModuleNotFoundError for auto_orchestrator.
- `python -m pytest -q`: exit 1; pytest is absent from the environment.
- `python -m unittest discover -s tests -p test_packaging_cli.py -v`: exit 1; 5 tests ran, 6 failures including review-command subtests. Installed package imports/CLI are unavailable.

## Prepared implementation

- Move original modules unchanged into src/auto_orchestrator; preserve public imports and CLI behavior.
- Move all existing tests unchanged into tests.
- Add setuptools packaging, Python >=3.11 metadata, zero runtime dependencies and optional pytest development dependency.
- Add installed-package subprocess tests for public imports, run, both reviews, explicit whitespace fixes, and invalid commands. Isolated subprocesses use a temporary working directory.
- Add main-targeting pull-request pytest CI on Python 3.11–3.14, read-only permissions, no secrets or inference.
- Reconcile README/CONTRIBUTING with actual layout, installation, run subcommand and safety limitations.

## Checks actually completed after implementation

- `PYTHONPATH=src python -m auto_orchestrator.cli run 'Summarize text'`: exit 0; valid JSON, summarizer selected, `[Plan only]` output, succeeded=true. This is source-level evidence, NOT an installation check.
- `python -m compileall -q src tests`: exit 0.
- `git diff --check`: exit 0.

## Remaining gate

Automatic approval review rejected installing pytest, setuptools and wheel because repository instructions require explicit package-install approval. No existing pytest installation was found in the default or system Python. Do not bypass this with CI installation before approval.

After approval, install development/build dependencies inside .venv, verify editable install, run focused and full pytest, and repeat the install/CLI checks in a fresh clone. Open the draft PR and record actual CI results and URL. Windows remains unverified. No merge is authorized.

No runtime algorithms were changed. No external skills, model APIs, paid services, or other feature branches are involved.

## Approved verification (2026-11-19, Python 3.12.14)

The user explicitly approved pytest, setuptools, wheel and their four transitive dependencies for the isolated M0 environment and CI. The earlier remaining-gate text above documents the historical red phase, not the current state.

- `.venv/bin/python -m pip install --index-url https://pypi.org/simple 'pytest>=8,<10' 'setuptools>=68' wheel`: exit 0; installed only pytest 9.2.0, setuptools 84.2.1, wheel 0.48.0, iniconfig 2.3.1, packaging 26.3, pluggy 1.7.0, pygments 2.21.0.
- `.venv/bin/python -m pip install --no-deps --no-build-isolation -e .`: exit 0, built and installed editable auto-orchestrator 0.1.0.
- `.venv/bin/python -m pytest tests/test_packaging_cli.py -q`: exit 0; 5 passed, 2 subtests passed.
- `.venv/bin/python -m pytest -q`: exit 0; 16 passed, 2 subtests passed.
- `.venv/bin/python -m auto_orchestrator.cli run 'Summarize text'`: exit 0; valid JSON, succeeded=true, summarizer plan-only output.
- `.venv/bin/python -m auto_orchestrator.cli /code-review src/auto_orchestrator/cli.py`: exit 0; 0 heuristic findings.
- `.venv/bin/python -m auto_orchestrator.cli /security-review src/auto_orchestrator/cli.py`: exit 0; 0 heuristic findings.
- Metadata inspection: exit 0; version 0.1.0, Python >=3.11, no required runtime dependencies, optional pytest dev extra.
- `git diff main...HEAD --check`: exit 0; modules and existing tests moved without content change. Added packaging, docs, CI and CLI regression tests only. No credential pattern matched in changed content (heuristic scan, not a complete secret audit).
- CI matrix configures 3.11, 3.12, 3.13, 3.14; only local 3.12.14 executed before PR. GitHub CI results will be checked after PR creation.
