import conf.config as config
import pymysql
import threading

def synchronized(func):
    func.__lock__ = threading.Lock()
    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)
    return lock_func

class SQL_Helper:
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        if cls.instance is  None:
            cls.instance = object.__new__(cls)
        return cls.instance


    def __init__(self, db_config):
        self.cfg = db_config
        self.cursor = None
        self.db = None

        try:
            self.db = pymysql.connect(**self.cfg)
            self.cursor = self.db.cursor()
        except:
            print("Fail to connect database!")


        self.cursor.execute("select version()")
        data = self.cursor.fetchone()
        print(" Database Version:%s" % data)
        print("MYSQL init sucess!")

    def keep_interacitve(self):
        sql = "SELECT * FROM INSECTS"
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            print("Success to keep interactive!")
        except:
            print("Fail to keep interactive!")
    def get_name_by_code(self, insect_code):
        sql = "SELECT INSECT_NAME FROM INSECTS WHERE INSECT_CODE = '%s'; " % insect_code
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            return data[0]
        except:
            print("Fail to query, get_name_by_code")
    def query(self, insect_code):
        sql = "SELECT * FROM INSECTS WHERE INSECT_CODE = '%s'; " % insect_code
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            entry = {}
            entry['ORDER_NAME'] = data[0]
            entry['ORDER_CODE'] = data[1]
            entry['FAMILIY_NAME'] = data[2]
            entry['FAMILIY_CODE'] = data[3]
            entry['GENUS_NAME'] = data[4]
            entry['GENUS_CODE'] = data[5]
            entry['INSECT_NAME'] = data[6]
            entry['INSECT_CODE'] = data[7]
            entry['LATIN_NAME'] = data[8]
            entry['FOOD'] = data[9]
            entry['AREA'] = data[10]
            return entry
        except:
            print("Fail to query!")

def task(arg):
    obj = SQL_Helper()
    print(obj)


if __name__ == '__main__':
    helper1 = SQL_Helper()
    print(helper1.query('C15102015005'))
    # helper2 = SQL_Helper()
    # helper3 = SQL_Helper()
    # print(helper1, helper2, helper3)
    # 多线程下可能报错 以后使用数据库链接池做



