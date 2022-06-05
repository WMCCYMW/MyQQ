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
    password = str(handler.connection.recv(1024),encoding="utf-8")
    # print(name + "\n" + password + "\n")
    isSucceed = SqlServer.LoginHandler.login_check(name, password)
    handler.connection.sendall(bytes(str(isSucceed),"utf-8"))
    return [name, isSucceed]

# 注册函数
def RegistSever(handler):
    # 获取name和password
    name = str(handler.connection.recv(1024).decode())
    password = str(handler.connection.recv(1024).decode())
    isSucceed = SqlServer.LoginHandler.create_new_user(name, password)
    handler.connection.sendall(bytes(str(isSucceed),"utf-8"))

# 通过name得到(id,name)
def search_one_by_name(name):
    result = SqlServer.SearchHandler.search_one_by_name(name)
    return result

# 通过id得到(id, name)
def search_one_by_id(id):
    result = SqlServer.SearchHandler.search_one_by_id(id)
    return result


# 发送好友申请
def add_friend(handler):
    applicant = handler.id
    recipient_name = str(handler.connection.recv(1024).decode())
    recipient = search_one_by_name(recipient_name)[0]
    result = SqlServer.FriendApplicantHandler.application(applicant, recipient)
    handler.connection.sendall(bytes(str(result), "utf-8"))

# 处理好友申请
def handle_friend_application(handler, args):
    recipient = handler.id
    applicant = int(str(handler.connection.recv(1024).decode()))
    result = SqlServer.FriendApplicantHandler.handle_it(applicant, recipient, args)
    handler.connection.sendall(bytes(str(result), "utf-8"))


# 获取好友列表
def get_list(handler, state):
    id = handler.id
    result = SqlServer.FriendApplicantHandler.get_friend_list(id, state)
    return result



