import socket
client=socket.socket(socket.AF_INET)
client.connect(('192.168.0.102',8888))
print("这是一个测试用客户端")
while True:
    print("1.登录 2.注册")
    test=input("请选择要测试的功能")
    if(int(test)==1):
        id=input("请输入用户名")
        password=input("请输入密码")
        client.send("login".encode())
        client.send(id.encode(encoding='utf-8'))
        client.send(password.encode(encoding='utf-8'))
        if(str(client.recv(1024),encoding='utf-8')=='1'):
            print("登录成功")
        else: print("登录失败")
    elif(int(test)==2):
        id = input("请输入用户名")
        password = input("请输入密码")
        client.send("login".encode())
        client.send(id.encode(encoding='utf-8'))
        client.send(password.encode(encoding='utf-8'))
        if (str(client.recv(1024), encoding='utf-8') == '1'):
            print("注册成功")
        else:
            print("注册失败")




