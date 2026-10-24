"""Typed data models used by AUTO's orchestration pipeline."""
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Task:
    id: str
    description: str
    capabilities: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True)
class SkillMatch:
    skill_name: str
    score: float
    matched_capabilities: tuple[str, ...] = ()


@dataclass
class TaskExecution:
    task_id: str
    skill_name: str | None
    status: str
    output: str = ""
    error: str | None = None
    estimated_tokens: int = 0


@dataclass
class RunResult:
    prompt: str
    tasks: list[Task]
    executions: list[TaskExecution]
    context: dict[str, str] = field(default_factory=dict)

    @property
    def succeeded(self) -> bool:
        return all(item.status == "success" for item in self.executions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt": self.prompt,
            "tasks": [{"id": t.id, "description": t.description,
                       "capabilities": list(t.capabilities), "depends_on": list(t.depends_on)} for t in self.tasks],
            "executions": [vars(e) for e in self.executions],
            "context": self.context,
            "succeeded": self.succeeded,
        }
