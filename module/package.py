"""
规定命令格式：
[name].py pyinstaller/nuitka "[打包命令]"
打包命令规格如下：
直接写出后面的选项，如pyinstaller的-w -d之类
如：
python [name].py pyinstaller " -w"
不必写文件名
"""
import json
import logging
import os
import pprint
import shutil
import subprocess
import sys
import threading
import time

logging.basicConfig(
    level=logging.INFO,
    format="{[%(filename)s-%(lineno)d (%(process)s-%(threadName)s)]}: %(levelname)s-%("
    "asctime)s: %(message)s",
    encoding="utf-8",
)

pcgfile = """{
    "pythonFile": [],
    "exeFilePlace": {},
    "delete": [],
    "deleteTree": [],
    "copyPathName": {},
    "workpath": "",
    "workpathAfterCopy": ""
}"""


class Setting(object):
    set = {}

    # @overload
    def __init__(self,
                 filename,
                 name=None,
                 value=None,
                 mode="a",
                 isFormat=True,
                 encoding="utf-8"):
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
        self.io_r = open(filename, "r", encoding=encoding)  # io_r指read的io
        self.text = self.io_r.read()

        self.io_r.close()
        self.io = open(filename, self.mode, encoding=encoding)
        self.encoding = encoding
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
        with open(self.filename, "w", encoding=self.encoding) as f:
            f.write(string)
        self.io = open(self.filename, self.mode, encoding=self.encoding)
        with open(self.filename, encoding=self.encoding) as f:
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
        like `memset` function in c++, but it will only
        setting all values, not keys
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
        self.io_r = open(self.filename, "r",
                         encoding=self.encoding)  # io_r指read的io
        self.text = self.io_r.read()
        self.io_r.close()
        self.io = open(self.filename, self.mode, encoding=self.encoding)
        if self.text == "":
            return
        self.set = json.loads(self.text)

    def close(self):
        try:
            self.io.close()
            self.io_r.close()
        except:
            pass

    def init(self, key: list, value: list):
        for i in range(len(key)):
            if key[i] not in self.getKey():
                self.set[key[i]] = value[i]
        self.save()

    def init_(self, dic):
        self.set.update(dic)
        self.save()

    def __del__(self):
        self.close()
        del self


def copy(target_path, source_path):
    logging.info(
        f"Copy {os.path.abspath(source_path)} to {os.path.abspath(target_path)}."
    )
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if os.path.exists(source_path):
        shutil.rmtree(target_path)
    shutil.copytree(source_path, target_path)


def deletedir(target_path):
    try:
        shutil.rmtree(target_path)
    except Exception as err:
        logging.warning(f"{os.path.abspath(target_path)} is not existed")


s: Setting
config: Setting


def init():
    if not os.path.exists("package.json"):
        logging.info("package.json file is not existed, create.")
        with open("package.json", "w") as f:
            f.write(pcgfile)
        print("PLEASE WRITE PACKAGE.FILE")
        import sys

        sys.exit(1)
    else:
        global s, config
        s = Setting("setting.json")
        config = Setting("package.json")


def move(file, place):
    if not os.path.exists(place):
        os.makedirs(place)


def main():
    try:
        init()
        # copy
        if config["workpath"] != "":
            os.chdir(config["workpath"])
        ts = time.time()
        for i in config["copyPathName"]:
            try:
                copy(config["copyPathName"][i], i)
                logging.info(
                    f"Copy {os.path.abspath(i)} to {os.path.abspath(config['copyPathName'][i])}"
                )
            except:
                logging.warning(f"Copy {os.path.abspath(i)} error, continue.")
        te = time.time()
        logging.info("Copy use time {}.".format(te - ts))
        if config["workpathAfterCopy"] != "":
            os.chdir(config["workpathAfterCopy"])
        for i in config["delete"]:
            try:
                os.remove(i)
                logging.info(f"Delete a file named {os.path.abspath(i)}")
            except:
                logging.warning(
                    f"Delete file named {os.path.abspath(i)} failed.")
        for i in config["deleteTree"]:
            try:
                shutil.rmtree(i)
                logging.info(f"Delete a tree named {os.path.abspath(i)}")
            except:
                logging.warning(
                    f"Delete tree named {os.path.abspath(i)} failed.")
        for i in config["pythonFile"]:
            x = subprocess.Popen(f"{sys.argv[1]} {sys.argv[2]} {i}",
                                 shell=True)
            x.wait()
            if x.returncode == 0:
                logging.info(f"{i} 打包完成")
            else:
                logging.warning(f"{i} 打包失败")
            try:
                os.remove(i)
                os.remove(os.path.split(os.path.split(i)[-1])[0] + ".spec")
            except:
                pass
        shutil.rmtree("build")
    except Exception as err:
        logging.error(err)
        logging.warning("Packaging failed, cleaning up...")
        for i in config["copyPathName"]:
            logging.info(f"Clean {i}...")
            try:
                shutil.rmtree(i)
            except Exception as err:
                logging.info(
                    "Cleaning error: {}, please clean by your self. Please clean: {}"
                    .format(err, "\n" + "\n".join(config["copyPathName"])))
                shutil.rmtree(".")
                main()


main()
