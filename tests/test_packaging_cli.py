"""Installed-package regressions; compatible with pytest and stdlib unittest."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class InstalledPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def run_python(self, *args):
        return subprocess.run(
            [sys.executable, '-I', *args], cwd=self.directory,
            capture_output=True, text=True, check=False,
        )

    def test_public_imports(self):
        result = self.run_python('-c',
            'from auto_orchestrator import AutoOrchestrator, SkillRegistry, Skill; '
            'from auto_orchestrator.models import Task; '
            'from auto_orchestrator.review import code_review')
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_run_cli(self):
        result = self.run_python('-m', 'auto_orchestrator.cli', 'run', 'Summarize text')
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload['succeeded'])
        self.assertEqual(payload['executions'][0]['skill_name'], 'summarizer')
        self.assertTrue(payload['executions'][0]['output'].startswith('[Plan only]'))

    def test_review_commands(self):
        for command, source, rule in [
            ('/code-review', 'result = eval(user_input)\n', 'PY-EVAL'),
            ('/security-review', 'subprocess.run(cmd, shell=True)\n', 'SEC-SHELL-TRUE'),
        ]:
            with self.subTest(command=command):
                fixture = self.directory / 'sample.py'
                fixture.write_text(source, encoding='utf-8')
                result = self.run_python('-m', 'auto_orchestrator.cli', command, str(fixture))
                self.assertEqual(result.returncode, 0, result.stderr)
                findings, _ = json.JSONDecoder().raw_decode(result.stdout)
                self.assertIn(rule, {finding['rule_id'] for finding in findings})
                self.assertEqual(fixture.read_text(encoding='utf-8'), source)

    def test_review_fix_command(self):
        fixture = self.directory / 'sample.py'
        fixture.write_text('x = 1   ', encoding='utf-8')
        result = self.run_python('-m', 'auto_orchestrator.cli', '/code-review', str(fixture), '-fix')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Applied safe formatting fixes to 1 file(s).', result.stdout)
        self.assertEqual(fixture.read_text(encoding='utf-8'), 'x = 1\n')

    def test_invalid_command(self):
        result = self.run_python('-m', 'auto_orchestrator.cli', 'invalid-command')
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid choice', result.stderr)
