import pymysql
import pymongo
from twisted.enterprise import adbapi


class Mongo(object):
    '''
    mongodb操作基础类
    '''
    def __init__(self, mongo_uri):
        self.client = pymongo.MongoClient(mongo_uri)

    def save_to_mongo(self, item):
        '''
        保存数据到mongodb数据库中
        :param item: 解析器提取下来的数据
        :return:
        '''
        raise NotImplementedError


class Mydb(object):
    def __init__(self, host, user, password, database, port, charset):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset

    def connect_db(self):
        try:
            db = pymysql.connect(
                self.host,
                self.user,
                self.password,
                self.database,
                self.port,
                self.charset
            )

            cursor = db.cursor()
            return cursor
        except Exception as e:
            print(e)
            return None

    def save(self, cursor):
        raise NotImplementedError


class Mdb(object):
    '''
    一个使用twisted实现的异步插入数据的类
    '''
    def __init__(self, user, pwd, host, db, port, charset):
        params = dict(
            host=host,
            user=user,
            password=pwd,
            db=db,
            port=port,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.dbpool = adbapi.ConnectionPool('pymysql', **params)

    def save(self, item):
        '''
        保存数据的方法
        :param item: 解析器解析后的网页数据
        :return:
        '''
        query = self.dbpool.runInteraction(self.insert_item, item)
        query.addErrback(self._errors)

    def insert_item(self, cursor, item):
        '''
        插入数据的方法
        :param cursor: mysql数据游标
        :param item: 解析器解析后的数据
        :return:
        '''
        raise NotImplementedError

    def _errors(self, msg):
        '''
        插入出错时执行的函数
        :param msg: 出错消息
        :return:
        '''
        raise NotImplementedError
