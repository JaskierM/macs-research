from typing import Callable, Dict, Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):

    def __init__(self) -> None:
        self._map: Dict[str, T] = {}

    def register(self, name: str) -> Callable[[T], T]:

        def decorator(obj: T) -> T:
            if name in self._map:
                raise KeyError(f"{name!r} already registered.")
            self._map[name] = obj
            return obj

        return decorator

    def get(self, name: str) -> T:
        return self._map[name]

    def list(self) -> list[str]:
        return list(self._map.keys())

    def has(self, name: str) -> bool:
        return name in self._map
