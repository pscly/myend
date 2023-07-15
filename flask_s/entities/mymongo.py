from pymongo import MongoClient
import os
from addict import Dict


class MyMongo1:
    def __init__(self, table_name=None):
        ip = os.y.config.get("mongodb_ip")
        port = os.y.config.get("mongodb_port")
        user = os.y.config.get("mongodb_user") or ""
        pwd = os.y.config.get("mongodb_pwd") or ""
        # self.client = MongoClient('127.0.0.1', 27017)
        # 构建MongoDB URI
        if user and pwd:
            uri = f"mongodb://{user}:{pwd}@{ip}:{port}/"
            self.client = MongoClient(uri)
        else:
            self.client = MongoClient(ip, int(port))

        self.db = self.client["yend1"]  # 等同于：client.db1
        if table_name:
            self.table_user = self.db[table_name]
        else:
            self.table_user = self.db["userinfo"]  # 等同于：db.user

    # __instance = None
    # def __new__(
    #     cls,
    #     table_name="userinfo",
    #     ip="127.0.0.1",
    #     port=27017,
    #     username="",
    #     password="",
    #     db_name="yend1",
    # ):
    #     """

    #     原本就光一个table_name就可以了 但是为了后续扩展性方便 我就加了个db_name
    #     """
    #     if cls.__instance is None:
    #         cls.__instance = super().__new__(cls)
    #         cls.__instance.ip = ip
    #         cls.__instance.port = port
    #         cls.__instance.username = username
    #         cls.__instance.password = password
    #         cls.__instance.db_name = db_name
    #         cls.__instance.table_name = table_name or "userinfo"
    #         cls.__instance.connect()
    #     return cls.__instance

    # def connect(self):
    #     try:
    #         client = MongoClient(
    #             host=self.ip,
    #             port=self.port,
    #             username=self.username,
    #             password=self.password,
    #             authSource=self.db_name,
    #             authMechanism="SCRAM-SHA-256",
    #         )
    #         self.db = client[self.db_name]
    #         self.table_user = self.db[self.table_name]
    #     except Exception as e:
    #         print(f"Failed to connect to MongoDB: {e}")

    def disconnect(self):
        self.client.close()

    def save(self, data):
        """
        data 可以是一个dict or list
        args:
            data [dict or list]:
        """
        if isinstance(data, dict):
            if self.find({"_id": data.get("_id")}):
                self.update({"_id": data.get("_id")}, data)
            else:
                self.table_user.insert_many([data])
            return
        if isinstance(data, list):
            self.table_user.insert_many(data)
            return

    def find(self, tiaojian: dict):
        return self.table_user.find_one(tiaojian)  # 这个又是相当于是普通的find，返回对象，需要for

    def find_many(self, tiaojian):
        if tiaojian:
            return self.table_user.find(tiaojian)
        return self.table_user.find()   # 返回所有

    def find_all(self):
        """
        出去后需要自己转换一下才能用 [Dict(i) for i in data]
        """
        return self.table_user.find()

    # #7、更新

    def update(self, tiaojian: dict, data: dict, hebing=False):
        """
        tiaojian : 条件(字典)
        data: 修改后的数据(字典)
        hebing: 是否合并原本数据
        """
        if hebing:
            data1 = self.find(tiaojian)
            data1.update(data)
            data = data1
        # print(self.table_user.update_one.__doc__)
        # self.table_user.update(tiaojian, data)
        # self.table_user.update_many(tiaojian, {'$inc': data})
        # TODO 有一说一，聚合函数每太弄懂
        # set, inc 这些是聚合函数 https://docs.mongodb.com/manual/reference/method/db.collection.updateMany/#std-label-updateMany-example-agg
        self.table_user.update_many(tiaojian, {"$set": data})

    def delete(self, tiaojian: dict):
        self.table_user.delete_one(tiaojian)


if __name__ == "__main__":
    os.y = Dict(
        {
            "config": {
                "mongodb_ip": "127.0.0.1",
                # "mongodb_ip": "192.168.2.2",
                "mongodb_port": "27017",
                "mongodb_user": "root",
                # "mongodb_user": "",
                "mongodb_pwd": "x",
                # "mongodb_pwd": "",
            }
        }
    )

    # mongodb_ip
    # mongodb_port
    # mongodb_user
    # mongodb_pwd

    # table = 'test1'
    # # x = MyMongo1(table).find({"_id": "202040030805"})
    # print(x)
    # x = MyMongo1()
    # MyMongo1(table).save(
    #     [{"_id": "111", "名字112345": "qeqw1re1332"},
    #      {"_id": "222", "名字112345": "qeqw1re1332"}])
    # # 更新
    # # MyMongo1(table).update({"_id": "202040030805"}, {" 字112345": "11xxx"})

    # 创建 MyMongo1 实例对象
    mongo = MyMongo1("tt")
    # mongo = MyMongo1('tt',ip='192.168.2.2', port=27018, username='root', password='y1C;r;K:27ZO-PQnb>X3+5=f0@W9uePIJ',db_name='yend1')
    # mongo.save(
    #     [
    #         {"_id": "111", "名字112345": "qeqw1re1332"},
    #         {"_id": "222", "名字112345": "qeqw1re1332"},
    #     ]
    # )
    # 查询 asd=123 的文档
    # result = mongo.table_user.find_one({"name": 123})
    # print(result)
    all_data = mongo.find_all()
    for data in all_data:
        print(dict(data))
