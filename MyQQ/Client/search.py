import json
from functools import partial
import serverModule
from PyQt5 import QtWidgets, uic, QtCore
import general
from MyQQ.Client import MessageQueue


class SearchInterface(QtWidgets.QMainWindow):
    switch_to_main_window = QtCore.pyqtSignal()

    def __init__(self, friend_list: list):
        super().__init__()
        # 传入好友列表
        self.friend_list = friend_list
        uic.loadUi("search.ui", self)
        self.returnButton.clicked.connect(self.on_return_button_clicked)
        self.searchButton.clicked.connect(self.on_search_button_clicked)
        self.addOrDelButton.setVisible(False)
        self.searchFailed.setText("")
        self.friendName.setText("")
        self.show()

    def on_search_button_clicked(self):
        search_name = self.searchText.text()
        # 搜索好友在好友列表中时，显示删除按钮，链接删除功能
        is_in_friend_list = False
        for i, friend_name in enumerate(self.friend_list):
            if search_name == friend_name[1]:
                self.display_delete_friend(i, search_name)
                is_in_friend_list = True
                break
        if not is_in_friend_list:
            # 不在列表中时查找，找到的话显示添加按钮/功能，没找到显示查找失败文字
            if self.search_friend(search_name):
                self.display_add_friend(search_name)
            else:
                self.display_not_found()

    def on_delete_friend_button_clicked(self, friend_pos, search_name):
        print("deleted friend" + search_name + "in pos" + str(friend_pos))

    def display_delete_friend(self, friend_pos, search_name):
        try:
            self.addOrDelButton.clicked.disconnect()
        except TypeError:
            pass
        self.addOrDelButton.setVisible(True)
        self.addOrDelButton.clicked.connect(
            partial(self.on_delete_friend_button_clicked, friend_pos, search_name))
        self.addOrDelButton.setText("删除")
        self.friendName.setText(search_name)
        self.searchFailed.setText("")
        QtWidgets.QApplication.processEvents()
        self.show()

    def display_add_friend(self, search_name):
        try:
            self.addOrDelButton.clicked.disconnect()
        except TypeError:
            pass
        self.addOrDelButton.setVisible(True)
        self.addOrDelButton.clicked.connect(
            partial(self.on_add_friend_button_clicked, search_name))
        self.addOrDelButton.setText("添加")
        self.friendName.setText(search_name)
        self.searchFailed.setText("")
        QtWidgets.QApplication.processEvents()
        self.show()

    def display_not_found(self):
        self.friendName.setText("")
        self.addOrDelButton.setVisible(False)
        self.searchFailed.setText("查无此人")
        QtWidgets.QApplication.processEvents()
        self.show()

    def search_friend(self, search_name) -> bool:
        #print("searched friend" + search_name)

        pkt = ("search_user", search_name)
        pkt_json = json.dumps(pkt)
        serverModule.ss.sendall(pkt_json.encode())
        while True :
            response=MessageQueue.mq.get(True)
            if(response[0] == "search_user" and (response[1] == "无匹配项" or response[1] == "数据库错误")):
                return False
            else:
            # 登录成功，更新自己的id
                return True
            MessageQueue.mq.put(response,True)
        return False
    def on_add_friend_button_clicked(self, search_name):
        pkt = ("add_friend", search_name)
        pkt_json = json.dumps(pkt)
        serverModule.ss.sendall(pkt_json.encode())
        while True :
            response=MessageQueue.mq.get(True)
            if(response[0] == "add_friend" and (response[1] == "3" )):
                self.show_error_message("数据库错误，发送失败")
                break
            else:
                break
            MessageQueue.mq.put(response,True)

    def on_return_button_clicked(self):
        self.switch_to_main_window.emit()

    def show_error_message(self, msg: str):
        tempBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", msg, QtWidgets.QMessageBox.Cancel)
        tempBox.exec_()
