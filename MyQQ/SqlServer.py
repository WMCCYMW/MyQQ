# 数据库函数
import pymysql
import sys

# 用于处理登录注册等操作的handler
class LoginHandler(object):
    @staticmethod
    def login_check(name, password): # 检测用户登录
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork") # 连接数据库
        cursor = db.cursor() # 获取数据库的游标
        sql = "SELECT * FROM test01 WHERE name = '%s'" % (name) # 查询语句
        try:
            cursor.execute(sql) # 执行语句
            result = cursor.fetchone() # 获得结果
            db.close() # 关闭连接
            if password == result[2]: # 如果密码相符
                # print(name + "欢迎登录！")
                return 1
            else:
                # print("密码错误，登录失败！")
                return 2
        except:
            # print("登录失败，未知错误！")
            return 3

    @staticmethod
    def create_new_user(name, password): # 创建新用户
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork")  # 连接数据库
        cursor = db.cursor()
        sql = "INSERT INTO test01 (name, password) VALUES (%s, %s)"
        args = (name, password)
        try:
            cursor.execute(sql, args)
            db.commit()
            db.close()
            # print(name + "加入成功！")
            return 1
        except:
            # print("数据库出错！")
            db.rollback() # 回滚
            db.close()
            return 3

# 用于好友申请的handler
class FriendApplicantHandler(object):
    # 发送好友申请
    @staticmethod
    def application(applicant, recipient):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork")  # 连接数据库
        cursor = db.cursor()  # 获取数据库的游标
        sql = "INSERT INTO friend_application VALUES (%s, %s, 0)" # 插入语句
        args = (applicant, recipient)
        try:
            cursor.execute(sql, args)
            db.commit()
            db.close()
            return 1
        except:
            db.rollback()
            db.close()
            return 3
    # 处理好友申请
    @staticmethod
    def handle_it(applicant, recipient, args):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork")  # 连接数据库
        cursor = db.cursor()  # 获取数据库的游标
        sql = ""
        if(args == 1): # 同意
            sql = "UPDATE friend_application SET state = 1 WHERE applicant = %s and recipient = %s"
        else: # 拒绝
            sql = "DELETE FROM friend_application WHERE applicant = %s and recipient = %s"
        args = (applicant, recipient)
        try:
            cursor.execute(sql, args)
            db.commit()
            db.close()
            return 1
        except Exception as e:
            db.rollback()
            db.close()
            print(e)
            return 3
    # 获取好友列表或者好友申请
    @staticmethod
    def get_friend_list(id, state):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork") # 连接数据库
        cursor = db.cursor() # 获取数据库的游标
        sql = "SELECT * FROM friend_application WHERE (applicant = %s or recipient = %s) and state = %s"
        args = (id, id, state)
        try:
            cursor.execute(sql, args)
            result = cursor.fetchall()
            db.close()
            return result
        except:
            return 3

# 包含各种查的方法的总类
class SearchHandler(object):
    # 通过name得到(id, name)
    @staticmethod
    def search_one_by_name(name):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork") # 连接数据库
        cursor = db.cursor() # 获取数据库的游标
        sql = "SELECT id, name FROM test01 WHERE name = %s"
        args = (name)
        try:
            cursor.execute(sql, args)
            result = cursor.fetchone()
            db.close()
            return result
        except Exception as e:
            print(str(e))
            return 3

    # 通过id得到(id, name)
    @staticmethod
    def search_one_by_id(id):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork") # 连接数据库
        cursor = db.cursor() # 获取数据库的游标
        sql = "SELECT id, name FROM test01 WHERE id = %s"
        args = (id)
        try:
            cursor.execute(sql, args)
            result = cursor.fetchone()
            db.close()
            return result
        except Exception as e:
            print(str(e))
            return 3














