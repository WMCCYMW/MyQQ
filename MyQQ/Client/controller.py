import sys
import signup
import login
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

    # 从注册界面切换到登录界面

    def switch_to_login(self):
        self.signup_window.close()
        self.login_window = login.LoginInterface()
        self.login_window.show()
        self.login_window.switch_to_signup_window.connect(self.switch_to_signup)

    # 从登录界面切换到注册界面

    def switch_to_signup(self):
        self.login_window.close()
        self.signup_window = signup.SignupInterface()
        self.signup_window.show()
        self.signup_window.switch_to_login_window.connect(self.switch_to_login)

    # 从登录界面切换到聊天主界面（还没写）
    def switch_to_main_window(self):
        self.login_window.switch_to_main_window.connect(self.switch_to_main_window())
        pass
