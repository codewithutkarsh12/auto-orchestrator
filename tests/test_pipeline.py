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

def _fail(task, context):
    raise RuntimeError("simulated prerequisite failure")


def test_failed_prerequisite_blocks_dependent_execution():
    called = []
    registry = SkillRegistry()
    registry.register(Skill("failing", "Fails", ["fail"], runner=_fail))
    registry.register(Skill("dependent", "Dependent", ["write"],
                            runner=lambda task, ctx: called.append(task) or "unexpected"))
    tasks = [Task("first", "fail", ("fail",)),
             Task("second", "write", ("write",), ("first",))]

    executions, context = ExecutionPipeline(registry, SkillRouter(registry)).execute(tasks)

    assert [item.status for item in executions] == ["failed", "skipped"]
    assert executions[1].skill_name is None
    assert "first" in executions[1].error
    assert "failed" in executions[1].error
    assert called == []
    assert "second" not in context


def test_skipped_prerequisite_blocks_dependent_execution():
    called = []
    registry = SkillRegistry()
    registry.register(Skill("dependent", "Dependent", ["write"],
                            runner=lambda task, ctx: called.append(task) or "unexpected"))
    tasks = [Task("missing", "unknown", ("not-registered",)),
             Task("dependent", "write", ("write",), ("missing",))]

    executions, context = ExecutionPipeline(registry, SkillRouter(registry)).execute(tasks)

    assert [item.status for item in executions] == ["skipped", "skipped"]
    assert "missing" in executions[1].error
    assert "skipped" in executions[1].error
    assert called == []
    assert context == {}


def test_transitive_failure_blocks_downstream_tasks():
    called = []
    registry = SkillRegistry()
    registry.register(Skill("failing", "Fails", ["fail"], runner=_fail))
    registry.register(Skill("dependent", "Dependent", ["write"],
                            runner=lambda task, ctx: called.append(task) or "unexpected"))
    tasks = [Task("a", "fail", ("fail",)),
             Task("b", "write", ("write",), ("a",)),
             Task("c", "write", ("write",), ("b",))]

    executions, context = ExecutionPipeline(registry, SkillRouter(registry)).execute(tasks)

    assert [item.status for item in executions] == ["failed", "skipped", "skipped"]
    assert "b" in executions[2].error
    assert called == []
    assert context == {}


def test_independent_tasks_continue_after_failure():
    called = []
    registry = SkillRegistry()
    registry.register(Skill("failing", "Fails", ["fail"], runner=_fail))
    registry.register(Skill("writer", "Writes", ["write"],
                            runner=lambda task, ctx: called.append(task) or "done"))
    tasks = [Task("a", "fail", ("fail",)),
             Task("independent", "write", ("write",)),
             Task("blocked", "write", ("write",), ("a",))]

    executions, context = ExecutionPipeline(registry, SkillRouter(registry)).execute(tasks)

    assert [item.status for item in executions] == ["failed", "success", "skipped"]
    assert called == ["write"]
    assert context == {"independent": "done"}


def test_successful_prerequisite_allows_dependent_execution():
    registry = SkillRegistry()
    registry.register(Skill("writer", "Writes", ["write"],
                            runner=lambda task, ctx: "first-output" if not ctx else ctx["a"] + "-second"))
    tasks = [Task("b", "write", ("write",), ("a",)),
             Task("a", "write", ("write",))]

    executions, context = ExecutionPipeline(registry, SkillRouter(registry)).execute(tasks)

    assert [(item.task_id, item.status) for item in executions] == [
        ("a", "success"), ("b", "success")]
    assert context["b"] == "first-output-second"


def test_multiple_prerequisites_block_if_any_failed():
    called = []
    registry = SkillRegistry()
    registry.register(Skill("writer", "Writes", ["write"],
                            runner=lambda task, ctx: called.append(task) or "done"))
    registry.register(Skill("failing", "Fails", ["fail"], runner=_fail))
    tasks = [Task("a", "write", ("write",)),
             Task("b", "fail", ("fail",)),
             Task("c", "write", ("write",), ("a", "b"))]

    executions, context = ExecutionPipeline(registry, SkillRouter(registry)).execute(tasks)

    assert [item.status for item in executions] == ["success", "failed", "skipped"]
    assert "b" in executions[2].error
    assert called == ["write"]
    assert "c" not in context


def test_multiple_successful_prerequisites_allow_execution():
    registry = SkillRegistry()
    registry.register(Skill("writer", "Writes", ["write"],
                            runner=lambda task, ctx: task))
    tasks = [Task("a", "one", ("write",)),
             Task("b", "two", ("write",)),
             Task("c", "three", ("write",), ("a", "b"))]

    executions, context = ExecutionPipeline(registry, SkillRouter(registry)).execute(tasks)

    assert [item.status for item in executions] == ["success"] * 3
    assert context["c"] == "three"
