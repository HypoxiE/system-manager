from main import *

import json
def json_template(inp: dict[str, any]) -> str:
    return json.dumps(inp, indent=4, sort_keys=True)

def systemd_template(inp: dict[str, str | int]):
    result = ""
    for title, params in inp.items():
        result += f"\n[{title}]\n"
        for name, value in params.items():
            if isinstance(value, str | int):
                result += f"{name}={value}\n"
    return result

#print(type(test_template))
a = Configuration("./config.conf", json_template)
#a.test = "qwerty"
#a.ytre.tyer = "qwertt"
#print(a)
#a.write()

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
