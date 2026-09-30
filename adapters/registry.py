from adapters.portable_adapter import PortableAdapter


class AdapterRegistry:
    def __init__(self):
        self._adapters: dict[str, PortableAdapter] = {}

    def register(self, name: str, adapter: PortableAdapter) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("adapter name must be a non-empty string")
        self._adapters[name] = adapter

    def get(self, name: str) -> PortableAdapter:
        try:
            return self._adapters[name]
        except KeyError as exc:
            raise KeyError(f"adapter not registered: {name}") from exc

    def names(self) -> list[str]:
        return sorted(self._adapters)
