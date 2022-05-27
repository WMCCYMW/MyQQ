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





