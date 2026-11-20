"""Capability-based skill routing."""
from .models import Task, SkillMatch
from .registry import SkillRegistry

class SkillRouter:
    def __init__(self, registry: SkillRegistry, max_skills_per_batch: int = 4,
                 granted_permissions: set[str] | None = None) -> None:
        if max_skills_per_batch < 1:
            raise ValueError("max_skills_per_batch must be >= 1")
        self.registry = registry
        self.max_skills_per_batch = max_skills_per_batch
        self.granted_permissions = granted_permissions or set()

    def route(self, task: Task) -> list[SkillMatch]:
        task_caps = {c.lower().strip() for c in task.capabilities}
        ranked: list[SkillMatch] = []
        for skill in self.registry.all():
            if not set(skill.permissions).issubset(self.granted_permissions):
                continue
            caps = {c.lower().strip() for c in skill.capabilities}
            matched = task_caps & caps
            words = set(task.description.lower().split())
            lexical = sum(1 for c in caps if c in words)
            score = (len(matched) * 2.0) + lexical
            if score > 0:
                ranked.append(SkillMatch(skill_name=skill.name, score=score,
                                      matched_capabilities=tuple(sorted(matched))))
        ranked.sort(key=lambda m: (-m.score, m.skill_name))
        return ranked[:self.max_skills_per_batch]
