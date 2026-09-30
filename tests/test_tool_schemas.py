from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_tool_schema_shape():
    for path in (ROOT / "tools").glob("*.yaml"):
        data = yaml.safe_load(path.read_text())
        assert data["name"] == path.stem
        assert data["description"]
        assert data["version"]
        assert isinstance(data["input_schema"], dict)
        assert isinstance(data["output_schema"], dict)
        assert data["implementation"]["type"] == "script"
        assert data["implementation"]["path"] == "../core/inventory.py"
        assert data["implementation"]["runtime"] == "python3"
