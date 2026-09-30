import os
import pytest

from config.settings import ConfigurationError, load_settings
from core.agent import InventoryAgent
from core.inventory import ValidationError, assess_inventory, calculate_reorder, reconcile_stock, summarize_inventory
from contracts.registry import ToolRegistry
from contracts.tool_contract import ToolContract
from tools.runtime import build_registry
from adapters.registry import AdapterRegistry
from adapters.portable_adapter import PortableAdapter
from adapters.openai_adapter import openai_Adapter
from adapters.crewai_adapter import crewai_Adapter
from adapters.claude_code_adapter import claude_code_Adapter
from adapters.lyzr_adapter import lyzr_Adapter


def test_inventory_status():
    result = assess_inventory({"sku": "A", "on_hand": 10, "reorder_point": 10, "target_stock": 30})
    assert result["inventory_status"] == "REORDER"
    assert result["recommended_reorder"] == 20


def test_out_of_stock():
    assert assess_inventory({"sku": "A", "on_hand": 0, "reorder_point": 5, "target_stock": 10})["inventory_status"] == "OUT_OF_STOCK"


def test_healthy():
    assert assess_inventory({"sku": "A", "on_hand": 11, "reorder_point": 10, "target_stock": 30})["inventory_status"] == "HEALTHY"


def test_reorder_calculation():
    assert calculate_reorder("A", 20, 25, 60)["recommended_quantity"] == 40


def test_reorder_no_negative_quantity():
    assert calculate_reorder("A", 80, 25, 60)["recommended_quantity"] == 0


def test_invalid_negative_quantity():
    with pytest.raises(ValidationError):
        assess_inventory({"sku": "A", "on_hand": -1, "reorder_point": 5, "target_stock": 10})


def test_target_must_cover_reorder_point():
    with pytest.raises(ValidationError):
        assess_inventory({"sku": "A", "on_hand": 2, "reorder_point": 10, "target_stock": 5})


def test_reconciliation_match():
    assert reconcile_stock(10, 10)["reconciliation_status"] == "MATCH"


def test_reconciliation_mismatch():
    result = reconcile_stock(10, 7)
    assert result["variance"] == -3
    assert result["reconciliation_status"] == "MISMATCH"


def test_summary():
    result = summarize_inventory([
        {"sku": "A", "on_hand": 0, "reorder_point": 5, "target_stock": 10},
        {"sku": "B", "on_hand": 20, "reorder_point": 10, "target_stock": 30},
    ])
    assert result["record_count"] == 2
    assert result["status_counts"]["OUT_OF_STOCK"] == 1
    assert result["status_counts"]["HEALTHY"] == 1


def test_registry_discovery_and_execution():
    registry = build_registry()
    assert registry.discover() == ["inventory-status", "inventory-summary", "reorder-calculation", "stock-reconciliation"]
    result = registry.execute("inventory-status", {"sku": "A", "on_hand": 0, "reorder_point": 5, "target_stock": 10})
    assert result["status"] == "ok"


def test_registry_unknown_tool():
    assert build_registry().execute("missing", {})["status"] == "error"


def test_contract_rejects_non_object():
    contract = ToolContract("x", "test", {}, {}, lambda x: {"status": "ok"})
    assert contract.validate_and_execute([])["status"] == "error"


def test_agent_unknown_operation():
    assert InventoryAgent().run("missing", {})["status"] == "error"


def test_portable_adapters():
    for adapter in [openai_Adapter(), crewai_Adapter(), claude_code_Adapter(), lyzr_Adapter()]:
        result = adapter.invoke("stock-reconciliation", {"recorded_quantity": 5, "observed_quantity": 6})
        assert result["variance"] == 1


def test_adapter_registry():
    registry = AdapterRegistry()
    registry.register("openai", PortableAdapter())
    assert registry.names() == ["openai"]
    assert registry.get("openai").invoke("stock-reconciliation", {"recorded_quantity": 1, "observed_quantity": 1})["status"] == "ok"


def test_config_requires_environment(monkeypatch):
    monkeypatch.delenv("INVENTORY_AGENT_ENV", raising=False)
    with pytest.raises(ConfigurationError):
        load_settings()


def test_config_loads_environment(monkeypatch):
    monkeypatch.setenv("INVENTORY_AGENT_ENV", "test")
    assert load_settings()["environment"] == "test"
