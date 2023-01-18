from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import sys
from ua import ua
from random import choice
from func import Setting

headers = {
    'user-agent': choice(ua)
}
try:
    set = Setting("./setting.json", mode='r')
    # set = Setting("../setting.json", mode='r')
    headers['cookie'] = set['cookie']
except FileNotFoundError:
    raise OSError('cookie not found, please login first and write to setting.json')


class Ui_Widget(QMainWindow):
    def __init__(self):
        super(Ui_Widget, self).__init__()
        self.setupUi(self)

    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Widget)
        self.centralwidget.setObjectName("Widget")
        self.wgt_video = QVideoWidget(self.centralwidget)
        self.wgt_video.setGeometry(QtCore.QRect(0, 0, 800, 500))
        self.wgt_video.setObjectName("wgt_video")
        self.pushButton = QtWidgets.QPushButton(Widget)
        self.pushButton.setGeometry(QtCore.QRect(350, 560, 93, 29))
        self.pushButton.setObjectName("pushButton")
        Widget.setCentralWidget(self.centralwidget)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))
        self.pushButton.setText(_translate("Widget", "Start"))
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_video)
        self.pushButton.clicked.connect(self.openVideoFile)

    def openVideoFile(self):
        # 播放网络视频
        # self.player.setMedia(QMediaContent(QUrl.fromLocalFile("https://vd1.bdstatic.com/mda-hg6uempmez9u6mqi/sc/mda-hg6uempmez9u6mqi.mp4?auth_key=1562172911-0-0-4c22196ad1d0fcc49402d91336c999c5&bcevod_channel=searchbox_feed&pd=bjh&abtest=all")))
        # 选择本地视频播放
        self.player.setMedia(QMediaContent(
            QFileDialog.getOpenFileUrl()[0]))  # 选取本地视频文件
        self.player.play()  # 播放视频


def start():
    app = QApplication(sys.argv)
    video_gui = Ui_Widget()
    video_gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_gui = Ui_Widget()
    video_gui.show()
    sys.exit(app.exec_())
