import socket
import datetime
import json
from threading import Thread


# 发出请求的线程
class SendRequestHandler(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
    def run(self):
        try:
            self.show_details()
            while True:
                print("1.删除用户 2.注册账号 3.更改用户名 4.更改密码 5.刷新信息")
                request=input("请选择的功能：")
                # 删除用户
                if(int(request)==1):
                    self.delete_user()

                # 注册账号
                elif(int(request)==2):
                    self.register()

                # 更新消息
                elif(int(request)==5):
                    self.show_details()

                # 更改用户名
                elif(int(request) == 3):
                    self.change_user_name()

                # 更改密码
                elif(int(request) == 4):
                    self.change_user_pwd()



        except Exception as e:
            print(str(e))
        finally:
            try:
                self.client.close()
            except Exception as e:
                print(str(e))
                print("连接关闭失败")

    # 删除用户
    def delete_user(self):
        id = input("请输入欲删除用户的id：")
        pkt = ("delete_user", id)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 注册
    def register(self):
        name = input("请输入用户名：")
        password = input("请输入密码：")
        pkt = ("register", name, password)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 展示信息
    def show_details(self):
        pkt = ("show_details",0)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 更改用户名
    def change_user_name(self):
        id = input("请输入更改用户名的id：")
        name = input("请输入更改后的用户名：")
        pkt = ("change_user_name", id, name)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 更改密码
    def change_user_pwd(self):
        id = input("请输入更改用户名的id：")
        pwd = input("请输入更改后的密码：")
        pkt = ("change_user_pwd", id, pwd)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())


# 接收响应的线程
class RecvRespHandler(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
    def run(self):
        try:
            while True:
                response_json = str(client.recv(1024), encoding='utf-8') # 收包
                response = json.loads(response_json) # 解包
                request = response[0] # 判断
                if request == "show_details":
                    print("\n大家伙儿的平均发言条数：" + response[1][0])
                    print("=================================================================================================================")
                    print("|\t\tid\t\t|\t\tname\t\t|\t\tpassword\t\t|\t\t \t  最后登录时间  \t\t|\t\t发言条数\t\t|")
                    for detail in response[1][1]:
                        print("=================================================================================================================")
                        print("|\t\t"+str(detail[0])+"\t\t|\t\t"+str(detail[1])+"\t\t\t|\t\t  "+str(detail[2])+"  \t\t\t|\t\t"+str(detail[3])+"\t\t|\t\t  "+str(detail[4])+"  \t\t|")
                    print("=================================================================================================================")



        except Exception as e:
            print(str(e))
        finally:
            try:
                self.client.close()
            except Exception as e:
                print(str(e))
                print("连接关闭失败")

if __name__ == "__main__":
    try:
        # 连接部分
        client = socket.socket(socket.AF_INET)
        client.connect(('127.0.0.1', 3457))
        print("这是一个管理员客户端")
        SendRequestHandler(client).start()
        RecvRespHandler(client).start()
    except Exception as e:
        print("连接失败："+str(e))














