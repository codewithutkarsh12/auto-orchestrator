"""Provider-neutral context and token-budget helpers."""
from math import ceil

class TokenOptimizer:
    def __init__(self, max_tokens: int = 2000, chars_per_token: float = 4.0) -> None:
        if max_tokens < 1 or chars_per_token <= 0:
            raise ValueError("token budget and chars_per_token must be positive")
        self.max_tokens = max_tokens
        self.chars_per_token = chars_per_token

    def estimate_tokens(self, text: str) -> int:
        return ceil(len(text) / self.chars_per_token)

    def trim(self, context: dict[str, str]) -> dict[str, str]:
        """Retain newest context first, clipping to the budget; estimate is approximate."""
        remaining = self.max_tokens
        output: dict[str, str] = {}
        for key, value in reversed(list(context.items())):
            if remaining <= 0:
                break
            allowed_chars = int(remaining * self.chars_per_token)
            clipped = value[-allowed_chars:] if len(value) > allowed_chars else value
            used = self.estimate_tokens(clipped)
            if used:
                output[key] = clipped
                remaining -= used
        return dict(reversed(list(output.items())))
