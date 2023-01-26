# 用bfs的方式获取搜索词汇
import json
import time

import requests as r
from queue import SimpleQueue
import threading as t


def getproxy(n=None):
    _url = "http://localhost:5555/random"
    text = r.get(_url).text
    if n is not None:
        text = n
    return {
        "http": f"http://{text}",
        "https": f"https://{text}"
    }


def get_advice(it):
    _url = "http://s.search.bilibili.com/main/suggest"
    b = r.get(
        _url,
        params={"term": it},
        headers={"user-agant": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46 "},
    )
    print(b.json())
    b.encoding = "utf-8"
    c = json.loads(b.text)
    b.close()
    ret = [c[i]["value"] for i in c]
    return ret


def BFS(start, deep=4):
    # BFS
    nowDeep = 1
    q = SimpleQueue()
    q.put_nowait(start)
    m = [start]
    while deep > nowDeep or not q.empty():
        now = q.get_nowait()
        for i in get_advice(now):
            q.put_nowait(i)
            m.append(i)
            m = list(set(m))
            with open("词典.txt", "a", encoding="utf-8") as f:
                f.write(', '.join(m))
            time.sleep(0.1)
        nowDeep += 1
    return list(set(m))


def find(start, end):
    # 暴搜, 依照Unicode码集全部搜索并存入文件
    # 不会数据库的痛惜
    for i in range(start, end + 1):
        with open("词典.txt", "a", encoding="utf-8") as f:
            a = get_advice(chr(i))
            print(a)
            if a != []:
                f.write(", ".join(a) + ", \n")
        print(i, chr(i))
        time.sleep(0.17)


if __name__ == "__main__":
    # already have run
    # 基本字符集
    # basic = t.Thread(target=find, args=(20756, 40869))
    # basic.start()
    # basic.join()
    # # 扩充A
    # A = t.Thread(target=find, args=(13312, 19893))
    # A.start()
    # A.join()
    # # 扩充B
    # B = t.Thread(target=find, args=(131072, 173782))
    # B.start()
    # B.join()
    # # 扩充C
    # C = t.Thread(target=find, args=(173824, 177972))
    # C.start()
    find(19968, 40869)
    find(13312, 19893)
    find(131072, 173782)
    find(173824, 177972)
