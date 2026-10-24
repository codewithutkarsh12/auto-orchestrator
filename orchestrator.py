"""Public AUTO orchestration facade."""
from .decomposer import PromptDecomposer
from .models import RunResult
from .pipeline import ExecutionPipeline
from .registry import SkillRegistry
from .router import SkillRouter
from .token_optimizer import TokenOptimizer

class AutoOrchestrator:
    def __init__(self, registry: SkillRegistry | None = None, max_skills_per_batch: int = 4,
                 token_budget: int = 2000, granted_permissions: set[str] | None = None) -> None:
        self.registry = registry or SkillRegistry()
        self.decomposer = PromptDecomposer()
        self.router = SkillRouter(self.registry, max_skills_per_batch, granted_permissions)
        self.pipeline = ExecutionPipeline(self.registry, self.router, TokenOptimizer(token_budget))

    def run(self, prompt: str) -> RunResult:
        tasks = self.decomposer.decompose(prompt)
        executions, context = self.pipeline.execute(tasks)
        return RunResult(prompt=prompt, tasks=tasks, executions=executions, context=context)
