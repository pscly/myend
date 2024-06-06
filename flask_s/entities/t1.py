import os
from pymongo import MongoClient


class MyMongo1:

    __instances = {}

    def __new__(cls, table_name='userinfo', *args, **kwargs):
        if table_name not in cls.__instances:
            cls.__instances[table_name] = super().__new__(cls)
        return cls.__instances[table_name]

    def __init__(self, ip='127.0.0.1', port=27017, username=None, password=None, db_name='yend1', table_name='userinfo'):
        self.ip =  ip or os.y.config.get('mongodb_ip')
        self.port = port or os.y.config.get('mongodb_port')
        self.username = username or os.y.config.get('mongodb_user')
        self.password = password or os.y.config.get('mongodb_pwd')
        self.db_name = db_name or os.y.config.get('mongodb_db_name')
        self.table_name = table_name

        self.connect()

    def connect(self):
        try:
            client = MongoClient(host=self.ip, port=self.port,
                                    username=self.username, password=self.password)
            self.db = client[self.db_name]
            self.table = self.db[self.table_name]
        except Exception as e:
            print(f"Failed to connect to MongoDB{self.ip}{self.port}: {e}")

    def disconnect(self):
        self.client.close()

    def change_table(self, table_name):
        """切换到另一个表"""
        self.table_name = table_name
        self.table = self.db[self.table_name]
    
    def find(self, query:dict=None, projection:dict=None):
        """
        查询数据
        :param query: 查询条件  # {'age': {'$gt': 10}} 
        :param projection: 返回结果筛选条件
        :return: 满足查询条件的数据列表
        :rtype: list[dict]
        """
        cursor = self.table.find(query, projection)
        return [doc for doc in cursor]
    
    def save(self, data, primary_key="_id"):
        """
        保存数据，如果已经存在相同的主键值，则更新记录，否则新增记录。
        :param data: 要保存的文档（即记录），可以是单个字典或者是一个列表套字典
        :type data: dict or list[dict]
        :param primary_key: 作为主键的字段名，默认为 "_id"
        :type primary_key: str
        """
        if isinstance(data, dict):
            result = self.table.replace_one({primary_key: data[primary_key]}, data, upsert=True)
            return result.upserted_id or result.modified_count
        elif isinstance(data, list):
            count = 0
            for doc in data:
                result = self.table.replace_one({primary_key: doc[primary_key]}, doc, upsert=True)
                count += result.upserted_id is not None or result.modified_count
            return count
        else:
            raise TypeError("data must be a dict or a list of dicts.")
    def update(self, data, primary_key="_id", merge=True):
        """
        更新数据，如果已经存在相同的主键值，则根据参数 "merge" 的值执行不同的操作。
        args: 
            data: 要更新的文档（即记录），可以是单个字典或者是一个列表套字典
                type : dict or list[dict]
            primary_key: 作为主键的字段名，默认为 "_id"
                type primary_key: str
            merge: 是否合并原始记录。如果是，则将新文档中的字段合并到旧文档中。否则，删除旧文档并插入新文档。
                type merge: bool
        """
        if isinstance(data, dict):
            if merge:
                result = self.table.update_one({primary_key: data[primary_key]}, {"$set": data})
                return result.modified_count
            else:
                result = self.table.replace_one({primary_key: data[primary_key]}, data, upsert=True)
                return result.upserted_id or result.modified_count
        elif isinstance(data, list):
            count = 0
            for doc in data:
                if merge:
                    result = self.table.update_one({primary_key: doc[primary_key]}, {"$set": doc})
                    count += result.modified_count
                else:
                    result = self.table.replace_one({primary_key: doc[primary_key]}, doc, upsert=True)
                    count += result.upserted_id is not None or result.modified_count
            return count
        else:
            raise TypeError("data must be a dict or a list of dicts.")
        
if __name__ == '__main__':
    
    # # 创建 MyMongo1 实例对象，连接 userinfo 表
    # mongo1 = MyMongo1(table_name='userinfo')

    # # 查询 asd=123 的文档
    # result1 = mongo1.table.find_one({'asd': 123})
    # print(result1)

    # # 切换到 t1 表
    # mongo1.change_table('t1')

    # # 查询 name='tom' 的文档
    # result2 = mongo1.table.find_one({'name': 'tom'})
    # print(result2)

    # # 连接 test 表
    # mongo2 = MyMongo1(table_name='test')

    # # 查询 age=20 的文档
    # result3 = mongo2.table.find_one({'age': 20})
    # print(result3)
    
    # 创建 MyMongo1 实例对象
    mongo = MyMongo1(ip='192.168.2.2', port=27018, db_name='a1', table_name='t1',username='root', password='y2YhNRHkIpYB54P3Tupt8PJz3D2BcTZaKRMZ')
    
    # 查询 age > 10 的文档
    # result = mongo.table.find({'age': {'$gt': 10}})
    # single_data = {'_id': 1, 'name': 'Alice', 'age': 25}
    # mongo.save(single_data)
    # print(result)
    # 
    # x3 = mongo.find({'age': {'$gt': 10}}, {'_id': 0, 'name': 1})   # 不返回id，只返回name
    # x = mongo.find_many({'age': {'$gt': 10}})
    # x2 = mongo.find1({'age': {'$gt': 10}})
    # x3 = mongo.find1({'age': {'$gt': 10}}, {'_id': 0, 'name': 1})   # 不返回id，只返回name
    # x = mongo.find_many({'age': {'$gt': 10}})
    # 将 name = test 的 age 改为 133
    mongo.update({'name': 'test', 'age': 1331}, primary_key='name')
    
    # query = {'name': 'test'}
    # update = {'$set': {'age': 133}}

    # result = mongo.table.update_many(query, update)
    # print(f"Number of documents modified: {result.modified_count}")


    