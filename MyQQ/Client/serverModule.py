import os
import socket
import MessageQueue
import json
import login
import mainWindow


def Reciver(clientsocket,cont):
    while True:
        try:
            response_json= str(clientsocket.recv(1024),encoding='utf-8')
            response = json.loads(response_json)
        except:
            pass

        response_name = response[0]
        print(response)


        if response_name == "receive_from_friend": # 如果是私聊信息，则写入文件
            friend_id = response[1] # 来源id
            time = response[2] # 发送时间
            message = response[3] # 消息内容
            # 判断文件夹存在，若不存在，则新建
            if not os.path.exists("messages\\" + str(login.LoginInterface.self_id)):
                os.makedirs("messages\\" + str(login.LoginInterface.self_id))
            # 判断文件
            if not os.path.exists("messages\\" + str(login.LoginInterface.self_id) + "\\" + str(friend_id) + "_messages.txt"):
                file = open("messages\\" + str(login.LoginInterface.self_id) + "\\" + str(friend_id) + "_messages.txt","a")
                file.close()
            file = open("messages\\"+ str(login.LoginInterface.self_id) +"\\"+ str(friend_id) +"_messages.txt", "a") # 历史消息文件格式： /messages/selfId/friendId_messages
            file.write("<1><" + time + ">:\n\t" + message + "\n") # 第一个<1>代表是好友发送的：<1><time>\n\t你好 <0><time>我发的
            #.flush()
            file.close()
            #自动刷新聊天框
            try:
                cont.chat_windows[friend_id].message_reminder.emit(friend_id)
            except:
                # 提醒在对应的位置亮红点
                cont.mainWindow.message_reminder.emit(friend_id)

        elif response_name == "get_friend_application": # 如果是好友申请信息，则给个小红点
            '''
                在对应的位置亮小红点
            '''
            pass

        else:
            #其余的，则加入消息队列
            cont.q.put(response)
            

