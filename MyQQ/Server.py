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
    name = pkt[1]
    password = pkt[2]
    isSucceed = SqlServer.LoginHandler.login_check(name, password)
    response = ("login", str(isSucceed))
    response_json = json.dumps(response)
    handler.connection.sendall(bytes(response_json,"utf-8"))
    return [name, isSucceed]

# 注册函数
def RegistSever(handler, pkt):
    # 获取name和password
    name = pkt[1]
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
def add_friend(handler, pkt):
    applicant = handler.id
    recipient_name = pkt[1]
    recipient = search_one_by_name(recipient_name)[0]
    response = list()
    response.append("add_friend")
    result = SqlServer.FriendApplicantHandler.application(applicant, recipient)
    response.append(result)
    response_json = json.dumps(response)
    handler.connection.sendall(bytes(response_json, "utf-8"))

# 处理好友申请
def handle_friend_application(handler, pkt):
    args = int(pkt[1])
    recipient = handler.id
    applicant = int(pkt[2])
    result = SqlServer.FriendApplicantHandler.handle_it(applicant, recipient, args)
    response = ("handle_friend_application", result)
    response_json = json.dumps(response)
    handler.connection.sendall(bytes(response_json, "utf-8"))


# 获取好友列表
def get_friend_list(handler, pkt):
    state = pkt[1]
    id = handler.id
    result = SqlServer.FriendApplicantHandler.get_friend_list(id, state)
    response = list()
    response.append("get_friend_list")
    if result == 3:
        response.append("数据库错误")
    else:
        response.append("成功")
        for subRes in result:
            if (subRes[0] == handler.id):
                friend = search_one_by_id(subRes[1])
            else:
                friend = search_one_by_id(subRes[0])
            response.append(friend)
        response_json = json.dumps(response)
        handler.connection.sendall(bytes(response_json, "utf-8"))

# 查找用户
def find_user(handler, pkt):
    result = search_one_by_name(pkt[1])
    response = list()
    response.append("search_user")
    if result == 3:
        response.append("数据库错误")
    elif result is None:
        response.append("无匹配项")
    else:
        response.append("成功")
        response.append(result)
        response_json = json.dumps(response)
        handler.connection.sendall(bytes(response_json, "utf-8"))


# 给好友发送消息
def send_to_friend(handler, friend_socket, pkt):
    message = pkt[2]
    # 把pkt[1]，也就是目标改为来源；pkt[0]改为"receive_from_friend"
    pkt[1] = handler.name
    pkt[0] = "receive_from_friend"
    pkt_json = json.dumps(pkt)
    friend_socket.sendall(bytes(pkt_json, encoding='utf-8'))  # 发送消息

# 接收好友的消息
def receive_from_friend(handler, friend_socket):
    message = str(handler.connection.recv(1024).decode())







