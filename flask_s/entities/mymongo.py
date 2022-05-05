from pymongo import MongoClient
from settings import *


class MyMongo1():

    def __init__(self, table_name=None):
        self.client = MongoClient('127.0.0.1', 27017)

        self.db = self.client['jwjc1']  # 等同于：client.db1
        if table_name:
            self.table_user = self.db[table_name]
        else:
            self.table_user = self.db['userinfo']  # 等同于：db.user

    def save(self, data):
        if isinstance(data, dict):
            if self.find({'_id': data.get('_id')}):
                self.update({'_id': data.get('_id')}, data)
            else:
                self.table_user.insert_many([data])
            return
        raise Exception('保存数据库那边为啥不考虑直接传字典呢?')
        user0 = {
            "xh": data[0],
            # "birth":datetime.datetime.now(),
            "name": data[1],
        }
        print(user0)

        # self.table_user.insert([{'aa':'b'}])
        # self.table_user.find_one()
        self.table_user.insert_many([user0])

    # print(table_user.count())

    #6、查找
    def find(self, tiaojian: dict):
        '''
        '''
        x = self.table_user.find_one(tiaojian)  # 这个又是相当于是普通的find，返回对象，需要for
        return x

    # #7、更新
    def update(self, tiaojian: dict, data: dict, hebing=False):
        '''
        tiaojian : 条件(字典)
        data: 修改后的数据(字典)
        hebing: 是否合并原本数据
        '''
        if hebing:
            data1 = self.find(tiaojian)
            data1.update(data)
            data = data1
        # print(self.table_user.update_one.__doc__)
        # self.table_user.update(tiaojian, data)
        # self.table_user.update_many(tiaojian, {'$inc': data})
        # TODO 有一说一，聚合函数每太弄懂
        # set, inc 这些是聚合函数 https://docs.mongodb.com/manual/reference/method/db.collection.updateMany/#std-label-updateMany-example-agg
        self.table_user.update_many(tiaojian, {'$set': data})

    def delete(self, tiaojian: dict):
        self.table_user.delete_one(tiaojian)
        
    # #8、传入新的文档替换旧的文档
    # table_user.save(
    #     {
    #         "_id":2,
    #         "name":'egon_xxx'
    #     }
    # )
if __name__ == '__main__':
    # MyMongo1(MONGODB_TABLE1).save(data={""})
    x = MyMongo1(MONGODB_TABLE1).find({"_id": "202040030805"})
    print(x)
    # MyMongo1(MONGODB_TABLE1).update({"_id":"202040030805"}, {"名字1234":"qeqw1re1332"})
    MyMongo1(MONGODB_TABLE1).save(
        {"_id": "202040030805", "名字112345": "qeqw1re1332"})
