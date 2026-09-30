---
name: reorder-planning
description: Calculate deterministic replenishment quantities from current stock, reorder point, and target stock.
compatibility: Framework-independent; uses the reorder-calculation tool.
metadata:
  version: "1.0.0"
  category: inventory
---
# Reorder Planning

## Purpose
Determine whether replenishment is required and calculate the quantity needed to reach target stock.

## Inputs
Provide a SKU and non-negative `on_hand`, `reorder_point`, and `target_stock` values.

## Behavior
The recommendation is `max(target_stock - on_hand, 0)`. The skill does not create or submit a purchase order.
