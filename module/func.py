"""
# This is a module for bilibili video download.
"""
# from Crypto.Cipher import AES
import base64
import inspect
import json
import os

# import copy
import pprint
import re
import subprocess

# import time
import sys

# from module import ua
from random import choice

import requests

from module.ua import ua

sysLog = sys.stdout


def printf(*args, sep=" ", end="\n"):
    """
    Like the function `print()`.
    I write it to do this:
    >>> printf("My life")
    My life
    >>> sysLog = open("log.log", "a")
    >>> printf("HI")
    In the file 'log.log':
    EOF;
    >>> printf("MY PRINT FUNCTION")
    In the file 'log.log':
    EOF;
    >>> sysLog.close()
    In the file 'log.log':
    HI
    MY PRINT FUNCTION
    EOF;
    """
    ret = ""
    for i in args[0:-1]:
        ret += str(i)
        ret += sep
    ret += str(args[-1])
    ret += end
    sysLog.write(ret)


class SetErr(Exception):

    def __init__(self, message):
        self.message = message


class Setting(object):
    set = {}

    # @overload
    def __init__(self,
                 filename,
                 name=None,
                 value=None,
                 mode="a",
                 isFormat=True):
        """
        setting `self.filename`, `self.text`, `self.mode`
        and setting self.setting
        """
        # 由于open函数不可以又读又写
        # 所以需要有一个读的对象以及一个写的对象
        self.filename = filename
        self.mode = mode
        self.isFormat = isFormat
        if not os.path.exists(filename):
            open(filename, "w").close()
        self.io_r = open(filename, "r")  # io_r指read的io
        self.text = self.io_r.read()
        self.io_r.close()
        self.io = open(filename, self.mode)
        if self.text == "":
            return
        self.set = json.loads(self.text)
        if name is not None:
            # 初始化设置
            for i in range(len(name)):
                self.set.get(name[i], value[i])

    def __getitem__(self, text):
        return self.set[text]

    def __setitem__(self, text, value):
        self.set[text] = value

    def __delitem__(self, text):
        del self.set[text]

    def save(self):
        """
        save the dictionary in your file
        >>> a = Setting(".json")
        >>> a["l"] = 10
        >>> a.getKey()
        ["l"]
        >>> a.save()
        >>> with open(".json") as f:
        >>>     text = f.read()
        >>> text
        '''{
            "l": 10
        }'''
        >>> a["q"] = 20
        >>> with open(".json") as f:
        >>>     text = f.read()
        >>> text
        '''{
            "l": 10,
            "q": 20
        }'''
        >>> a.getKey()
        ["l", "q"]
        """
        if self.isFormat:
            string: str = json.dumps(self.set, sort_keys=True, indent=4)
        else:
            string: str = json.dumps(self.set)
        with open(self.filename, "w") as f:
            f.write(string)
        self.io = open(self.filename, self.mode)
        with open(self.filename) as f:
            self.text: str = f.read()

    def saveEnd(self):
        """
        Just save the pswList, and close the file.
        """
        # 用完就挂了,慎用
        if self.isFormat:
            s = json.dumps(self.set, sort_keys=True, indent=4)
        else:
            s = json.dumps(self.set)
        with open(self.filename, "w") as f:
            f.write(s)

    def set_dict(self, name, value):
        """
        :params `name`: a list of dict's key
        :params `value`: a list of dict's value
        :params `return`: none
        **this function will not save**
        **if len(name) != len(value), func will raise Error**
        """
        # 设置字典
        if len(name) != len(value):
            raise ValueError(
                f"The 'name' and 'value' must be the same length.")
        for i in range(len(value)):
            self.set[name[i]] = value[i]

    def append(self, dict):
        """
        :params `dict`: a dict you will append to the pswList
        """
        # 链接一个字典
        for i in dict:
            self.set[i] = dict[i]

    def __len__(self):
        """
        :return the length of self.setting
        """
        return len(self.set)

    def change(self, name, value):
        """
        change a value in self.setting
        if it's not exists, it will be created
        """
        self.set[name] = value

    def get(self, name, default=None):
        """
        by dictionary's `get` function
        """
        return self.set.get(name, default)

    def clear(self):
        """
        clear all values and keys in self.setting
        won't save
        """
        self.set.clear()

    def delete(self, name):
        """
        delete a pair of value and key in self.setting
        """
        del self.set[name]

    def memset(self, value):
        """
        like `memset` function in c++, but it will only setting all values, not keys
        """
        for i in self.set:
            self.set[i] = value

    def print(self):
        """
        print all values and keys in self.setting
        """
        pprint.pprint(self.set)

    def isExists(self, key, val=None):
        a = key in self.getKey()
        if val is None:
            return a
        else:
            return a or self.set[key] == val

    def getKey(self):
        ret = list(self.set)
        return ret

    def getValue(self):
        ret = [self.set[i] for i in self.set]
        return ret

    def refresh(self):
        self.io_r = open(self.filename, "r")  # io_r指read的io
        self.text = self.io_r.read()
        self.io_r.close()
        self.io = open(self.filename, self.mode)
        if self.text == "":
            return
        self.set = json.loads(self.text)

    def close(self):
        self.io.close()
        self.io_r.close()

    def init(self, key: list, value: list):
        for i in range(len(key)):
            if key[i] not in self.getKey():
                self.set[key[i]] = value[i]
        self.save()

    def init_(self, dic):
        for i in dic:
            if i not in self.set:
                self.set[i] = dic[i]
        self.save()

    def __del__(self):
        self.close()
        # del self.text
        # del self.io, self.io_r
        # del self.set
        del self


if 1:
    # The av 2 bv function is from https://github.com/SocialSisterYi/bilibili-API-collect
    table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"  # 码表
    tr = {}  # 反查码表
    # 初始化反查码表
    for i in range(58):
        tr[table[i]] = i
    s = [11, 10, 3, 8, 4, 6]  # 位置编码表
    xor = 177451812  # 固定异或值
    add = 8728348608  # 固定加法值


def bv2av(x: str):
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58**i
    return (r - add) ^ xor


def av2bv(x):
    if type(x) == type(" "):
        x = int(x[2:])
    x = (x ^ xor) + add
    r = list("BV1  4 1 7  ")
    for i in range(6):
        r[s[i]] = table[x // 58**i % 58]
    return "".join(r)


if 1:
    # end from
    # 变量提前定义
    path = os.getcwd()
    os.chdir(path)
    header = {"user-agent": choice(ua)}
    # 变量提前定义
    # header['cookie'] = get_cookie()\

    qxd = {
        "240P": 6,
        "360P": 16,
        "480P": 32,
        "720P": 64,
        "720P60": 74,
        "1080P": 80,
        "1080P+": 112,
        "1080P60": 116,
        "4K": 120,
    }
    setting = {}
    setting["qxd"] = qxd["1080P"]
    sess = requests.session()


class DownloadErr(Exception):

    def __init__(self, message):
        self.message = message


def get_bv_from_url(text):
    pattern = re.compile(r"https://www.bilibili.com/video/(.+)?\?.*")
    bv = re.findall(pattern, text)
    printf(bv)
    return bv[0]


# get_bv_from_url('https://www.bilibili.com/video/BV1K5411S7UM?spm_id_from=333.851.b_7265636f6d6d656e64.6')
"""
检测登录状态
https://api.bilibili.com/x/web-interface/nav
"""


def get_user_info(headers):

    class LoginError(Exception):

        def __init__(self, message):
            self.message = message

    url = "https://api.bilibili.com/x/web-interface/nav"
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"
    response.raise_for_status()
    resp = response.json()
    # if not resp['data']['isLogin']:
    #     raise LoginError('isLogin is False')
    return response.text


# def get_cid(bv, headers):
#     if bv[:2].lower() == 'av':
#         bv = av2bv(bv)
#     __url = "https://api.bilibili.com/x/web-interface/view"
#     data = {
#         'bvid': bv,
#     }
#     resp = requests.get(__url, headers=headers, params=data)
#     resp.encoding = 'utf-8'
#     resp.raise_for_status()
#     json_response = resp.json()
#     return_text = []
#     # print(json_response)
#     for i in json_response['data']['pages']:
#         return_text.append(i['cid'])
#     return return_text


def get_cid(bv, headers):
    __url = "https://api.bilibili.com/x/web-interface/view"
    data = {
        "bvid": bv,
    }
    resp = requests.get(__url, headers=headers, params=data, timeout=10)
    resp.encoding = "utf-8"
    resp.raise_for_status()
    json_response = resp.json()
    return_text = []
    # print(json_response)
    try:
        for i in json_response["data"]["pages"]:
            return_text.append(i["cid"])
    except:
        return_text.append(json_response["data"]["cid"])
    return return_text


def get_video_info(bv, headers):
    if bv[:2].lower() == "av":
        bv = av2bv(bv)

    cidlist = get_cid(bv, headers)
    if len(cidlist) == 1:
        cid = cidlist[0]
        _url = "http://api.bilibili.com/x/player/playurl"
        _params = {
            "bvid": bv,
            "cid": cid,
            "fnval": "16",
        }
        session = sess
        try:
            response = session.get(_url,
                                   params=_params,
                                   headers=headers,
                                   timeout=10)
        except requests.exceptions.ConnectionError as ce:
            raise DownloadErr(f"错误：{ce}")
        response.encoding = "utf-8"
        response.raise_for_status()
        resp = response.json()
        return resp
    else:
        cid1 = cidlist
        retlist = []
        for cid in cid1:
            _url = "http://api.bilibili.com/x/player/playurl"
            _params = {
                "bvid": bv,
                "cid": cid,
                "fnval": "16",
            }
            session = sess
            response = session.get(_url,
                                   params=_params,
                                   headers=headers,
                                   timeout=10)
            response.encoding = "utf-8"
            response.raise_for_status()
            resp = response.json()
            retlist.append(resp)
        return retlist


def get_video_title_or_desc(bv, headers):
    if bv[:2].lower() == "av":
        bv = av2bv(bv)
    url = "https://api.bilibili.com/x/web-interface/view"
    data = {
        "bvid": bv,
    }
    resp = requests.get(url, headers=headers, params=data, timeout=10)
    resp.encoding = "utf-8"
    resp.raise_for_status()
    json_response = resp.json()
    return {
        "title": json_response["data"]["title"],
        "desc": json_response["data"]["desc"],
    }


def download(json, bv, page=1, name=None) -> dict:
    """
    ## download a video from BiliBili
    use `aria2c` to download
    """
    if bv[:2].lower() == "av":
        bv = av2bv(bv)
    if name is None:
        name = bv
    name.replace("\\", "")
    name.replace("/", "")
    ds = f"""{path}\\bin\\aria2c -s 32 --dir=.\\temp\\ -D -o "{name}.m4s" "{json}" --referer=https://www.bilibili.com/video/{bv}?p={page}"""
    # subprocess.call(ds)
    return {"filename": name + ".m4s", "name": name, "cmd": ds}


def download_music(json, bv, page=1, name=None) -> dict:
    """
    ## download music from bilibili
    use `aria2c` to download
    """
    if bv[:2].lower() == "av":
        bv = av2bv(bv)
    if name is None:
        name = bv
    name.replace("\\", "")
    name.replace("/", "")
    ds = rf"""{path}\bin\aria2c -s 32 --dir=.\temp\ -D -o "{name}.mp3" "{json}" --referer=https://www.bilibili.com/video/{bv}?p={page}"""
    # subprocess.call(ds)
    return {"filename": name + ".mp3", "name": name, "cmd": ds}


def clean(filename: str) -> None:
    subprocess.call(f'del "{path}\\temp\\{filename}"', shell=True)


def makedirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def download_video(bv, headers, page=1, isLog=True, path="."):
    makedirs(os.path.join(path, "video"))
    if bv[:2].lower() == "av":
        bv = av2bv(bv)
    try:
        if isLog:
            printf("获取视频信息")
        json1 = get_video_info(bv, headers)
    except KeyError:
        return 1
    a = ""
    list1 = []
    # try:
    #     for i in range(1, page):
    #         list1.append(download(json[i], bv, i))
    # except:
    #     a = download(json, bv, page)
    try:
        if type(json1) == type([1, 2, 3]):
            # url = json1[0]['data']['dash']['video'][0]['baseUrl']
            # for i in json1:
            # 远程主机未响应
            # 咋加一个批量化这么难呢？
            url = json1[0]["data"]["dash"]["video"][0]["baseUrl"]
            title = get_video_title_or_desc(bv, headers=headers)["title"]
            title = title.replace("/", "").replace("\\", "")
            if isLog:
                printf("下载视频部分")
            a = download(url, bv, page, name=title)
            subprocess.call(a["cmd"])
            url = json1[0]["data"]["dash"]["audio"][0]["baseUrl"]
            if isLog:
                printf("下载音频部分")
            b = download_music(url, bv, page, name=title)
            subprocess.call(b["cmd"])
        else:
            url = json1["data"]["dash"]["video"][0]["baseUrl"]
            title = get_video_title_or_desc(bv, headers=headers)["title"]
            if isLog:
                printf("下载视频部分")
            a = download(url, bv, page, name=title)
            subprocess.call(a["cmd"])
            b = None
            try:
                url = json1["data"]["dash"]["audio"][0]["baseUrl"]
                if isLog:
                    printf("下载音频部分")
                b = download_music(url, bv, page, name=title)
                subprocess.call(b["cmd"])
            except KeyError:
                process = subprocess.call(
                    f"bin\\ffmpeg -y -i \"temp\\{a['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\"",
                    shell=True,
                )
                clean(a["filename"])
                return {
                    "video":
                    a,
                    "music":
                    b,
                    "cmd":
                    f"bin\\ffmpeg -y -i \"temp\\{a['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\"",
                }
                # 删除临时文件
    except:
        with open("../test.json", "w") as f:
            json.dump(json1, f)
        return 1
    # 调用ffmpeg
    # 输入命令像这样: ffmpeg -y -i  D:\\ffmpeg_test\\1.webm  -r 30  D:\\ffmpeg_test\\1.mp4
    # 这里就是将1.webm的视频转成每秒30帧的视频1.mp4。这里指定1.mp4的绝对路径，如果不指定的话则生成的视频文件会落到当前ffmpeg命令的执行目录下。
    # 以上语句来自https://cloud.tencent.com/developer/article/1877108
    process = subprocess.call(
        f"bin\\ffmpeg -y -i \"temp\\{a['filename']}\" -i \"temp\\{b['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\"",
        shell=True,
    )
    # 删除临时文件
    clean(a["filename"])
    clean(b["filename"])
    return {
        "video":
        a,
        "music":
        b,
        "cmd":
        f"bin\\ffmpeg -y -i \"temp\\{a['filename']}\" -i \"temp\\{b['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\"",
    }


def downloadWithJson(json, header, page=None):
    """
    if page is None, download all
    download from get_video_info(bv, headers)
    """
    if page is None:
        for i in json:
            pass
            # TODO: 完成多视频解析


def kill() -> None:
    """
    # taskill杀进程
    """
    subprocess.call(f"taskkill /F /PID aria2c.exe")
    subprocess.call(f"taskkill /F /PID ffmpeg.exe")


def search(keywords, headers, pages=0):
    ret = []
    s = Setting("../setting.json", mode="r")
    if pages == 0:
        for i in range(1, s["mostSearch"] + 1):
            data = {"keyword": keywords, "page": i}
            res = requests.get(
                "http://api.bilibili.com/x/web-interface/search/all/v2",
                headers=headers,
                params=data,
                timeout=10,
            )
            try:
                res.raise_for_status()
            except:
                return ret
            js = res.json()
            try:
                data = js["data"]["result"][10]["data"]
            except:
                return 1
            for i in range(len(data)):
                temp = {}
                temp["title"] = data[i]["title"]
                temp["bvid"] = data[i]["bvid"]
                temp["author"] = data[i]["author"]
                ret.append(temp)
        return ret
    else:
        data = {"keyword": keywords, "page": pages}
        res = requests.get(
            "http://api.bilibili.com/x/web-interface/search/all/v2",
            headers=headers,
            params=data,
            timeout=10,
        )
        try:
            res.raise_for_status()
        except:
            return ret
        js = res.json()
        try:
            data = js["data"]["result"][10]["data"]
        except:
            return 1
        for i in range(len(data)):
            temp = {}
            temp["title"] = data[i]["title"]
            temp["bvid"] = data[i]["bvid"]
            temp["author"] = data[i]["author"]
            ret.append(temp)
        return ret


def getSearchAdvice(key):
    _url = "http://s.search.bilibili.com/main/suggest"
    data = {"term": key}
    resp = requests.get(_url, params=data, timeout=10)
    resp.encoding = "utf-8"
    return resp.json()


def get_count(id, ua):
    headers = ua
    url = "https://api.bilibili.com/x/space/arc/search"
    resp = requests.get(url, headers=headers, params={"mid": id}, timeout=10)
    count = resp.json()["data"]["page"]["count"]
    resp.close()
    return count


def getUsrPage(id, ua):
    return int(get_count(id, ua) / 50) + 1


def get_usr_video(id, ua, pages=None):
    """
    # 获取用户视频
    调用接口：https://api.bilibili.com/x/space/arc/search
    传入参数：
    mid: 用户ID，纯数字
    user-agent: UA(好像不加也行，但还是加一下)
    """
    headers = ua
    url = "https://api.bilibili.com/x/space/arc/search"

    try:
        if pages is None:

            def get_count(id, ua):
                headers = ua
                url = "https://api.bilibili.com/x/space/arc/search"
                resp = requests.get(url,
                                    headers=headers,
                                    params={"mid": id},
                                    timeout=10)
                count = resp.json()["data"]["page"]["count"]
                resp.close()
                return count

            count = get_count(id, ua)
            if count <= 50:
                data = {"mid": id, "ps": 50}
                resp = requests.get(url,
                                    headers=headers,
                                    params=data,
                                    timeout=10)
                json1 = resp.json()["data"]["list"]["vlist"]
                ret = [{
                    "bvid": i["bvid"],
                    "title": i["title"],
                    "author": i["author"],
                    "desc": i["description"],
                } for i in json1]
                return ret
            else:
                ret = []
                p = int(count / 50) + 1
                for i in range(p):
                    data = {"mid": id, "ps": 50, "pn": i + 1}
                    resp = requests.get(url,
                                        headers=headers,
                                        params=data,
                                        timeout=10)
                    resp.encoding = "utf-8"
                    json1 = resp.json()["data"]["list"]["vlist"]
                    ret += [{
                        "bvid": i["bvid"],
                        "title": i["title"],
                        "author": i["author"],
                        "desc": i["description"],
                    } for i in json1]
                return ret
        else:
            ret = []
            data = {"mid": id, "ps": 50, "pn": pages + 1}
            resp = requests.get(url, headers=headers, params=data, timeout=10)
            resp.encoding = "utf-8"
            json1 = resp.json()["data"]["list"]["vlist"]
            ret += [{
                "bvid": i["bvid"],
                "title": i["title"],
                "author": i["author"],
                "desc": i["description"],
            } for i in json1]
            return ret
    except:
        sys.stderr.write("ERR: 哔哩哔哩发现力(悲)")


def get_usr_pic(id):
    url = "http://api.bilibili.com/x/space/acc/info"
    data = {"mid": id}
    headers = {
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47 "
    }
    resp = requests.get(url, headers=headers, params=data, timeout=10)
    json1 = resp.json()["data"]
    url = json1["face"]
    rsp = requests.get(url)
    return (rsp, json1["name"])


def ip_get():
    """
    由bilibili提供的测ip服务
    """
    resp = requests.get("http://api.bilibili.com/x/web-interface/zone",
                        timeout=10)
    resp = resp.json()
    return resp["data"]


def get_usr_mid(bv, header):
    _url = "http://api.bilibili.com/x/web-interface/view"
    rsp = requests.get(_url, params={"bvid": bv}, headers=header, timeout=10)
    json1 = rsp.json()
    return json1["data"]["owner"]["mid"]


def analysis(string: str):
    """
    A function to analysis a str
    >>> analysis("1, 2, 3-5")
    [1, 2, 3, 4, 5]
    >>> analysis("5-10")
    [5, 6, 7, 8, 9, 10]
    >>> analysis("3, 2, 1, 1, 10-15")
    [1, 2, 3, 10, 11, 12, 13, 14, 15]
    """
    # Delete space char
    wait = string.replace(" ", "").split(",")
    ret = []  # a list
    for i in wait:
        if "-" not in i:
            # like "1"
            ret.append(int(i))
        else:
            # like "1-5"
            a, b = i.split("-")
            a = int(a)
            b = int(b)
            ret += list(range(a, b + 1))
    # make it unique and sorted
    ret = list(set(ret))
    return ret


class Save:
    """
    由json提供的Save
    """

    def __init__(self, filename, ifGetNot=None):
        self.string = None
        self.dict = {}
        self.filename = filename
        self.re = re.compile(r"([a-zA-Z0-9_]+?):(?: *?)(.*?)")
        self.ifGetNot = ifGetNot

    def load(self):
        with open(self.filename, "w") as f:
            text = f.read()
        self.analysis(text)

    def analysis(self, text):
        self.dict = json.loads(text)

    def dump(self, dictionary, filename):
        self.dict = dictionary
        with open(filename, "w") as f:
            self.string = json.dumps(dictionary, sort_keys=True, indent=4)
            f.write(self.string)

    def __getitem__(self, text):
        return self.dict.get(text, self.ifGetNot)


# test
# download_video('BV1et411b73Z', headers=header)
