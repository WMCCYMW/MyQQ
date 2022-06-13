import sys
import signup
import login
import mainWindow
import chat
from PyQt5 import QtWidgets, uic


# controller类，实现界面的切换

class Controller:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = login.LoginInterface()
        self.widget = QtWidgets.QStackedWidget()
        self.login_window = login.LoginInterface()
        self.login_window.show()
        self.login_window.switch_to_signup_window.connect(self.switch_to_signup)
        self.login_window.switch_to_main_window.connect(self.switch_to_main_window)
        self.chat_windows = {}


    # 从注册界面切换到登录界面

    def switch_to_login(self):
        self.signup_window.close()
        self.login_window = login.LoginInterface()
        self.login_window.show()
        self.login_window.switch_to_signup_window.connect(self.switch_to_signup)
        self.login_window.switch_to_main_window.connect(self.switch_to_main_window)

    # 从登录界面切换到注册界面

    def switch_to_signup(self):
        self.login_window.close()
        self.signup_window = signup.SignupInterface()
        self.signup_window.show()
        self.signup_window.switch_to_login_window.connect(self.switch_to_login)

    # 从登录界面切换到聊天主界面（还没写）
    def switch_to_main_window(self,username,userid):
        self.login_window.close()
        self.mainWindow = mainWindow.MainWindow(username,userid)
        self.mainWindow.open_chat_window.connect(self.open_chat_window)
        self.mainWindow.show()



    def open_chat_window(self, friend_name: str,friend_id:int):
        self.chat_windows[friend_name] = chat.ChatInterface(friend_name,friend_id)
        self.chat_windows[friend_name].show()

    def on_received_message(self, receiver: str, message: str, sender: str):
        self.chat_windows[receiver].on_receive_message(sender, message)
