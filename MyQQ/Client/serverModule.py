import socket
import MessageQueue
import json
import login
import mainWindow
import chat
ss=socket.socket(socket.AF_INET)

def Reciver(clientsocket):
    while True:
        response_json= str(clientsocket.recv(1024),encoding='utf-8')
        response=json.loads(response_json)
        response_name = response[0]


        if response_name == "receive_from_friend": # 如果是私聊信息，则写入文件
            friend_id = response[1] # 来源id
            time = response[2] # 发送时间
            message = response[3] # 消息内容
            file = open("/messages/"+ login.LoginInterface.self_id +"/"+ friend_id +"_messages", "a") # 历史消息文件格式： /messages/selfId/friendId_messages
            file.write("<1><" + time + ">" + message + "\n") # 第一个<1>代表是好友发送的
            #.flush()
            file.close()
                #提醒在对应的位置亮红点
            mainWindow.MainWindow.on_receive_new_message(friend_id)
            #自动刷新聊天框
            chat.ChatInterface.message_reminder.emit(friend_id)

        elif response_name == "get_friend_application": # 如果是好友申请信息，则给个小红点
            '''
                在对应的位置亮小红点
           '''
        else:
            #其余的，则加入消息队列
            MessageQueue.mq.put(response)
            

