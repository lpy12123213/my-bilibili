import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Editor(QWebEngineView):
    def __init__(self, par):
        super().__init__(par)
        self.editor_flag = []

        # 这里是本地html路径,需根据实际情况进行修改.
        self.editor_index = (os.path.split(os.path.realpath(__file__))[
                             0]) + "./editor/index.html"
        self.load(QUrl.fromLocalFile(self.editor_index))

    def get_value(self):
        """设置编辑器内容"""
        self.page().runJavaScript(
            "monaco.editor.getModels()[0].getValue()", self.putValVar)
        return self.res

    def set_value(self, data):
        """获取编辑器内容"""
        import base64
        data = base64.b64encode(data.encode())
        data = data.decode()
        self.page().runJavaScript(
            "monaco.editor.getModels()[0].setValue(Base.decode('{}'))".format(data))

    def change_language(self, lan):
        """切换智能提示语言"""
        self.page().runJavaScript(
            "monaco.editor.setModelLanguage(monaco.editor.getModels()[0],'{}')".format(lan))

    def putValVar(self, res):
        self.res = res

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Editor(None)
    w.setWindowTitle('Editor')
    w.show()
    # sys.exit(app.exec_())
    ret = app.exec_()
    print(w.get_value())
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Editor(None)
    w.setWindowTitle('Editor')
    w.show()
    # sys.exit(app.exec_())
    ret = app.exec_()
    print(w.get_value())
