# Inventory Management Agent

A framework-independent OpenGAP agent for deterministic inventory assessment, reorder planning, stock reconciliation, and inventory summaries.

## Capabilities
- Assess individual inventory records.
- Calculate reorder quantities from explicit reorder and target-stock parameters.
- Reconcile recorded and observed stock counts.
- Summarize inventory status across multiple records.

## Architecture
`core/` contains domain logic. `contracts/` contains framework-independent tool contracts. `tools/` contains OpenGAP/MCP-compatible declarative definitions. `adapters/` provides portable boundaries for OpenAI SDK, CrewAI, Claude Code, and Lyzr-shaped invocations. `verification/` contains local structural checks.

## Configuration
Runtime configuration is loaded from environment variables. Copy `.env.example` to `.env` for local use and provide `INVENTORY_AGENT_ENV`; secrets are not required by the deterministic core.

## Validation
Run `pytest -q`. The local suite validates the implementation and OpenGAP-oriented structural assumptions. The `opengap` CLI was not available in the build environment, so official CLI validation remains unverified.

The manifest targets OpenGAP specification version 0.1.0.
