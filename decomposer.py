"""Simple, deterministic prompt decomposition baseline."""
import re
from .models import Task

_SPLIT = re.compile(r"\s+(?:and then|then|and|also|plus)\s+", re.IGNORECASE)


class PromptDecomposer:
    """Convert a prompt into lightweight tasks; replace with an LLM adapter later."""

    def decompose(self, prompt: str) -> list[Task]:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        chunks = [c.strip(" .;\n\t") for c in _SPLIT.split(prompt.strip()) if c.strip(" .;\n\t")]
        if not chunks:
            chunks = [prompt.strip()]
        tasks = []
        for i, chunk in enumerate(chunks, 1):
            low = chunk.lower()
            caps = []
            for keyword, capability in {
                "research": "research", "search": "research", "compare": "analyze",
                "analysis": "analyze", "analyze": "analyze", "summar": "summarize",
                "write": "write", "draft": "write", "plan": "plan", "code": "code",
                "implement": "code", "test": "test", "review": "review",
            }.items():
                if keyword in low and capability not in caps:
                    caps.append(capability)
            if not caps:
                caps = ["general"]
            tasks.append(Task(id=f"task-{i}", description=chunk, capabilities=tuple(caps),
                            depends_on=(f"task-{i-1}",) if i > 1 else ()))
        return tasks
