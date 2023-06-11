import requests as r
import json
# import wget
import subprocess as sub
from module.func import Setting

s = Setting(filename="SETTING\\files.json")


def get():
    resp = r.get("http://154.12.55.235:10289/gx.json")
    resp.encoding = "utf-8"
    v = resp.json()
    return v


def package():
    rsp = r.get("http://154.12.55.235:10289/requirements.txt")
    with open("requirements.txt", "w") as f:
        f.write(rsp.text)
    for i in rsp.text.split("\n"):
        if i:
            sub.Popen(f"pip install {i}")
    print("安装完成")


def ifgx(jsonfile):
    v = jsonfile[0]["version"]
    with open("SETTING/setting.json", encoding="utf-8") as f:
        j = json.loads(f.read())
    v1 = j["version"]
    a = []
    for i in jsonfile:
        a += [i["intro"]]
    if v > v1:
        return True, a
    return False, a


def buque():
    """ 补全文件 """
    import os
    for k in s.set:
        i = s.set[k]
        if not os.path.exists(i["place"]):
            # wget.download(i["URL"], i["place"])
            a = sub.Popen(f"curl {i['URL']} -o {i['saveas']}")
            print(f"缺少{k}, 下载中...")
            a.wait()
            exec(i["code"])
            print("已下载", i["place"])


def main():
    m = ifgx(get())
    if m[0]:
        print("已是最新版")
    buque()
    package()


if __name__ == '__main__':
    main()
