from auto_orchestrator.review import code_review, security_review, apply_safe_fixes


def test_code_review_detects_eval(tmp_path):
    f = tmp_path / "unsafe.py"
    f.write_text("result = eval(user_input)\n", encoding="utf-8")
    assert "PY-EVAL" in {x.rule_id for x in code_review(tmp_path)}


def test_security_review_detects_shell_true(tmp_path):
    f = tmp_path / "unsafe.py"
    f.write_text("subprocess.run(cmd, shell=True)\n", encoding="utf-8")
    assert "SEC-SHELL-TRUE" in {x.rule_id for x in security_review(tmp_path)}


def test_fix_only_trailing_whitespace(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text("x = 1   ", encoding="utf-8")
    assert apply_safe_fixes(tmp_path) == 1
    assert f.read_text(encoding="utf-8") == "x = 1\n"
