import pymysql
import re
import traceback


class DB:
    __url = "localhost"
    __user = "root"
    __pwd = ""
    __database = "python"
    __db = None

    def __init__(self):
        self.__db = self.open_connect()

    # 链接数据库
    def open_connect(self, url, user, pwd, database):
        self.__db = pymysql.connect(host='localhost', port=3306, user=user, passwd=pwd, db=database, charset="utf8")
        return self.__db

    # 链接数据库
    def open_connect(self):
        self.__db = pymysql.connect(host='localhost', port=3306, user=self.__user, passwd=self.__pwd,
                                    db=self.__database, charset="utf8")
        return self.__db

    # 将参数设置到对应的?占位符中
    def deal_sql1(self, sql, params):
        for item in params:
            sql = sql.replace("?", "'"+str(item)+"'", 1)
        return sql

    # 处理#号占位符
    def deal_sql2(self, sql, json):
        # 创建正则表达式
        re_compile = re.compile("#[\w]+")
        # 将参数设置到sql语句中
        for item in json:
            for key in re_compile.findall(sql):
                if key.find(item) > 0:
                    sql = sql.replace(key, "'"+str(json[item])+"'", 1)
        # 将没有的参数至为1=1
        re_compile = re.compile("[\w]+=#[\w]+")
        findall = re_compile.findall(sql)
        for repl in findall:
            sql = sql.replace(repl, '1=1', 1)
        return sql

    # 处理sql
    def deal_sql(self, sql, params):
        if sql.find("?") > 0:
            return self.deal_sql1(sql, params)
        elif sql.find("#") > 0:
            return self.deal_sql2(sql, params[0])

    # 查询所有
    def select_all(self, sql, *params):
        sql = self.deal_sql(sql, params)
        try:
            self.open_connect()
            # 获取当前游标的位置
            cursor = self.__db.cursor()
            # 执行sql
            cursor.execute(sql)
            # 获取第一条数据
            data = cursor.fetchall()
            # 返回数据
            return data
        except Exception:
            traceback.print_exc()
            # 回滚数据
            self.__db.rollback()
        finally:
            # 关闭链接
            self.__db.close()

    # 插入数据
    def insert(self, sql, *params):
        sql = self.deal_sql(sql, params)
        try:
            self.open_connect()
            # 获取当前游标的位置
            cursor = self.__db.cursor()
            # 执行sql
            cursor.execute(sql)
            # 将数据提交到数据库中
            self.__db.commit()
        except Exception:
            traceback.print_exc()
            # 回滚数据
            self.__db.rollback()
        finally:
            # 关闭链接
            self.__db.close()

    # 更新数据
    def update(self, sql, *params):
        sql = self.deal_sql(sql, params)
        try:
            self.open_connect()
            # 获取当前游标的位置
            cursor = self.__db.cursor()
            # 执行sql
            cursor.execute(sql)
            # 将数据提交到数据库中
            self.__db.commit()
        except Exception:
            traceback.print_exc()
            # 回滚数据
            self.__db.rollback()
        finally:
            # 关闭链接
            self.__db.close()
