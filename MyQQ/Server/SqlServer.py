# 数据库函数
import datetime

import pymysql
import sys

# 用于处理登录注册等操作的handler
class LoginHandler(object):
    @staticmethod
    def login_check(name, password): # 检测用户登录
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork") # 连接数据库
        cursor = db.cursor() # 获取数据库的游标
        sql = "SELECT * FROM user WHERE name = '%s'" % (name) # 查询语句
        try:
            cursor.execute(sql) # 执行语句
            result = cursor.fetchone() # 获得结果
            if password == result[2]: # 如果密码相符
                # 更新last_login_time
                now_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                sql_update_login_time = "UPDATE user SET last_login_time = %s WHERE name = %s"
                args_login_time = (now_time, name)
                cursor_login_time = db.cursor()
                result_login_time = cursor_login_time.execute(sql_update_login_time, args_login_time)
                # print(name + "欢迎登录！")
            else:
                # print("密码错误，登录失败！")
                return "密码错误"
        except Exception as e:
            # print("登录失败，未知错误！")
            print(e)
            return "数据库错误"
        finally:
            db.commit()
            db.close() # 关闭连接
        # 返回自己的id和name
        return result

    @staticmethod
    def create_new_user(name, password): # 创建新用户
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork")  # 连接数据库
        cursor = db.cursor()
        sql = "INSERT INTO user (name, password, message_count) VALUES (%s, %s, 0)"
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
        # 获取好友申请列表
        if state == 0:
            sql = "SELECT * FROM friend_application WHERE recipient = %s and state = 0" % (id)
        # 获取好友列表
        else:
            sql = "SELECT * FROM friend_application WHERE (applicant = %s or recipient = %s) and state = 1" % (id ,id)
        try:
            cursor.execute(sql)
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
        sql = "SELECT id, name FROM user WHERE name = %s"
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
        sql = "SELECT id, name FROM user WHERE id = %s"
        args = (id)
        try:
            cursor.execute(sql, args)
            result = cursor.fetchone()
            db.close()
            return result
        except Exception as e:
            print(str(e))
            return 3

# 数据处理的Handler
class DataUpdateHandler:
    # 增加发消息数
    @staticmethod
    def message_count_increase(id):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork") # 连接数据库
        cursor = db.cursor() # 获取数据库的游标
        sql = "UPDATE user SET message_count = message_count + 1 WHERE id = %s"
        args = (id)
        try:
            cursor.execute(sql, args)
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()

    # 管理员：删除用户
    @staticmethod
    def delete_user(id):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork")  # 连接数据库
        cursor = db.cursor()  # 获取数据库的游标
        sql = "DELETE FROM user WHERE id = %s"
        args = (id)
        try:
            cursor.execute(sql, args)
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()

    # 管理员：展示信息
    @staticmethod
    def show_details():
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork")  # 连接数据库
        cursor = db.cursor()  # 获取数据库的游标
        sql_avg_message_count = "SELECT round(avg(message_count),2) FROM user" # 查询平均发言条数
        sql_details = "SELECT * FROM user" # 查询所有信息
        try:
            cursor.execute(sql_avg_message_count)
            result_avg_message_count = str(cursor.fetchone())[10:14]
            cursor.execute(sql_details)
            result_details = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            db.close()
        result = list()
        result.append(result_avg_message_count)
        result.append(result_details)
        return result

    # 管理员更改用户名
    @staticmethod
    def change_user_name(id, name):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork")  # 连接数据库
        cursor = db.cursor()  # 获取数据库的游标
        sql = "UPDATE user SET name = %s WHERE id = %s"
        args = (name, id)
        try:
            cursor.execute(sql, args)
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()

    # 管理员更改用户密码
    @staticmethod
    def change_user_pwd(id, pwd):
        db = pymysql.connect(host="localhost", user="root", password="chen123456", db="pythonwork")  # 连接数据库
        cursor = db.cursor()  # 获取数据库的游标
        sql = "UPDATE user SET password = %s WHERE id = %s"
        args = (pwd, id)
        try:
            cursor.execute(sql, args)
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()














