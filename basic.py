from auto_orchestrator import AutoOrchestrator, SkillRegistry, Skill

registry = SkillRegistry()
registry.register(Skill("writer", "Writes concise text", ["write"],
                      runner=lambda task, context: f"Draft plan for: {task}"))
result = AutoOrchestrator(registry).run("Write a project overview")
print(result.to_dict())
