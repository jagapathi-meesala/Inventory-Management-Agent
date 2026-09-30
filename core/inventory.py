from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ValidationError(ValueError):
    pass


def _non_negative_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{field} must be a number")
    if value < 0:
        raise ValidationError(f"{field} must be non-negative")
    return float(value)


def _positive_number(value: Any, field: str) -> float:
    value = _non_negative_number(value, field)
    if value == 0:
        raise ValidationError(f"{field} must be greater than zero")
    return value


def validate_inventory_record(record: dict[str, Any]) -> None:
    if not isinstance(record, dict):
        raise ValidationError("record must be an object")
    sku = record.get("sku")
    if not isinstance(sku, str) or not sku.strip():
        raise ValidationError("sku must be a non-empty string")
    _non_negative_number(record.get("on_hand"), "on_hand")
    _non_negative_number(record.get("reorder_point"), "reorder_point")
    _non_negative_number(record.get("target_stock"), "target_stock")
    if record["target_stock"] < record["reorder_point"]:
        raise ValidationError("target_stock must be greater than or equal to reorder_point")


def assess_inventory(record: dict[str, Any]) -> dict[str, Any]:
    validate_inventory_record(record)
    on_hand = float(record["on_hand"])
    reorder_point = float(record["reorder_point"])
    target_stock = float(record["target_stock"])
    if on_hand == 0:
        status = "OUT_OF_STOCK"
    elif on_hand <= reorder_point:
        status = "REORDER"
    else:
        status = "HEALTHY"
    recommended = max(target_stock - on_hand, 0.0)
    return {
        "status": "ok",
        "sku": record["sku"],
        "inventory_status": status,
        "on_hand": on_hand,
        "reorder_point": reorder_point,
        "target_stock": target_stock,
        "recommended_reorder": recommended,
        "rule": "max(target_stock - on_hand, 0); status threshold uses reorder_point",
    }


def calculate_reorder(sku: str, on_hand: Any, reorder_point: Any, target_stock: Any) -> dict[str, Any]:
    record = {"sku": sku, "on_hand": on_hand, "reorder_point": reorder_point, "target_stock": target_stock}
    result = assess_inventory(record)
    return {
        "status": "ok",
        "sku": result["sku"],
        "reorder_required": result["inventory_status"] in {"OUT_OF_STOCK", "REORDER"},
        "recommended_quantity": result["recommended_reorder"],
        "inventory_status": result["inventory_status"],
    }


def reconcile_stock(recorded_quantity: Any, observed_quantity: Any) -> dict[str, Any]:
    recorded = _non_negative_number(recorded_quantity, "recorded_quantity")
    observed = _non_negative_number(observed_quantity, "observed_quantity")
    variance = observed - recorded
    return {
        "status": "ok",
        "recorded_quantity": recorded,
        "observed_quantity": observed,
        "variance": variance,
        "reconciliation_status": "MATCH" if variance == 0 else "MISMATCH",
    }


def summarize_inventory(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(records, list):
        raise ValidationError("records must be an array")
    assessed = [assess_inventory(record) for record in records]
    counts = {"OUT_OF_STOCK": 0, "REORDER": 0, "HEALTHY": 0}
    for item in assessed:
        counts[item["inventory_status"]] += 1
    return {
        "status": "ok",
        "record_count": len(assessed),
        "status_counts": counts,
        "total_on_hand": sum(item["on_hand"] for item in assessed),
        "total_recommended_reorder": sum(item["recommended_reorder"] for item in assessed),
        "items": assessed,
    }
