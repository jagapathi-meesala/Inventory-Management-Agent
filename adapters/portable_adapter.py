from typing import Any

from core.agent import InventoryAgent


class PortableAdapter:
    framework = "portable"

    def __init__(self, agent: InventoryAgent | None = None):
        self.agent = agent or InventoryAgent()

    def invoke(self, operation: str, inputs: dict[str, Any]) -> dict[str, Any]:
        return self.agent.run(operation, inputs)
