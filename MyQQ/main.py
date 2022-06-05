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
                        # 获取自己的id
                        self.id = Server.search_one_by_name(name)[0]
                # 注册
                elif request=="register":
                    Server.RegistSever(self)

                # 获取好友列表
                elif request == "get_friend_list":
                    state = int(self.connection.recv(1024).decode())
                    result = Server.get_list(self, state)
                    if result == 3:
                        connection.sendall(bytes(str("数据库错误"), "utf-8"))
                    else:
                        connection.sendall(bytes(str("成功"), "utf-8"))
                        for subRes in result:
                            if(subRes[0] == self.id):
                                friend = Server.search_one_by_id(subRes[1])
                                friend_name = friend[1]
                                connection.sendall(bytes(str(friend_name), "utf-8"))
                            else:
                                friend_name = Server.search_one_by_id(subRes[0])[1]
                                connection.sendall(bytes(str(friend_name), "utf-8"))
                        connection.sendall(bytes(str("结束"), "utf-8")) # 要是有个name叫做"结束"就完蛋了。。。

                # 查找用户
                elif request == "search_one":
                    name = str(connection.recv(1024).decode())
                    result = Server.search_one_by_name(name)
                    if result == 3:
                        connection.sendall(bytes(str("数据库错误"), "utf-8"))
                    elif result == None:
                        connection.sendall(bytes(str("无匹配项"), "utf-8"))
                    else:
                        connection.sendall(bytes(str("成功"), "utf-8"))
                        connection.sendall(bytes(str(result[0]), "utf-8")) # 发送id
                        connection.sendall(bytes(str(result[1]), "utf-8")) # 发送name

                # 添加好友
                elif request == "add_friend":
                    Server.add_friend(self)

                # 处理好友申请
                elif request == "handle_friend_application":
                    args = int(self.connection.recv(1024).decode())
                    print(args)
                    Server.handle_friend_application(self, args)
                    # result如果为1，则成功处理好友申请，如果为3则为数据库错误
                    # 给客户端送过去还没写

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





