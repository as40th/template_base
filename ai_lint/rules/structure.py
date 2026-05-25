def check(file, content):
    errors = []

    if "orchestrator" in str(file) and "decision" not in content:
        errors.append(
            f"{file}: отсутствует decision logic"
        )

    return errors