import unittest

from oss_contributor.cli import build_query, render_markdown
from oss_contributor.scoring import score_issue, to_candidate


class IssueScoringTests(unittest.TestCase):
    def test_beginner_issue_with_acceptance_criteria_scores_higher(self):
        issue = {
            "title": "Fix a small parser bug",
            "body": "Expected behavior and acceptance criteria. Add a regression test.",
            "labels": [{"name": "good first issue"}, {"name": "help wanted"}],
            "updated_at": "2099-01-01T00:00:00Z",
        }
        score, reasons = score_issue(issue)
        self.assertGreaterEqual(score, 80)
        self.assertTrue(any("completion criteria" in reason for reason in reasons))

    def test_complex_issue_receives_penalty(self):
        issue = {
            "title": "Architecture redesign",
            "body": "This requires a distributed migration and rewrite.",
            "labels": [],
            "updated_at": "",
        }
        score, reasons = score_issue(issue)
        self.assertLessEqual(score, 20)
        self.assertTrue(any("high-complexity" in reason for reason in reasons))

    def test_candidate_maps_repository_and_labels(self):
        issue = {
            "repository_url": "https://api.github.com/repos/example/project",
            "number": 12,
            "title": "Improve docs",
            "html_url": "https://github.com/example/project/issues/12",
            "labels": [{"name": "good first issue"}],
        }
        candidate = to_candidate(issue)
        self.assertEqual(candidate["repository"], "example/project")
        self.assertEqual(candidate["number"], 12)
        self.assertEqual(candidate["labels"], ["good first issue"])

    def test_query_includes_language_label_and_repo(self):
        query = build_query("Python", "good first issue", "example/project")
        self.assertIn("language:Python", query)
        self.assertIn('label:"good first issue"', query)
        self.assertIn("repo:example/project", query)

    def test_markdown_report_handles_empty_results(self):
        self.assertIn("No matching issues", render_markdown([]))


if __name__ == "__main__":
    unittest.main()
