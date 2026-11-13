"""CLI for discovering and ranking open-source contribution opportunities."""
from __future__ import annotations

import argparse
from pathlib import Path

from .github_client import GitHubApiError, search_open_issues
from .scoring import to_candidate


def build_query(language: str, label: str, repository: str | None) -> str:
    parts = ["is:issue", "is:open"]
    if label:
        parts.append(f'label:"{label}"')
    if language:
        parts.append(f"language:{language}")
    if repository:
        parts.append(f"repo:{repository}")
    return " ".join(parts)


def render_markdown(candidates: list[dict]) -> str:
    lines = [
        "# AUTO Open Source Contribution Shortlist",
        "",
        "> Scores are transparent heuristics, not guarantees of issue availability or PR acceptance.",
        "> Re-check that each issue is still open and read the repository's CONTRIBUTING guide.",
        "",
    ]
    if not candidates:
        lines.append("No matching issues found. Try another language, label, or repository.")
        return "\n".join(lines) + "\n"

    for item in candidates:
        lines.extend([
            f"## [{item['repository']}#{item['number']}]({item['url']}) — {item['score']}/100",
            "",
            f"**{item['title']}**",
            "",
            f"- Updated: {item['updated_at'] or 'unknown'}",
            f"- Labels: {', '.join(item['labels']) or 'none returned'}",
            f"- Why it ranked: {'; '.join(item['reasons'])}",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Discover and rank open-source issues for AUTO."
    )
    parser.add_argument("--language", default="Python", help="GitHub language qualifier")
    parser.add_argument("--label", default="good first issue", help="Issue label")
    parser.add_argument("--repo", help="Optional owner/repository filter")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--min-score", type=int, default=35)
    parser.add_argument("--sort", choices=["updated", "created", "comments", "reactions"], default="updated")
    parser.add_argument("--output", help="Optional Markdown report path")
    args = parser.parse_args()

    if not 0 <= args.min_score <= 100:
        parser.error("--min-score must be between 0 and 100")

    query = build_query(args.language, args.label, args.repo)
    try:
        raw_issues = search_open_issues(query, limit=args.limit, sort=args.sort)
    except (GitHubApiError, ValueError) as exc:
        parser.exit(1, f"Discovery failed: {exc}\n")

    candidates = [
        to_candidate(issue)
        for issue in raw_issues
    ]
    candidates = sorted(
        (item for item in candidates if item["score"] >= args.min_score),
        key=lambda item: item["score"],
        reverse=True,
    )
    report = render_markdown(candidates)

    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(report, encoding="utf-8")
        print(f"Saved {len(candidates)} candidate(s) to {destination}")
    else:
        print(report)
    print("\nNext: inspect the issue, read CONTRIBUTING.md, and confirm maintainer intent before coding.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
