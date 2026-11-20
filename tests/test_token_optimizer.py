from auto_orchestrator.token_optimizer import TokenOptimizer

def test_estimate_and_trim_budget():
    opt = TokenOptimizer(max_tokens=2, chars_per_token=4)
    assert opt.estimate_tokens("12345678") == 2
    trimmed = opt.trim({"old": "abcdefgh", "new": "ijklmnop"})
    assert opt.estimate_tokens("".join(trimmed.values())) <= 2
    assert "new" in trimmed
