from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest = yaml.safe_load((ROOT / "agent.yaml").read_text())
    assert manifest["spec_version"] == "0.1.0"
    assert re.fullmatch(r"[a-z][a-z0-9-]*", manifest["name"])
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", str(manifest["version"]))
    for skill in manifest["skills"]:
        assert (ROOT / "skills" / skill / "SKILL.md").is_file(), skill
    for tool in manifest["tools"]:
        assert (ROOT / "tools" / f"{tool}.yaml").is_file(), tool
    text = (ROOT / "EXPLAINABILITY.md").read_text()
    headings = re.findall(r"^## .+$", text, flags=re.MULTILINE)
    required = ["## Inputs and Data Sources", "## Decision and Reasoning", "## Limits and Constraints"]
    assert headings[:3] == required
    for heading in required:
        assert heading in text
    assert "\n## Inputs\n" not in text
    assert "\n## Decision\n" not in text
    assert "\n## Limits\n" not in text
    print("Local structural audit passed")


if __name__ == "__main__":
    main()
