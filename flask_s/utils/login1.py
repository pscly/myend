from flask_login import LoginManager, UserMixin
import os
from addict import Dict
from entities.mymongo import MyMongo1


def get_all_users():
    mo = MyMongo1("users")
    users1 = mo.find_all()
    # users1 = Dict(mo.find({"user_type": "all_user"}) or {"user_type": "all_user", "all_users": {}})
    users = {}
    # 将 user1 : [{"name": "pscly", "pwd": "123"},{"name": "bbb", "pwd": "1234"}]
    # 转化为 users:  {"pscly": {"name": "pscly", "pwd": "123"}} ...
    for user in users1:
        if user.get("name"):
            users[user.get("name")] = Dict(user)
    # os.y.users1 = users
    return users


def get_one_user(name):
    mo = MyMongo1("users")
    users = Dict(mo.find({"name": name}))
    return users


def save_all_users():
    mo = MyMongo1("users")
    mo.save(os.y.users1)


def save_one_user(userdata: dict):
    mo = MyMongo1("users")
    mo.save(userdata)


class User(UserMixin):
    def __init__(self):
        pass
