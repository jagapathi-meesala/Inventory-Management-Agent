---
name: inventory-analysis
description: Assess supplied inventory records and classify stock status using explicit reorder thresholds.
compatibility: Framework-independent; uses the inventory-status tool.
metadata:
  version: "1.0.0"
  category: inventory
---
# Inventory Analysis

## Purpose
Classify each supplied inventory record as OUT_OF_STOCK, REORDER, or HEALTHY and calculate its deterministic recommended replenishment quantity.

## Inputs
Provide `sku`, `on_hand`, `reorder_point`, and `target_stock`.

## Behavior
Validate all quantities as non-negative numbers and require target_stock to be at least reorder_point. Return a structured result and report validation failures without changing the input values.
