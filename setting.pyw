import os
import sys
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from func import Setting
from time import sleep
s = Setting('setting.json')
s.init(['Qss', 'cookie', 'isBBDown', 'isCookieExists', 'isFirst', 'isLogin', 'isNeedBackground', 'isNeedLogin', 'playerEverytime', 'startSetting',
       'thread', 'mostSearch'], ['C:/Users/lpy/Desktop/bilibili-api/bin/style/style.qss', '', False, False, False, True, False, True, False, False, False, 5])
s.saveEnd()


class Ui_Setting(object):
    s = Setting('setting.json')

    def setupUi(self, Setting):
        Setting.setObjectName("Setting")
        Setting.resize(663, 404)
        Setting.setStyleSheet("""/*
Material Dark Style Sheet for QT Applications
Author: Jaime A. Quiroga P.
Inspired on https://github.com/jxfwinter/qt-material-stylesheet
Company: GTRONICK
Last updated: 04/12/2018, 15:00.
Available at: https://github.com/GTRONICK/QSS/blob/master/MaterialDark.qss
*/
QMainWindow {
    background-color: #1e1d23;
}

QDialog {
    background-color: #1e1d23;
}

QColorDialog {
    background-color: #1e1d23;
}

QTextEdit {
    background-color: #1e1d23;
    color: #a9b7c6;
}

QPlainTextEdit {
    selection-background-color: #007b50;
    background-color: #1e1d23;
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: transparent;
    border-width: 1px;
    color: #a9b7c6;
}

QPushButton {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: transparent;
    border-width: 1px;
    border-style: solid;
    color: #a9b7c6;
    padding: 2px;
    background-color: #1e1d23;
}

QPushButton::default {
    border-style: inset;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: #04b97f;
    border-width: 1px;
    color: #a9b7c6;
    padding: 2px;
    background-color: #1e1d23;
}

QToolButton {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: #04b97f;
    border-bottom-width: 1px;
    border-style: solid;
    color: #a9b7c6;
    padding: 2px;
    background-color: #1e1d23;
}

QToolButton:hover {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: #37efba;
    border-bottom-width: 2px;
    border-style: solid;
    color: #FFFFFF;
    padding-bottom: 1px;
    background-color: #1e1d23;
}

QPushButton:hover {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: #37efba;
    border-bottom-width: 1px;
    border-style: solid;
    color: #FFFFFF;
    padding-bottom: 2px;
    background-color: #1e1d23;
}

QPushButton:pressed {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: #37efba;
    border-bottom-width: 2px;
    border-style: solid;
    color: #37efba;
    padding-bottom: 1px;
    background-color: #1e1d23;
}

QPushButton:disabled {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: #808086;
    border-bottom-width: 2px;
    border-style: solid;
    color: #808086;
    padding-bottom: 1px;
    background-color: #1e1d23;
}

QLineEdit {
    border-width: 1px;
    border-radius: 4px;
    border-color: rgb(58, 58, 58);
    border-style: inset;
    padding: 0 8px;
    color: #a9b7c6;
    background: #1e1d23;
    selection-background-color: #007b50;
    selection-color: #FFFFFF;
}

QLabel {
    color: #a9b7c6;
}

QLCDNumber {
    color: #37e6b4;
}

QProgressBar {
    text-align: center;
    color: rgb(240, 240, 240);
    border-width: 1px;
    border-radius: 10px;
    border-color: rgb(58, 58, 58);
    border-style: inset;
    background-color: #1e1d23;
}

QProgressBar::chunk {
    background-color: #04b97f;
    border-radius: 5px;
}

QMenuBar {
    background-color: #1e1d23;
}

QMenuBar::item {
    color: #a9b7c6;
    spacing: 3px;
    padding: 1px 4px;
    background: #1e1d23;
}

QMenuBar::item:selected {
    background: #1e1d23;
    color: #FFFFFF;
}

QMenu::item:selected {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: #04b97f;
    border-bottom-color: transparent;
    border-left-width: 2px;
    color: #FFFFFF;
    padding-left: 15px;
    padding-top: 4px;
    padding-bottom: 4px;
    padding-right: 7px;
    background-color: #1e1d23;
}

QMenu::item {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: transparent;
    border-bottom-width: 1px;
    border-style: solid;
    color: #a9b7c6;
    padding-left: 17px;
    padding-top: 4px;
    padding-bottom: 4px;
    padding-right: 7px;
    background-color: #1e1d23;
}

QMenu {
    background-color: #1e1d23;
}

QTabWidget {
    color: rgb(0, 0, 0);
    background-color: #1e1d23;
}

QTabWidget::pane {
    border-color: rgb(77, 77, 77);
    background-color: #1e1d23;
    border-style: solid;
    border-width: 1px;
    border-radius: 6px;
}

QTabBar::tab {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: transparent;
    border-bottom-width: 1px;
    border-style: solid;
    color: #808086;
    padding: 3px;
    margin-left: 3px;
    background-color: #1e1d23;
}

QTabBar::tab:selected,
QTabBar::tab:last:selected,
QTabBar::tab:hover {
    border-style: solid;
    border-top-color: transparent;
    border-right-color: transparent;
    border-left-color: transparent;
    border-bottom-color: #04b97f;
    border-bottom-width: 2px;
    border-style: solid;
    color: #FFFFFF;
    padding-left: 3px;
    padding-bottom: 2px;
    margin-left: 3px;
    background-color: #1e1d23;
}

QCheckBox {
    color: #a9b7c6;
    padding: 2px;
}

QCheckBox:disabled {
    color: #808086;
    padding: 2px;
}

QCheckBox:hover {
    border-radius: 4px;
    border-style: solid;
    padding-left: 1px;
    padding-right: 1px;
    padding-bottom: 1px;
    padding-top: 1px;
    border-width: 1px;
    border-color: rgb(87, 97, 106);
    background-color: #1e1d23;
}

QCheckBox::indicator:checked {

    height: 10px;
    width: 10px;
    border-style: solid;
    border-width: 1px;
    border-color: #04b97f;
    color: #a9b7c6;
    background-color: #04b97f;
}

QCheckBox::indicator:unchecked {

    height: 10px;
    width: 10px;
    border-style: solid;
    border-width: 1px;
    border-color: #04b97f;
    color: #a9b7c6;
    background-color: transparent;
}

QRadioButton {
    color: #a9b7c6;
    background-color: #1e1d23;
    padding: 1px;
}

QRadioButton::indicator:checked {
    height: 10px;
    width: 10px;
    border-style: solid;
    border-radius: 5px;
    border-width: 1px;
    border-color: #04b97f;
    color: #a9b7c6;
    background-color: #04b97f;
}

QRadioButton::indicator: !checked {
    height: 10px;
    width: 10px;
    border-style: solid;
    border-radius: 5px;
    border-width: 1px;
    border-color: #04b97f;
    color: #a9b7c6;
    background-color: transparent;
}

QStatusBar {
    color: #027f7f;
}

QSpinBox {
    color: #a9b7c6;
    background-color: #1e1d23;
}

QDoubleSpinBox {
    color: #a9b7c6;
    background-color: #1e1d23;
}

QTimeEdit {
    color: #a9b7c6;
    background-color: #1e1d23;
}

QDateTimeEdit {
    color: #a9b7c6;
    background-color: #1e1d23;
}

QDateEdit {
    color: #a9b7c6;
    background-color: #1e1d23;
}

QComboBox {
    color: #a9b7c6;
    background: #1e1d23;
}

QComboBox:editable {
    background: #1e1d23;
    color: #a9b7c6;
    selection-background-color: #1e1d23;
}

QComboBox QAbstractItemView {
    color: #a9b7c6;
    background: #1e1d23;
    selection-color: #FFFFFF;
    selection-background-color: #1e1d23;
}

QComboBox: !editable:on,
QComboBox::drop-down:editable:on {
    color: #a9b7c6;
    background: #1e1d23;
}

QFontComboBox {
    color: #a9b7c6;
    background-color: #1e1d23;
}

QToolBox {
    color: #a9b7c6;
    background-color: #1e1d23;
}

QToolBox::tab {
    color: #a9b7c6;
    background-color: #1e1d23;
}

QToolBox::tab:selected {
    color: #FFFFFF;
    background-color: #1e1d23;
}

QScrollArea {
    color: #FFFFFF;
    background-color: #1e1d23;
}

QSlider::groove:horizontal {
    height: 5px;
    background: #04b97f;
}

QSlider::groove:vertical {
    width: 5px;
    background: #04b97f;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
    border: 1px solid #5c5c5c;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}

QSlider::handle:vertical {
    background: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #b4b4b4, stop:1 #8f8f8f);
    border: 1px solid #5c5c5c;
    height: 14px;
    margin: 0 -5px;
    border-radius: 7px;
}

QSlider::add-page:horizontal {
    background: white;
}

QSlider::add-page:vertical {
    background: white;
}

QSlider::sub-page:horizontal {
    background: #04b97f;
}

QSlider::sub-page:vertical {
    background: #04b97f;
}
/* 感谢提供此模板的大佬 */""")
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

        self.pushButton.clicked.connect(self.commit)
        self.QSSfile.clicked.connect(self.openFile)

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
            None, "Open File", "./bin/style/", "All Files(*);;Wav(*.wav);;Txt (*.txt)")
        if fname:
            self.s['Qss'] = fname

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
            self.label.setText("设置成功")
            self.s.saveEnd()

            def _():
                sleep(5)
                os._exit(0)
            t = Thread(target=_)
            t.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Setting()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
