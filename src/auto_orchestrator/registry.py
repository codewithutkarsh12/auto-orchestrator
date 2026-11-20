"""In-memory skill registry with conservative metadata validation."""
from .skills import Skill

class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        self.validate(skill)
        key = skill.name.strip().lower()
        if key in self._skills:
            raise ValueError(f"skill already registered: {skill.name}")
        self._skills[key] = skill

    @staticmethod
    def validate(skill: Skill) -> None:
        if not skill.name or not skill.name.strip():
            raise ValueError("skill name is required")
        if not skill.description or not skill.description.strip():
            raise ValueError("skill description is required")
        if not skill.capabilities or any(not c.strip() for c in skill.capabilities):
            raise ValueError("skill needs non-empty capabilities")
        if skill.risk not in {"low", "medium", "high"}:
            raise ValueError("risk must be low, medium, or high")
        if skill.max_context_chars < 0:
            raise ValueError("max_context_chars cannot be negative")

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name.strip().lower())

    def all(self) -> list[Skill]:
        return list(self._skills.values())

    def names(self) -> list[str]:
        return sorted(self._skills)
