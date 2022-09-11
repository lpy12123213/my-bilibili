r"""
爬取哔哩哔哩上的视频
支持使用网页端登录，简易播放视频（不建议）
目前暂时支持使用bilibili api下载视频，未来会考虑使用BBDown下载
本人不对此软件造成的后果负责
已知bug：
不少的视频中都会有 "/" 的字符，这种字符会影响下载的保存位置，现在的解决办法是将所有的 "/" 和 "\" 替换掉
"""

import datetime
import logging
# noinspection PyUnresolvedReferences
import os
# noinspection PyUnresolvedReferences
import re
# noinspection PyUnresolvedReferences
import subprocess
# noinspection PyUnresolvedReferences
import sys
import threading as thread  # 导入线程模块, 之后要用
import time
# noinspection PyUnresolvedReferences
from random import choice

import pyperclip as perclip
import qdarkstyle
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPalette, QPixmap, QBrush
from PyQt5.QtWidgets import QApplication, QWidget

from func import *
# noinspection PyUnresolvedReferences
from ua import ua
import cgitb

cgitb.enable(format='text')

setting = Setting('setting.json')
if not setting['isDebugging']:
    sys.stdout = open(".\\log\\print.out", "a")
N = "%Y-%m-%d %H:%m:%S(%p)"
if not setting['isDebugging']:
    sys.stderr = open(".\\log\\main.err", "a")
print(datetime.datetime.now().strftime(N))
__version__ = "0.0.1"
__author__ = "Lypengyu at https://space.bilibili.com/450158456"
flag = True
path = os.getcwd()

os.chdir(path)
headers = {
    # 'user-agent': choice(ua)
    'user-agant': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
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


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def readQssFile(qss_file_name):
        with open(qss_file_name, 'r', encoding='UTF-8') as file:
            return file.read()


if setting['Qss'].lower() != 'other':
    style_sheet = QSSLoader.readQssFile(setting['Qss'])
else:
    style_sheet = (qdarkstyle.load_stylesheet_pyqt5())


class Thread1(QThread):
    signal = pyqtSignal(list, bool, int)

    def __init__(self, key, header):
        super(Thread1, self).__init__()
        self.key = key
        self.header = header

    def run(self):
        for i in range(1, setting['mostSearch'] + 1):
            self.result = search(self.key, self.header, i)
            self.signal.emit(self.result, True, (i - 1) * 20)


class Thread2(QThread):
    signal = pyqtSignal(list)

    def __init__(self, mid, header):
        super().__init__()
        self.key = mid
        self.header = header

    def run(self):
        self.result = get_usr_video(self.key, self.header)
        self.signal.emit(self.result)


class ThreadForAdvice(QThread):
    signal = pyqtSignal(list)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        try:
            self.respForSearchAdvide = getSearchAdvice(self.text)
        except:
            print("触发风控，请待会再试")
            return
        self.advice = [self.respForSearchAdvide[str(i)]
                       for i in range(len(self.respForSearchAdvide))]
        self.signal.emit(self.advice)


class Ui_bilibili_get(object):
    show_main_win_signal = pyqtSignal()
    header = headers
    cookie = None
    result = []
    bv = None
    json = None
    usr_mid = None

    def setupUi(self, bilibili_get):
        bilibili_get.setObjectName("bilibili_get")
        bilibili_get.resize(1070, 654)
        self.op = QtWidgets.QGraphicsOpacityEffect()
        self.op.setOpacity(0.38888)
        if setting.get("isNeedBackground") == False:
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
        self.tabWidget.setGeometry(QtCore.QRect(0, 70, 1081, 581))
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
        self.lineEdit = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit.setGeometry(QtCore.QRect(650, 0, 158, 21))
        self.lineEdit.setText("")
        self.lineEdit.setFrame(False)
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_2.setGeometry(QtCore.QRect(710, 510, 251, 25))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_2.setGeometry(QtCore.QRect(970, 510, 93, 29))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_5)
        self.textEdit_2.setEnabled(True)
        self.textEdit_2.setGeometry(QtCore.QRect(0, 40, 1061, 461))
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tab_5)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(820, 0, 241, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.findS = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.findS.setObjectName("findS")
        self.horizontalLayout_2.addWidget(self.findS)
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
        self.videoOfAuthor.setObjectName("videoOfAuthor")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(780, 30, 241, 20))
        self.label.setText("")
        self.label.setObjectName("label")
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
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.label_2 = QtWidgets.QLabel(self.tab_6)
        self.label_2.setGeometry(QtCore.QRect(30, 20, 81, 31))
        self.label_2.setObjectName("label_2")
        self.downloadName = QtWidgets.QLabel(self.tab_6)
        self.downloadName.setGeometry(QtCore.QRect(120, 20, 931, 31))
        self.downloadName.setObjectName("downloadName")
        self.progressBar = QtWidgets.QProgressBar(self.tab_6)
        self.progressBar.setGeometry(QtCore.QRect(30, 70, 461, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.tabWidget.addTab(self.tab_6, "")
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
        # self.pushButton.clicked.connect(self.sear)
        self.start_bfq.clicked.connect(self.bfqstart)
        self.pushButton_3.clicked.connect(self.exit)
        self.pushButton_2.clicked.connect(self.go)
        # self.pushButton_5.clicked.connect(self.author)
        self.cmdButton.clicked.connect(self.cmdAction)
        self.getUsrInfo.clicked.connect(self.getUsrInfoAction)
        self.findS.clicked.connect(self.sear)
        self.lineEdit.returnPressed.connect(self.sear)
        self.authorMid.returnPressed.connect(self.getUsrInfoAction)
        self.bv_line.returnPressed.connect(self.d)

    def retranslateUi(self, bilibili_get):
        _translate = QtCore.QCoreApplication.translate
        bilibili_get.setWindowTitle(_translate("bilibili_get", "Widget"))
        self.cookie_button.setText(_translate("bilibili_get", "获得cookie"))
        self.start_bfq.setText(_translate("bilibili_get", "启动播放器"))
        self.pushButton_3.setText(_translate("bilibili_get", "退出"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("bilibili_get", "主页"))
        self.lineEdit.setPlaceholderText(_translate("bilibili_get", "搜索内容"))
        self.lineEdit_2.setPlaceholderText(_translate("bilibili_get", "选定范围（就是每个结果前面的）"))
        self.pushButton_2.setText(_translate("bilibili_get", "sure"))
        self.findS.setText(_translate("bilibili_get", "搜索"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("bilibili_get", "搜索列表"))
        self.getUsrInfo.setText(_translate("bilibili_get", "解析作者"))
        self.input_a.setPlaceholderText(_translate("bilibili_get", "输入下载区间，详见“关于”"))
        self.okForAuthor.setText(_translate("bilibili_get", "确定"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("bilibili_get", "作者解析"))
        self.about.setHtml(_translate("bilibili_get",
                                      "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                      "p, li { white-space: pre-wrap; }\n"
                                      "</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                      "<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-family:\'Open Sans\',\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; color:#606c71;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">本软件只提供视频解析，不提供任何资源上传、存储到服务器的功能。</li>\n"
                                      "<li style=\" font-family:\'Open Sans\',\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; color:#606c71;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">本软件仅解析来自B站的内容，不会对解析到的音视频进行二次编码，部分视频会进行有限的格式转换、拼接等操作。</li>\n"
                                      "<li style=\" font-family:\'Open Sans\',\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; color:#606c71;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">本软件解析得到的所有内容均来自B站UP主上传、分享，其版权均归原作者所有。内容提供者、上传者（UP主）应对其提供、上传的内容承担全部责任。</li>\n"
                                      "<li style=\" font-family:\'Open Sans\',\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; color:#606c71;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">本软件提供的所有内容，仅可用作学习交流使用，未经原作者授权，禁止用于其他用途。请在下载24小时内删除。为尊重作者版权，请前往资源的原始发布网站观看，支持原创，谢谢。</span></li>\n"
                                      "<li style=\" font-family:\'Open Sans\',\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; color:#606c71;\" style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">因使用本软件产生的版权问题，软件作者概不负责。</li></ol>\n"
                                      "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Open Sans\',\'Helvetica Neue\',\'Helvetica\',\'Arial\',\'sans-serif\'; color:#606c71;\"><br /></span></p></body></html>"))
        self.label_4.setText(_translate("bilibili_get", "关于"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("bilibili_get", "关于"))
        self.cmd.setPlaceholderText(_translate("bilibili_get", "命令"))
        self.cmdButton.setText(_translate("bilibili_get", "执行"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("bilibili_get", "命令页"))
        self.label_2.setText(_translate("bilibili_get", "正在下载："))
        self.downloadName.setText(_translate("bilibili_get", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("bilibili_get", "下载页"))
        self.bv_line.setPlaceholderText(_translate("bilibili_get", "bv号"))
        self.sure_button.setText(_translate("bilibili_get", "确定"))
        self.unsure_button.setText(_translate("bilibili_get", "取消"))
        self.pushButton_5.setText(_translate("bilibili_get", "解析作者"))
        self.lineEdit.textChanged.connect(self.searchAdvice)

        if setting["isNeedBackground"] == True:
            self.tabWidget.setGraphicsEffect(self.op)
            self.tabWidget.setAutoFillBackground(True)

    def ThreadSearchAdviceAction(self, lst):
        temp_list = QtWidgets.QCompleter(lst)
        self.lineEdit.setCompleter(temp_list)

    def searchAdvice(self):
        def do():
            self.t = ThreadForAdvice(self.lineEdit.text())
            self.t.signal.connect(self.ThreadSearchAdviceAction)
            self.t.start()

        t = thread.Thread(target=do)
        t.start()

    def getcookie(self):
        def _():
            self.ztl.append("！！请打开open1.py文件并获得cookie，之后重新点击此按钮！！")
            if not os.path.exists("open1.pyw"):
                subprocess.Popen("open1.exe")
            else:
                subprocess.call("python open1.pyw")
            logging.warning("cookie文件无效，等待获取：文件不存在")

        try:
            setting.refresh()
            self.cookie = setting['cookie']
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
        if not setting.isExists("cookie", {}) and not setting.isExists("cookie", ""):
            self.textEdit_2.insertHtml("<h1>cookie不存在</h1>")
            return
        self.usrId = self.authorMid.text()
        self.videoOfAuthor.clear()
        try:
            a = int(self.usrId)
        except:
            self.videoOfAuthor.setText("输入错误")
            return
        self.threadForGetAuthor = Thread2(self.usrId, self.header)
        self.threadForGetAuthor.signal.connect(
            self.getUsrInfoActionThreadAction)
        self.threadForGetAuthor.start()

    def getUsrInfoActionThreadAction(self, lst):
        self.resultForAuthor = lst
        for i in range(len(lst)):
            self.videoOfAuthor.append(
                f"{i + 1} BVID: {lst[i]['bvid']} TITLE: {lst[i]['title']}")

    def downloadUsrVideo(self):
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
            need = analysis(self.lineEdit_2.text())

    def d(self) -> None:  # download file
        def download(bv):
            P = download_video(bv, self.header)
            if P == 1:
                print("视频下载失败")
                logging.info(f"视频{bv}下载失败")
                self.ztl.append(f"视频{bv}下载失败")

        def _():
            try:
                self.bv = self.bv_line.text().replace(" ", "").split(",")
            except:
                print("输入错误")
                self.ztl.append("输入错误")
                return
            for i in self.bv:
                download(i)

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
        self.result = []
        if not setting.isExists("cookie", {}) or not setting.isExists("cookie", ""):
            self.textEdit_2.insertHtml("<h1>cookie不存在</h1>")
            return
        self.textEdit_2.clear()
        self.search_text = self.lineEdit.text()
        self.th = Thread1(self.search_text, self.header)
        self.th.signal.connect(self.searThreadAction)
        self.th.start()

    def searThreadAction(self, lst, isCon, con):
        if isCon:
            self.result += lst
        else:
            self.result = lst
        if isCon:
            temp = con + 1
        else:
            temp = 1
        for i in lst:
            self.textEdit_2.insertHtml(
                f"{temp} bv:{i['bvid']} title:{i['title']} author:{i['author']}<br>")
            temp += 1

    def bfqstart(self):
        def _():
            if not os.path.exists('player.exe'):
                subprocess.call("python player.pyw")
            else:
                subprocess.call("start player.exe")

        t = thread.Thread(target=_)
        t.start()

    def exit(self) -> None:
        def _():
            if __file__.split('.')[-1] == 'py':
                subprocess.call("taskkill /F /PID python.exe")
                subprocess.call("taskkill /F /PID pythonw.exe")
            elif __file__.split('.')[-1] == 'exe':
                subprocess.call("taskkill /F /PID %s" %
                                __file__.split('\\')[-1])
            kill()

        t = thread.Thread(target=_)
        sys.stdout.close()
        t.start()
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
            need = analysis(self.lineEdit_2.text())
            if setting['thread']:
                for i in need:
                    t.append(thread.Thread(target=d, args=[self.result[i - 1]['bvid']]))
                for i in range(int(len(t) / 10 + 1)):
                    for j in range(10):
                        t[m].start()
                        m += 1
            else:
                for i in need:
                    d(self.result[i]['bvid'])

        t0bj = thread.Thread(target=_)
        t0bj.start()

    def cmdAction(self):
        def _():
            ans = 0
            ac = self.cmd.toPlainText()
            logging.debug("执行代码{}".format(ac))
            locNow = locals()
            l = locals()
            for i in locNow:
                l[i] = locNow[i]
            try:
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

        _()


ui = Ui_bilibili_get()


def main1():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.resize(1072, 647)

    def get_bv_from_paste():  # 从剪贴版中获取bilibili链接
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
            if a is not None and b != a:
                temp = ui.bv_line.text()
                t1 = temp + f"{a}, "
                ui.bv_line.setText(t1)
                b = a

    t1obj = thread.Thread(target=get_bvid)
    t1obj.start()
    # 获取cookie.json文件内容
    try:  # 包含了文件不存在，文件为空的情况
        cookie = setting['cookie']
        if cookie == '' or cookie == {}:
            raise ValueError("cookie值为空")
        ui.header['cookie'] = cookie
        ui.ztl.append("获取cookie成功")
        ui.usrJsonObj = get_user_info(ui.header)
        ui.userName.setText(ui.usrJsonObj['data']['uname'])
    except:
        pass
    MainWindow.show()
    a = app.exec_()
    sys.stdout.close()
    sys.stderr.close()
    os._exit(a)
    # sys.exit()


def main2():
    if len(sys.argv) > 1:
        pass
    app = QApplication(sys.argv)
    logging.debug("程序启动成功")  # 关于好像logging没有输出的这件事
    w = QWidget()
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
        cookie = setting['cookie']
        if cookie == '' or cookie == {}:
            raise ValueError("cookie值为空")
        ui.header['cookie'] = cookie
        ui.ztl.append("获取cookie成功")
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
    # sys.exit()


if __name__ == '__main__':
    setting["isFirst"] = False
    setting.save()
    if setting.get("isNeedBackground"):
        main2()
    else:
        main1()
