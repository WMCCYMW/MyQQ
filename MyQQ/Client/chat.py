import datetime
import json
import os

from PyQt5 import QtWidgets, uic, QtCore, QtGui
import login
from MyQQ.Client import serverModule, mainWindow


class ChatInterface(QtWidgets.QMainWindow):
    message_reminder=QtCore.pyqtSignal(int)

    def __init__(self, friend_name: str,friend_id:int,socket,queue):
        super().__init__()
        self.ss=socket
        self.q=queue
        uic.loadUi("chat.ui", self)
        self.friend_name = friend_name
        self.friend_id=friend_id

        self.sendButton.clicked.connect(self.on_send_button_clicked)
        self.clearButton.clicked.connect(self.on_clear_button_clicked)
        self.load_chat_history()
        self.friendName.setText(friend_name)

    #刷新聊天记录
    def flush_chat_history(self,friend_id):
        if friend_id==self.friend_id:
            self.messageBrowser.clear()
            self.load_chat_history()

    def load_chat_history(self):
        self.messageBrowser.clear()
        # 判断文件夹存在，若不存在，则新建
        if not os.path.exists("messages\\"+str(login.LoginInterface.self_id)):
            os.makedirs("messages\\"+str(login.LoginInterface.self_id))
        # 判断文件
        if not os.path.exists("messages\\" + str(login.LoginInterface.self_id) + "\\" + str(self.friend_id) + "_messages.txt"):
            file = open("messages\\"+ str(login.LoginInterface.self_id) +"\\"+ str(self.friend_id) +"_messages.txt", "a")
            file.close()
        #在这里读取文件:
        file = open("messages\\" + str(login.LoginInterface.self_id) + "\\" + str(self.friend_id) + "_messages.txt", "r")  # 历史消息文件格式： /messages/selfId/friendId_messages.txt
        line = file.readline()
        while line != '':
            if ((line.startswith('<1>') or line.startswith('<0>'))): # 判断是否进行字符串的替换
                # 进行字符串的替换
                flag = line[1]
                if flag == '0': # 这是自己发的
                    new_line = line.replace('0', mainWindow.MainWindow.username, 1)
                elif flag == '1': # 这是friend发的
                    new_line = line.replace('1', self.friend_name, 1)
            else:
                if line.startswith('\t'):
                    new_line = line
                else:
                    new_line = '\t' + line
            # 使用self.messageBrowser.append()追加读取到的消息
            self.messageBrowser.append(new_line)
            line = file.readline()
        file.close()
        self.messageBrowser.moveCursor(QtGui.QTextCursor.End)
        QtWidgets.QApplication.processEvents()
        self.show()

    def on_send_button_clicked(self):
        message = self.messageEditor.toPlainText()
        if len(message) == 0:
            return
        else:
            # 发包
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pkt = ("send_to_friend", self.friend_id, now_time, message)
            pkt_json = json.dumps(pkt)
            self.ss.sendall(pkt_json.encode())
            # 判断是否发送成功
            while True:
                response = self.q.get(True)
                if (response[0] == "send_to_friend" and response[2] != "成功"):
                    self.show_error_message(response[2])
                    break
                else:
                    self.write_to_file(message)
                    self.load_chat_history()
                    break
                self.q.put(response, True)
            # self.messageBrowser.moveCursor(QtGui.QTextCursor.End)
            self.messageEditor.clear()
            # QtWidgets.QApplication.processEvents()
            # self.show()

    def on_receive_message(self, sender: str, message: str):
        self.messageBrowser.append(sender + "：")
        self.messageBrowser.append(message)
        self.write_to_file(message)
        QtWidgets.QApplication.processEvents()
        self.show()

    def write_to_file(self, message):
        time = datetime.datetime.now()
        file = open("messages\\" + str(login.LoginInterface.self_id) + "\\" + str(self.friend_id) + "_messages.txt", "a")  # 历史消息文件格式： /messages/selfId/friendId_messages
        file.write("<0><" + time.strftime("%Y-%m-%d %H:%M:%S") + ">:\n\t" + message + "\n")  # 第一个<1>代表是好友发送的：<1><time>\n\t你好 <0><time>我发的
        file.close()


    def on_clear_button_clicked(self):
        self.messageBrowser.clear()

    def show_error_message(self, msg: str):
        tempBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "警告", msg, QtWidgets.QMessageBox.Cancel)
        tempBox.exec_()
