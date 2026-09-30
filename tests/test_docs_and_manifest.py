from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_and_references():
    manifest = yaml.safe_load((ROOT / "agent.yaml").read_text())
    assert manifest["spec_version"] == "0.1.0"
    assert manifest["name"] == "inventory-management-agent"
    assert re.fullmatch(r"[a-z][a-z0-9-]*", manifest["name"])
    assert re.fullmatch(r"\d+\.\d+\.\d+", str(manifest["version"]))
    assert set(manifest) <= {"spec_version", "name", "version", "description", "author", "license", "model", "extends", "dependencies", "skills", "tools", "agents", "delegation", "runtime", "a2a", "compliance", "tags", "metadata"}
    for skill in manifest["skills"]:
        assert (ROOT / "skills" / skill / "SKILL.md").exists()
    for tool in manifest["tools"]:
        assert (ROOT / "tools" / f"{tool}.yaml").exists()


def test_explainability_parser_safety():
    text = (ROOT / "EXPLAINABILITY.md").read_text()
    headings = re.findall(r"^## .+$", text, re.MULTILINE)
    assert headings[:3] == ["## Inputs and Data Sources", "## Decision and Reasoning", "## Limits and Constraints"]
    assert "\n## Inputs\n" not in text
    assert "\n## Decision\n" not in text
    assert "\n## Limits\n" not in text
    for heading in headings[:3]:
        start = text.index(heading) + len(heading)
        next_heading = text.find("\n## ", start)
        section = text[start: next_heading if next_heading != -1 else len(text)]
        sentences = re.findall(r"[^.!?]+[.!?]", section)
        assert len(sentences) >= 2


def test_required_files():
    required = ["agent.yaml", "SOUL.md", "AGENTS.md", "DUTIES.md", "RULES.md", "EXPLAINABILITY.md", ".env.example", ".gitignore", "README.md", "pytest.ini", "requirements.txt"]
    assert all((ROOT / name).exists() for name in required)
