from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ToolContract:
    name: str
    purpose: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    execute: Callable[[dict[str, Any]], dict[str, Any]]

    def validate_and_execute(self, inputs: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(inputs, dict):
            return {"status": "error", "error": "inputs must be an object"}
        return self.execute(inputs)
