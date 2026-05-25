FORBIDDEN = [
    "requests.get(",
    "requests.post(",
]


def check(file, content):
    errors = []

    if "adapters/tools" in str(file):
        return errors

    for f in FORBIDDEN:
        if f in content:
            errors.append(
                f"{file}: tool вызов вне ToolPort запрещён"
            )

    return errors