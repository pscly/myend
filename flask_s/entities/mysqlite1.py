import sqlite3
from addict import Dict
import os


class MySqlite:
    def __init__(self, table_name=None):
        db_path = os.y.config.get("sqlite_db_path", "mydatabase.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.table_name = table_name or "userinfo"
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        """
        是为了避免没有这个行列存在的情况
        他就创建了两个列  _id 和 name
        """
        self.cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {self.table_name}
                            (_id TEXT PRIMARY KEY, 
                            name TEXT)"""
        )
        self.conn.commit()

    def disconnect(self):
        self.conn.close()

    def save(self, data):
        if isinstance(data, dict):
            if self.find({"_id": data.get("_id")}):
                self.update({"_id": data.get("_id")}, data)
            else:
                columns = ", ".join(data.keys())
                placeholders = ", ".join("?" * len(data))
                sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
                self.cursor.execute(sql, tuple(data.values()))
                self.conn.commit()
        elif isinstance(data, list):
            for item in data:
                self.save(item)

    def find(self, condition: dict):
        """
        这个只能查询到第一个w
        """
        where_clause = " AND ".join(f"{key}=?" for key in condition)
        sql = f"SELECT * FROM {self.table_name} WHERE {where_clause}"
        self.cursor.execute(sql, tuple(condition.values()))
        return self.cursor.fetchone()

    def find_many(self, condition=None):
        if condition:
            where_clause = " AND ".join(f"{key}=?" for key in condition)
            sql = f"SELECT * FROM {self.table_name} WHERE {where_clause}"
            self.cursor.execute(sql, tuple(condition.values()))
        else:
            sql = f"SELECT * FROM {self.table_name}"
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def find_all(self):
        return self.find_many()

    def update(self, condition: dict, data: dict, hebing=False):
        if hebing:
            data1 = self.find(condition)
            if data1:
                data1 = dict(zip(data1.keys(), data1))
                data1.update(data)
                data = data1
        set_clause = ", ".join(f"{key}=?" for key in data)
        where_clause = " AND ".join(f"{key}=?" for key in condition)
        sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"
        self.cursor.execute(sql, tuple(data.values()) + tuple(condition.values()))
        self.conn.commit()

    def delete(self, condition: dict):
        where_clause = " AND ".join(f"{key}=?" for key in condition)
        sql = f"DELETE FROM {self.table_name} WHERE {where_clause}"
        self.cursor.execute(sql, tuple(condition.values()))
        self.conn.commit()


if __name__ == "__main__":
    os.y = Dict(
        {
            "config": {
                "sqlite_db_path": "mydatabase.db",
            }
        }
    )
    # 创建 MySqlite 实例对象
    sqlite = MySqlite("user1")
    # sqlite = MyMongo1('tt',ip='192.168.2.2', port=27018, username='root', password='y1C;r;K:27ZO-PQnb>X3+5=f0@W9uePIJ',db_name='yend1')
    sqlite.save(
        [
            {"_id": "111", "name": "qeqw1re1332"},
            {"_id": "222", "name": "qeqw1re1332"},
            {"_id": "333", "name": "qeqw1re1332"},
        ]
    )
    # 查询 asd=123 的文档
    # result = sqlite.table_user.find_one({"name": 123})
    # print(result)
    all_data = sqlite.find_all()
    for data in all_data:
        print(data)