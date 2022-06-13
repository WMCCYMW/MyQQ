from PyQt5 import QtWidgets, uic, QtCore, QtGui


class ChatInterface(QtWidgets.QMainWindow):

    def __init__(self, friend_name: str):
        super().__init__()
        uic.loadUi("chat.ui", self)
        self.friend_name = friend_name

        self.sendButton.clicked.connect(self.on_send_button_clicked)
        self.clearButton.clicked.connect(self.on_clear_button_clicked)
        self.load_chat_history()
        self.friendName.setText(friend_name)

    def load_chat_history(self):
        #在这里读取文件
        #使用self.messageBrowser.append()追加读取到的消息
        self.messageBrowser.moveCursor(QtGui.QTextCursor.End)
        QtWidgets.QApplication.processEvents()
        self.show()

    def on_send_button_clicked(self):
        message = self.messageEditor.toPlainText()
        if len(message) == 0:
            return
        else:
            self.messageBrowser.append("你：")
            self.messageBrowser.append(message)
            self.messageBrowser.moveCursor(QtGui.QTextCursor.End)
            self.messageEditor.clear()
            self.write_to_file(message)
            QtWidgets.QApplication.processEvents()
            self.show()

    def on_receive_message(self, sender: str, message: str):
        self.messageBrowser.append(sender + "：")
        self.messageBrowser.append(message)
        self.write_to_file(message)
        QtWidgets.QApplication.processEvents()
        self.show()

    def write_to_file(self, message):
        pass

    def on_clear_button_clicked(self):
        self.messageBrowser.clear()
