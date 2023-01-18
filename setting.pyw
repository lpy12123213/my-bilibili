import os
import sys
from threading import Thread

import qdarkstyle
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from module.func import Setting
from time import sleep

s = Setting('setting.json')

s.init_({'Qss': './bin/style/style.qss', 'cookie': {}, 'downloadAll': True,
         'isBBDown': False, 'isCookieExists': False, 'isDebugging': False, 'isFirst': False, 'isLogin': True,
         'isNeedBackground': False, 'isNeedLogin': True, 'mostSearch': 5, 'path': '.', 'playerEverytime': False,
         'proxy': {'http': '', 'https': ''}, 'startSetting': False, 'thread': True, "whoToChoose": "general",
         "isPY": True})
s['cookie'] = ''
s.saveEnd()


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def readQssFile(qss_file_name):
        with open(qss_file_name, 'r', encoding='UTF-8') as file:
            return file.read()


if s['Qss'].lower() != 'other':
    style_sheet = QSSLoader.readQssFile(s['Qss'])
else:
    style_sheet = (qdarkstyle.load_stylesheet_pyqt5())


class Ui_Setting(object):
    s = Setting('setting.json')

    def setupUi(self, Setting):
        Setting.setObjectName("Setting")
        Setting.resize(663, 404)
        Setting.setStyleSheet(style_sheet)
        self.pushButton = QtWidgets.QPushButton(Setting)
        self.pushButton.setGeometry(QtCore.QRect(560, 360, 93, 29))
        self.pushButton.setStyleSheet("border-radius\n"
                                      "border-top-left-radius\n"
                                      "border-top-right-radius\n"
                                      "border-bottom-left-radius\n"
                                      "border-bottom-right-radius")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Setting)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 581, 331))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.isNeedBackground = QtWidgets.QCheckBox(
            self.horizontalLayoutWidget)
        self.isNeedBackground.setEnabled(True)
        self.isNeedBackground.setStyleSheet("border-radius\n"
                                            "        border-top-left-radius\n"
                                            "        border-top-right-radius\n"
                                            "        border-bottom-left-radius\n"
                                            "        border-bottom-right-radius")
        self.isNeedBackground.setChecked(True)
        self.isNeedBackground.setAutoRepeat(False)
        self.isNeedBackground.setAutoExclusive(False)
        self.isNeedBackground.setTristate(False)
        self.isNeedBackground.setObjectName("isNeedBackground")
        self.verticalLayout.addWidget(self.isNeedBackground)
        self.isNeedLogin = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.isNeedLogin.setChecked(True)
        self.isNeedLogin.setObjectName("isNeedLogin")
        self.verticalLayout.addWidget(self.isNeedLogin)
        self.isLogin = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.isLogin.setChecked(True)
        self.isLogin.setObjectName("isLogin")
        self.verticalLayout.addWidget(self.isLogin)
        self.isBBDown = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.isBBDown.setEnabled(False)
        self.isBBDown.setObjectName("isBBDown")
        self.verticalLayout.addWidget(self.isBBDown)
        self.playerEverytime = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.playerEverytime.setEnabled(False)
        self.playerEverytime.setObjectName("playerEverytime")
        self.verticalLayout.addWidget(self.playerEverytime)
        self.start = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.start.setEnabled(False)
        self.start.setObjectName("start")
        self.verticalLayout.addWidget(self.start)
        self.threadOne = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.threadOne.setEnabled(False)
        self.threadOne.setObjectName("threadOne")
        self.verticalLayout.addWidget(self.threadOne)
        self.downloadAll = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        # self.downloadAll.setEnabled(False)
        self.downloadAll.setObjectName("downloadAll")
        self.verticalLayout.addWidget(self.downloadAll)
        self.cookie = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.cookie.setStyleSheet("border-top-left-radius:10px;\n"
                                  "border-top-right-radius:10px;\n"
                                  "border-bottom-left-radius:10px;\n"
                                  "border-bottom-right-radius:10px;\n"
                                  "color: rgb(170, 255, 255);\n"
                                  "border:1px solid rgb(255,255,255);\n"
                                  "border-radius:20px;")
        self.cookie.setText("")
        self.cookie.setFrame(False)
        self.cookie.setClearButtonEnabled(True)
        self.cookie.setObjectName("cookie")
        self.verticalLayout.addWidget(self.cookie)
        self.mostSearch = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.mostSearch.setObjectName("mostSearch")
        self.mostSearch.setStyleSheet("border-top-left-radius:10px;\n"
                                      "border-top-right-radius:10px;\n"
                                      "border-bottom-left-radius:10px;\n"
                                      "border-bottom-right-radius:10px;\n"
                                      "color: rgb(170, 255, 255);\n"
                                      "border:1px solid rgb(255,255,255);\n"
                                      "border-radius:20px;")
        self.verticalLayout.addWidget(self.mostSearch)
        self.QSSfile = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.QSSfile.setFlat(True)
        self.QSSfile.setObjectName("QSSfile")
        self.verticalLayout.addWidget(self.QSSfile)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(Setting)
        QtCore.QMetaObject.connectSlotsByName(Setting)

        self.isNeedBackground.setChecked(self.s['isNeedBackground'])
        self.isNeedLogin.setChecked(self.s['isNeedLogin'])
        self.isLogin.setChecked(self.s['isLogin'])
        self.playerEverytime.setChecked(self.s['playerEverytime'])
        self.start.setChecked(self.s['startSetting'])
        self.downloadAll.setChecked(self.s['thread'])
        self.cookie.setText(self.s['cookie'])
        self.isBBDown.setChecked(self.s['isBBDown'])
        self.mostSearch.setText(str(self.s['mostSearch']))

        self.pushButton.clicked.connect(self.commit)
        self.QSSfile.clicked.connect(self.openFile)
        self.setUI()

    def retranslateUi(self, Setting):
        _translate = QtCore.QCoreApplication.translate
        Setting.setWindowTitle(_translate("Setting", "Widget"))
        self.pushButton.setText(_translate("Setting", "Commit!"))
        self.isNeedBackground.setText(_translate("Setting", "需要背景"))
        self.isNeedLogin.setText(_translate("Setting", "需要登录"))
        self.isLogin.setText(_translate("Setting", "需要登录下载"))
        self.isBBDown.setText(_translate("Setting", "使用BBDown下载（未完成）"))
        self.playerEverytime.setText(_translate("Setting", "每次启动播放器（未完成）"))
        self.start.setText(_translate("Setting", "开机启动（不建议）"))
        self.threadOne.setText(_translate("Setting", "下载启用多线程"))
        self.downloadAll.setText(_translate("Setting", "下载多个视频（暂不开启）"))
        self.cookie.setPlaceholderText(_translate("Setting", "cookie值（不填为空）"))
        self.mostSearch.setPlaceholderText(_translate("Setting", "最多搜索页面"))
        self.QSSfile.setText(_translate("Setting", "选择QSS文件"))

    def openFile(self):
        # 如果添加一个内容则需要加两个分号
        fname, ftype = QFileDialog.getOpenFileName(
            None, "Open File", "./bin/style/", "All Files(*)")
        if fname:
            self.s['Qss'] = fname
            print(1)

    def commit(self):
        try:
            self.s['isNeedBackground'] = self.isNeedBackground.isChecked()
            self.s['isNeedLogin'] = self.isNeedLogin.isChecked()
            self.s['isLogin'] = self.isLogin.isChecked()
            self.s['isBBDown'] = self.isBBDown.isChecked()
            self.s['cookie'] = self.cookie.text()
            self.s['startSetting'] = self.start.isChecked()
            self.s['thread'] = self.downloadAll.isChecked()
            self.s['mostSearch'] = int(self.mostSearch.text())
        finally:
            # self.label.setText("设置成功")
            self.s.saveEnd()

            def _():
                sleep(5)
                os._exit(0)

            t = Thread(target=_)
            t.start()

    def setUI(self):
        s = self.s.set
        self.isNeedBackground.setChecked(s['isNeedBackground'])
        self.isLogin.setChecked(s['isLogin'])
        self.isNeedLogin.setChecked(s['isNeedLogin'])
        self.playerEverytime.setChecked(s['playerEverytime'])
        # self.threadOne.setChecked(s['threadOne'])
        self.downloadAll.setChecked(s['downloadAll'])
        self.isBBDown.setChecked(s['isBBDown'])
        self.start.setChecked(s['startSetting'])
        self.cookie.setText(s["cookie"] if s["cookie"] != {} or s["cookie"] != "" else "")
        self.mostSearch.setText(str(s["mostSearch"]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Setting()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
