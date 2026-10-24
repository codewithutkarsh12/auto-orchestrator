"""Skill metadata and the local callable contract."""
from dataclasses import dataclass, field
from typing import Callable

SkillRunner = Callable[[str, dict[str, str]], str]

@dataclass
class Skill:
    name: str
    description: str
    capabilities: list[str]
    runner: SkillRunner | None = None
    dependencies: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=list)
    risk: str = "low"
    max_context_chars: int = 4000
    version: str = "0.1.0"

    def run(self, task: str, context: dict[str, str]) -> str:
        if self.runner is None:
            return f"[Plan only] {self.name} matched task: {task}"
        result = self.runner(task, context)
        if not isinstance(result, str):
            raise TypeError(f"skill {self.name!r} must return a string")
        return result
