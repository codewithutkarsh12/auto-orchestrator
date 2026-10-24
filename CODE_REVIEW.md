# Local code and security review

AUTO's built-in review is an early warning layer, not a security certification.

## Commands

```bash
python -m auto_orchestrator.cli /code-review .
python -m auto_orchestrator.cli /code-review . -fix
python -m auto_orchestrator.cli /security-review .
```

## Scope

- Code review: Python parse errors, bare exception handlers, `eval`/`exec`, and pass-only functions.
- Security review: suspicious `eval`/`exec`, subprocess `shell=True`, TLS `verify=False`, likely inline credentials, and pickle deserialization.
- Safe autofix: trailing whitespace and missing final newline only.

## Limitations

The scanner is regex/AST based, does not understand data flow or runtime context, and can both miss vulnerabilities and report harmless code. `-fix` does not fix bug findings. Always inspect the diff, run tests, and use dedicated tools (for example Bandit, pip-audit, and a secret scanner) plus human review before publishing.
