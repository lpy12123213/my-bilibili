r"""
爬取哔哩哔哩上的视频
支持使用网页端登录，简易播放视频（不建议）
目前暂时支持使用bilibili api下载视频，未来会考虑使用BBDown下载
本人不对此软件造成的后果负责
"""

import datetime
from xml.sax import parseString
from func import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPalette, QPixmap, QBrush, QImage
import json
import sys
import threading as thread  # 导入线程模块, 之后要用
import logging
import os
import subprocess
import re
import pyperclip as perclip
import time
import QCandyUi.CandyWindow
import qdarkstyle
from ua import ua
from random import choice
sys.stdout = open(".\\log\\print.out", "a")
N = "%Y-%m-%d %H:%m:%S(%p)"
sys.stderr = open(".\\log\\main.err", "a")
print(datetime.datetime.now().strftime(N))
__version__ = "0.0.1"
__author__ = "Lypengyu at https://space.bilibili.com/450158456"
flag = True
path = os.getcwd()

os.chdir(path)
headers = {
    'user-agent': choice(ua)
}

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    filename='.\\log\\.log',
                    encoding="utf-8")

if not os.path.isdir(".\\video"):
    os.mkdir(".\\video")
    logging.debug("创建文件夹video")

if not os.path.isdir(".\\temp"):
    os.mkdir(".\\temp")
    logging.debug("创建文件夹temp")

if sys.platform != "win32":
    # 判断系统
    print("暂时只有windows可以使用，其它系统暂不知道")
    isContinue = input("若想继续，请按\"Yes\"，可能会有少数功能失效 \nReally?[Yes/No]")
    if isContinue.lower() == 'no' or isContinue.lower() == 'n':
        time.sleep(3)
        sys.exit(114514)  # 你是一个一个的程序啊!

set = Setting('setting.json')


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r', encoding='UTF-8') as file:
            return file.read()


if set['Qss'].lower() != 'other':
    style_sheet = QSSLoader.read_qss_file(set['Qss'])
else:
    style_sheet = (qdarkstyle.load_stylesheet_pyqt5())


class Ui_bilibili_get(object):
    show_main_win_signal = pyqtSignal()
    header = headers
    cookie = None
    result = None
    bv = None
    json = None
    usr_mid = None

    def setupUi(self, bilibili_get):
        bilibili_get.setObjectName("bilibili_get")
        bilibili_get.resize(1070, 654)
        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0.38888)
        if set.get("isNeedBackground") == False:
            bilibili_get.setStyleSheet(style_sheet)
        else:
            bilibili_get.setStyleSheet("QPushButton {\n"
                                       "    color: red;\n"
                                       "    font-size: 20;\n"
                                       "}\n"
                                       "QLineEdit {\n"
                                       "    color: blue;\n"
                                       "    font-size: 20;\n"
                                       "}\n"
                                       "tabWidget{\n"
                                       "    color: green;\n"
                                       "    font-size: 15px;\n"
                                       "}")
        self.tabWidget = QtWidgets.QTabWidget(bilibili_get)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 70, 1071, 581))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.cookie_button = QtWidgets.QPushButton(self.tab)
        self.cookie_button.setGeometry(QtCore.QRect(10, 10, 141, 41))
        self.cookie_button.setFlat(True)
        self.cookie_button.setObjectName("cookie_button")
        self.ztl = QtWidgets.QTextEdit(self.tab)
        self.ztl.setEnabled(True)
        self.ztl.setGeometry(QtCore.QRect(10, 60, 931, 501))
        self.ztl.setReadOnly(True)
        self.ztl.setOverwriteMode(False)
        self.ztl.setObjectName("ztl")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(940, 60, 121, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.start_bfq = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.start_bfq.setFlat(True)
        self.start_bfq.setObjectName("start_bfq")
        self.verticalLayout.addWidget(self.start_bfq)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.tabWidget.addTab(self.tab, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setStyleSheet("pushButton{\n"
"    color: #070608;\n"
"};")
        self.tab_5.setObjectName("tab_5")
        self.pushButton = QtWidgets.QPushButton(self.tab_5)
        self.pushButton.setGeometry(QtCore.QRect(960, 10, 93, 21))
        self.pushButton.setStyleSheet("*{\n"
"    color: #070608;\n"
"}")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit.setGeometry(QtCore.QRect(790, 10, 158, 21))
        self.lineEdit.setText("")
        self.lineEdit.setFrame(False)
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_2.setGeometry(QtCore.QRect(440, 570, 251, 25))
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_2.setGeometry(QtCore.QRect(700, 570, 93, 29))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_5)
        self.textEdit_2.setEnabled(True)
        self.textEdit_2.setGeometry(QtCore.QRect(0, 40, 1061, 521))
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.authorMid = QtWidgets.QLineEdit(self.tab_2)
        self.authorMid.setGeometry(QtCore.QRect(20, 30, 551, 31))
        self.authorMid.setClearButtonEnabled(True)
        self.authorMid.setObjectName("authorMid")
        self.getUsrInfo = QtWidgets.QPushButton(self.tab_2)
        self.getUsrInfo.setGeometry(QtCore.QRect(600, 30, 93, 29))
        self.getUsrInfo.setObjectName("getUsrInfo")
        self.input_a = QtWidgets.QLineEdit(self.tab_2)
        self.input_a.setGeometry(QtCore.QRect(570, 510, 261, 25))
        self.input_a.setObjectName("input_a")
        self.okForAuthor = QtWidgets.QPushButton(self.tab_2)
        self.okForAuthor.setGeometry(QtCore.QRect(840, 510, 111, 29))
        self.okForAuthor.setObjectName("okForAuthor")
        self.videoOfAuthor = QtWidgets.QTextEdit(self.tab_2)
        self.videoOfAuthor.setGeometry(QtCore.QRect(20, 80, 1031, 411))
        self.videoOfAuthor.setObjectName("textEdit")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.about = QtWidgets.QTextEdit(self.tab_3)
        self.about.setEnabled(True)
        self.about.setGeometry(QtCore.QRect(0, 30, 1071, 591))
        self.about.setObjectName("about")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 1061, 20))
        self.label_4.setObjectName("label_4")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.cmd = QtWidgets.QTextEdit(self.tab_4)
        self.cmd.setGeometry(QtCore.QRect(20, 10, 921, 171))
        self.cmd.setObjectName("cmd")
        self.cmdButton = QtWidgets.QPushButton(self.tab_4)
        self.cmdButton.setGeometry(QtCore.QRect(960, 10, 93, 29))
        self.cmdButton.setObjectName("cmdButton")
        self.cmdReturn = QtWidgets.QTextEdit(self.tab_4)
        self.cmdReturn.setGeometry(QtCore.QRect(20, 200, 1041, 341))
        self.cmdReturn.setReadOnly(True)
        self.cmdReturn.setObjectName("cmdReturn")
        self.tabWidget.addTab(self.tab_4, "")
        self.bv_line = QtWidgets.QLineEdit(bilibili_get)
        self.bv_line.setGeometry(QtCore.QRect(10, 20, 311, 31))
        self.bv_line.setText("")
        self.bv_line.setFrame(False)
        self.bv_line.setClearButtonEnabled(True)
        self.bv_line.setObjectName("bv_line")
        self.horizontalLayoutWidget = QtWidgets.QWidget(bilibili_get)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(320, 20, 391, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sure_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.sure_button.setStyleSheet("")
        self.sure_button.setFlat(True)
        self.sure_button.setObjectName("sure_button")
        self.horizontalLayout.addWidget(self.sure_button)
        self.unsure_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.unsure_button.setStyleSheet("")
        self.unsure_button.setFlat(True)
        self.unsure_button.setObjectName("unsure_button")
        self.horizontalLayout.addWidget(self.unsure_button)
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setFlat(True)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.userName = QtWidgets.QLabel(bilibili_get)
        self.userName.setGeometry(QtCore.QRect(850, 20, 181, 20))
        self.userName.setText("")
        self.userName.setObjectName("userName")

        self.retranslateUi(bilibili_get)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(bilibili_get)
        
        self.cookie_button.clicked.connect(self.getcookie)
        self.sure_button.clicked.connect(self.d)
        self.unsure_button.clicked.connect(self.killer)
        self.pushButton.clicked.connect(self.sear)
        self.start_bfq.clicked.connect(self.bfqstart)
        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.go)
        # self.pushButton_5.clicked.connect(self.author)
        self.cmdButton.clicked.connect(self.cmdAction)
        self.getUsrInfo.clicked.connect(self.getUsrInfoAction)


    def retranslateUi(self, bilibili_get):
        _translate = QtCore.QCoreApplication.translate
        bilibili_get.setWindowTitle(_translate("bilibili_get", "Widget"))
        self.cookie_button.setText(_translate("bilibili_get", "获得cookie"))
        self.start_bfq.setText(_translate("bilibili_get", "启动播放器"))
        self.pushButton_3.setText(_translate("bilibili_get", "退出"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("bilibili_get", "主页"))
        self.pushButton.setText(_translate("bilibili_get", "确定"))
        self.lineEdit.setPlaceholderText(_translate("bilibili_get", "搜索内容"))
        self.lineEdit_2.setText(_translate("bilibili_get", "选定范围（就是每个结果前面的）"))
        self.pushButton_2.setText(_translate("bilibili_get", "sure"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("bilibili_get", "搜索列表"))
        self.getUsrInfo.setText(_translate("bilibili_get", "解析作者"))
        self.input_a.setPlaceholderText(_translate("bilibili_get", "输入下载区间，详见“关于”"))
        self.okForAuthor.setText(_translate("bilibili_get", "确定"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("bilibili_get", "作者解析"))
        self.label_4.setText(_translate("bilibili_get", "关于"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("bilibili_get", "关于"))
        self.cmd.setPlaceholderText(_translate("bilibili_get", "命令"))
        self.cmdButton.setText(_translate("bilibili_get", "执行"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("bilibili_get", "命令页"))
        self.bv_line.setPlaceholderText(_translate("bilibili_get", "bv号"))
        self.sure_button.setText(_translate("bilibili_get", "确定"))
        self.unsure_button.setText(_translate("bilibili_get", "取消"))
        self.pushButton_5.setText(_translate("bilibili_get", "解析作者"))

        if set["isNeedBackground"] == True:
            self.tabWidget.setGraphicsEffect(self.op)
            self.tabWidget.setAutoFillBackground(True)

    def getcookie(self):
        def _():
            self.ztl.append("！！请打开open1.py文件并获得cookie，之后重新点击此按钮！！")
            if not os.path.exists("open1.pyw"):
                subprocess.Popen("open1.exe")
            else:
                subprocess.call("python open1.pyw")
            logging.warning("cookie文件无效，等待获取：文件不存在")

        try:
            set.refresh()
            self.cookie = set['cookie']
            if self.cookie == "":
                raise ValueError("cookie文件无效")
        except ValueError:
            self.ztl.append("cookie.json文件错误，请重新获取cookie")
            logging.warning("cookie.json文件错误，请重新获取cookie: 文件内容无效")
            t = thread.Thread(target=_)
            t.start()
            return
        if self.cookie != {}:
            self.header['cookie'] = self.cookie
        if type(self.cookie) != type(''):
            try:
                raise ValueError(
                    f"Cookie must be a string, not a {type(self.cookie)}")
            except ValueError as ve:
                self.ztl.append(f"错误：{ve}，请重新获取cookie")
                logging.error(f"Cookie值错误：{ve}")
                t = thread.Thread(target=_)
                t.start()
                return
        self.ztl.append(
            f"已获取cookie: {self.cookie[:50]}...\n程序不会记录您的cookie值，也请您在传播时注意cookie的保护")
        logging.info('已获取cookie')
        logging.debug(f'用户cookie值: {self.cookie[:50]}...')
        self.usrJsonObj = get_user_info(headers=self.header)
        try:
            self.userName.setText(self.usrJsonObj['data']['uname'])
        except Exception:
            self.ztl.append("出现错误:cookie值无法验证")
        if self.cookie != '':
            return
        t = thread.Thread(target=_)
        t.start()
        del _

    def getUsrInfoAction(self):
        self.usrId = self.authorMid.text()
        self.resultForAuthor = get_usr_video(self.usrId, self.header)
        for i in range(len(self.resultForAuthor)):
            self.videoOfAuthor.append(
                f"{i + 1} BVID: {self.resultForAuthor[i]['bvid']} TITLE: {self.resultForAuthor[i]['title']} DESC: {self.resultForAuthor[i]['desc']}")

    def d(self) -> None:  # download file
        def d(bv):
            p = download_video(bv, headers=self.header)
            if p == 0:
                logging.debug(
                    f"视频信息：{get_video_info(bv, self.header)}")
                logging.info(f"视频下载完成：{bv}")
            else:
                self.ztl.append("视频下载失败！")
                logging.warning(f"视频{bv}下载失败: 结束码异常")

        def _() -> None:
            try:
                self.bv = tuple(
                    self.bv_line.text().replace(' ', '').split(','))
                print(self.bv)
            except:
                self.ztl.append("输入格式错误！")
                logging.debug(f"用户输入格式错误！")
                self.bv = None
                self.json = None
                self.usr_mid = None
            else:
                if type(self.bv) == type(''):
                    a = self.bv
                    self.usr_mid = get_usr_mid(a, self.header)
                    self.json = get_usr_video(self.usr_mid)
                elif type(self.bv) == type((1, 2, 3)) or type(self.bv) == type([1, 2, 3]):
                    a = self.bv[0]
                    self.usr_mid = get_usr_mid(a, self.header)
                    self.json = get_usr_video(self.usr_mid)
                else:
                    print("Cannot get it!")
                # print(a, self.usr_mid, self.json, sep="\n")
                logging.debug("输入完成")
                if type(self.bv) == type((1, 2, 3)):  # 判断输入类型
                    # 如果是多个bv
                    thread_list = []  # -> thread.Thread()
                    i = 0
                    for j in self.bv:
                        # thread_list.append(thread.Thread(target=d, args=[j]))
                        # thread_list[i].start()
                        d(j)
                        i += 1
                else:
                    # 单个bv
                    t = thread.Thread(target=d, args=[self.bv])
                    t.start()

        do = thread.Thread(target=_)
        do.start()
        del _

    def killer(self) -> None:  # taskkill aria2c and ffmpeg
        def _():
            kill()

        t = thread.Thread(target=_)
        t.start()
        logging.debug("用户取消下载，执行taskkill关闭线程")

    def sear(self) -> None:
        # 放线程里会凭空的闪退，线程退出代码-1073740940(0xC000005)
        self.textEdit_2.clear()
        self.search_text = self.lineEdit.text()
        try:
            self.result = search(self.search_text, self.header)
        except:
            return
        if self.result == 1:
            self.textEdit_2.insertHtml(
                f"<strong>获取失败<\strong>")
            logging.warning("搜索结果获取失败")
            return 1
        j = 1
        for i in self.result:
            self.textEdit_2.insertHtml(
                f"{j} bv:{i['bvid']} title:{i['title']} author:{i['author']}<br>")
            j += 1

    def closeEvent(self, event):  # 函数名固定不可变
        self.exit()

    def bfqstart(self):
        def _():
            if not os.path.exists('player.exe'):
                # 如果是源码
                subprocess.call("python player.pyw")
            else:
                # 如果已经编译
                subprocess.call("start player.exe")

        t = thread.Thread(target=_)
        t.start()

    def exit(self) -> None:
        def _():
            # 是不是只能在windows下用呢？
            if __file__.split('.')[-1] == 'py':
                # kill掉python进程
                subprocess.call("taskkill /F /PID python.exe")
            elif __file__.split('.')[-1] == 'exe':
                # 提示：使用f进行字符串格式化不能有反斜杠
                # kill掉exe进程
                subprocess.call("taskkill /F /PID %s" %
                                __file__.split('\\')[-1])
            kill()
        # # 使用线程进行操作，防止卡顿
        t = thread.Thread(target=_)
        sys.stdout.close()
        t.start()
        # 放弃了使用taskkill，改用os._exit()
        # os._exit(0)

    def go(self):
        def d(bv):
            p = download_video(bv, headers=self.header)
            if p == 0:
                logging.debug(
                    f"视频信息：{get_video_info(bv, self.header)}")
                logging.info(f"视频下载完成：{bv}")
            else:
                self.ztl.append("视频下载失败！")
                logging.warning(f"视频{bv}下载失败: 结束码异常")

        def _():
            if self.result is None:
                return
            fw = self.lineEdit_2.text()  # fw代表范围
            fw = fw.replace(' ', '')
            fw = fw.split(',')
            t = []
            m = 0
            for i in fw:
                if '-' in i:
                    fanwei = (int(i.split('-')[0]), int(i.split('-')[1]))
                    for j in range(fanwei[0] - 1, fanwei[1] - 1):
                        # t.append(thread.Thread(
                        #     target=d, args=[self.result[j]['bvid']]))
                        # t[m].start()
                        d(self.result[j]['bvid'])
                        m += 1
                else:
                    fa = int(i)
                    # t.append(thread.Thread(
                    #     target=d, args=[self.result[fa]['bvid']]))
                    # t[m].start()
                    d(self.result[fa]['bvid'])

        t0bj = thread.Thread(target=_)
        t0bj.start()

    def cmdAction(self):
        ans = 0
        ac = self.cmd.toPlainText()
        logging.debug("执行代码{}".format(ac))
        locNow = locals()
        l = locals()
        for i in locNow:
            l[i] = locNow[i]
        try:
            # self.command = f"ans = {ac}"
            # if ':\n' not in ac.replace(' ', ''):
            #     loc = locals()
            #     exec(f"ans = {ac}")
            #     ans = loc['ans']
            #     self.cmdReturn.setText(str(ans))
            # else:
            #     exec(ac)
            self.command = f"ans = {ac}"
            loc = locals()
            exec(self.command)
            ans = loc['ans']
            self.cmdReturn.setText(str(ans))
        except:
            try:
                exec(ac)
            except:
                ac = ac.replace("tsk", "taskkill")
                try:
                    subprocess.call(ac)
                except:
                    self.cmdReturn.append("error executing")
    # def author(self):
    # 暂时还不想搞
    #     if self.json is None:
    #         return
    #     self.textEdit.clear()

    #     def _():
    #         m, self.author_name = get_usr_pic(self.usr_mid)
    #         with open("author.jpg", 'wb') as f:
    #             f.write(m)
    #         # img = QImage.fromdata(m)
    #         redImg = QImage()
    #         QImage.load(redImg, './data/red.png', format='png')
    #         self.label_2.setPixmap(QtGui.QPixmap(redImg))

    #     t = thread.Thread(target=_)
    #     t.start()


def main1():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_bilibili_get()
    ui.setupUi(MainWindow)
    MainWindow.resize(1072, 647)

    def get_bv_from_paste() -> str:  # 从剪贴版中获取bilibili链接
        re_1obj = re.compile(
            r'(?:https|http)://www.bilibili.com/video/([^?/]+)?(?:\?.*){0,1}')
        perc = perclip.paste()
        ret = re_1obj.search(perc)
        # 判断是不是没匹配到，若是，便退出函数
        if ret == None:
            return None
        return (ret.group(1))

    def get_bvid() -> None:
        b = None
        while True:
            time.sleep(0.5)
            a = get_bv_from_paste()
            if a != None and b != a:
                temp = ui.bv_line.text()
                t1 = temp + f"{a}, "
                ui.bv_line.setText(t1)
                b = a

    t1obj = thread.Thread(target=get_bvid)
    t1obj.start()
    # 获取cookie.json文件内容
    try:  # 包含了文件不存在，文件为空的情况
        cookie = set['cookie']
        if cookie == '' or cookie == {}:
            raise ValueError("cookie值为空")
        ui.header['cookie'] = cookie
        ui.usrJsonObj = get_user_info(ui.header)
        ui.userName.setText(ui.usrJsonObj['data']['uname'])
    except:
        pass
    MainWindow.show()
    a = app.exec_()
    sys.stdout.close()
    sys.stderr.close()
    os._exit(a)


def main2():
    if len(sys.argv) > 1:
        pass
    app = QApplication(sys.argv)
    logging.debug("程序启动成功")  # 关于好像logging没有输出的这件事
    w = QWidget()
    ui = Ui_bilibili_get()
    ui.setupUi(w)

    def get_bv_from_paste() -> str:  # 从剪贴版中获取bilibili链接
        re_1obj = re.compile(
            r'(?:https|http)://www.bilibili.com/video/([^?/]+)?(?:\?.*){0,1}')
        perc = perclip.paste()
        ret = re_1obj.search(perc)
        # 判断是不是没匹配到，若是，便退出函数
        if ret == None:
            return None
        return (ret.group(1))

    def get_bvid() -> None:
        b = None
        while True:
            time.sleep(0.5)
            a = get_bv_from_paste()
            if a != None and b != a:
                temp = ui.bv_line.text()
                t1 = temp + f"{a}, "
                ui.bv_line.setText(t1)
                b = a

    t1obj = thread.Thread(target=get_bvid)
    t1obj.start()
    # 获取cookie.json文件内容
    try:  # 包含了文件不存在，文件为空的情况
        cookie = set['cookie']
        if cookie == '' or cookie == {}:
            raise ValueError("cookie值为空")
        ui.header['cookie'] = cookie
        ui.usrJsonObj = get_user_info(ui.header)
        ui.userName.setText(ui.usrJsonObj['data']['uname'])
    except:
        pass
    ui.ztl.append("目前只支持下载与获取cookie")
    ui.ztl.append("请保护好您的cookie!")
    logging.debug("窗口初始化成功")
    w.resize(1072, 647)
    palette = QPalette()
    pix = QPixmap("./background.jpg")
    pix = pix.scaled(w.width(), w.height())
    palette.setBrush(QPalette.Background, QBrush(pix))
    w.setPalette(palette)
    logging.debug("窗口背景设置成功")
    w.show()
    a = app.exec_()
    sys.stdout.close()
    sys.stderr.close()
    os._exit(a)  # 勿改，否则退不出去


if __name__ == '__main__':
    set.change("isFirst", False)
    set.save()
    if set.get("isNeedBackground"):
        main2()
    else:
        main1()
