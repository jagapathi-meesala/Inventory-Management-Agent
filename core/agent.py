from typing import Any

from core.inventory import assess_inventory, calculate_reorder, reconcile_stock, summarize_inventory


class InventoryAgent:
    """Portable domain entry point with no LLM/framework dependency."""

    def run(self, operation: str, inputs: dict[str, Any]) -> dict[str, Any]:
        try:
            if operation == "inventory-status":
                return assess_inventory(inputs)
            if operation == "reorder-calculation":
                return calculate_reorder(
                    inputs.get("sku"), inputs.get("on_hand"), inputs.get("reorder_point"), inputs.get("target_stock")
                )
            if operation == "stock-reconciliation":
                return reconcile_stock(inputs.get("recorded_quantity"), inputs.get("observed_quantity"))
            if operation == "inventory-summary":
                return summarize_inventory(inputs.get("records"))
            return {"status": "error", "error": f"unknown operation: {operation}"}
        except (TypeError, ValueError) as exc:
            return {"status": "error", "error": str(exc)}
