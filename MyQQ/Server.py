import json
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
def send_string(socket,content):
    socket.sendall(bytes(content,encoding='utf-8').__len__().to_bytes(4,byteorder='big')) # 发送消息长度
    socket.sendall(bytes(content,encoding='utf-8')) # 发送消息

# 检测登录函数
def LoginSever(handler, pkt):
    # 获取name和password
    # name = str(handler.connection.recv(1024),encoding="utf-8")
    name = pkt[1]
    # password = str(handler.connection.recv(1024),encoding="utf-8")
    password = pkt[2]
    # print(name + "\n" + password + "\n")
    isSucceed = SqlServer.LoginHandler.login_check(name, password)
    response = ("login", str(isSucceed))
    response_json = json.dumps(response)
    handler.connection.sendall(bytes(response_json,"utf-8"))
    return [name, isSucceed]

# 注册函数
def RegistSever(handler, pkt):
    # 获取name和password
    # name = str(handler.connection.recv(1024).decode())
    name = pkt[1]
    # password = str(handler.connection.recv(1024).decode())
    password = pkt[2]
    isSucceed = SqlServer.LoginHandler.create_new_user(name, password)
    response = ("register", str(isSucceed))
    response_json = json.dumps(response)
    handler.connection.sendall(bytes(response_json,"utf-8"))

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
    if result == 3:
        handler.connection.sendall(bytes(str("数据库错误"), "utf-8"))
    else:
        handler.connection.sendall(bytes(str("成功"), "utf-8"))
        for subRes in result:
            if (subRes[0] == handler.id):
                friend = search_one_by_id(subRes[1])
                friend_name = friend[1]
                handler.connection.sendall(bytes(str(friend_name), "utf-8"))
            else:
                friend_name = search_one_by_id(subRes[0])[1]
                handler.connection.sendall(bytes(str(friend_name), "utf-8"))
        handler.connection.sendall(bytes(str("结束"), "utf-8"))  # 要是有个name叫做"结束"就完蛋了。。。

# 查找用户
def find_user(handler, pkt):
    result = search_one_by_name(pkt[1])
    response = list("search_user")
    if result == 3:
        # handler.connection.sendall(bytes(str("数据库错误"), "utf-8"))
        response.append("数据库错误")
    elif result is None:
        # handler.connection.sendall(bytes(str("无匹配项"), "utf-8"))
        response.append("无匹配项")
    else:
        # handler.connection.sendall(bytes(str("成功"), "utf-8"))
        response.append("成功")
        response.append(result[0])
        response.append(result[1])
        # handler.connection.sendall(bytes(str(result[0]), "utf-8"))  # 发送id
        # handler.connection.sendall(bytes(str(result[1]), "utf-8"))  # 发送name
        response_json = json.dumps(response)
        handler.connection.sendall(bytes(response_json, "utf-8"))


# 给好友发送消息
def send_to_friend(handler, friend_socket):
    message = str(handler.id) + ":" + recvc_string(handler)
    send_string(friend_socket, message)
    handler.connection.sendall(bytes(str("已发送：" + message), "utf-8"))

# 接收好友的消息
def receive_from_friend(handler, friend_socket):
    message = str(handler.connection.recv(1024).decode())







