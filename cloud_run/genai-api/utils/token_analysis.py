from services.gemini import GeminiClient

# Pricing per 1M tokens (approximate, check current pricing)
# https://cloud.google.com/vertex-ai/generative-ai/pricing
PRICING = {
    "gemini-2.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
}

CONTEXT_WINDOWS = {
    "gemini-2.5-flash": 1_000_000,
    "gemini-2.0-flash": 1_000_000,
}


def analyze_prompt(prompt: str, model_name: str = "gemini-2.5-flash") -> dict:
    """Analyze a prompt for token usage and cost."""
    gemini_client = GeminiClient()
    token_count = gemini_client.count_tokens(prompt, model_name)

    pricing = PRICING.get(model_name, PRICING["gemini-2.5-flash"])
    estimated_cost = (token_count / 1_000_000) * pricing["input"]

    context_window = CONTEXT_WINDOWS.get(model_name, 1_000_000)
    context_usage = (token_count / context_window) * 100

    warnings = []
    if context_usage > 80:
        warnings.append("Approaching context limit (>80%)")
    if context_usage > 95:
        warnings.append("Critical: Very close to context limit (>95%)")

    return {
        "token_count": token_count,
        "estimated_cost_usd": round(estimated_cost, 6),
        "context_usage_percent": round(context_usage, 2),
        "warnings": warnings,
    }
