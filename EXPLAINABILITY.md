# Explainability

## Inputs and Data Sources
The agent accepts structured inventory records supplied directly by the caller, including SKU identifiers, on-hand quantities, reorder points, and target stock levels. Reconciliation inputs contain recorded and observed quantities, while summary operations consume a list of the same validated inventory records; no external data source is silently queried.

## Decision and Reasoning
Inventory status is determined deterministically: zero on-hand stock is `OUT_OF_STOCK`, positive stock at or below the reorder point is `REORDER`, and stock above the reorder point is `HEALTHY`. Recommended replenishment is calculated as `max(target_stock - on_hand, 0)`, while reconciliation variance is `observed_quantity - recorded_quantity` and a zero variance produces `MATCH`.

## Limits and Constraints
The agent depends on the caller to provide current and accurate inventory data, and it does not establish real-time warehouse state by itself. It does not execute purchases, modify external systems, infer demand forecasts, or silently repair invalid inputs; invalid records are returned as structured errors.

## Agent Purpose
The agent provides repeatable inventory calculations and structured operational recommendations. Its results are intended to support inventory review rather than replace purchasing authorization or warehouse controls.

## Input Mechanisms
Inputs arrive as Python dictionaries through the framework-independent tool contract. OpenGAP tool definitions describe the corresponding object schemas so compatible runtimes can map their native calls to the same contract.

## Decision Mechanisms
The implementation uses explicit threshold comparisons and arithmetic rather than probabilistic model output. This makes the core calculations reproducible for identical inputs.

## Execution Limits
No network call, database mutation, purchase submission, or supplier lookup is performed by the deterministic core. The caller remains responsible for supplying authoritative inventory records and for taking any action based on a recommendation.

## Output Contract
Successful operations return `status: ok` plus operation-specific fields. Validation failures return `status: error` and a human-readable error message without exposing secrets or changing supplied records.

## Complete Execution Lifecycle
A caller selects a named operation, the registry locates the corresponding contract, the contract validates that the input is an object, and the domain function performs deeper field validation. The result is returned through the same portable adapter boundary regardless of which supported framework-shaped adapter invoked it.

## Tool-by-tool Behavior
### Inventory Status Tool
The inventory-status tool validates one inventory record and classifies its stock condition. It returns the original numeric inputs, the classification, and the deterministic recommended replenishment quantity.

### Reorder Calculation Tool
The reorder-calculation tool applies the same validated stock inputs but focuses its output on whether replenishment is required and how many units are recommended. It does not place an order or select a supplier.

### Stock Reconciliation Tool
The stock-reconciliation tool validates recorded and observed quantities and computes their difference. A zero difference is reported as MATCH; any non-zero difference is reported as MISMATCH.

### Inventory Summary Tool
The inventory-summary tool validates and assesses each supplied record, then aggregates counts, total on-hand units, and total recommended replenishment. One invalid record causes the operation to fail rather than being silently omitted.

## Tool Inputs
Each tool uses explicit named fields defined in its corresponding `tools/*.yaml` contract. Numeric quantities must be non-negative, SKU must be non-empty, and target stock must not be below the reorder point.

## Tool Validation
The Python domain layer performs runtime validation in addition to the declarative schemas. Validation errors are converted to structured error responses at the portable agent boundary.

## Tool Failure Behavior
Unknown operations and unregistered tools return structured error objects. Invalid values raise domain validation errors that are converted into `status: error` responses rather than producing partial calculations.

## Deterministic Rules
The status thresholds and replenishment formula are documented in RULES.md and implemented in `core/inventory.py`. No unstated threshold or hidden fallback is used by the deterministic core.

## Formulas
Recommended replenishment equals `max(target_stock - on_hand, 0)`. Reconciliation variance equals `observed_quantity - recorded_quantity`.

## Worked Examples
For SKU `SKU-001` with on-hand 20, reorder point 25, and target stock 60, the status is REORDER and the recommended quantity is 40. For recorded quantity 100 and observed quantity 97, variance is -3 and the reconciliation status is MISMATCH.

## Explainability of Calculated Results
Every calculated quantity can be reproduced from the input values and the formulas above. The result includes the relevant classification or variance so a caller can trace the output without hidden model reasoning.

## Provenance
The agent's inventory calculations are derived only from caller-supplied structured inputs and the deterministic rules implemented in this repository. No external source is represented as authoritative unless a future adapter explicitly supplies such data through the documented contract.
