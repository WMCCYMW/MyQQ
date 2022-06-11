import socket
import time
import json

client=socket.socket(socket.AF_INET)
client.connect(('192.168.0.103',3456))
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
        response_json = str(client.recv(1024),encoding='utf-8')
        response = json.loads(response_json)
        result = response[1]
        if(result == "数据库错误" or result == "无匹配项"):
            print(result)
        elif(result == "成功"):
            id = str(response[2][0])
            name = response[2][1]
            print("id = " + id + " ;  name = " + name)
            add_friend = input("输入1向其发送好友申请")
            if add_friend == "1":
                pkt = ("add_friend", name)
                pkt_json = json.dumps(pkt)
                client.send(pkt_json.encode())
                response_json = str(client.recv(1024), encoding='utf-8')
                response = json.loads(response_json)
                result = str(response[1])
                if result == "1":
                    print("已发送")
                elif result == "3":
                    print("数据库错误，发送失败")

    elif(int(test) == 4):
        state = input("输入1获取好友目录，输入0获取接收的好友申请") # 有个问题：获取的好友申请，并不仅是接收的，还包括自己发出去的
        pkt = ("get_friend_list", state)
        pkt_json = json.dumps(pkt)
        client.send(pkt_json.encode())
        response_json = str(client.recv(1024), encoding='utf-8')
        response = json.loads(response_json)
        result = response[1]
        if(result == "数据库错误"):
            print(result)
        elif(result == "成功"):
            print("结果如下：")
            for friend in response[2:]:
                print(friend)

            # 处理好友申请
            if(state == "0"):
                toHandle = input("按1进行处理，按2不处理")
                if toHandle == "2":
                    continue
                else:
                    agree = input("按1同意，按0拒绝")
                    applicant_id = "5" # 这个得通过前端传回applicant的id
                    pkt = ("handle_friend_application", agree, applicant_id)
                    pkt_json = json.dumps(pkt)
                    client.send(pkt_json.encode())
                    response_json = str(client.recv(1024), encoding='utf-8')
                    response = json.loads(response_json)
                    result = str(response[1])
                    if(result == "1"):
                        print("成功处理")
                    elif(result == "3"):
                        print("数据库错误")
            # 给好友发送消息
            if(state == "1"):
                if "1" == input("按1给好友lisi发送消息"):
                    message = input("请输入发送内容：")
                    friend_name = "lisi"
                    pkt = ("send_to_friend", friend_name, message)
                    pkt_json = json.dumps(pkt)
                    client.send(pkt_json.encode())
                    response_json = str(client.recv(1024), encoding='utf-8')
                    response = json.loads(response_json)
                    result = response[1]
                    print(result)
