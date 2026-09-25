from pathlib import Path
import re
import sys

REQUIRED = (
    "README.md",
    "specs/master-specification.md",
    "requirements/master-feature-matrix.md",
    "docs/handbook/00-handbook-overview.md",
    "implementation/README.md",
)

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED if not (root / p).is_file()]
    errors = [f"missing required file: {p}" for p in missing]

    for markdown in root.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "<")):
                continue
            candidate = (markdown.parent / target).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{markdown.relative_to(root)}: link escapes repository: {target}")
                continue
            if not candidate.exists():
                errors.append(f"{markdown.relative_to(root)}: broken link: {target}")

    if errors:
        print("repository validation: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1
    print("repository validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
