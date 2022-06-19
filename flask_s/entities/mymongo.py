from pymongo import MongoClient


class MyMongo1():

    def __init__(self, table_name=None):
        self.client = MongoClient('127.0.0.1', 27017)

        self.db = self.client['yend1']  # 等同于：client.db1
        if table_name:
            self.table_user = self.db[table_name]
        else:
            self.table_user = self.db['userinfo']  # 等同于：db.user

    def save(self, data):
        """
        data 可以是一个dict or list
        args:
            data [dict or list]: 
        """
        if isinstance(data, dict):
            if self.find({'_id': data.get('_id')}):
                self.update({'_id': data.get('_id')}, data)
            else:
                self.table_user.insert_many([data])
            return
        if isinstance(data, list):
            self.table_user.insert_many(data)
            return

    def find(self, tiaojian: dict):
        return self.table_user.find_one(tiaojian)  # 这个又是相当于是普通的find，返回对象，需要for

    def find_many(self, tiaojian):
        return self.table_user.find(tiaojian)
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


if __name__ == '__main__':
    table = 'test1'
    x = MyMongo1(table).find({"_id": "202040030805"})
    print(x)
    MyMongo1(table).save(
        [{"_id": "111", "名字112345": "qeqw1re1332"},
         {"_id": "222", "名字112345": "qeqw1re1332"}])
    # 更新
    # MyMongo1(table).update({"_id": "202040030805"}, {" 字112345": "11xxx"})
