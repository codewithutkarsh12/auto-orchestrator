# Token optimization

AUTO uses simple, provider-neutral controls to avoid loading unnecessary context.

## Current controls

- Task-level routing instead of loading every skill.
- `max_skills_per_batch` caps distinct skills selected in a routing batch.
- Skills can specify `max_context_chars`.
- `TokenOptimizer` estimates tokens and truncates context to a budget.
- Pipeline passes only prior task outputs, not full skill metadata.

## Limitations

The default estimate (`chars / 4`) is a rough heuristic. Tokenization varies by
model, language, and content. This project does not claim a fixed percentage of
savings. Measure actual provider usage when adding an LLM adapter.

## Recommended future metrics

- Prompt tokens / completion tokens per task
- Context dropped and retained
- Skills loaded / skills considered
- Routing precision and task success rate
- Cost per completed workflow
