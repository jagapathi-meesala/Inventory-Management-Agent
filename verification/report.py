from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

for path in sorted(ROOT.rglob("*")):
    if path.is_file() and ".git" not in path.parts:
        print(path.relative_to(ROOT))
