import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
try:
    from func import Setting as _setting
except:
    from module.func import Setting as _setting

# 先来个窗口
setting = _setting('./setting.json')


class window1(QWidget):
    def __init__(self):
        super().__init__()
        self.cookie = {}
        self.setup()

    def setup(self):
        self.box = QVBoxLayout(self)  # 创建一个垂直布局来放控件
        self.btn_get = QPushButton('点击获取cookies')  # 创建一个按钮涌来了点击获取cookie
        self.btn_get.clicked.connect(self.get_cookie)  # 绑定按钮点击事件
        self.web = MyWebEngineView()  # 创建浏览器组件对象
        self.web.resize(800, 600)  # 设置大小
        self.web.load(QUrl("https://www.bilibili.com"))  # 打开百度页面来测试
        self.box.addWidget(self.btn_get)  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.web)  # 再放浏览器
        self.web.show()  # 最后让页面显示出来

    def get_cookie(self):
        self.cookie = self.web.get_cookie()
        print('获取到cookie: ', self.cookie, '\n')


# 创建自己的浏览器控件，继承自QWebEngineView
class MyWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(MyWebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}  # 存放cookie字典

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value  # 将cookie保存到字典里'

    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():  # 遍历字典
            cookie_str += (key + '=' + value + '; ')  # 将键值对拿出来拼接一下
        return cookie_str  # 返回拼接好的字符串


def open_web():
    my_application = QApplication(sys.argv)  # 创建QApplication类的实例
    main_demo = window1()
    main_demo.show()
    my_application.exec_()
    set = _setting('./setting.json')
    set['cookie'] = main_demo.cookie
    set.saveEnd()


if __name__ == '__main__':
    # global cookie
    my_application = QApplication(sys.argv)  # 创建QApplication类的实例
    main_demo = window1()
    main_demo.show()
    my_application.exec_()
    # return main_demo.cookie
    # 注意文件路径: 调用时在main.py文件中, 所以./setting.json是指main.py的上一位中
    setting.change("cookie", main_demo.cookie)
    setting.saveEnd()
    # subprocess.call("python main.py", shell=True)
'''————————————————
版权声明：本文为CSDN博主「做我的code吧」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/yueguangMaNong/article/details/81146816'''
