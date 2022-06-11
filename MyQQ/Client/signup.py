from PyQt5 import QtWidgets, uic, QtCore
import general
import serverModule
import MessageQueue
import json
class SignupInterface(QtWidgets.QMainWindow):
    switch_to_login_window = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi("signup.ui", self)
        self.signup.clicked.connect(self.on_signup_button_clicked)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def on_signup_button_clicked(self):
        signup_id = self.username.text()
        password = self.password.text()
        confirm_password = self.confirmPassword.text()
        if password == '' or confirm_password == '' or signup_id == '':
            print("empty")
        elif password == confirm_password:
           # print(signup_id, password)
           pkt=("register",signup_id,password)
           pkt_json=json.dumps(pkt)
           serverModule.ss.sendall(pkt_json.encode())
           while True:
               response=MessageQueue.mq.get(True)
               if(response[0]=='register'and response[1]=='1'):
                   self.switch_to_login()
                   break
               elif(response[0]=='register'and response[1]!='1'):
                   print("failed")
                   break
               MessageQueue.mq.put(response,True)
        else:
            print("password not the same")

    def switch_to_login(self):
        self.switch_to_login_window.emit()
