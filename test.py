from main import *
from typing import Any
import json

try:
    from pydantic import validate_call
except:
    print("WARNING: pydantic cannot import \n")
    def validate_call(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

@validate_call
def json_template(inp: dict[str, Any]) -> str:
    return json.dumps(inp, indent=4, sort_keys=True)

@validate_call
def systemd_template(inp: dict[str, int | dict[str, int | str]]):
    result = ""
    for title, params in inp.items():
        result += f"\n[{title}]\n"
        for name, value in params.items():
            if isinstance(value, str | int):
                result += f"{name}={value}\n"
    return result

a = Configuration("./config.conf", json_template)
a.test = "qwerty"
a.ytre.tyer = "qwertt"
print(a)
# a.write()

a = Configuration("./config.conf", systemd_template)
a.Unit.Description = "My Custom Service"
a.Unit.After = "network.target"

a.Service.Type = "simple"
a.Service.User = "username"
a.Service.WorkingDirectory = "/home/username/myapp"
a.Service.ExecStart = "/usr/bin/python3 /home/username/myapp/script.py"
a.Service.Restart = "always"
a.Service.RestartSec = 5 

print(a)
a.write()



print("\n")
