"""Dependency-aware, local-only task execution pipeline."""
from .models import Task, TaskExecution
from .registry import SkillRegistry
from .router import SkillRouter
from .token_optimizer import TokenOptimizer

class ExecutionPipeline:
    def __init__(self, registry: SkillRegistry, router: SkillRouter,
                 optimizer: TokenOptimizer | None = None) -> None:
        self.registry = registry
        self.router = router
        self.optimizer = optimizer or TokenOptimizer()

    @staticmethod
    def order(tasks: list[Task]) -> list[Task]:
        by_id = {t.id: t for t in tasks}
        if len(by_id) != len(tasks):
            raise ValueError("task IDs must be unique")
        ordered: list[Task] = []
        visiting: set[str] = set()
        visited: set[str] = set()
        def visit(task_id: str) -> None:
            if task_id in visiting:
                raise ValueError("task dependency cycle detected")
            if task_id in visited:
                return
            if task_id not in by_id:
                raise ValueError(f"unknown dependency: {task_id}")
            visiting.add(task_id)
            for dep in by_id[task_id].depends_on:
                visit(dep)
            visiting.remove(task_id)
            visited.add(task_id)
            ordered.append(by_id[task_id])
        for task in tasks:
            visit(task.id)
        return ordered

    def execute(self, tasks: list[Task]) -> tuple[list[TaskExecution], dict[str, str]]:
        context: dict[str, str] = {}
        executions: list[TaskExecution] = []
        status_by_id: dict[str, str] = {}
        for task in self.order(tasks):
            blocked = [dep for dep in task.depends_on if status_by_id[dep] != "success"]
            if blocked:
                reason = ", ".join(f"{dep} ({status_by_id[dep]})" for dep in blocked)
                executions.append(TaskExecution(task.id, None, "skipped",
                                                error=f"Blocked by prerequisite(s): {reason}"))
                status_by_id[task.id] = "skipped"
                continue
            matches = self.router.route(task)
            if not matches:
                executions.append(TaskExecution(task.id, None, "skipped", error="No eligible skill"))
                status_by_id[task.id] = "skipped"
                continue
            skill = self.registry.get(matches[0].skill_name)
            assert skill is not None
            bounded_context = self.optimizer.trim(context)
            try:
                output = skill.run(task.description, bounded_context)
                output = output[:skill.max_context_chars]
                context[task.id] = output
                context = self.optimizer.trim(context)
                executions.append(TaskExecution(task.id, skill.name, "success", output,
                                             estimated_tokens=self.optimizer.estimate_tokens(output)))
                status_by_id[task.id] = "success"
            except Exception as exc:  # isolate a skill failure from the rest of the workflow
                executions.append(TaskExecution(task.id, skill.name, "failed", error=str(exc)))
                status_by_id[task.id] = "failed"
        return executions, context
