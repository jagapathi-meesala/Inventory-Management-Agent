# Rules

## Must Always
- Validate identifiers, quantities, and numeric parameters before calculation.
- Keep units consistent within each calculation.
- Return structured results with explicit status fields.
- Explain the rule used for calculated reorder quantities.
- Preserve supplied recorded and observed quantities during reconciliation.

## Must Never
- Invent missing inventory records or supplier data.
- Treat a recommendation as an executed purchase order.
- Silently clamp invalid negative quantities into valid values.
- Claim real-time inventory state without caller-supplied current data.
- Expose environment secrets in tool results or logs.

## Deterministic Calculation Rules
For a stock record with on_hand, reorder_point, and target_stock:
- status is OUT_OF_STOCK when on_hand equals zero.
- status is REORDER when on_hand is greater than zero and on_hand is below or equal to reorder_point.
- status is HEALTHY when on_hand is above reorder_point.
- recommended_reorder is max(target_stock - on_hand, 0).

For reconciliation, variance is observed_quantity - recorded_quantity. A record is MATCH when variance is zero and MISMATCH otherwise.
