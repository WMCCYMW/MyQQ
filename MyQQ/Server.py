import SqlServer
# 检测登录函数
def LoginSever(handler):
    # 获取name和password
    name = str(handler.connection.recv(1024).decode())
    password  = str(handler.connection.recv(1024).decode())
    isSucceed = SqlServer.LoginHandler.login_check(name, password)
    if(isSucceed == 1):
        handler.connection.sendAll(bytes(str(isSucceed),"utf-8"))
        return [isSucceed, name]
    else:
        handler.connection.sendAll(bytes(str(isSucceed),"utf-8"))


def RegistSever(handler):
    # 获取name和password
    name = str(handler.connection.recv(1024).decode())
    password = str(handler.connection.recv(1024).decode())
    isSucceed =  SqlServer.LoginHandler.create_new_user(name, password)
    handler.connection.sendAll(bytes(str(isSucceed),"utf-8"))
