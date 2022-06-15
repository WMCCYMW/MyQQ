import json
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
from MyQQ.Client import serverModule, MessageQueue


class Controller:
    def __init__(self,socket):
        self.ss=socket
        self.q=MessageQueue.mq
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = login.LoginInterface(self.q,self.ss)
        self.widget = QtWidgets.QStackedWidget()
        self.login_window = login.LoginInterface(self.q,self.ss)
        self.login_window.show()
        self.login_window.switch_to_signup_window.connect(self.switch_to_signup)
        self.login_window.switch_to_main_window.connect(self.switch_to_main_window)

        self.chat_windows = {}
        self.request_list = []
        self.user_name = ""
        self.user_id=""
        self.is_MainWindow_exist = False




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
        self.signup_window = signup.SignupInterface(self.q,self.ss)
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

        if not self.is_MainWindow_exist:
            self.is_MainWindow_exist = True
            self.mainWindow = mainWindow.MainWindow(username,userid,self.ss,self.q)
            self.user_name=username
            self.user_id=userid
            self.mainWindow.open_chat_window.connect(self.open_chat_window)
            self.mainWindow.switch_to_search_window.connect(self.switch_to_search_window)
            self.mainWindow.switch_to_friend_req_window.connect(self.switch_to_friend_req_window)
            self.mainWindow.message_reminder.connect(self.mainWindow.on_receive_new_message)
            self.mainWindow.show()



    def open_chat_window(self, friend_name: str,friend_id:int):
        try:
            self.chat_windows[friend_id] = chat.ChatInterface(friend_name,friend_id,self.ss,self.q)
            self.chat_windows[friend_id].message_reminder.connect(self.chat_windows[friend_id].flush_chat_history)
            self.chat_windows[friend_id].show()
        except:
            pass

    def switch_to_search_window(self):
        self.mainWindow.close()
        self.is_MainWindow_exist = False
        self.searchWindow = search.SearchInterface(mainWindow.MainWindow.friends_name_list,self.ss,self.q)
        self.searchWindow.switch_to_main_window.connect(partial(self.switch_to_main_window, self.user_name,self.user_id))

    def switch_to_friend_req_window(self):
        self.mainWindow.close()
        self.is_MainWindow_exist = False
        pkt = ("get_friend_list", 0)
        pkt_json = json.dumps(pkt)
        self.ss.send(pkt_json.encode())
        self.request_list.clear()
        while True :
            response=MessageQueue.mq.get(True)
            if(response[0] == "get_friend_list" and (response[1] == "数据库错误" )):
                self.show_error_message("数据库错误，发送失败")
                break
            else:
                for i in response[2:]:
                    self.request_list.append(i)
                break
            MessageQueue.mq.put(response,True)
        self.friendReqWindow = friendRequest.FriendReqInterface(self.request_list,self.ss,self.q)
        self.friendReqWindow.switch_to_main_window.connect(partial(self.switch_to_main_window, self.user_name,self.user_id))

    def on_received_message(self, receiver: str, message: str, sender: str):
        self.chat_windows[receiver].on_receive_message(sender, message)

    def show_error_message(self, msg:str):
        tempBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", msg, QtWidgets.QMessageBox.Cancel)
        tempBox.exec_()
