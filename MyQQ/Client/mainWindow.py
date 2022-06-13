from functools import partial
import serverModule
import json
import MessageQueue
from PyQt5 import QtWidgets, uic, QtCore


class MainWindow(QtWidgets.QMainWindow):
    friends_name_list = ["f1", "f2", "f3", "f4", "f5",
                         "f6", "f7", "f8", "f9", "f10",
                         "f11", "f12", "f13", "f14", "f15",
                         "f16", "f17", "f18", "f19", "f20", "f21", "f22"]
    friends_new_message_status = []
    current_friend_page = 0
    open_chat_window = QtCore.pyqtSignal(str,int)
    username = ""

    def __init__(self, username: str,userid):
        super().__init__()
        self.username = username
        uic.loadUi("mainWindow.ui", self)
        self.user_label.setText("欢迎" + username)
        #发送获取好友列表请求
        pkt = ("get_friend_list", '1')
        pkt_json = json.dumps(pkt)
        serverModule.ss.send(pkt_json.encode())
        #接收好友列表
        MainWindow.friends_name_list.clear()
        while True:
            response = MessageQueue.mq.get(True)
            if (response[0] == "get_friend_list" and (response[1] == "无匹配项" or response[1] == "数据库错误")):
                print(response[1])
                break
            else:
                # 返回成功，更新列表
                for i in response[2:]:
                    MainWindow.friends_name_list.append(i)
                break
            MessageQueue.mq.put(response, True)
        for i in range(self.friends_name_list.__len__()):
            MainWindow.friends_new_message_status.append(False)
        self.load_friend()
        self.prev_page.clicked.connect(self.on_prev_button_clicked)
        self.next_page.clicked.connect(self.on_next_button_clicked)

    def load_friend(self):
        print(self.current_friend_page)
        friend_button_map = {0: self.friend_1, 1: self.friend_2, 2: self.friend_3, 3: self.friend_4,
                             4: self.friend_5, 5: self.friend_6, 6: self.friend_7, 7: self.friend_8,
                             8: self.friend_9, 9: self.friend_10}
        for i in range(10):
            friend_button_map[i].setStyleSheet("background-color: white")

        if self.friends_name_list.__len__() > (self.current_friend_page + 1) * 10:

            for i in range(10):
                friend_button_map[i].setText(self.friends_name_list[self.current_friend_page * 10 + i][1])
                friend_button_map[i].setEnabled(True)
                try:
                    friend_button_map[i].clicked.disconnect()
                except TypeError:
                    pass
                friend_button_map[i].clicked.connect(
                    partial(self.on_friend_button_clicked, self.current_friend_page * 10 + i))
                #来新消息了按钮变红
                if self.friends_new_message_status[self.current_friend_page * 10 + i]:
                    friend_button_map[i].setStyleSheet("background-color: red")
                # friend_button_map[i].clicked.connect(
                #     (lambda temp=i: lambda: self.on_friend_button_clicked(
                #         self.current_friend_page * 10 + temp))())

        else:
            for i in range(10):
                if self.friends_name_list.__len__() > self.current_friend_page * 10 + i:
                    try:
                        friend_button_map[i].clicked.disconnect()
                    except TypeError:
                        pass
                    friend_button_map[i].setText(self.friends_name_list[self.current_friend_page * 10 + i][1])
                    friend_button_map[i].setEnabled(True)
                    if self.friends_new_message_status[self.current_friend_page * 10 + i]:
                        friend_button_map[i].setStyleSheet("background-color: red")
                    friend_button_map[i].clicked.connect(
                        partial(self.on_friend_button_clicked, self.current_friend_page * 10 + i))
                else:
                    try:
                        friend_button_map[i].clicked.disconnect()
                    except TypeError:
                        pass
                    friend_button_map[i].setEnabled(False)
                    friend_button_map[i].setText("")

    def on_friend_button_clicked(self, friend_pos: int):
        print("friend position in list:" + MainWindow.friends_name_list[friend_pos][1])
        MainWindow.friends_new_message_status[friend_pos] = False
        self.sender().setStyleSheet("background-color: white")
        QtWidgets.QApplication.processEvents()
        self.show()
        self.open_chat_window.emit(self.friends_name_list[friend_pos][1],self.friends_name_list[friend_pos][0])

    def on_next_button_clicked(self):
        if self.friends_name_list.__len__() > (self.current_friend_page + 1) * 10:
            self.current_friend_page += 1
            self.load_friend()
            QtWidgets.QApplication.processEvents()
            self.show()

    def on_prev_button_clicked(self):
        if self.current_friend_page > 0:
            self.current_friend_page -= 1
            self.load_friend()
            QtWidgets.QApplication.processEvents()
            self.show()

    def on_receive_new_message(friend_id: int):
        for i, (f, f_status) in enumerate(zip(MainWindow.friends_name_list, MainWindow.friends_new_message_status)):
            if f[0] == friend_id:
                MainWindow.friends_new_message_status[i] = True
