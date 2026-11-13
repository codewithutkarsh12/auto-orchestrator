"""Transparent heuristics for ranking possible first contributions."""
from __future__ import annotations

from datetime import datetime, timezone


COMPLEXITY_TERMS = (
    "rewrite", "migration", "distributed", "kubernetes", "production outage",
    "breaking change", "architecture redesign", "performance regression",
)


def _age_days(updated_at: str | None) -> int | None:
    if not updated_at:
        return None
    try:
        value = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        return max(0, (datetime.now(timezone.utc) - value).days)
    except ValueError:
        return None


def score_issue(issue: dict) -> tuple[int, list[str]]:
    """Return a 0-100 explainable score; this is triage, not a merge prediction."""
    labels = {
        str(label.get("name", "")).strip().lower()
        for label in issue.get("labels", [])
        if isinstance(label, dict)
    }
    body = (issue.get("body") or "").lower()
    title = (issue.get("title") or "").lower()
    text = f"{title}\n{body}"
    score = 30
    reasons = ["Open issue returned by GitHub search"]

    if "good first issue" in labels or "good-first-issue" in labels:
        score += 25
        reasons.append("Has a beginner-friendly issue label")
    if "help wanted" in labels:
        score += 10
        reasons.append("Maintainers marked it as help wanted")
    if any(term in body for term in ("acceptance criteria", "expected behavior", "done when")):
        score += 15
        reasons.append("Contains explicit completion criteria")
    if any(term in body for term in ("test", "reproduction", "steps to reproduce")):
        score += 5
        reasons.append("Mentions tests or reproduction steps")
    if len(body.strip()) > 250:
        score += 5
        reasons.append("Provides some implementation context")
    if any(term in text for term in COMPLEXITY_TERMS):
        score -= 20
        reasons.append("Contains potentially high-complexity wording")

    age = _age_days(issue.get("updated_at"))
    if age is not None and age <= 30:
        score += 10
        reasons.append("Updated within the last 30 days")
    elif age is not None and age > 180:
        score -= 10
        reasons.append("No update for more than 180 days")

    score = max(0, min(100, score))
    return score, reasons


def to_candidate(issue: dict) -> dict:
    score, reasons = score_issue(issue)
    repository_url = issue.get("repository_url", "")
    repository = "/".join(repository_url.rstrip("/").split("/")[-2:])
    return {
        "repository": repository or "unknown/unknown",
        "number": issue.get("number"),
        "title": issue.get("title", "Untitled issue"),
        "url": issue.get("html_url", ""),
        "updated_at": issue.get("updated_at", ""),
        "labels": [
            label.get("name", "")
            for label in issue.get("labels", [])
            if isinstance(label, dict)
        ],
        "score": score,
        "reasons": reasons,
        "body": issue.get("body") or "",
    }
