# Security Policy

## Supported versions

The latest `main` branch and latest tagged release are the initial supported targets.

## Reporting a vulnerability

Please do **not** report exploitable vulnerabilities in public issues. Use GitHub's
private vulnerability reporting feature if enabled for this repository, or contact
maintainers privately through a verified channel listed in the repository profile.

Include affected version/commit, impact, reproduction steps, and a proposed mitigation
when possible. Do not include real secrets or personal data in the report.

## Security boundaries

AUTO's core is a planner and local execution framework. It does not intentionally
run arbitrary code or contact external services. Extensions can change that risk.

- Treat skill packages, prompts, model outputs, and remote metadata as untrusted.
- Do not execute downloaded skill code without provenance, review, and sandboxing.
- Do not place API keys, tokens, passwords, or private user data in skills or logs.
- External actions (send, publish, delete, deploy, purchase, permission changes)
  must be implemented by explicit adapters and require user approval.
- Validate and sanitize outputs before passing them to tools or integrations.
- Use least privilege and narrow allowlists for integrations.
- Never allow skill text to override system or application security policy.

## Disclosure

Please allow maintainers a reasonable opportunity to investigate and release a fix
before public disclosure.
