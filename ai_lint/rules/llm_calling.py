FORBIDDEN = [
    "openai.",
    "anthropic.",
]


def check(file, content):
    errors = []

    if "adapters/llm" in str(file):
        return errors  # разрешено

    for f in FORBIDDEN:
        if f in content:
            errors.append(
                f"{file}: прямой вызов LLM запрещён (используй LLMPort)"
            )

    return errors