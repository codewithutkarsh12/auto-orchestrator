# Architecture

## Pipeline

```text
User prompt
    │
    ▼
PromptDecomposer ──► Task list + dependencies
    │
    ▼
SkillRouter ──────► ranked skills (bounded batch)
    │
    ▼
ExecutionPipeline ─► TaskExecutor ─► structured task outputs
    │                    ▲
    ▼                    │
TokenOptimizer ── bounded prior outputs / prompt context
    │
    ▼
RunResult + trace
```

## Core modules

- **models.py**: immutable task, skill selection, execution record, and result types.
- **decomposer.py**: baseline deterministic decomposition. It splits common conjunctions and assigns dependencies; it is deliberately replaceable by a model adapter.
- **skills.py**: `Skill` metadata and callable contract. A skill's `run` function receives task input and bounded context and returns a string.
- **registry.py**: registration, duplicate detection, lookup, and metadata validation.
- **router.py**: capability overlap scoring, permission filtering, and maximum skills per batch.
- **pipeline.py**: topological task ordering, context passing, permission check, error capture.
- **token_optimizer.py**: conservative character-based token estimate and context trimming. The estimate is approximate, not tokenizer-exact.
- **orchestrator.py**: public façade.

## Skill model

A skill declares `name`, `description`, `capabilities`, optional `dependencies`, `permissions`, `risk`, and `max_context_chars`. The starter supports callable local skills. Remote packages and dynamic code loading are intentionally out of scope.

## Routing

Each task has normalized keywords. Each skill has capability labels. The router scores exact capability matches and lexical overlap, then filters skills whose required permissions are not granted. The router returns at most `max_skills_per_batch` distinct skills. This is a simple baseline; production deployments should evaluate relevance and false-positive rates against a test corpus.

## Execution

Tasks are executed in dependency order. Each task selects one routed skill. The task output is added to context only after passing the configured character budget. The baseline executor does not run shell commands, make network requests, or invoke MCP tools.

## Token optimization

Token count is estimated as `ceil(chars / chars_per_token)` and may differ from a provider tokenizer. Context is clipped to the configured budget, retaining the most recent output snippets. Production adapters should use the exact tokenizer for their model and record usage.

## Extending safely

1. Implement an adapter behind a narrow interface.
2. Declare permissions and external effects.
3. Validate input/output schemas.
4. Add tests for denial, malformed output, and failure behavior.
5. Require user approval before side-effecting operations.
