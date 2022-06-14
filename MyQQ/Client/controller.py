import sys
import signup
import login
import mainWindow
import chat
import search
import friendRequest
from PyQt5 import QtWidgets, uic
from functools import partial


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
        try:
            self.login_window.close()
        except:
            pass
        try:
            self.searchWindow.close()
        except:
            pass
        try:
            self.friendReqWindow.close()
        except:
            pass

        self.mainWindow = mainWindow.MainWindow(username,userid)
        self.mainWindow.open_chat_window.connect(self.open_chat_window)
        self.mainWindow.switch_to_search_window.connect(self.switch_to_search_window)
        self.mainWindow.switch_to_friend_req_window.connect(self.switch_to_friend_req_window)
        self.mainWindow.show()



    def open_chat_window(self, friend_name: str,friend_id:int):
        self.chat_windows[friend_id] = chat.ChatInterface(friend_name,friend_id)
        self.chat_windows[friend_id].message_reminder.connect(self.chat_windows[friend_id].flush_chat_history)
        self.chat_windows[friend_id].show()

    def switch_to_search_window(self):
        self.mainWindow.close()
        self.searchWindow = search.SearchInterface(self.friend_list)
        self.searchWindow.switch_to_main_window.connect(partial(self.switch_to_main_window, self.user_name))

    def switch_to_friend_req_window(self):
        self.mainWindow.close()
        self.friendReqWindow = friendRequest.FriendReqInterface(self.request_list)
        self.friendReqWindow.switch_to_main_window.connect(partial(self.switch_to_main_window, self.user_name))

    def on_received_message(self, receiver: str, message: str, sender: str):
        self.chat_windows[receiver].on_receive_message(sender, message)
