"""Local, dependency-free code and security review helpers for AUTO.

These checks are heuristics, not a substitute for expert review or dedicated scanners.
"""
from __future__ import annotations
import ast
from dataclasses import dataclass, asdict
from pathlib import Path
import re

@dataclass
class Finding:
    rule_id: str
    severity: str
    file: str
    line: int
    message: str
    suggestion: str = ""
    fixable: bool = False

    def to_dict(self):
        return asdict(self)


def _python_files(path: Path):
    if path.is_file():
        return [path] if path.suffix == ".py" else []
    return sorted(p for p in path.rglob("*.py") if not any(x in p.parts for x in (".venv", "venv", "__pycache__", ".git")))


def code_review(path: str | Path) -> list[Finding]:
    root = Path(path)
    findings = []
    for file in _python_files(root):
        try:
            source = file.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        try:
            ast.parse(source, filename=str(file))
        except SyntaxError as e:
            findings.append(Finding("PY-SYNTAX", "error", str(file), e.lineno or 1, e.msg))
            continue
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                findings.append(Finding("PY-BARE-EXCEPT", "warning", str(file), node.lineno, "Bare except catches every exception.", "Catch a specific exception."))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                findings.append(Finding("PY-EVAL", "warning", str(file), node.lineno, "eval() executes dynamically constructed code.", "Use a parser or explicit dispatch."))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "exec":
                findings.append(Finding("PY-EXEC", "warning", str(file), node.lineno, "exec() executes arbitrary Python code.", "Avoid exec or isolate and validate inputs."))
            if isinstance(node, ast.FunctionDef) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                findings.append(Finding("PY-EMPTY-FUNCTION", "info", str(file), node.lineno, f"Function '{node.name}' is only pass."))
    return findings


SECURITY_RULES = [
    ("SEC-EVAL", "high", re.compile(r"\beval\s*\("), "Avoid eval; parse data or use explicit dispatch."),
    ("SEC-EXEC", "high", re.compile(r"\bexec\s*\("), "Avoid exec; never execute untrusted skill content."),
    ("SEC-SHELL-TRUE", "high", re.compile(r"subprocess\.(?:run|Popen|call|check_output)\([^\n]*shell\s*=\s*True"), "Use an argument list and shell=False."),
    ("SEC-VERIFY-TLS", "high", re.compile(r"verify\s*=\s*False"), "Keep TLS certificate verification enabled."),
    ("SEC-SECRET-LITERAL", "critical", re.compile(r"(?i)(?:api[_-]?key|secret|password|token)\s*=\s*['\"][A-Za-z0-9_\-./+=]{12,}['\"]"), "Load secrets from environment or a secret manager; rotate exposed credentials."),
    ("SEC-PICKLE", "high", re.compile(r"\bpickle\.loads?\s*\("), "Do not unpickle untrusted data; use JSON or a constrained format."),
]


def security_review(path: str | Path) -> list[Finding]:
    root = Path(path)
    findings = []
    files = list(_python_files(root))
    if root.is_dir():
        files += sorted(p for p in root.rglob("*.yml") if ".git" not in p.parts)
        files += sorted(p for p in root.rglob("*.yaml") if ".git" not in p.parts)
    for file in files:
        try: lines = file.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError): continue
        for lineno, line in enumerate(lines, 1):
            # Ignore comments to reduce noisy matches; this is deliberately conservative.
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            for rule, severity, pattern, suggestion in SECURITY_RULES:
                if pattern.search(line):
                    findings.append(Finding(rule, severity, str(file), lineno, f"Potential security issue: {rule}.", suggestion))
    return findings


def apply_safe_fixes(path: str | Path) -> int:
    """Apply only conservative formatting fixes; security findings are never auto-fixed."""
    root = Path(path)
    changed = 0
    for file in _python_files(root):
        try: original = file.read_text(encoding="utf-8")
        except (OSError, UnicodeError): continue
        # Safe and semantics-preserving: remove trailing whitespace and ensure final newline.
        fixed = "\n".join(line.rstrip() for line in original.splitlines()) + ("\n" if original else "")
        if fixed != original:
            file.write_text(fixed, encoding="utf-8")
            changed += 1
    return changed
