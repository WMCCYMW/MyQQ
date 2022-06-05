import math
import SqlServer
import math
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
    handler.connection.sendall(bytes(content,encoding='utf-8').__len__().to_bytes(4,byteorder='big'))
    handler.connection.sendall(bytes(content,encoding='utf-8'))

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

# 通过name找人
def search_one(handler):
    name = str(handler.connection.recv(1024).decode())
    result = SqlServer.FriendApplicantHandler.search_one(name)
    return result

# 添加好友
def add_friend(handler):
    applicant = SqlServer.FriendApplicantHandler.search_one(handler.name)[0]
    recipient = str(handler.connection.recv(1024).decode())
    SqlServer.FriendApplicantHandler.application(applicant, recipient)

# 处理好友申请
def handle_friend_application(handler, args):
    recipient = SqlServer.FriendApplicantHandler.search_one(handler.name)[0]
    applicant = str(handler.connection.recv(1024).decode())
    SqlServer.FriendApplicantHandler.application(applicant, recipient, args)

# 获取好友列表
def get_list(handler, state):
    id = SqlServer.FriendApplicantHandler.search_one(handler.name)[0]
    result = SqlServer.FriendApplicantHandler.search_friend(id, state)
    return result



