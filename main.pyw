from module.func import get_dic as getdic
from subprocess import call
from gx import main as bq
from module.func import ip_get

if __name__ == '__main__':
    print(ip_get())
    print("对项目进行补全中，请不要取消程序！！")
    bq()
    d = getdic("SETTING/setting.json", ["isPY", "whoToChoose"], mode=True)
    s, s1 = d['isPY'], d["whoToChoose"]
    if s:
        print(f"python.exe {s1 + '.py'}")
        call(f"python.exe {s1 + '.py'}")
    else:
        print(f"{s1 + '.exe'}")
        call(f"{s1 + '.exe'}")
