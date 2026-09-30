from contracts.registry import ToolRegistry
from contracts.tool_contract import ToolContract
from core.inventory import assess_inventory, calculate_reorder, reconcile_stock, summarize_inventory


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ToolContract("inventory-status", "Assess a single inventory record.", {}, {}, assess_inventory))
    registry.register(ToolContract("reorder-calculation", "Calculate a deterministic reorder quantity.", {}, {}, lambda x: calculate_reorder(x.get("sku"), x.get("on_hand"), x.get("reorder_point"), x.get("target_stock"))))
    registry.register(ToolContract("stock-reconciliation", "Compare recorded and observed stock.", {}, {}, lambda x: reconcile_stock(x.get("recorded_quantity"), x.get("observed_quantity"))))
    registry.register(ToolContract("inventory-summary", "Summarize multiple inventory records.", {}, {}, lambda x: summarize_inventory(x.get("records"))))
    return registry
