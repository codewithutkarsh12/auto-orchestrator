"""Small, dependency-free GitHub issue search client.

Only public issue metadata is read. No repository code is downloaded or executed.
"""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class GitHubApiError(RuntimeError):
    """Raised when GitHub returns an error or cannot be reached."""


def search_open_issues(
    query: str,
    *,
    limit: int = 20,
    token: str | None = None,
    sort: str = "updated",
) -> list[dict]:
    """Search public GitHub issues. Pull requests are excluded from results."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    if sort not in {"updated", "created", "comments", "reactions"}:
        raise ValueError("unsupported sort value")

    auth_token = token or os.getenv("GITHUB_TOKEN")
    params = urlencode({
        "q": query,
        "per_page": limit,
        "sort": sort,
        "order": "desc",
    })
    request = Request(
        f"https://api.github.com/search/issues?{params}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "AUTO-OSS-Contributor/0.1",
            **({"Authorization": f"Bearer {auth_token}"} if auth_token else {}),
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        if exc.code in {403, 429}:
            raise GitHubApiError(
                "GitHub rate limit or access restriction. Set GITHUB_TOKEN and retry later. "
                f"Details: {detail}"
            ) from exc
        raise GitHubApiError(f"GitHub API returned HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise GitHubApiError(f"GitHub request failed: {exc}") from exc

    items = payload.get("items", [])
    return [item for item in items if "pull_request" not in item]
