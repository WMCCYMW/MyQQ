import json
from functools import partial

from PyQt5 import QtWidgets, uic, QtCore

from MyQQ.Client import serverModule


class FriendReqInterface(QtWidgets.QMainWindow):
    friend_request_list = []
    has_processed_friend_req = []
    current_request_page = 0
    switch_to_main_window = QtCore.pyqtSignal()

    def __init__(self, friend_request_list: list,socket,queue):
        super().__init__()
        self.friend_request_list = friend_request_list
        self.ss=socket
        self.q=queue
        for i in enumerate(friend_request_list):
            self.has_processed_friend_req.append(False)
        uic.loadUi("friendRequest.ui", self)
        self.add_button_map = {0: self.addButton_1, 1: self.addButton_2, 2: self.addButton_3, 3: self.addButton_4,
                               4: self.addButton_5, 5: self.addButton_6}
        self.decline_button_map = {0: self.declineButton_1, 1: self.declineButton_2, 2: self.declineButton_3,
                                   3: self.declineButton_4, 4: self.declineButton_5, 5: self.declineButton_6}
        self.friend_label_map = {0: self.friend_1, 1: self.friend_2, 2: self.friend_3, 3: self.friend_4,
                                 4: self.friend_5,
                                 5: self.friend_6,
                                 }
        self.prevPageButton.clicked.connect(self.on_prev_page_button_clicked)
        self.nextPageButton.clicked.connect(self.on_next_page_button_clicked)

        self.load_request()
        self.show()

    def load_request(self):
        # 把申请人标签与添加和拒绝按钮编号

        if self.friend_request_list.__len__() > (self.current_request_page + 1) * 6:
            for i in range(6):
                if self.has_processed_friend_req[self.current_request_page * 6 + i]:
                    self.add_button_map[i].setVisible(False)
                    self.decline_button_map[i].setVisible(False)
                    self.friend_label_map[i].setText("已处理")
                    continue
                self.friend_label_map[i].setText(self.friend_request_list[self.current_request_page * 6 + i][1])
                try:
                    self.add_button_map[i].clicked.disconnect()
                except TypeError:
                    pass
                try:
                    self.decline_button_map[i].clicked.disconnect()
                except TypeError:
                    pass
                self.add_button_map[i].setVisible(True)
                self.decline_button_map[i].setVisible(True)
                self.add_button_map[i].clicked.connect(
                    partial(self.on_add_button_clicked, self.current_request_page * 6 + i)
                )
                self.decline_button_map[i].clicked.connect(
                    partial(self.on_del_button_clicked, self.current_request_page * 6 + i)
                )
        else:
            for i in range(6):
                if self.friend_request_list.__len__() > self.current_request_page * 6 + i:
                    if self.has_processed_friend_req[self.current_request_page * 6 + i]:
                        self.add_button_map[i].setVisible(False)
                        self.decline_button_map[i].setVisible(False)
                        self.friend_label_map[i].setText("已处理")
                        continue
                    self.friend_label_map[i].setText(self.friend_request_list[self.current_request_page * 6 + i][1])
                    try:
                        self.add_button_map[i].clicked.disconnect()
                    except TypeError:
                        pass
                    try:
                        self.decline_button_map[i].clicked.disconnect()
                    except TypeError:
                        pass
                    self.add_button_map[i].setVisible(True)
                    self.decline_button_map[i].setVisible(True)
                    self.add_button_map[i].clicked.connect(
                        partial(self.on_add_button_clicked, self.current_request_page * 6 + i)
                    )
                    self.decline_button_map[i].clicked.connect(
                        partial(self.on_del_button_clicked, self.current_request_page * 6 + i)
                    )
                else:
                    self.friend_label_map[i].setText("")
                    try:
                        self.add_button_map[i].clicked.disconnect()
                    except TypeError:
                        pass
                    try:
                        self.decline_button_map[i].clicked.disconnect()
                    except TypeError:
                        pass
                    self.add_button_map[i].setVisible(False)
                    self.decline_button_map[i].setVisible(False)

    def on_add_button_clicked(self, request_pos: int):
        # 这里插入接受请求代码
        pkt = ("handle_friend_application", '1',self.friend_request_list[request_pos][0])
        pkt_json = json.dumps(pkt)
        self.ss.sendall(pkt_json.encode())
        pos_on_page = request_pos % 6
        print("added friend request pos:" + str(request_pos))
        #
        while True :
            response=self.q.get(True)
            if(response[0] == "handle_friend_application" and (response[1] == "3" )):
                self.show_error_message("数据库错误")
                break
            else:
                self.add_button_map[pos_on_page].setVisible(False)
                self.decline_button_map[pos_on_page].setVisible(False)
                self.friend_label_map[pos_on_page].setText("已接受")
                self.has_processed_friend_req[request_pos] = True
                QtWidgets.QApplication.processEvents()
                self.show()
                break
            self.q.put(response,True)
    def on_del_button_clicked(self, request_pos: int):
        # 这里插入拒绝请求代码
        pkt = ("handle_friend_application", '0', self.friend_request_list[request_pos][0])
        pkt_json = json.dumps(pkt)
        self.ss.sendall(pkt_json.encode())
        pos_on_page = request_pos % 6
        print("rejected friend request pos:" + str(request_pos))
        #
        while True:
            response = self.q.get(True)
            if (response[0] == "handle_friend_application" and (response[1] == "3")):
                self.show_error_message("数据库错误")
                break
            else:
                self.add_button_map[pos_on_page].setVisible(False)
                self.decline_button_map[pos_on_page].setVisible(False)
                self.friend_label_map[pos_on_page].setText("已拒绝")
                self.has_processed_friend_req[request_pos] = True
                QtWidgets.QApplication.processEvents()
                self.show()
                break
            self.q.put(response, True)


    def on_prev_page_button_clicked(self):
        if self.current_request_page > 0:
            self.current_request_page -= 1
            self.load_request()
            QtWidgets.QApplication.processEvents()
            self.show()

    def on_next_page_button_clicked(self):
        if self.friend_request_list.__len__() > (self.current_request_page + 1) * 6:
            self.current_request_page += 1
            self.load_request()
            QtWidgets.QApplication.processEvents()
            self.show()

    def on_return_button_clicked(self):
        self.switch_to_main_window.emit()

    def show_error_message(self, msg: str):
        tempBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", msg, QtWidgets.QMessageBox.Cancel)
        tempBox.exec_()
