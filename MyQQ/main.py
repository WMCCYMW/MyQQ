from threading import Thread
import Server
import socket

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
                request=str(self.connection.recv(1024).decode())
                # 登录
                if request=="login":
                    name, isSucceed = Server.LoginSever(self)
                    self.name = name
                    if(isSucceed == 1): # 添加到字典和列表中
                        # 获取自己的id
                        self.id = Server.search_one_by_name(name)[0]
                        connection_user[id] = self.connection
                        online_connection.append(id)

                # 注册
                elif request=="register":
                    Server.RegistSever(self)

                # 获取好友列表
                elif request == "get_friend_list":
                    state = int(self.connection.recv(1024).decode())
                    Server.get_list(self, state)

                # 查找用户
                elif request == "search_one":
                    name = str(connection.recv(1024).decode())
                    Server.find_user(name)

                # 添加好友
                elif request == "add_friend":
                    Server.add_friend(self)

                # 处理好友申请
                elif request == "handle_friend_application":
                    args = int(self.connection.recv(1024).decode())
                    print(args)
                    Server.handle_friend_application(self, args)
                    # result如果为1，则成功处理好友申请，如果为3则为数据库错误

                # 给好友发消息
                elif request == "send_to_friend":
                    friend_name = str(connection.recv(1024),encoding="utf-8")
                    friend_id = Server.search_one_by_name(friend_name)
                    if friend_id in online_connection:
                        connection.sendall(bytes(str("成功"), "utf-8"))
                        friend_socket = connection_user[friend_id]
                        Server.send_to_friend(self, friend_socket)
                    else:
                        # 发送失败消息
                        connection.sendall(bytes(str("好友未在线"), "utf-8"))




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
        listener.bind(('192.168.0.102',3456))
        listener.listen(20)
        while True :
            connection,address=listener.accept()
            print(str(address)+"连接成功")
            ConnectionHandler(connection,address).start()
    except Exception as e:
        print("服务器错误"+str(e))





