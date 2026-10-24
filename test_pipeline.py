import pytest
from auto_orchestrator.models import Task
from auto_orchestrator.pipeline import ExecutionPipeline
from auto_orchestrator.registry import SkillRegistry
from auto_orchestrator.router import SkillRouter
from auto_orchestrator.skills import Skill

def test_pipeline_runs_and_passes_context():
    r = SkillRegistry()
    r.register(Skill("writer", "Writes", ["write"], runner=lambda task, ctx: "done"))
    p = ExecutionPipeline(r, SkillRouter(r))
    executions, context = p.execute([Task("t1", "write", ("write",))])
    assert executions[0].status == "success"
    assert context["t1"] == "done"

def test_dependency_cycle_rejected():
    r = SkillRegistry(); r.register(Skill("s", "general", ["general"]))
    p = ExecutionPipeline(r, SkillRouter(r))
    with pytest.raises(ValueError):
        p.execute([Task("a", "a", ("general",), ("b",)), Task("b", "b", ("general",), ("a",))])
