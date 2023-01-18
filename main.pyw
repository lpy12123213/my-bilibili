from module.func import Setting
from subprocess import call
s = Setting(filename="setting.json")
if s["isPY"]:
    print(f"python.exe {s['whoToChoose']+'.py'}")
    call(f"python.exe {s['whoToChoose']+'.py'}")
else:
    print(f"{s['whoToChoose'] + '.exe'}")
    call(f"{s['whoToChoose'] + '.exe'}")