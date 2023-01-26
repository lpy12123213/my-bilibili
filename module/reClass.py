import re

reCompile = {
    "video": {
        "cmp":
        re.compile(
            r"(?:https|http)://www.bilibili.com/video/([^?/]+)\?(?:\?.*)?"),
        "page":
        -1,
    },
    "author": {
        "cmp":
        re.compile(r"(?:https|http)://space.bilibili.com/(\d+)\?(?:\?.*)?"),
        "page": 2,
    },
}

video = reCompile["video"]
author = reCompile["author"]
