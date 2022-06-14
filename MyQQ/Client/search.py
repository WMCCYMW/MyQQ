from functools import partial

from PyQt5 import QtWidgets, uic, QtCore
import general


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
        search_id = self.searchText.text()
        # 搜索好友在好友列表中时，显示删除按钮，链接删除功能
        is_in_friend_list = False
        for i, friend_name in enumerate(self.friend_list):
            if search_id == friend_name:
                self.display_delete_friend(i, search_id)
                is_in_friend_list = True
                break
        if not is_in_friend_list:
            # 不在列表中时查找，找到的话显示添加按钮/功能，没找到显示查找失败文字
            if self.search_friend(search_id):
                self.display_add_friend(search_id)
            else:
                self.display_not_found()

    def on_delete_friend_button_clicked(self, friend_pos, search_id):
        print("deleted friend" + search_id + "in pos" + str(friend_pos))

    def display_delete_friend(self, friend_pos, search_id):
        try:
            self.addOrDelButton.clicked.disconnect()
        except TypeError:
            pass
        self.addOrDelButton.setVisible(True)
        self.addOrDelButton.clicked.connect(
            partial(self.on_delete_friend_button_clicked, friend_pos, search_id))
        self.addOrDelButton.setText("删除")
        self.friendName.setText(search_id)
        self.searchFailed.setText("")
        QtWidgets.QApplication.processEvents()
        self.show()

    def display_add_friend(self, search_id):
        try:
            self.addOrDelButton.clicked.disconnect()
        except TypeError:
            pass
        self.addOrDelButton.setVisible(True)
        self.addOrDelButton.clicked.connect(
            partial(self.on_add_friend_button_clicked, search_id))
        self.addOrDelButton.setText("添加")
        self.friendName.setText(search_id)
        self.searchFailed.setText("")
        QtWidgets.QApplication.processEvents()
        self.show()

    def display_not_found(self):
        self.friendName.setText("")
        self.addOrDelButton.setVisible(False)
        self.searchFailed.setText("查无此人")
        QtWidgets.QApplication.processEvents()
        self.show()

    def search_friend(self, search_id) -> bool:
        print("searched friend" + search_id)
        return False

    def on_add_friend_button_clicked(self, search_id):
        print("added friend" + search_id)

    def on_return_button_clicked(self):
        self.switch_to_main_window.emit()
