from threading import Thread
import Server
import socket
import json

connection_user=dict() # value为连接的socket， key为id
online_connection=list() # 在线用户的连接列表，用于群发消息

class ConnectionHandler(Thread):
    def __init__(self,connection,address):
        Thread.__init__(self)
        self.connection=connection
        self.address=address
    def run(self) :
        try:
            while True:
                pkt_json=str(self.connection.recv(1024).decode())
                pkt = json.loads(pkt_json)
                request = pkt[0]
                # 登录
                if request=="login":
                    name, isSucceed = Server.LoginSever(self, pkt)
                    self.name = name
                    if(isSucceed == 1): # 添加到字典和列表中
                        # 获取自己的id
                        self.id = Server.search_one_by_name(name)[0]
                        connection_user[self.id] = self.connection
                        online_connection.append(self.id)

                # 注册
                elif request=="register":
                    Server.RegistSever(self, pkt)

                # 获取好友列表
                elif request == "get_friend_list":
                    Server.get_friend_list(self, pkt)

                # 查找用户
                elif request == "search_user":
                    Server.find_user(self, pkt)

                # 添加好友
                elif request == "add_friend":
                    Server.add_friend(self, pkt)
                    # 给接收申请方发包，提示之
                    recipient_name = pkt[1]
                    recipient_id = Server.search_one_by_name(recipient_name)[0]
                    try:
                        recipient_socket = connection_user[recipient_id]
                        response = ("get_friend_application")
                        response_json = json.dumps(response)
                        recipient_socket.sendall(bytes(response_json, "utf-8"))
                    except:
                        pass

                # 处理好友申请
                elif request == "handle_friend_application":
                    Server.handle_friend_application(self, pkt)

                # 给好友发消息
                elif request == "send_to_friend":
                    friend_id = pkt[1]
                    response = list() # 给发出信息方以反馈
                    response.append("send_to_friend")
                    friend_name = Server.search_one_by_id(friend_id)[1]
                    response.append(friend_name)
                    if friend_id in online_connection:
                        response.append("成功")
                        response.append(pkt[2])
                        friend_socket = connection_user[friend_id]
                        Server.send_to_friend(self, friend_socket, pkt)
                    else:
                        # 发送失败消息
                        response.append("好友未在线")
                    response_json = json.dumps(response)
                    self.connection.sendall(bytes(response_json, "utf-8"))

                # 管理员：删除用户请求
                elif request == "delete_user":
                    Server.delete_user(self, pkt)

                # 管理员：展示信息请求
                elif request == "show_details":
                    Server.show_details(self)

                # 管理员：更改用户名
                elif request == "change_user_name":
                    Server.change_user_name(self, pkt)

                # 管理员：更改密码
                elif request == "change_user_pwd":
                    Server.change_user_pwd(self, pkt)






        except Exception as e:
            print(str(e))
            print(str(self.address)+"连接异常，准备关闭")
        finally:
            try:
                self.connection.close()
                online_connection.remove(self.connection)
                connection_user.pop()
            except:
                print("连接关闭失败")





if __name__=="__main__":
    try:
        listener=socket.socket(socket.AF_INET)
        listener.bind(('127.0.0.1',3457))
        listener.listen(20)
        print("服务器启动完毕")
        while True :
            connection,address=listener.accept()
            print(str(address)+"连接成功")
            ConnectionHandler(connection,address).start()
    except Exception as e:
        print("服务器错误"+str(e))





