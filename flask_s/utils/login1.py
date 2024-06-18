from flask_login import LoginManager, UserMixin
import os
from addict import Dict
# from entities.mymongo import MyMongo1
from entities.ysqlite import YSqlite1


def get_all_users():
    ysql = YSqlite1()
    with ysql:
        try: 
            users1 = ysql.find_all('users')
        except Exception as e:
            if 'no such table:' in str(e):
                print("没有users表")
                ysql.create_table('users', {'id': 'INTEGER PRIMARY KEY','name': 'str', 'pwd': 'str', 'user_type': 'int', 'is_ban': 'int'})
                print("创建users表完毕")
            users1 = {}
    # users1 = Dict(ysql.find({"user_type": "all_user"}) or {"user_type": "all_user", "all_users": {}})
    # 将 user1 : [{"name": "pscly", "pwd": "123"},{"name": "bbb", "pwd": "1234"}]
    # 转化为 users:  {"pscly": {"name": "pscly", "pwd": "123"}} ...
    # users 表结构该为 
    # {id, name, pwd, user_type, is_ban}
    users = {}
    for user in users1:
        if user.get("name"):
            users[user.get("name")] = Dict(user)
    return users


def get_one_user(name):
    ysql = YSqlite1()
    with ysql:
        users = ysql.find("users", {"name": name})
        if users:
            users = Dict(users[0])
    return users


def save_all_users():
    ysql = YSqlite1()
    with ysql:
        ysql.save("users", os.y.users1)  # TODO ??? 这啥 2024-06-18 12:00:39


def save_one_user(userdata: dict):
    ysql = YSqlite1()
    with ysql:
        ysql.save("users", userdata)


class User(UserMixin):
    def __init__(self):
        pass
