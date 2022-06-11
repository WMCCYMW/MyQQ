from PyQt5 import QtWidgets, uic, QtCore
import general
import MessageQueue
import serverModule
import json

# 自己的id，默认未登录是-1
self_id = -1

class LoginInterface(QtWidgets.QMainWindow):
    switch_to_signup_window = QtCore.pyqtSignal()
    switch_to_main_window=QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.loginButton.clicked.connect(self.on_login_button_clicked)
        self.signupButton.clicked.connect(self.on_signup_button_clicked)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    # “重新链接”按钮被点时的操作
    def on_login_button_clicked(self):
        user_id = self.username.text()
        password = self.password.text()
        pkt = ("login", user_id, password)
        pkt_json = json.dumps(pkt)
        serverModule.ss.sendall(pkt_json.encode())
        while True :
            response=MessageQueue.mq.get(True)
            if(response[0] == "login" and (response[1] == "密码错误" or response[1] == "数据库错误")):
                print(response[1])
                break
            else:
                # 登录成功，更新自己的id
                self.self_id = response[1][0]
                self.switch_to_main_window()
                break
            MessageQueue.mq.put(response,True)

    # 注册被点时的操作
    def on_signup_button_clicked(self):
        self.switch_to_signup()

    # 向上级槽传递切换界面信号
    def switch_to_signup(self):
        self.switch_to_signup_window.emit()

    def switch_to_main(self):
        self.switch_to_main_window.emit()