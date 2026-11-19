import pytest
from auto_orchestrator.models import Task
from auto_orchestrator.registry import SkillRegistry
from auto_orchestrator.router import SkillRouter
from auto_orchestrator.skills import Skill

def test_duplicate_skill_rejected():
    r = SkillRegistry(); s = Skill("writer", "Writes", ["write"])
    r.register(s)
    with pytest.raises(ValueError): r.register(s)

def test_router_matches_capability_and_respects_limit():
    r = SkillRegistry()
    for name in ("a", "b", "c"):
        r.register(Skill(name, "test", ["write"]))
    matches = SkillRouter(r, max_skills_per_batch=2).route(Task("1", "write this", ("write",)))
    assert len(matches) == 2

def test_permissions_filter_skills():
    r = SkillRegistry(); r.register(Skill("remote", "Remote", ["research"], permissions=["network"]))
    assert SkillRouter(r).route(Task("1", "research", ("research",))) == []
