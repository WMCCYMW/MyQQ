import SqlServer
# 检测登录函数
def LoginSever(handler):
    # 获取name和password
    name = str(handler.connection.recv(1024),encoding="utf-8")
    password  = str(handler.connection.recv(1024),encoding="utf-8")
    # print(name + "\n" + password + "\n")
    isSucceed = SqlServer.LoginHandler.login_check(name, password)
    handler.connection.sendall(bytes(str(isSucceed),"utf-8"))
    return [isSucceed, name]

# 注册函数
def RegistSever(handler):
    # 获取name和password
    name = str(handler.connection.recv(1024).decode())
    password = str(handler.connection.recv(1024).decode())
    isSucceed =  SqlServer.LoginHandler.create_new_user(name, password)
    handler.connection.sendall(bytes(str(isSucceed),"utf-8"))
