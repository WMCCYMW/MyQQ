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
            while True:
                print("1.登录 2.注册 3.查找用户 4.获取好友列表")
                request=input("请选择要测试的功能")
                # 登录
                if(int(request)==1):
                    self.login()

                # 注册
                elif(int(request)==2):
                    self.register()

                # 查询用户
                elif(int(request)==3):
                    self.search_user()

                    # 发送好友请求
                    add_friend = input("输入1向其发送好友申请")
                    if add_friend == "1":
                        '''
                            此处的name应该由用户点击添加好友后自动传入
                        '''
                        name = input("请前端返回申请好友的名称")
                        self.add_friend(name)


                elif(int(request) == 4):
                    state = input("输入1获取好友目录，输入0获取接收的好友申请") # 有个问题：获取的好友申请，并不仅是接收的，还包括自己发出去的
                    '''
                        客户端做选择
                    '''
                    self.get_friend_list(state)

                    # 处理好友申请
                    if(state == "0"):
                        # 选择是否处理，如果暂不处理在前端直接返回即可
                        toHandle = input("按1进行处理，按2不处理")
                        if toHandle == "2":
                            continue
                        else:
                            agree = input("按1同意，按0拒绝")
                            '''
                                此处的applicant_id应该由用户点击添加好友后自动传入
                            '''
                            applicant_id = input("请前端返回发送好友申请的id")
                            self.handle_friend_application(agree, applicant_id)

                    # 给好友发送消息
                    if(state == "1"):
                        '''
                            此处的friend_id应该由用户点击发起私聊后自动传入
                        '''
                        friend_id = "请前端返回好友id以发起私聊"
                        message = input("请输入发送内容：")
                        now_time = datetime.datetime.now()
                        self.send_to_friend(friend_id, now_time, message)


        except Exception as e:
            print(str(e))
            print(str(self.address)+"连接异常，准备关闭")
        finally:
            try:
                self.client.close()
            except Exception as e:
                print(str(e))
                print("连接关闭失败")

    # 登录
    def login(self):
        name = input("请输入用户名")
        password = input("请输入密码")
        pkt = ("login", name, password)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 注册
    def register(self):
        name = input("请输入用户名")
        password = input("请输入密码")
        pkt = ("register", name, password)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 查找用户
    def search_user(self):
        name = input("请输入查找的用户")
        pkt = ("search_user", name)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 添加好友
    def add_friend(self, name):
        pkt = ("add_friend", name)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 获取好友列表
    def get_friend_list(self, state):
        pkt = ("get_friend_list", state)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 处理好友申请
    def handle_friend_application(self, agree, applicant_id):
        pkt = ("handle_friend_application", agree, applicant_id)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())

    # 给好友发送信息
    def send_to_friend(self, friend_id, now_time, message):
        pkt = ("send_to_friend", friend_id, now_time, message)
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

                # 登录
                if request == "login":
                    if response[1] == '1':
                        print("登录成功")
                    elif response[1] == '2':
                        print("密码错误，登录失败！")
                    else:
                        print("登录失败，请稍后再试！")

                # 注册
                elif request == "register":
                    if (response[1] == '1'):
                        print("注册成功")
                    else:
                        print("注册失败")

                # 查找用户
                elif request == "search_user":
                    result = response[1]
                    if (result == "数据库错误" or result == "无匹配项"):
                        print(result)
                    elif(result == "成功"):
                        id = str(response[2][0])
                        name = response[2][1]
                        '''
                            response格式：("search_user", "成功", (id, name))
                            这里的前端页面是：因为name是唯一属性，所以结果就只有一行，然后后面有个添加好友的按键，按下需要传入name作为参数
                            引用add_friend(self, name)方法
                        '''
                        print("{id = " + id + ", name = " + name + "}")
                    else:
                        print("返回错误，请稍后再试")

                # 添加好友
                elif request == "add_friend":
                    result = str(response[1])
                    if result == "1":
                        print("已发送")
                    elif result == "3":
                        print("数据库错误，发送失败")

                # 获取好友列表
                elif request == "get_friend_list":
                    result = response[1]
                    if (result == "数据库错误"):
                        print(result)
                    elif (result == "成功"):
                        print("结果如下：")
                        for friend in response[2:]:
                            '''
                                返回的response格式: ("get_friend_list", "成功", (id1, name1), (id2, name2) ...)
                                所以应该为每一个friend为一栏
                                如果state为0，即是查看的好友申请列表，如果自己为接收者，可以处理请求（需要将id作为参数返回）
                                如果state为1，即是查看好友列表，可以发起私聊（需要将name作为参数返回）
                            '''
                            print(friend)

                # 处理好友申请
                elif request == "handle_friend_application":
                    result = str(response[1])
                    if (result == "1"):
                        print("成功处理")
                    elif (result == "3"):
                        print("数据库错误")

                # 给好友发送私聊后的反馈
                elif request == "send_to_friend":
                    if response[2] == "成功":
                        print("给好友’" + response[1] + "‘密语发送成功")
                    else:
                        print("给好友’" + response[1] + "‘密语发送失败")


                # 接收到了来自好友的私聊
                elif request == "receive_from_friend": # 已经在Server内完成对request的改名
                    friend_name = response[1] # message的来源
                    print("接收来自'" + friend_name + "'的密语：" + response[2])
                    '''
                        这个地方有个问题，要是friend改名了咋办
                        本来想传的是friend_id的，但是不知道前端是否有办法可以实时通过id得到好友列表中的name（再写一个函数用于实时通过id查name？）
                    '''


        except Exception as e:
            print(str(e))
            print(str(self.address)+"连接异常，准备关闭")
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
        client.connect(('192.168.0.103', 3456))
        print("这是一个测试用客户端")
        SendRequestHandler(client).start()
        RecvRespHandler(client).start()
    except Exception as e:
        print("连接失败："+str(e))














