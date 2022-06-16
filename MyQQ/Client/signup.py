from PyQt5 import QtWidgets, uic, QtCore
import general
import serverModule
import MessageQueue
import json
class SignupInterface(QtWidgets.QMainWindow):
    switch_to_login_window = QtCore.pyqtSignal()

    def __init__(self, queue, socket):
        super().__init__()
        uic.loadUi("signup.ui", self)
        self.ss = socket
        self.q = queue
        self.signup.clicked.connect(self.on_signup_button_clicked)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def on_signup_button_clicked(self):
        signup_name = self.username.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()
        if password == '' or confirm_password == '' or signup_name == '':
            print("用户名或密码不可为空，请重新输入")
        elif password == confirm_password:
           # print(signup_id, password)
            pkt=("register",signup_name,password)
            pkt_json=json.dumps(pkt)
            self.ss.sendall(pkt_json.encode())
            while True:
                response = self.q.get(True)
                self.q.task_done()
                if (response[0] == "register" and (response[1] == "密码错误" or response[1] == "数据库错误")):
                    print(response[1])
                    break
                elif response[0] == "register" and response[1] != "密码错误" and response[1] != "数据库错误":
                    self.switch_to_login_window.emit()
                    break
                else:
                    self.q.put(response, True)
        else:
            print("两次输入密码不一致，请重新输入")

    def switch_to_login(self):
        self.switch_to_login_window.emit()
