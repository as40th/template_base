REQUIRED = [
    "trace_id",
    "logger",
]


def check(file, content):
    errors = []

    if "orchestrator" in str(file):
        for r in REQUIRED:
            if r not in content:
                errors.append(
                    f"{file}: отсутствует observability ({r})"
                )

    return errors