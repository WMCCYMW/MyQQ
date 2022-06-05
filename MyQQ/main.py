from threading import Thread
import Server
import socket

connection_user=dict() # value为连接的socket， key为用户名
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
                        connection_user[name] = self.connection
                        online_connection.append(name)
                # 注册
                elif request=="register": Server.RegistSever(self)
                # 获取好友列表
                elif request == "get_list":
                    state = int(self.connection.recv(1024).decode())
                    result = Server.get_list(self, state)
                    # 给客户端送过去还没写

                # 查找好友
                elif request == "search_one":
                    result = Server.search_one(self)
                    # 给客户端送过去还没写

                # 添加好友
                elif request == "add_friend":
                    Server.add_friend(self)
                # 处理好友申请
                elif request == "handle_friend_application":
                    args = int(self.connection.recv(1024).decode())
                    Server.handle_friend_application(self, args)
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
        listener.bind(('192.168.23.1',3456))
        listener.listen(20)
        while True :
            connection,address=listener.accept()
            print(str(address)+"连接成功")
            ConnectionHandler(connection,address).start()
    except Exception as e:
        print("服务器错误"+str(e))





