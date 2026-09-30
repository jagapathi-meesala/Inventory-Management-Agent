---
name: stock-reconciliation
description: Compare recorded and observed inventory quantities and report deterministic variance.
compatibility: Framework-independent; uses the stock-reconciliation tool.
metadata:
  version: "1.0.0"
  category: inventory
---
# Stock Reconciliation

## Purpose
Identify differences between an inventory system's recorded quantity and a supplied physical observation.

## Inputs
Provide non-negative `recorded_quantity` and `observed_quantity` values.

## Behavior
Calculate variance as observed minus recorded. Return MATCH when variance is zero and MISMATCH otherwise.
