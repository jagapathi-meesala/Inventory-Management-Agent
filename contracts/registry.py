from contracts.tool_contract import ToolContract


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolContract] = {}

    def register(self, tool: ToolContract) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def discover(self) -> list[str]:
        return sorted(self._tools)

    def execute(self, name: str, inputs: dict) -> dict:
        if name not in self._tools:
            return {"status": "error", "error": f"tool not registered: {name}"}
        return self._tools[name].validate_and_execute(inputs)
