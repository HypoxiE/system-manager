import types
from typing import Any, Callable

class Unit:
    def __init__(self):
        self._level: dict[Any, Any]= {}

    def unpack(self) -> dict[Any, Any]:
        result: dict[Any, Any] = {}
        for key, unit in self._level.items():
            if isinstance(unit, Unit):
                result[key] = unit.unpack()
            else:
                result[key] = unit
        return result

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._level[name] = value

    def __getattr__(self, name):
        if not name in self._level.keys():
            self._level[name] = Unit()
        
        return self._level[name]


class Configuration:
    def __init__(self, path: str, creator_func: Callable[[dict[Any, Any]], str]):
        self._config = Unit()
        self._path: str = path
        self._creator = creator_func

    def __str__(self):
        return self._creator({})

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            setattr(self._config, name, value)

    def __getattr__(self, name):
        return getattr(self._config, name)

    def unpack(self) -> dict[str, int | float | str | bool | dict]:
        return self._config.unpack()

    def __str__(self):
        return self._creator(self.unpack())

    def write(self):
        with open(self._path, "w") as file:
            file.write(str(self))

