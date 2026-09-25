from pathlib import Path
import sys

REQUIRED = (
    "README.md",
    "specs/master-specification.md",
    "requirements/master-feature-matrix.md",
    "docs/handbook/00-handbook-overview.md",
    "implementation/README.md",
)

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED if not (root / p).is_file()]
    if missing:
        print("Missing required repository files:")
        for item in missing:
            print(f" - {item}")
        return 1
    print("repository validation: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
