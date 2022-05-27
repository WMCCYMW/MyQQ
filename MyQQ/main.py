from threading import Thread
import Server
import socket
connection_user=dict() # key为连接的socket， value为用户名
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
                if request=="login": Server.LoginSever()
                elif request=="register": Server.RegistSever()
        except Exception as e:
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
        listener=socket.socket()
        listener.bind(('127.0.0.1',8888))
        listener.listen(20)
        while True :
            connection,address=listener.accept()
            ConnectionHandler(connection,address).start()
    except Exception as e:
        print("服务器错误")





