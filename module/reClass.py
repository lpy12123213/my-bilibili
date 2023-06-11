import re

reCompile = {
    'video': {"cmp": re.compile(r'(?:https|http)://www.bilibili.com/video/([^?/]+)\?(?:\?.*)?'), "page": -1},
    'author': {"cmp": re.compile(r'(?:https|http)://space.bilibili.com/(\d+)\?(?:\?.*)?'), "page": 2},
    'videobyb23': {"cmp": re.compile(r"(?:https|http|)://"), "page": ...}
}

video = reCompile['video']
author = reCompile['author']
