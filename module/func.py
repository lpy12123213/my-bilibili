"""
# This is a module for bilibili video download.
"""
import json
# import time
import sys
import threading

import requests as request
import subprocess
import os
import re
# import copy
import pprint
import asyncio
from bilibili_api import video

try:
    from ua import ua
except:
    from module.ua import ua
# from module import ua
from random import choice

# from Crypto.Cipher import AES

sysLog = sys.stdout


def printf(*args, sep=' ', end='\n'):
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
    ret = ''
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
    def __init__(self, filename, name=None, value=None, mode='a', isFormat=True, encoding="utf-8"):
        """
        setting `self.filename`, `self.text`, `self.mode`
        and setting self.setting
        """
        # 由于open函数不可以又读又写
        # 所以需要有一个读的对象以及一个写的对象
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.isFormat = isFormat
        if not os.path.exists(filename):
            open(filename, 'w', encoding=encoding).close()
        self.io_r = open(filename, 'r', encoding=encoding)  # io_r指read的io
        self.text = self.io_r.read()
        self.io_r.close()
        self.io = open(filename, self.mode, encoding=encoding)
        if self.text == '':
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
        with open(self.filename, 'w') as f:
            f.write(string)
        self.io = open(self.filename, self.mode, encoding=self.encoding)
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
        with open(self.filename, "w", encoding=self.encoding) as f:
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
        ret = [i for i in self.set]
        return ret

    def getValue(self):
        ret = [self.set[i] for i in self.set]
        return ret

    def refresh(self):
        self.io_r = open(self.filename, 'r', encoding=self.encoding)  # io_r指read的io
        self.text = self.io_r.read()
        self.io_r.close()
        self.io = open(self.filename, self.mode, encoding=self.encoding)
        if self.text == '':
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


def get_dic(file, text, mode=False, encoding="utf-8"):
    # TEXT可以是str或int
    with open(file, encoding=encoding) as f:
        if not mode:
            return json.loads(f.read())[text]
        if mode:
            # text必须是一个可迭代对象
            d = {}
            dic = json.loads(f.read())
            for i in text:
                d[i] = dic[i]
            return d


if 1:
    # The av 2 bv function is from https://github.com/SocialSisterYi/bilibili-API-collect
    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'  # 码表
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
        r += tr[x[s[i]]] * 58 ** i
    return (r - add) ^ xor


def av2bv(x):
    if type(x) == type(' '):
        x = int(x[2:])
    x = (x ^ xor) + add
    r = list('BV1  4 1 7  ')
    for i in range(6):
        r[s[i]] = table[x // 58 ** i % 58]
    return ''.join(r)


if 1:
    # end from
    # 变量提前定义
    path = os.getcwd()
    os.chdir(path)
    header = {
        'user-agent': choice(ua)
    }
    # 变量提前定义
    # header['cookie'] = get_cookie()\

    qxd = {
        '240P': 6,
        '360P': 16,
        '480P': 32,
        '720P': 64,
        '720P60': 74,
        '1080P': 80,
        '1080P+': 112,
        '1080P60': 116,
        '4K': 120
    }
    setting = {}
    setting['qxd'] = qxd["1080P"]
    requests = request.session()
    requests.proxies = get_dic(".\\SETTING\\setting.json", "proxy")


class DownloadErr(Exception):
    def __init__(self, message):
        self.message = message


def get_bv_from_url(text):
    pattern = re.compile(r'https://www.bilibili.com/video/(.+)?\?.*')
    bv = re.findall(pattern, text)
    printf(bv)
    return bv[0]


# get_bv_from_url('https://www.bilibili.com/video/BV1K5411S7UM?spm_id_from=333.851.b_7265636f6d6d656e64.6')

'''
检测登录状态
https://api.bilibili.com/x/web-interface/nav
'''


def get_user_info(headers):
    class LoginError(Exception):
        def __init__(self, message):
            self.message = message

    url = 'https://api.bilibili.com/x/web-interface/nav'
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
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
        'bvid': bv,
    }
    resp = requests.get(__url, headers=headers, params=data, timeout=10)
    resp.encoding = 'utf-8'
    resp.raise_for_status()
    json_response = resp.json()
    return_text = []
    # print(json_response)
    try:
        for i in json_response['data']['pages']:
            return_text.append(i['cid'])
    except:
        return_text.append(json_response['data']['cid'])
    return return_text


def get_video_info(bv, headers):
    if bv[:2].lower() == 'av':
        bv = av2bv(bv)

    cidlist = get_cid(bv, headers)
    if len(cidlist) == 1:
        cid = cidlist[0]
        _url = 'http://api.bilibili.com/x/player/playurl'
        _params = {
            'bvid': bv,
            'cid': cid,
            'fnval': '16',
        }
        session = requests
        try:
            response = session.get(_url, params=_params, headers=headers, timeout=10)
        except requests.exceptions.ConnectionError as ce:
            raise DownloadErr(f"错误：{ce}")
        response.encoding = 'utf-8'
        response.raise_for_status()
        resp = response.json()
        return resp
    else:
        cid1 = cidlist
        retlist = []
        for cid in cid1:
            _url = 'http://api.bilibili.com/x/player/playurl'
            _params = {
                'bvid': bv,
                'cid': cid,
                'fnval': '16',
            }
            session = requests
            response = session.get(_url, params=_params, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
            resp = response.json()
            retlist.append(resp)
        return retlist


def get_video_title_or_desc(bv, headers):
    if bv[:2].lower() == 'av':
        bv = av2bv(bv)
    url = 'https://api.bilibili.com/x/web-interface/view'
    data = {
        'bvid': bv,
    }
    resp = requests.get(url, headers=headers, params=data, timeout=10)
    resp.encoding = 'utf-8'
    resp.raise_for_status()
    json_response = resp.json()
    return {'title': json_response['data']['title'], 'desc': json_response['data']['desc']}


def download(json, bv, page=1, name=None) -> dict:
    """
    ## download a video from BiliBili
    use `aria2c` to download
    """
    if bv[:2].lower() == 'av':
        bv = av2bv(bv)
    if name is None:
        name = bv
    name.replace("\\", "")
    name.replace("/", "")
    ds = f"""{path}\\bin\\aria2c -s 32 --dir=.\\temp\\ -D -o "{name}.m4s" "{json}" --referer=https://www.bilibili.com/video/{bv}?p={page}"""
    # subprocess.call(ds)
    return {'filename': name + '.m4s', 'name': name, 'cmd': ds}


def download_music(json, bv, page=1, name=None) -> dict:
    '''
    ## download music from bilibili
    use `aria2c` to download
    '''
    if bv[:2].lower() == 'av':
        bv = av2bv(bv)
    if name is None:
        name = bv
    name.replace("\\", "")
    name.replace("/", "")
    ds = fr"""{path}\bin\aria2c -s 32 --dir=.\temp\ -D -o "{name}.mp3" "{json}" --referer=https://www.bilibili.com/video/{bv}?p={page}"""
    # subprocess.call(ds)
    return {'filename': name + '.mp3', 'name': name, 'cmd': ds}


def clean(filename: str) -> None:
    subprocess.call(f"del \"{path}\\temp\\{filename}\"", shell=True)


def makedirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def download_video(bv, headers, page=1, is_log=True, path="."):
    video_dir = os.path.join(path, "video")
    os.makedirs(video_dir, exist_ok=True)

    if bv[:2].lower() == 'av':
        bv = av2bv(bv)

    try:
        if is_log:
            print("Getting video information...")
        video_info = get_video_info(bv, headers)
    except KeyError:
        return None

    video_url = None
    audio_url = None
    title = get_video_title_or_desc(bv, headers=headers)['title']
    title = title.replace("/", "").replace("\\", "")

    if isinstance(video_info, list):
        video_url = video_info[0]['data']['dash']['video'][0]['baseUrl']
        audio_url = video_info[0]['data']['dash']['audio'][0]['baseUrl']
    else:
        video_url = video_info['data']['dash']['video'][0]['baseUrl']
        try:
            audio_url = video_info['data']['dash']['audio'][0]['baseUrl']
        except KeyError:
            pass

    video_file = download(video_url, bv, page, name=title)
    subprocess.call(video_file['cmd'])

    if audio_url:
        audio_file = download_music(audio_url, bv, page, name=title)
        subprocess.call(audio_file['cmd'])
        cmd = f"bin\\ffmpeg -y -i \"temp\\{video_file['filename']}\" -i \"temp\\{audio_file['filename']}\" -c:v copy -c:a aac -strict experimental \"{video_dir}\\{video_file['name']}.mp4\""
    else:
        cmd = f"bin\\ffmpeg -y -i \"temp\\{video_file['filename']}\" -c:v copy -c:a aac -strict experimental \"{video_dir}\\{video_file['name']}.mp4\""

    subprocess.call(cmd, shell=True)
    clean(video_file['filename'])
    if audio_url:
        clean(audio_file['filename'])

    return {"video": video_file, "music": audio_file, "cmd": cmd}


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
    '''
    # taskill杀进程
    '''
    subprocess.call(f"taskkill /F /PID aria2c.exe")
    subprocess.call(f"taskkill /F /PID ffmpeg.exe")


def search(keywords, headers, pages=0):
    ret = []
    s = Setting('./SETTING/setting.json', mode='r')
    if pages == 0:
        for i in range(1, s['mostSearch'] + 1):
            data = {
                'keyword': keywords,
                "page": i
            }
            res = requests.get(
                "http://api.bilibili.com/x/web-interface/search/all/v2",
                headers=headers,
                params=data,
                timeout=10
            )
            try:
                res.raise_for_status()
            except:
                return ret
            js = res.json()
            try:
                data = js['data']['result'][10]['data']
            except:
                return 1
            for i in range(len(data)):
                temp = {'title': data[i]['title'], 'bvid': data[i]['bvid'], 'author': data[i]['author']}
                ret.append(temp)
        return ret
    else:
        data = {
            'keyword': keywords,
            "page": pages
        }
        res = requests.get(
            "http://api.bilibili.com/x/web-interface/search/all/v2",
            headers=headers,
            params=data,
            timeout=10
        )
        try:
            res.raise_for_status()
        except:
            return ret
        js = res.json()
        try:
            data = js['data']['result'][10]['data']
        except:
            return 1
        for i in range(len(data)):
            temp = {'title': data[i]['title'], 'bvid': data[i]['bvid'], 'author': data[i]['author']}
            ret.append(temp)
        return ret


def getSearchAdvice(key):
    _url = "https://s.search.bilibili.com/main/suggest"
    data = {
        "term": key
    }
    resp = requests.get(_url, params=data, timeout=10)
    resp.encoding = 'utf-8'
    return resp.json()


def get_count(id, ua):
    headers = ua
    url = 'https://api.bilibili.com/x/space/arc/search'
    resp = requests.get(url, headers=headers, params={'mid': id}, timeout=10)
    print(resp.text)
    count = resp.json()['data']['page']['count']
    resp.close()
    return count


def getUsrPage(id, ua):
    return int(get_count(id, ua) / 50) + 1


def get_usr_video(id, ua, pages=None):
    '''
    # 获取用户视频
    调用接口：https://api.bilibili.com/x/space/arc/search
    传入参数：
    mid: 用户ID，纯数字
    user-agent: UA(好像不加也行，但还是加一下)
    '''
    headers = ua
    url = 'https://api.bilibili.com/x/space/arc/search'

    try:
        if pages is None:
            def get_count(id, ua):
                headers = ua
                url = 'https://api.bilibili.com/x/space/arc/search'
                resp = requests.get(url, headers=headers, params={'mid': id}, timeout=10)
                count = resp.json()['data']['page']['count']
                resp.close()
                return count

            count = get_count(id, ua)
            if count <= 50:
                data = {
                    'mid': id,
                    'ps': 50
                }
                resp = requests.get(url, headers=headers, params=data, timeout=10)
                json1 = resp.json()['data']['list']['vlist']
                ret = [{'bvid': i['bvid'],
                        'title': i['title'],
                        'author': i['author'],
                        'desc': i['description']}
                       for i in json1
                       ]
                return ret
            else:
                ret = []
                p = int(count / 50) + 1
                for i in range(p):
                    data = {
                        'mid': id,
                        'ps': 50,
                        'pn': i + 1
                    }
                    resp = requests.get(url, headers=headers, params=data, timeout=10)
                    resp.encoding = "utf-8"
                    json1 = resp.json()['data']['list']['vlist']
                    ret += [{'bvid': i['bvid'],
                             'title': i['title'],
                             'author': i['author'],
                             'desc': i['description']}
                            for i in json1
                            ]
                return ret
        else:
            ret = []
            data = {
                'mid': id,
                'ps': 50,
                'pn': pages + 1
            }
            resp = requests.get(url, headers=headers, params=data, timeout=10)
            resp.encoding = "utf-8"
            json1 = resp.json()['data']['list']['vlist']
            ret += [{'bvid': i['bvid'],
                     'title': i['title'],
                     'author': i['author'],
                     'desc': i['description']}
                    for i in json1
                    ]
            return ret
    except:
        return {"ERR": "哔哩哔哩发现力(悲)"}


def get_usr_pic(id):
    url = 'http://api.bilibili.com/x/space/acc/info'
    data = {
        'mid': id
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47 '
    }
    resp = requests.get(url, headers=headers, params=data, timeout=10)
    json1 = resp.json()['data']
    url = json1['face']
    rsp = requests.get(url)
    return (rsp, json1['name'])


def ip_get():
    """
    由bilibili提供的测ip服务
    """
    resp = requests.get('http://api.bilibili.com/x/web-interface/zone', timeout=10)
    resp = resp.json()
    return resp['data']


def get_short_url(url):
    """
    Get short url of the video by https://xiaojuzi.fun/bili-short-url/.
    """
    url = f"https://service-ijd4slqi-1253419200.gz.apigw.tencentcs.com/release/short_url?url={url}&href=\
          https://xiaojuzi.fun/bili-short-url/"
    r = requests.get(url, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55"})
    js = r.json()
    return js["short_url"] if js["success"] else Exception("ERR!")


def get_usr_mid(bv, header):
    _url = 'http://api.bilibili.com/x/web-interface/view'
    rsp = requests.get(_url, params={'bvid': bv}, headers=header, timeout=10)
    json1 = rsp.json()
    return json1['data']['owner']['mid']


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
            ret += [j for j in range(a, b + 1)]
    # make it unique and sorted
    ret = list(set(ret))
    return ret


def likeVideo(bv, headers):
    _url = "http://api.bilibili.com/x/web-interface/archive/like"
    c = headers["cookie"].replace(" ", "").split(";")
    print(c)
    csrf = None
    for i in c:
        if "bili_jct" in i:
            csrf = i.split("=")[1]
            break
    params = {
        "like": 1,
        "csrf": csrf,
        "bvid": bv
    }
    print(csrf)
    r = requests.post(_url, headers=headers, params=params)
    print(r.text)


if 1:
    # From https://www.cnblogs.com/suwings/p/6216279.html
    class LoopException(Exception):
        """循环异常自定义异常，此异常并不代表循环每一次都是非正常退出的"""

        def __init__(self, msg="LoopException"):
            self._msg = msg

        def __str__(self):
            return self._msg


    class SwPipe:
        """
        与任意子进程通信管道类，可以进行管道交互通信
        """

        def __init__(self, commande, func, exitfunc, readyfunc=None,
                     shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, code="GBK"):
            """
            commande 命令
            func 正确输出反馈函数
            exitfunc 异常反馈函数
            readyfunc 当管道创建完毕时调用
            """
            self._thread = threading.Thread(target=self.__run, args=(commande, shell, stdin, stdout, stderr, readyfunc))
            self._code = code
            self._func = func
            self._exitfunc = exitfunc
            self._flag = False
            self._CRFL = "\r\n"

        def __run(self, commande, shell, stdin, stdout, stderr, readyfunc):
            """ 私有函数 """
            try:
                self._process = subprocess.Popen(
                    commande,
                    shell=shell,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=stderr
                )
            except OSError as e:
                self._exitfunc(e)
            self._flag = True
            if readyfunc != None:
                threading.Thread(target=readyfunc).start()  # 准备就绪
            while True:
                line = self._process.stdout.readline()
                if not line:
                    break
                try:
                    tmp = line.decode(self._code)
                except UnicodeDecodeError:
                    tmp = \
                        self._CRFL + "[PIPE_CODE_ERROR] <Code ERROR: UnicodeDecodeError>\n" \
                        + "[PIPE_CODE_ERROR] Now code is: " + self._code + self._CRFL
                self._func(self, tmp)

            self._flag = False
            self._exitfunc(LoopException("While Loop break"))  # 正常退出

        def write(self, msg):
            if self._flag:
                # 请注意一下这里的换行
                self._process.stdin.write((msg + self._CRFL).encode(self._code))
                self._process.stdin.flush()
                # sys.stdin.write(msg)#怎么说呢，无法直接用代码发送指令，只能默认的stdin
            else:
                raise LoopException("Shell pipe error from '_flag' not True!")  # 还未准备好就退出

        def start(self):
            """ 开始线程 """
            self._thread.start()

        def destroy(self):
            """ 停止并销毁自身 """
            self._process.stdout.close()
            self._thread.stop()
            del self


def printAndRet(*args, **kwargs):
    print(*args, **kwargs)
    return args


def mma(tex):
    """
    WolframAlpha爬取结果
    """
    # ToExpression["x^2 \\le 0", TeXForm, HoldForm]
    print(f"wolframscript -code \"ToExpression[\\\"{tex}\\\", TeXForm, HoldForm]\"")
    s = subprocess.Popen(f"wolframscript -code \"ToExpression[\\\"{tex}\\\", TeXForm, HoldForm]\"",
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return s.stdout.read()


def getmma(text):
    import re
    # 使用正则表达式提取HoldForm[]中中括号内容
    re = re.compile(r"HoldForm\[(.*?)\]")
    # 提取出来的内容
    s = re.findall(text)
    return s

# class Save:
#     """
#     由json提供的Save
#     """
#
#     def __init__(self, filename, ifGetNot=None):
#         self.string = None
#         self.dict = {}
#         self.filename = filename
#         self.re = re.compile(r"([a-zA-Z0-9_]+?): *?(.*?)")
#         self.ifGetNot = ifGetNot
#
#     def load(self):
#         with open(self.filename, 'w') as f:
#             text = f.read()
#         self.analysis(text)
#
#     def analysis(self, text):
#         self.dict = json.loads(text)
#
#     def dump(self, dictionary, filename):
#         self.dict = dictionary
#         with open(filename, "w") as f:
#             self.string = json.dumps(dictionary, sort_keys=True, indent=4)
#             f.write(self.string)
#
#     def __getitem__(self, text):
#         return self.dict.get(text, self.ifGetNot)

# test
# download_video('BV1et411b73Z', headers=header)
