# Agents

## Architecture
The core package is framework-independent Python. Domain tools implement deterministic inventory operations and expose contracts through the registry. Adapters translate external framework-shaped calls into the same portable execution contract.

## Development Rules
Keep domain logic in `core/`, contracts in `contracts/`, adapters in `adapters/`, and declarative OpenGAP tool definitions in `tools/`. Avoid framework imports in the core agent.

## Testing Rules
Run `pytest -q` from the repository root. Tests cover validation, deterministic calculations, registry behavior, documentation structure, adapter boundaries, and security-related configuration behavior.

## Portability
OpenAI SDK, CrewAI, Claude Code, and Lyzr adapters expose the same portable invocation boundary. Their framework packages are intentionally not required for the core test suite; adapter tests verify translation and execution semantics only.
