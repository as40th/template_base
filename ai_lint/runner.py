import pathlib
from rules import llm_usage, tools_usage, structure, observability

RULES = [
    llm_usage.check,
    tools_usage.check,
    structure.check,
    observability.check,
]


def run_lint(root: str):
    root_path = pathlib.Path(root)
    errors = []

    for file in root_path.rglob("*.py"):
        content = file.read_text()

        for rule in RULES:
            result = rule(file, content)
            errors.extend(result)

    return errors


if __name__ == "__main__":
    errors = run_lint(".")

    if errors:
        for e in errors:
            print(f"[ERROR] {e}")
        exit(1)
    else:
        print("AI Runtime Contract: OK")