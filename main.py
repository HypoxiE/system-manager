import types
from typing import Callable, Union
from typing import get_type_hints, get_origin, get_args








from dataclasses import dataclass

@dataclass()
class UnionNode:
    child: "UnionNode"
    leafs: set


def expand_type(t):
    origin = get_origin(t)
    if origin is types.UnionType:
        res = UnionNode(None, set())
        for arg in get_args(t):
            orar = get_origin(arg)
            if orar is dict:
                res.child = expand_type(arg)
            else:
                res.leafs.add(expand_type(arg))
        return res
    if origin is dict:
        k_t, v_t = get_args(t)
        res = UnionNode(expand_type(v_t), set())
        return res

    return t.__name__

def infer_type(data):
    if isinstance(data, dict):
        key_types = set()
        value_types = set()

        for k, v in data.items():
            key_types.add(infer_type(k))
            value_types.add(infer_type(v))

        def union(types: set):
            result = types.pop()
            while len(types) != 0:
                result |= types.pop()
            return result

        key_type = key_types.pop() if len(key_types) == 1 else union(key_types)
        value_type = value_types.pop() if len(value_types) == 1 else union(value_types)

        return dict[key_type, value_type]
    return type(data)



class Unit:
    def __init__(self, child: UnionNode | None, leafs: UnionNode | str):
        self._child = child
        self._leafs = leafs

        self._level: dict[str, int | float | str | bool | "Unit"] = {}

    def unpack(self) -> dict[str, int | float | str | bool | dict]:
        result: dict[str, int | float | str | bool | dict] = {}
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
            if type(value).__name__ in self._leafs or 'any' in self._leafs:
                self._level[name] = value
            else:
                raise TypeError(f"You can use only this types: {self._leafs}, but {value} is {type(value)}")

    def __getattr__(self, name):
        if not name in self._level.keys():
            if self._child is not None: 
                self._level[name] = Unit(self._child.child, self._child.leafs)
            elif 'dict' in self._leafs or 'any' in self._leafs:
                self._level[name] = Unit(None, 'any')
            else:
                raise TypeError(f"Cannot create dict: {name}. Available only this types: {self._leafs}")
        
        return self._level[name]


class Configuration:
    def __init__(self, path: str, creator_func: Callable[[dict[str, any]], str]):
        creator_type = expand_type(get_type_hints(creator_func)["inp"])
        print(creator_type)
        self._config = Unit(creator_type.child, creator_type.leafs) if not creator_type == 'any' else Unit(None, 'any')
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
        hints = get_type_hints(self._creator)

        return self._creator(self.unpack())

    def write(self):
        with open(self._path, "w") as file:
            file.write(str(self))

