import socket
import time
import json

client=socket.socket(socket.AF_INET)
client.connect(('192.168.0.102',3456))
print("这是一个测试用客户端")
while True:
    print("1.登录 2.注册 3.查找用户 4.获取好友列表")
    test=input("请选择要测试的功能")
    if(int(test)==1):
        name=input("请输入用户名")
        password=input("请输入密码")

        pkt = ("login", name, password)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())
        # client.send("login".encode())
        # time.sleep(0.2)
        # client.send(name.encode(encoding='utf-8'))
        # time.sleep(0.2)
        # client.send(password.encode(encoding='utf-8'))
        response_json = str(client.recv(1024),encoding='utf-8')
        response = json.loads(response_json)
        if(response[1]=='1'):
            print("登录成功")
        else: print("登录失败")

    elif(int(test)==2):
        name = input("请输入用户名")
        password = input("请输入密码")

        pkt = ("register", name, password)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())
        # client.send(pkt_json.encode())
        # client.send("register".encode())
        # time.sleep(0.2)
        # client.send(name.encode(encoding='utf-8'))
        # time.sleep(0.2)
        response_json = str(client.recv(1024),encoding='utf-8')
        response = json.loads(response_json)
        if (response[1] == '1'):
            print("注册成功")
        else:
            print("注册失败")

    elif(int(test)==3):
        name = input("请输入查找的用户")

        pkt = ("search_user", name)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())
        # client.send("search_one".encode())
        # time.sleep(0.2)
        # client.send(name.encode(encoding='utf-8'))
        response_json = str(client.recv(1024),encoding='utf-8')
        response = json.loads(response_json)
        result = response[1]
        if(result == "数据库错误" or result == "无匹配项"):
            print(result)
        elif(result == "成功"):
            id = response[2]
            name = response[3]
            print("id = " + id + " ;  name = " + name)
            add_friend = input("输入1向其发送好友申请")
            if add_friend == "1":
                client.send("add_friend".encode())
                time.sleep(0.2)
                client.send(name.encode())
                result = str(client.recv(1024), encoding='utf-8')
                if result == "1":
                    print("已发送")
                elif result == "3":
                    print("数据库错误，发送失败")

    elif(int(test) == 4):
        client.send("get_friend_list".encode())
        state = input("输入1获取好友目录，输入0获取接收的好友申请") # 有个问题：获取的好友申请，并不仅是接收的，还包括自己发出去的
        client.send(state.encode())
        result = str(client.recv(1024), encoding='utf-8')
        if(result == "数据库错误"):
            print(result)
        elif(result == "成功"):
            print("结果如下：")
            name = str(client.recv(1024), encoding='utf-8')
            friend_names = list()
            # 要是有个name叫做"结束"就不妙了
            if(name == "结束"):
                print("NULL")
            while name != "结束":
                print(name)
                friend_names.append(name)
                name = str(client.recv(1024), encoding='utf-8')
            # 处理好友申请
            if(state == "0"):
                toHandle = input("按1进行处理，按2不处理")
                if toHandle == "2":
                    continue
                else:
                    client.send("handle_friend_application".encode())
                    agree = input("按1同意，按0拒绝")
                    client.send(agree.encode())
                    time.sleep(0.2)
                    applicant_id = "5" # 这个得通过前端传回applicant的id
                    client.send(applicant_id.encode())
                    result = str(client.recv(1024), encoding='utf-8')
                    if(result == "1"):
                        print("成功处理")
                    elif(result == "3"):
                        print("数据库错误")
            # 给好友发送消息
            if(state == "1"):
                if "1" == input("按1给好友lisi发送消息"):
                    message = input("请输入发送内容：")
                    lisi = "lisi"
                    client.send("send_to_friend".encode())
                    time.sleep(0.2)
                    client.send(lisi.encode())
                    result = str(client.recv(1024), encoding='utf-8')
                    if result == "成功":
                        client.sendall(bytes(message, encoding='utf-8').__len__().to_bytes(4, byteorder='big'))  # 发送消息长度
                        time.sleep(0.2)
                        client.sendall(bytes(message, encoding='utf-8'))  # 发送消息
                        result = str(client.recv(1024), encoding='utf-8')
                        print(result)
                    else:
                        print(result)









