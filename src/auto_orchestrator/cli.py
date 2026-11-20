"""Command-line entry point for AUTO's planning baseline."""
import argparse
import json
from . import AutoOrchestrator, SkillRegistry, Skill
from .review import code_review, security_review, apply_safe_fixes

def build_demo() -> AutoOrchestrator:
    registry = SkillRegistry()
    registry.register(Skill("planner", "Creates a safe task plan", ["plan", "general"]))
    registry.register(Skill("summarizer", "Summarizes content", ["summarize", "write"]))
    registry.register(Skill("analyst", "Analyzes and compares", ["analyze", "research"]))
    registry.register(Skill("coder", "Plans code tasks", ["code", "test", "review"]))
    return AutoOrchestrator(registry=registry)

def main() -> None:
    parser = argparse.ArgumentParser(description="AUTO: AI Skill Orchestrator")
    sub = parser.add_subparsers(dest="command")
    run_parser = sub.add_parser("run", help="Decompose and route a prompt")
    run_parser.add_argument("prompt", help="User prompt to decompose")
    review_parser = sub.add_parser("/code-review", help="Review Python code for common bugs")
    review_parser.add_argument("path", nargs="?", default=".")
    review_parser.add_argument("-fix", dest="fix", action="store_true", help="Apply safe whitespace fixes only")
    sec_parser = sub.add_parser("/security-review", help="Scan for common security hazards")
    sec_parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args()
    if args.command == "/code-review":
        if args.fix:
            print(f"Applied safe formatting fixes to {apply_safe_fixes(args.path)} file(s).")
        findings = code_review(args.path)
    elif args.command == "/security-review":
        findings = security_review(args.path)
    elif args.command == "run":
        print(json.dumps(build_demo().run(args.prompt).to_dict(), indent=2))
        return
    else:
        parser.print_help()
        return
    print(json.dumps([f.to_dict() for f in findings], indent=2))
    print(f"\n{len(findings)} finding(s). Heuristic review only; verify manually.")

if __name__ == "__main__":
    main()
