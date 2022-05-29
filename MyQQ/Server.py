import math
import SqlServer
import math
# 检测登录函数
def recvc_string(handler):
    length=int.from_bytes(handler.connection.recv(4),byteorder='big')
    b_size=3*1024
    times=math.ceil(length/b_size)
    content=''
    for i in range(times):
        if i==times-1:
            subcontent=handler.connection.recv(length%b_size)
        else:
            subcontent=handler.connection.recv(b_size)
        content+=str(subcontent,encoding='utf-8')
    return content
def send_string(handler,content):
    handler.connection.sendall(bytes(content,encoding='uft-8').__len__().to_bytes(4,byteorder='big'))
    handler.connection.sendall(bytes(content,encoding='uutf-8'))
def LoginSever(handler):
    # 获取name和password
    name = str(handler.connection.recv(1024),encoding="utf-8")
    password  = str(handler.connection.recv(1024),encoding="utf-8")
    isSucceed = SqlServer.LoginHandler.login_check(name, password)
    if(isSucceed == 1):
        handler.connection.sendall(bytes(str(isSucceed),"utf-8"))
        return [isSucceed, name]
    else:
        handler.connection.sendall(bytes(str(isSucceed),"utf-8"))

# 注册函数
def RegistSever(handler):
    # 获取name和password
    name = str(handler.connection.recv(1024).decode())
    password = str(handler.connection.recv(1024).decode())
    isSucceed =  SqlServer.LoginHandler.create_new_user(name, password)
    handler.connection.sendall(bytes(str(isSucceed),"utf-8"))
