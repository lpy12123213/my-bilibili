"""
# This is a module for bilibili video download.
"""
import json
# import time
import sys

import requests
import subprocess
import os
import re
# import copy
import pprint
# from . import ua
# import ua
# from module import ua
from random import choice
from Crypto.Cipher import AES
import base64
import inspect

ua = ["Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
      "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
      "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
      "Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
      "Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)",
      "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
      "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)",
      "Mozilla/5.0 ( ; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
      "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 7.1; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C)",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; AskTB5.5)",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.2; .NET4.0C; .NET4.0E)",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C)",
      "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; FDM; .NET CLR 1.1.4322; .NET4.0C; .NET4.0E; Tablet PC 2.0)",
      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)",
      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)",
      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 3.0.04506.30)",
      "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0; Trident/4.0; FBSMTWB; .NET CLR 2.0.34861; .NET CLR 3.0.3746.3218; .NET CLR 3.5.33652; msn OptimizedIE8;ENUS)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.3; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MS-RTC LM 8)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; msn OptimizedIE8;ZHCN)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; InfoPath.3; .NET4.0C; .NET4.0E) chromeframe/8.0.552.224",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E; Zune 4.7; InfoPath.3)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; .NET4.0C; .NET4.0E; Zune 4.7)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; Zune 4.0)",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; MS-RTC LM 8; Zune 4.7)",
      "Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
      "Mozilla/5.0 (X11; Linux x86_64; rv:2.2a1pre) Gecko/20100101 Firefox/4.2a1pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110323 Firefox/4.2a1pre",
      "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
      "Mozilla/5.0 (Windows NT 5.1; rv:2.0b9pre) Gecko/20110105 Firefox/4.0b9pre",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101213 Firefox/4.0b8pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101128 Firefox/4.0b8pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
      "Mozilla/5.0 (Windows NT 5.1; rv:2.0b8pre) Gecko/20101127 Firefox/4.0b8pre",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b8) Gecko/20100101 Firefox/4.0b8",
      "Mozilla/5.0 (Windows NT 6.1; rv:2.0b7pre) Gecko/20100921 Firefox/4.0b7pre",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20100101 Firefox/4.0b7",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b6pre) Gecko/20100903 Firefox/4.0b6pre",
      "Mozilla/5.0 (Windows NT 6.1; rv:2.0b6pre) Gecko/20100903 Firefox/4.0b6pre Firefox/4.0b6pre",
      "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4",
      "Mozilla/5.0 (X11; Linux i686; rv:2.0b3pre) Gecko/20100731 Firefox/4.0b3pre",
      "Mozilla/5.0 (Windows NT 5.2; rv:2.0b13pre) Gecko/20110304 Firefox/4.0b13pre",
      "Mozilla/5.0 (Windows NT 5.1; rv:2.0b13pre) Gecko/20110223 Firefox/4.0b13pre",
      "Mozilla/5.0 (X11; Linux i686; rv:2.0b12pre) Gecko/20110204 Firefox/4.0b12pre",
      "Mozilla/5.0 (X11; Linux i686; rv:2.0b12pre) Gecko/20100101 Firefox/4.0b12pre",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b11pre) Gecko/20110128 Firefox/4.0b11pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b11pre) Gecko/20110131 Firefox/4.0b11pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b11pre) Gecko/20110129 Firefox/4.0b11pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b11pre) Gecko/20110128 Firefox/4.0b11pre",
      "Mozilla/5.0 (Windows NT 6.1; rv:2.0b11pre) Gecko/20110126 Firefox/4.0b11pre",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b11pre) Gecko/20110126 Firefox/4.0b11pre",
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b10pre) Gecko/20110118 Firefox/4.0b10pre",
      "Mozilla/5.0 (Windows NT 6.1; rv:2.0b10pre) Gecko/20110113 Firefox/4.0b10pre",
      "Mozilla/5.0 (X11; Linux i686; rv:2.0b10) Gecko/20100101 Firefox/4.0b10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:2.0b10) Gecko/20110126 Firefox/4.0b10",
      "Mozilla/5.0 (Windows NT 6.1; rv:2.0b10) Gecko/20110126 Firefox/4.0b10",
      "Mozilla/5.0 (X11; U; Linux x86_64; pl-PL; rv:2.0) Gecko/20110307 Firefox/4.0",
      "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:2.0) Gecko/20110404 Fedora/16-dev Firefox/4.0",
      "Mozilla/5.0 (X11; Arch Linux i686; rv:2.0) Gecko/20110321 Firefox/4.0",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows NT 6.1; rv:2.0) Gecko/20110319 Firefox/4.0",
      "Mozilla/5.0 (Windows NT 6.1; rv:1.9) Gecko/20100101 Firefox/4.0",
      "Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/20121223 Ubuntu/9.25 (jaunty) Firefox/3.8",
      "Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.25 (jaunty) Firefox/3.8",
      "Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.25 (jaunty) Firefox/3.8",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.3) Gecko/20100401 Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.25 (jaunty) Firefox/3.8",
      "Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.3a5pre) Gecko/20100526 Firefox/3.7a5pre",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2b5) Gecko/20091204 Firefox/3.6b5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2b5) Gecko/20091204 Firefox/3.6b5",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.2b5) Gecko/20091204 Firefox/3.6b5",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2) Gecko/20091218 Firefox 3.6b5",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.2b4) Gecko/20091124 Firefox/3.6b4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2b4) Gecko/20091124 Firefox/3.6b4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2b1) Gecko/20091014 Firefox/3.6b1 GTB5",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2a1pre) Gecko/20090428 Firefox/3.6a1pre",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2a1pre) Gecko/20090405 Firefox/3.6a1pre",
      "Mozilla/5.0 (X11; U; Linux i686; ru-RU; rv:1.9.2a1pre) Gecko/20090405 Ubuntu/9.04 (jaunty) Firefox/3.6a1pre",
      "Mozilla/5.0 (Windows; Windows NT 5.1; es-ES; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre",
      "Mozilla/5.0 (Windows; Windows NT 5.1; en-US; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2a1pre) Gecko/20090402 Firefox/3.6a1pre (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.9) Gecko/20100915 Gentoo Firefox/3.6.9",
      "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.2.9) Gecko/20100913 Firefox/3.6.9",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9",
      "Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.9.2.8) Gecko/20101230 Firefox/3.6.8",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100723 SUSE/3.6.8-0.1.1 Firefox/3.6.8",
      "Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.2.8) Gecko/20100722 Ubuntu/10.04 (lucid) Firefox/3.6.8",
      "Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
      "Mozilla/5.0 (X11; U; Linux i686; fi-FI; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.8) Gecko/20100727 Firefox/3.6.8",
      "Mozilla/5.0 (X11; U; Linux i686; de-DE; rv:1.9.2.8) Gecko/20100725 Gentoo Firefox/3.6.8",
      "Mozilla/5.0 (X11; U; FreeBSD i386; de-CH; rv:1.9.2.8) Gecko/20100729 Firefox/3.6.8",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; pt-BR; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.2.8) Gecko/20100722 AskTbADAP/3.9.1.14019 Firefox/3.6.8",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; he; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.2.8) Gecko/20100722 Firefox 3.6.8 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0C)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.2.8) Gecko/20100722 Firefox 3.6.8",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.2.3) Gecko/20121221 Firefox/3.6.8",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-TW; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100723 Fedora/3.6.7-1.fc13 Firefox/3.6.7",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.7) Gecko/20100726 CentOS/3.6-3.el5.centos Firefox/3.6.7",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; hu; rv:1.9.2.7) Gecko/20100713 Firefox/3.6.7 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.7 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-PT; rv:1.9.2.7) Gecko/20100713 Firefox/3.6.7 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) Firefox/3.6.6 GTB7.1",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) Firefox/3.6.6 GTB7.0",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) Firefox/3.6.6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) Firefox/3.6.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; pt-PT; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; zh-CN; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; nl; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6 ( .NET CLR 3.5.30729; .NET4.0E)",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.4) Gecko/20100614 Ubuntu/10.04 (lucid) Firefox/3.6.4",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.4) Gecko/20100625 Gentoo Firefox/3.6.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-TW; rv:1.9.2.4) Gecko/20100611 Firefox/3.6.4 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.4) Gecko/20100513 Firefox/3.6.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ja; rv:1.9.2.4) Gecko/20100611 Firefox/3.6.4 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs; rv:1.9.2.4) Gecko/20100513 Firefox/3.6.4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; zh-CN; rv:1.9.2.4) Gecko/20100513 Firefox/3.6.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja; rv:1.9.2.4) Gecko/20100513 Firefox/3.6.4 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.4) Gecko/20100527 Firefox/3.6.4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.4) Gecko/20100527 Firefox/3.6.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.4) Gecko/20100513 Firefox/3.6.4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-CA; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW; rv:1.9.2.4) Gecko/20100611 Firefox/3.6.4 GTB7.0 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.4) Gecko/20100513 Firefox/3.6.4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.4) Gecko/20100503 Firefox/3.6.4 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; nb-NO; rv:1.9.2.4) Gecko/20100611 Firefox/3.6.4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ko; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.2.4) Gecko/20100611 Firefox/3.6.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3pre) Gecko/20100405 Firefox/3.6.3plugin1 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.2.3) Gecko/20100403 Fedora/3.6.3-4.fc13 Firefox/3.6.3",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.3) Gecko/20100403 Firefox/3.6.3",
      "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.3) Gecko/20100401 SUSE/3.6.3-1.1 Firefox/3.6.3",
      "Mozilla/5.0 (X11; U; Linux i686; ko-KR; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100404 Ubuntu/10.04 (lucid) Firefox/3.6.3",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 GTB7.1",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.3",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3",
      "Mozilla/5.0 (X11; U; Linux AMD64; en-US; rv:1.9.2.3) Gecko/20100403 Ubuntu/10.10 (maverick) Firefox/3.6.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; pl; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; hu; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 GTB7.0 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ca; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 GTB7.0",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.2) Gecko/20100316 AskTbSPC2/3.9.1.14019 Firefox/3.6.2",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; pl; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 GTB6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 ( .NET CLR 3.0.04506.648)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2 ( .NET CLR 3.0.04506.30)",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.7; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10pre) Gecko/20100902 Ubuntu/9.10 (karmic) Firefox/3.6.1pre",
      "Mozilla/5.0 (X11; U; Linux x86_64; ja-JP; rv:1.9.2.16) Gecko/20110323 Ubuntu/10.10 (maverick) Firefox/3.6.16",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.16) Gecko/20110323 Ubuntu/9.10 (karmic) Firefox/3.6.16 "
      "FirePHP/0.5",
      "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; pl; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ko; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16 ( .NET CLR 3.5.30729; .NET4.0E)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9.1.13) Gecko/20100914 Firefox/3.6.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.2.16) Gecko/20110319 AskTbUTR/3.11.3.15590 Firefox/3.6.16",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.16pre) Gecko/20110304 Ubuntu/10.10 (maverick) Firefox/3.6.15pre",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.15) Gecko/20110303 Ubuntu/10.04 (lucid) Firefox/3.6.15 FirePHP/0.5",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.15) Gecko/20110330 CentOS/3.6-1.el5.centos Firefox/3.6.15",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15 ( .NET CLR 3.5.30729; .NET4.0C) FirePHP/0.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.15) Gecko/20110303 AskTbBT4/3.11.3.15590 Firefox/3.6.15 ( .NET CLR 3.5.30729; .NET4.0C)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.14pre) Gecko/20110105 Firefox/3.6.14pre",
      "Mozilla/5.0 (X11; U; Linux armv7l; en-US; rv:1.9.2.14) Gecko/20110224 Firefox/3.6.14 MB860/Version.0.43.3.MB860.AmericaMovil.en.MX",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.14) Gecko/20110218 Firefox/3.6.14",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-AU; rv:1.9.2.14) Gecko/20110218 Firefox/3.6.14",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.2.14) Gecko/20110218 Firefox/3.6.14 GTB7.1 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.13) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; pl-PL; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; nb-NO; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; it; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.2.13) Gecko/20110103 Fedora/3.6.13-1.fc14 Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101223 Gentoo Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101219 Gentoo Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Red Hat/3.6-3.el4 Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-NZ; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.2.13) Gecko/20101206 Ubuntu/9.10 (karmic) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-GB; rv:1.9.2.13) Gecko/20101206 Red Hat/3.6-2.el5 Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; da-DK; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux MIPS32 1074Kf CPS QuadCore; en-US; rv:1.9.2.13) Gecko/20110103 Fedora/3.6.13-1.fc14 Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux i686; pt-BR; rv:1.9.2.13) Gecko/20101209 Fedora/3.6.13-1.fc13 Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux i686; es-ES; rv:1.9.2.13) Gecko/20101206 Ubuntu/9.10 (karmic) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.13) Gecko/20101209 CentOS/3.6-2.el5.centos Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13",
      "Mozilla/5.0 (X11; U; NetBSD i386; en-US; rv:1.9.2.12) Gecko/20101030 Firefox/3.6.12",
      "Mozilla/5.0 (X11; U; Linux x86_64; es-MX; rv:1.9.2.12) Gecko/20101027 Ubuntu/10.04 (lucid) Firefox/3.6.12",
      "Mozilla/5.0 (X11; U; Linux x86_64; es-ES; rv:1.9.2.12) Gecko/20101027 Fedora/3.6.12-1.fc13 Firefox/3.6.12",
      "Mozilla/5.0 (X11; U; Linux x86_64; es-ES; rv:1.9.2.12) Gecko/20101026 SUSE/3.6.12-0.7.1 Firefox/3.6.12",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.12) Gecko/20101102 Gentoo Firefox/3.6.12",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.12) Gecko/20101102 Firefox/3.6.12",
      "Mozilla/5.0 (X11; U; Linux ppc; fr; rv:1.9.2.12) Gecko/20101027 Ubuntu/10.10 (maverick) Firefox/3.6.12",
      "Mozilla/5.0 (X11; U; Linux i686; ko-KR; rv:1.9.2.12) Gecko/20101027 Ubuntu/10.10 (maverick) Firefox/3.6.12",
      "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.2.12) Gecko/20101027 Ubuntu/10.10 (maverick) Firefox/3.6.12 GTB7.1",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.12) Gecko/20101027 Fedora/3.6.12-1.fc13 Firefox/3.6.12",
      "Mozilla/5.0 (X11; FreeBSD x86_64; rv:2.0) Gecko/20100101 Firefox/3.6.12",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12 ( .NET CLR 3.5.30729; .NET4.0E)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; sv-SE; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12 (.NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; .NET CLR 3.5.21022)",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; de; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12 GTB5",
      "Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.2.11) Gecko/20101028 CentOS/3.6-2.el5.centos Firefox/3.6.11",
      "Mozilla/5.0 (X11; U; Linux armv7l; en-GB; rv:1.9.2.3pre) Gecko/20100723 Firefox/3.6.11",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; ru; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux x86_64; pt-BR; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux x86_64; pl-PL; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10 GTB7.1",
      "Mozilla/5.0 (X11; U; Linux x86_64; el-GR; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10 GTB7.1",
      "Mozilla/5.0 (X11; U; Linux x86_64; cs-CZ; rv:1.9.2.10) Gecko/20100915 Ubuntu/10.04 (lucid) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; pl-PL; rv:1.9.2.10) Gecko/20100915 Ubuntu/10.04 (lucid) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; fr-FR; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; es-AR; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100915 Ubuntu/9.04 (jaunty) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.2.11) Gecko/20101013 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; en-CA; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.10) Gecko/20100915 Ubuntu/9.10 (karmic) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.10) Gecko/20100915 Ubuntu/10.04 (lucid) Firefox/3.6.10",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.10) Gecko/20100914 SUSE/3.6.10-0.3.1 Firefox/3.6.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ro; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; nl; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.1) Gecko/20100122 firefox/3.6.1",
      "Mozilla/5.0(Windows; U; Windows NT 7.0; rv:1.9.2) Gecko/20100101 Firefox/3.6",
      "Mozilla/5.0(Windows; U; Windows NT 5.2; rv:1.9.2) Gecko/20100101 Firefox/3.6",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2) Gecko/20100222 Ubuntu/10.04 (lucid) Firefox/3.6",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2) Gecko/20100130 Gentoo Firefox/3.6",
      "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/20100312 Ubuntu/9.04 (jaunty) Firefox/3.6",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100128 Gentoo Firefox/3.6",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100115 Ubuntu/10.04 (lucid) Firefox/3.6",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 FirePHP/0.4",
      "Mozilla/5.0 (X11; Linux i686; rv:2.0) Gecko/20100101 Firefox/3.6",
      "Mozilla/5.0 (X11; FreeBSD i686) Firefox/3.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru-RU; rv:1.9.2) Gecko/20100105 MRA 5.6 (build 03278) Firefox/3.6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; lt; rv:1.9.2) Gecko/20100115 Firefox/3.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.3a3pre) Gecko/20100306 Firefox3.6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100806 Firefox/3.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.3) Gecko/20100401 Firefox/3.6;MEGAUPLOAD 1.0",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ar; rv:1.9.2) Gecko/20100115 Firefox/3.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.2) Gecko/20100115 Firefox/3.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.2) Gecko/20100105 Firefox/3.6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; pl; rv:1.9.2) Gecko/20100115 Firefox/3.6 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1b5pre) Gecko/20090517 Firefox/3.5b4pre (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1b4pre) Gecko/20090409 Firefox/3.5b4pre",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1b4pre) Gecko/20090401 Firefox/3.5b4pre",
      "Mozilla/5.0 (X11; U; Linux i686; nl-NL; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 GTB5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; fr; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b4) Gecko/20090423 Firefox/3.5b4 GTB5",
      "Mozilla/5.0 (X11; U; Linux x86_64; it; rv:1.9.1.9) Gecko/20100402 Ubuntu/9.10 (karmic) Firefox/3.5.9 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; it; rv:1.9.1.9) Gecko/20100330 Fedora/3.5.9-2.fc12 Firefox/3.5.9",
      "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.9) Gecko/20100317 SUSE/3.5.9-0.1.1 Firefox/3.5.9 GTB7.0",
      "Mozilla/5.0 (X11; U; Linux x86_64; es-CL; rv:1.9.1.9) Gecko/20100402 Ubuntu/9.10 (karmic) Firefox/3.5.9",
      "Mozilla/5.0 (X11; U; Linux x86_64; cs-CZ; rv:1.9.1.9) Gecko/20100317 SUSE/3.5.9-0.1.1 Firefox/3.5.9",
      "Mozilla/5.0 (X11; U; Linux i686; nl; rv:1.9.1.9) Gecko/20100401 Ubuntu/9.10 (karmic) Firefox/3.5.9",
      "Mozilla/5.0 (X11; U; Linux i686; hu-HU; rv:1.9.1.9) Gecko/20100330 Fedora/3.5.9-1.fc12 Firefox/3.5.9",
      "Mozilla/5.0 (X11; U; Linux i686; es-ES; rv:1.9.1.9) Gecko/20100317 SUSE/3.5.9-0.1 Firefox/3.5.9",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100401 Ubuntu/9.10 (karmic) Firefox/3.5.9 GTB7.1",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100315 Ubuntu/9.10 (karmic) Firefox/3.5.9",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.4) Gecko/20091028 Ubuntu/9.10 (karmic) Firefox/3.5.9",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; hu; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; et; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; nl; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; es-ES; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9 GTB5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; de; rv:1.9.2.13) Gecko/20101203 Firefox/3.5.9 (de)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; de; rv:1.9.1.9) Gecko/20100315 Firefox/3.5.9 GTB7.0 (.NET CLR 3.0.30618)",
      "Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.1.8) Gecko/20100216 Fedora/3.5.8-1.fc12 Firefox/3.5.8",
      "Mozilla/5.0 (X11; U; Linux x86_64; es-ES; rv:1.9.1.8) Gecko/20100216 Fedora/3.5.8-1.fc11 Firefox/3.5.8",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8) Gecko/20100318 Gentoo Firefox/3.5.8",
      "Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.1.8) Gecko/20100216 Fedora/3.5.8-1.fc12 Firefox/3.5.8",
      "Mozilla/5.0 (X11; U; Linux i686; ja-JP; rv:1.9.1.8) Gecko/20100216 Fedora/3.5.8-1.fc12 Firefox/3.5.8",
      "Mozilla/5.0 (X11; U; Linux i686; es-AR; rv:1.9.1.8) Gecko/20100214 Ubuntu/9.10 (karmic) Firefox/3.5.8",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.8) Gecko/20100214 Ubuntu/9.10 (karmic) Firefox/3.5.8",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.8) Gecko/20100202 Firefox/3.5.8",
      "Mozilla/5.0 (X11; U; FreeBSD i386; ja-JP; rv:1.9.1.8) Gecko/20100305 Firefox/3.5.8",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; sl; rv:1.9.1.8) Gecko/20100202 Firefox/3.5.8",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.8) Gecko/20100202 Firefox/3.5.8 (.NET CLR 3.5.30729) FirePHP/0.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW; rv:1.9.1.8) Gecko/20100202 Firefox/3.5.8 GTB6",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.1.8) Gecko/20100202 Firefox/3.5.8 GTB7.0 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2) Gecko/20100305 Gentoo Firefox/3.5.7",
      "Mozilla/5.0 (X11; U; Linux x86_64; cs-CZ; rv:1.9.1.7) Gecko/20100106 Ubuntu/9.10 (karmic) Firefox/3.5.7",
      "Mozilla/5.0 (X11; U; Linux i686; es-ES; rv:1.9.1.7) Gecko/20091222 SUSE/3.5.7-1.1.1 Firefox/3.5.7",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 GTB6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; de; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; fr; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.0.04506.648)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; fa; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 MRA 5.5 (build 02842) Firefox/3.5.7 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.6) Gecko/20091215 Ubuntu/9.10 (karmic) Firefox/3.5.6",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.6) Gecko/20100117 Gentoo Firefox/3.5.6",
      "Mozilla/5.0 (X11; U; Linux i686; zh-CN; rv:1.9.1.6) Gecko/20091216 Fedora/3.5.6-1.fc11 Firefox/3.5.6 GTB6",
      "Mozilla/5.0 (X11; U; Linux i686; es-ES; rv:1.9.1.6) Gecko/20091201 SUSE/3.5.6-1.1.1 Firefox/3.5.6 GTB6",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.6) Gecko/20100118 Gentoo Firefox/3.5.6",
      "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.6) Gecko/20091215 Ubuntu/9.10 (karmic) Firefox/3.5.6 GTB6",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.6) Gecko/20091215 Ubuntu/9.10 (karmic) Firefox/3.5.6 GTB7.0",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.6) Gecko/20091215 Ubuntu/9.10 (karmic) Firefox/3.5.6",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.6) Gecko/20091201 SUSE/3.5.6-1.1.1 Firefox/3.5.6",
      "Mozilla/5.0 (X11; U; Linux i686; cs-CZ; rv:1.9.1.6) Gecko/20100107 Fedora/3.5.6-1.fc12 Firefox/3.5.6",
      "Mozilla/5.0 (X11; U; Linux i686; ca; rv:1.9.1.6) Gecko/20091215 Ubuntu/9.10 (karmic) Firefox/3.5.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; it; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; id; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 MRA 5.4 (build 02647) Firefox/3.5.6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 (.NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.6) Gecko/20091201 MRA 5.5 (build 02842) Firefox/3.5.6 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.6) Gecko/20091201 MRA 5.5 (build 02842) Firefox/3.5.6",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB6 (.NET CLR 3.5.30729) FBSMTWB",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 (.NET CLR 3.5.30729) FBSMTWB",
      "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.5",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.8pre) Gecko/20091227 Ubuntu/9.10 (karmic) Firefox/3.5.5",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.5) Gecko/20091114 Gentoo Firefox/3.5.5",
      "Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; uk; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 MRA 5.5 (build 02842) Firefox/3.5.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.1.5) Gecko/20091102 MRA 5.5 (build 02842) Firefox/3.5.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; zh-CN; rv:1.9.1.5) Gecko/Firefox/3.5.5",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.5) Gecko/20091102 MRA 5.5 (build 02842) Firefox/3.5.5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.5) Gecko/20091102 MRA 5.5 (build 02842) Firefox/3.5.5",
      "Mozilla/5.0 (Windows NT 5.1; U; zh-cn; rv:1.8.1) Gecko/20091102 Firefox/3.5.5",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; pl; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 FBSMTWB",
      "Mozilla/5.0 (X11; U; Linux x86_64; ja; rv:1.9.1.4) Gecko/20091016 SUSE/3.5.4-1.1.2 Firefox/3.5.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.4) Gecko/20091016 Firefox/3.5.4 (.NET CLR 3.5.30729) FBSMTWB",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.4) Gecko/20091007 Firefox/3.5.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU; rv:1.9.1.4) Gecko/20091016 Firefox/3.5.4 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.1.4) Gecko/20091016 Firefox/3.5.4 ( .NET CLR 3.5.30729; .NET4.0E)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.4) Gecko/20091007 Firefox/3.5.4",
      "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.3pre",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090914 Slackware/13.0_stable Firefox/3.5.3",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
      "Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.1.3) Gecko/20091020 Ubuntu/9.10 (karmic) Firefox/3.5.3",
      "Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20090919 Firefox/3.5.3",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20090912 Gentoo Firefox/3.5.3 FirePHP/0.3",
      "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 GTB5",
      "Mozilla/5.0 (X11; U; FreeBSD i386; ru-RU; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.5.3;MEGAUPLOAD 1.0 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ko; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; fi; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 2.0.50727; .NET CLR 3.0.30618; .NET CLR 3.5.21022; .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; bg; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ko; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; pl; rv:1.9.1.2) Gecko/20090911 Slackware Firefox/3.5.2",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.2) Gecko/20090803 Slackware Firefox/3.5.2",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.2) Gecko/20090803 Firefox/3.5.2 Slackware",
      "Mozilla/5.0 (X11; U; Linux i686; ru-RU; rv:1.9.1.2) Gecko/20090804 Firefox/3.5.2",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090729 Slackware/13.0 Firefox/3.5.2",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2",
      "Mozilla/5.0 (X11; U; Linux i686 (x86_64); fr; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; pl; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 GTB7.1 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; es-MX; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; de; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; de; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; uk; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16 FirePHP/0.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.1.16) Gecko/20101130 AskTbMYC/3.9.1.14019 Firefox/3.5.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; it; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16 GTB7.1 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.16) Gecko/20101130 MRA 5.4 (build 02647) Firefox/3.5.16 ( .NET CLR 3.5.30729; .NET4.0C)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16 GTB7.1",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20101130 AskTbPLTV5/3.8.0.12304 Firefox/3.5.16 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16 GTB7.1 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.1.16) Gecko/20101130 Firefox/3.5.16 GTB7.1",
      "Mozilla/5.0 (X11; U; Linux x86_64; it; rv:1.9.1.15) Gecko/20101027 Fedora/3.5.15-1.fc12 Firefox/3.5.15",
      "Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.15) Gecko/20101027 Fedora/3.5.15-1.fc12 Firefox/3.5.15",
      "Mozilla/5.0 (Windows; U; Windows NT 5.0; ru; rv:1.9.1.13) Gecko/20100914 Firefox/3.5.13",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.12) Gecko/2009070611 Firefox/3.5.12",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.1.12) Gecko/20100824 MRA 5.7 (build 03755) Firefox/3.5.12",
      "Mozilla/5.0 (X11; U; Linux; en-US; rv:1.9.1.11) Gecko/20100720 Firefox/3.5.11",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11 ( .NET CLR 3.5.30729; .NET4.0C)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; hu; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.10) Gecko/20100504 Firefox/3.5.11 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.1.10) Gecko/20100506 SUSE/3.5.10-0.1.1 Firefox/3.5.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.1.10) Gecko/20100504 Firefox/3.5.10 GTB7.0 ( .NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux x86_64; rv:1.9.1.1) Gecko/20090716 Linux Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.3) Gecko/20100524 Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090716 Linux Mint/7 (Gloria) Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090716 Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.1) Gecko/20090714 SUSE/3.5.1-1.1 Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux x86; rv:1.9.1.1) Gecko/20090716 Linux Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux i686; nl; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.2pre) Gecko/20090729 Ubuntu/9.04 (jaunty) Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 GTB5",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.1) Gecko/20090722 Gentoo Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1.1) Gecko/20090714 SUSE/3.5.1-1.1 Firefox/3.5.1",
      "Mozilla/5.0 (X11; U; DragonFly i386; de; rv:1.9.1) Gecko/20090720 Firefox/3.5.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; tr; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; sv-SE; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 GTB5 (.NET CLR 4.0.20506)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 GTB5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; de; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1 GTB5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1) Gecko/20090630 Firefox/3.5 GTB6",
      "Mozilla/5.0 (X11; U; Linux i686; ja; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (X11; U; Linux i686; it-IT; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.04 (jaunty) Firefox/3.5",
      "Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1) Gecko/20090624 Firefox/3.5",
      "Mozilla/5.0 (X11; U; Linux i686; fr-FR; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
      "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1) Gecko/20090701 Ubuntu/9.04 (jaunty) Firefox/3.5",
      "Mozilla/5.0 (X11; U; Linux i686; en-us; rv:1.9.0.2) Gecko/2008092313 Ubuntu/9.04 (jaunty) Firefox/3.5",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1) Gecko/20090624 Ubuntu/8.04 (hardy) Firefox/3.5",
      "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.1) Gecko/20090624 Firefox/3.5",
      "Mozilla/5.0 (X11; U; Linux i686 (x86_64); de; rv:1.9.1) Gecko/20090624 Firefox/3.5",
      "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.1) Gecko/20090703 Firefox/3.5",
      "Mozilla/5.0 (X11; U; FreeBSD i386; en-US; rv:1.9.0.10) Gecko/20090624 Firefox/3.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; pl; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1) Gecko/20090612 Firefox/3.5 (.NET CLR 4.0.20506)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1) Gecko/20090612 Firefox/3.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 4.0.20506)",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.1) Gecko/20090624 Firefox/3.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; zh-TW; rv:1.9.1) Gecko/20090624 Firefox/3.5 (.NET CLR 3.5.30729)",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.25 (KHTML, like Gecko) Chrome/12.0.706.0 Safari/534.25",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24",
      "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.702.0 Chrome/12.0.702.0 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/12.0.702.0 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/12.0.702.0 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.699.0 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.699.0 Safari/534.24",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.698.0 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.697.0 Safari/534.24",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.43 Safari/534.24",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 Safari/534.24",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24",
      "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.14 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.12 Safari/534.24",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.04 Chromium/11.0.696.0 Chrome/11.0.696.0 Safari/534.24",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.0 Safari/534.24",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.694.0 Safari/534.24",
      "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.23 (KHTML, like Gecko) Chrome/11.0.686.3 Safari/534.23",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.682.0 Safari/534.21",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
      "Mozilla/5.0 (Windows NT) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.669.0 Safari/534.20",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.19 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.19",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.18 (KHTML, like Gecko) Chrome/11.0.661.0 Safari/534.18",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.18 (KHTML, like Gecko) Chrome/11.0.660.0 Safari/534.18",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.17 (KHTML, like Gecko) Chrome/11.0.655.0 Safari/534.17",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.17 (KHTML, like Gecko) Chrome/11.0.655.0 Safari/534.17",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.17 (KHTML, like Gecko) Chrome/11.0.654.0 Safari/534.17",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.17 (KHTML, like Gecko) Chrome/11.0.652.0 Safari/534.17",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.17 (KHTML, like Gecko) Chrome/10.0.649.0 Safari/534.17",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/534.17 (KHTML, like Gecko) Chrome/10.0.649.0 Safari/534.17",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.82 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux armv7l; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16",
      "Mozilla/5.0 (X11; U; FreeBSD x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16",
      "Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.134 Safari/534.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.134 Safari/534.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.134 Safari/534.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.134 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.133 Chrome/10.0.648.133 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.133 Chrome/10.0.648.133 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.127 Chrome/10.0.648.127 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.127 Safari/534.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.127 Safari/534.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.127 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru-RU) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.0 Chrome/10.0.648.0 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.648.0 Chrome/10.0.648.0 Safari/534.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.0 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.642.0 Chrome/10.0.642.0 Safari/534.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.639.0 Safari/534.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.638.0 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.634.0 Safari/534.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.634.0 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 SUSE/10.0.626.0 (KHTML, like Gecko) Chrome/10.0.626.0 Safari/534.16",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.613.0 Safari/534.15",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.613.0 Chrome/10.0.613.0 Safari/534.15",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.04 Chromium/10.0.612.3 Chrome/10.0.612.3 Safari/534.15",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Chrome/10.0.612.1 Safari/534.15",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.15 (KHTML, like Gecko) Ubuntu/10.10 Chromium/10.0.611.0 Chrome/10.0.611.0 Safari/534.15",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.602.0 Safari/534.14",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/9.1.0.0 Safari/540.0",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Ubuntu/10.10 Chromium/9.0.600.0 Chrome/9.0.600.0 Safari/534.14",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.599.0 Safari/534.13",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.84 Safari/534.13",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.44 Safari/534.13",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.19 Safari/534.13",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.596.0 Safari/534.13",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Ubuntu/10.04 Chromium/9.0.595.0 Chrome/9.0.595.0 Safari/534.13",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Ubuntu/9.10 Chromium/9.0.592.0 Chrome/9.0.592.0 Safari/534.13",
      "Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.579.0 Safari/534.12",
      "Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.576.0 Safari/534.12",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/8.1.0.0 Safari/540.0",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10",
      "Mozilla/5.0 (X11; U; CrOS i686 0.9.130; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.344 Safari/534.10",
      "Mozilla/5.0 (X11; U; CrOS i686 0.9.128; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.343 Safari/534.10",
      "Mozilla/5.0 (X11; U; CrOS i686 0.9.128; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.341 Safari/534.10",
      "Mozilla/5.0 (X11; U; CrOS i686 0.9.128; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.339 Safari/534.10",
      "Mozilla/5.0 (X11; U; CrOS i686 0.9.128; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.339",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 Chrome/8.0.552.237 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/533.3",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/534.10",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.215 Safari/534.10",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.210 Safari/534.10",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.200 Safari/534.10",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.551.0 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.548.0 Safari/534.10",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.544.0 Safari/534.10",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.15) Gecko/20101027 Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.9 (KHTML, like Gecko) Chrome/7.0.531.0 Safari/534.9",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.8 (KHTML, like Gecko) Chrome/7.0.521.0 Safari/534.8",
      "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.517.24 Safari/534.7",
      "Mozilla/5.0 (X11; U; Linux x86_64; fr-FR) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.6 (KHTML, like Gecko) Chrome/7.0.500.0 Safari/534.6",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; sv-se) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ko-kr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; it-it) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-fr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; es-es) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-gb) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; de-de) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; it-IT) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/534.16+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-ch) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; de-de) AppleWebKit/534.15+ (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; ar) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Android 2.2; Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; tr-TR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5",
      "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; he-il) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; fr; CPU iPhone OS 4_2_1 like Mac OS X; fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_1 like Mac OS X; zh-tw) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; pl-pl) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; en-gb) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F190 Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; nb-no) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; it-it) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; fr) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; fi-fi) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; fi-fi) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; th-th) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/531.2+",
      "Mozilla/5.0 (X11; U; Linux x86_64; en-ca) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/531.2+",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; zh-cn) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ru-ru) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ko-kr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; it-it) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/534.1+ (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-au) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; el-gr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ca-es) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-tw) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; it-it) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; fr-fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-en) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; nl-nl) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; de-de) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7; en-us) AppleWebKit/533.4 (KHTML, like Gecko) Version/4.1 Safari/533.4",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en) AppleWebKit/526.9 (KHTML, like Gecko) Version/4.0dp1 Safari/526.8",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; tr) AppleWebKit/528.4+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; en) AppleWebKit/528.4+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; de) AppleWebKit/528.4+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.1b3pre) Gecko/20081212 Mozilla/5.0 (Windows; U; Windows NT 5.1; en) AppleWebKit/526.9 (KHTML, like Gecko) Version/4.0dp1 Safari/526.8",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-gb) AppleWebKit/528.10+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-us) AppleWebKit/528.4+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-gb) AppleWebKit/528.4+ (KHTML, like Gecko) Version/4.0dp1 Safari/526.11.2",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-gb) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs-CZ) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; en-us) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; da-dk) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; ja-jp) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/533.4+ (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; de-de) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; ja-jp) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; nl-nl) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B5097d Safari/6531.22.7",
      "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7",
      "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10gin_lib.cc",
      "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10",
      "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/123",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-TW) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE) AppleWebKit/532+ (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; hu-hu) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.21.11 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; ru-ru) AppleWebKit/533.2+ (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; de-at) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
      "Mozilla/5.0 (iPhone; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
      "Mozilla/5.0 (iPhone Simulator; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7D11 Safari/531.21.10",
      "Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/53",
      "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; es-es) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B367 Safari/531.21.10",
      "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; es-es) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B360 Safari/531.21.10",
      "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.1021.10gin_lib.cc",
      "Mozilla/5.0 (iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; en-us) AppleWebKit/532.0+ (KHTML, like Gecko) Version/4.0.3 Safari/531.9.2009",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; en-us) AppleWebKit/532.0+ (KHTML, like Gecko) Version/4.0.3 Safari/531.9",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; nl-nl) AppleWebKit/532.3+ (KHTML, like Gecko) Version/4.0.3 Safari/531.9",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; fi-fi) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.3 Safari/531.21.10",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532+ (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; zh-TW) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; pl-PL) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 5.2; de-DE) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1",
      "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_7; en-us) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/4.0.1 Safari/530.18",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.1 Safari/530.18",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ru-RU) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528+ (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; es-es) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; en) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; sv-SE) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-PT) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; nb-NO) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Mozilla/5.0 (Windows; U; Windows NT 5.1; fi-FI) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
      "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10",
      "Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10",
      "Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (X11; Linux i686; U; ja) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (X11; Linux i686; U; fr) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 6.1; U; cs) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 5.1; U;) Presto/2.7.62 Version/11.01",
      "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.13) Gecko/20101213 Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01",
      "Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01",
      "Mozilla/5.0 (Windows NT 6.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01",
      "Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00",
      "Opera/9.80 (X11; Linux i686; U; it) Presto/2.7.62 Version/11.00",
      "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.6.37 Version/11.00",
      "Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
      "Opera/9.80 (Windows NT 6.1; U; ko) Presto/2.7.62 Version/11.00",
      "Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00",
      "Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00",
      "Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00",
      "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.7.39 Version/11.00",
      "Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.7.39 Version/11.00",
      "Opera/9.80 (Windows NT 5.1; U; MRA 5.5 (build 02842); ru) Presto/2.7.62 Version/11.00",
      "Opera/9.80 (Windows NT 5.1; U; it) Presto/2.7.62 Version/11.00",
      "Mozilla/5.0 (Windows NT 6.0; U; ja; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00",
      "Mozilla/5.0 (Windows NT 5.1; U; pl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00",
      "Mozilla/5.0 (Windows NT 5.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00",
      "Mozilla/4.0 (compatible; MSIE 8.0; X11; Linux x86_64; pl) Opera 11.00",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; fr) Opera 11.00",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; ja) Opera 11.00",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; en) Opera 11.00",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; pl) Opera 11.00",
      "Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.6.31 Version/10.70",
      "Mozilla/5.0 (Windows NT 5.2; U; ru; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.70",
      "Mozilla/5.0 (Windows NT 5.1; U; zh-cn; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.70",
      "Opera/9.80 (Windows NT 5.2; U; zh-cn) Presto/2.6.30 Version/10.63",
      "Opera/9.80 (Windows NT 5.2; U; en) Presto/2.6.30 Version/10.63",
      "Opera/9.80 (Windows NT 5.1; U; MRA 5.6 (build 03278); ru) Presto/2.6.30 Version/10.63",
      "Opera/9.80 (Windows NT 5.1; U; pl) Presto/2.6.30 Version/10.62",
      "Mozilla/5.0 (X11; Linux x86_64; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.62",
      "Mozilla/4.0 (compatible; MSIE 8.0; X11; Linux x86_64; de) Opera 10.62",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; en) Opera 10.62",
      "Opera/9.80 (X11; Linux i686; U; pl) Presto/2.6.30 Version/10.61",
      "Opera/9.80 (X11; Linux i686; U; es-ES) Presto/2.6.30 Version/10.61",
      "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.6.30 Version/10.61",
      "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.6.30 Version/10.61",
      "Opera/9.80 (Windows NT 6.0; U; it) Presto/2.6.30 Version/10.61",
      "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.6.30 Version/10.61",
      "Opera/9.80 (Windows 98; U; de) Presto/2.6.30 Version/10.61",
      "Opera/9.80 (Macintosh; Intel Mac OS X; U; nl) Presto/2.6.30 Version/10.61",
      "Opera/9.80 (X11; Linux i686; U; en) Presto/2.5.27 Version/10.60",
      "Opera/9.80 (Windows NT 6.0; U; nl) Presto/2.6.30 Version/10.60",
      "Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60",
      "Opera/10.60 (Windows NT 5.1; U; en-US) Presto/2.6.30 Version/10.60",
      "Opera/9.80 (X11; Linux i686; U; it) Presto/2.5.24 Version/10.54",
      "Opera/9.80 (X11; Linux i686; U; en-GB) Presto/2.5.24 Version/10.53",
      "Mozilla/5.0 (Windows NT 5.1; U; zh-cn; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53",
      "Mozilla/5.0 (Windows NT 5.1; U; Firefox/5.0; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53",
      "Mozilla/5.0 (Windows NT 5.1; U; Firefox/4.5; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53",
      "Mozilla/5.0 (Windows NT 5.1; U; Firefox/3.5; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.53",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; ko) Opera 10.53",
      "Opera/9.80 (Windows NT 6.1; U; fr) Presto/2.5.24 Version/10.52",
      "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.5.22 Version/10.51",
      "Opera/9.80 (Windows NT 6.0; U; cs) Presto/2.5.22 Version/10.51",
      "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51",
      "Opera/9.80 (Linux i686; U; en) Presto/2.5.22 Version/10.51",
      "Mozilla/5.0 (Windows NT 6.1; U; en-GB; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.51",
      "Mozilla/5.0 (Linux i686; U; en; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 10.51",
      "Mozilla/4.0 (compatible; MSIE 8.0; Linux i686; en) Opera 10.51",
      "Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.5.22 Version/10.50",
      "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.5.22 Version/10.50",
      "Opera/9.80 (Windows NT 6.1; U; sk) Presto/2.6.22 Version/10.50",
      "Opera/9.80 (Windows NT 6.1; U; ja) Presto/2.5.22 Version/10.50",
      "Opera/9.80 (Windows NT 6.0; U; zh-cn) Presto/2.5.22 Version/10.50",
      "Opera/9.80 (Windows NT 5.1; U; sk) Presto/2.5.22 Version/10.50",
      "Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.5.22 Version/10.50",
      "Opera/10.50 (Windows NT 6.1; U; en-GB) Presto/2.2.2",
      "Opera/9.80 (S60; SymbOS; Opera Tablet/9174; U; en) Presto/2.7.81 Version/10.5",
      "Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10",
      "Opera/9.80 (X11; Linux x86_64; U; it) Presto/2.2.15 Version/10.10",
      "Opera/9.80 (Windows NT 6.1; U; de) Presto/2.2.15 Version/10.10",
      "Opera/9.80 (Windows NT 6.0; U; Gecko/20100115; pl) Presto/2.2.15 Version/10.10",
      "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.2.15 Version/10.10",
      "Opera/9.80 (Windows NT 5.1; U; de) Presto/2.2.15 Version/10.10",
      "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.2.15 Version/10.10",
      "Mozilla/5.0 (Windows NT 6.0; U; tr; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 10.10",
      "Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux i686; de) Opera 10.10",
      "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 6.0; tr) Opera 10.10",
      "Opera/9.80 (X11; Linux x86_64; U; en-GB) Presto/2.2.15 Version/10.01",
      "Opera/9.80 (X11; Linux x86_64; U; en) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux i686; U; ru) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux i686; U; pt-BR) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux i686; U; pl) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux i686; U; nb) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux i686; U; en-GB) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux i686; U; en) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux i686; U; Debian; pl) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (X11; Linux i686; U; de) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 6.1; U; de) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 6.1; U; cs) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 6.0; U; de) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 5.2; U; en) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.2.15 Version/10.00",
      "Opera/9.80 (Windows NT 5.1; U; ru) Presto/2.2.15 Version/10.00",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; ja-jp) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
      "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0",
      "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
      "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)",
      "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.7.62 Version/11.01",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 3.0.04506.30)",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0",
      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
      "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
      "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
      "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-fr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
      "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
      "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; fr-fr) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
      "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
      "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
      "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
      "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
      "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36"
      ]


def get_variable_name(variable):
    """
    字如其名, 这是一个通过值来找变量名的函数
    >>> a = 10
    >>> get_variable_name(10)
    ['a']
    >>> b = c = "HelloWorld"
    >>> get_variable_name("HelloWorld").pop()
    'c'
    >>> get_variable_name("HelloWorld")
    ['b', 'c']
    """
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is variable]


sysLog = sys.stdout


def printf(*args, sep=' ', end='\n'):
    """
    Like the function `print()`.
    I write it to do this:
    >>> printf("My life")
    Myl life
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


def setVar(name: list, val=None):
    """
    SET MORE VAR
    >>> setVar(([f"n{i}"] for i in range(1, 51)), [i for i in range(50)])
    >>> n1
    0
    >>> n2
    1
    >>> print(n1, n2, n3 ... n10)
    0 1 2 3 4 5 6 7 8 9
    """
    names = globals()
    if type(val) == type([1, 2, 3]):
        for i in range(len(val)):
            names[name[i]] = val[i]
    else:
        for i in range(len(val)):
            names[name[i]] = val


BLOCK_SIZE = 16  # Bytes


def pad(s): return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                   chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s): return s[:-ord(s[len(s) - 1:])]


def aesEncrypt(key, data):
    '''
    AES的ECB模式加密方法
    :param key: 密钥
    :param data:被加密字符串（明文）
    :return:密文
    '''
    key = key.encode('utf8')
    # 字符串补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    printf(enctext)
    return enctext


def aesDecrypt(key, data):
    '''
    :param key: 密钥
    :param data: 加密后的数据（密文）
    :return:明文
    '''
    key = key.encode('utf8')
    data = base64.b64decode(data)
    cipher = AES.new(key, AES.MODE_ECB)

    # 去补位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf8')
    print(text_decrypted)
    return text_decrypted


'''# ————————————————
# 版权声明：本文为CSDN博主「hresh」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/Herishwater/article/details/92131547'''

class SetErr(Exception):
    def __init__(self, message):
        self.message = message


class Setting(object):
    set = {}

    # @overload
    def __init__(self, filename, name=None, value=None, mode='a', isFormat=True):
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
            open(filename, 'w').close()
        self.io_r = open(filename, 'r')  # io_r指read的io
        self.text = self.io_r.read()
        self.io_r.close()
        self.io = open(filename, self.mode)
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
        self.io = open(self.filename, self.mode)
        with open(self.filename) as f:
            self.text = f.read()

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
        ret = [i for i in self.set]
        return ret

    def getValue(self):
        ret = [self.set[i] for i in self.set]
        return ret

    def refresh(self):
        self.io_r = open(self.filename, 'r')  # io_r指read的io
        self.text = self.io_r.read()
        self.io_r.close()
        self.io = open(self.filename, self.mode)
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

    def __del__(self):
        self.close()
        # del self.text
        # del self.io, self.io_r
        # del self.set
        del self


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
    sess = requests.session()


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
    response = requests.get(url, headers=headers)
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
    resp = requests.get(__url, headers=headers, params=data)
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
        session = sess
        try:
            response = session.get(_url, params=_params, headers=headers)
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
            session = sess
            response = session.get(_url, params=_params, headers=headers)
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
    resp = requests.get(url, headers=headers, params=data)
    resp.encoding = 'utf-8'
    resp.raise_for_status()
    json_response = resp.json()
    return {'title': json_response['data']['title'], 'desc': json_response['data']['desc']}


def download(json, bv, page=1, name=None) -> dict:
    '''
    ## download a video from BiliBili
    use `aria2c` to download
    '''
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

def download_video(bv, headers, page=1, isLog=True, path="."):
    makedirs(os.path.join(path, "video"))
    if bv[:2].lower() == 'av':
        bv = av2bv(bv)
    try:
        if isLog:
            printf("获取视频信息")
        json1 = get_video_info(bv, headers)
    except KeyError:
        return 1
    a = ''
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
            url = json1[0]['data']['dash']['video'][0]['baseUrl']
            title = get_video_title_or_desc(bv, headers=headers)['title']
            title = title.replace("/", "").replace("\\", "")
            if isLog:
                printf("下载视频部分")
            a = download(url, bv, page, name=title)
            subprocess.call(a['cmd'])
            url = json1[0]['data']['dash']['audio'][0]['baseUrl']
            if isLog:
                printf("下载音频部分")
            b = download_music(
                url, bv, page, name=title)
            subprocess.call(b['cmd'])
        else:
            url = json1['data']['dash']['video'][0]['baseUrl']
            title = get_video_title_or_desc(bv, headers=headers)['title']
            if isLog:
                printf("下载视频部分")
            a = download(url, bv, page, name=title)
            subprocess.call(a["cmd"])
            b = None
            try:
                url = json1['data']['dash']['audio'][0]['baseUrl']
                if isLog:
                    printf("下载音频部分")
                b = download_music(url, bv, page, name=title)
                subprocess.call(b['cmd'])
            except KeyError:
                process = subprocess.call(
                    f"{path}\\bin\\ffmpeg -y -i \"{path}\\temp\\{a['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\"",
                    shell=True)
                clean(a['filename'])
                return {"video": a, "music": b, "cmd": f"{path}\\bin\\ffmpeg -y -i \"{path}\\temp\\{a['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\""}
                # 删除临时文件
    except:
        with open('../test.json', 'w') as f:
            json.dump(json1, f)
        return 1
    # 调用ffmpeg
    # 输入命令像这样: ffmpeg -y -i  D:\\ffmpeg_test\\1.webm  -r 30  D:\\ffmpeg_test\\1.mp4
    # 这里就是将1.webm的视频转成每秒30帧的视频1.mp4。这里指定1.mp4的绝对路径，如果不指定的话则生成的视频文件会落到当前ffmpeg命令的执行目录下。
    # 以上语句来自https://cloud.tencent.com/developer/article/1877108
    process = subprocess.call(
        f"{path}\\bin\\ffmpeg -y -i \"{path}\\temp\\{a['filename']}\" -i \"{path}\\temp\\{b['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\"",
        shell=True)
    # 删除临时文件
    clean(a['filename'])
    clean(b['filename'])
    return {"video": a, "music": b, "cmd": f"{path}\\bin\\ffmpeg -y -i \"{path}\\temp\\{a['filename']}\" -i \"{path}\\temp\\{b['filename']}\" -c:v copy -c:a aac -strict experimental \"{path}\\video\\{a['name']}.mp4\""}


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
    s = Setting('../setting.json', mode='r')
    if pages == 0:
        for i in range(1, s['mostSearch'] + 1):
            data = {
                'keyword': keywords,
                "page": i
            }
            res = requests.get(
                "http://api.bilibili.com/x/web-interface/search/all/v2",
                headers=headers,
                params=data
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
                temp = {}
                temp['title'] = data[i]['title']
                temp['bvid'] = data[i]['bvid']
                temp['author'] = data[i]['author']
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
            params=data
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
            temp = {}
            temp['title'] = data[i]['title']
            temp['bvid'] = data[i]['bvid']
            temp['author'] = data[i]['author']
            ret.append(temp)
        return ret


def getSearchAdvice(key):
    _url = "http://s.search.bilibili.com/main/suggest"
    data = {
        "term": key
    }
    resp = requests.get(_url, params=data)
    resp.encoding = 'utf-8'
    return resp.json()


def get_count(id, ua):
    headers = ua
    url = 'https://api.bilibili.com/x/space/arc/search'
    resp = requests.get(url, headers=headers, params={'mid': id})
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

    if pages is None:
        def get_count(id, ua):
            headers = ua
            url = 'https://api.bilibili.com/x/space/arc/search'
            resp = requests.get(url, headers=headers, params={'mid': id})
            count = resp.json()['data']['page']['count']
            resp.close()
            return count

        count = get_count(id, ua)
        if count <= 50:
            data = {
                'mid': id,
                'ps': 50
            }
            resp = requests.get(url, headers=headers, params=data)
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
                resp = requests.get(url, headers=headers, params=data)
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
        resp = requests.get(url, headers=headers, params=data)
        print(resp.text)
        json1 = resp.json()['data']['list']['vlist']
        ret += [{'bvid': i['bvid'],
                 'title': i['title'],
                 'author': i['author'],
                 'desc': i['description']}
                for i in json1
                ]
        return ret


def get_usr_pic(id):
    url = 'http://api.bilibili.com/x/space/acc/info'
    data = {
        'mid': id
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47 '
    }
    resp = requests.get(url, headers=headers, params=data)
    json1 = resp.json()['data']
    url = json1['face']
    rsp = requests.get(url)
    return (rsp, json1['name'])


def ip_get():
    """
    由bilibili提供的测ip服务
    """
    resp = requests.get('http://api.bilibili.com/x/web-interface/zone')
    resp = resp.json()
    return resp['data']


def get_usr_mid(bv, header):
    _url = 'http://api.bilibili.com/x/web-interface/view'
    rsp = requests.get(_url, params={'bvid': bv}, headers=header)
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
    wait = string.replace(" ", "").split(",")
    ret = []  # a setting
    for i in wait:
        if "-" not in i:
            ret.append(int(i))
        else:
            a, b = i.split("-")
            a = int(a)
            b = int(b)
            ret += [j for j in range(a, b + 1)]
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
        with open(self.filename, 'w') as f:
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
