from flask_login import UserMixin
from utils.db import get_db
from addict import Dict
from datetime import datetime
from utils.ip_location import get_ip_location
from entities.pgmodels import LoginRecord
from utils.database import SessionLocal


class User(UserMixin):
    def __init__(self, id, name, user_type, is_ban, created_at, last_login):
        self.id = id
        self.name = name
        self.user_type = user_type
        self.is_ban = is_ban
        self.created_at = created_at
        self.last_login = last_login

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.search_by_dict('Users', {'id': user_id}, to_dict=True)
        if user:
            user = user[0]
            return User(
                id=user['id'],
                name=user['name'],
                user_type=user['user_type'],
                is_ban=user['is_ban'],
                created_at=user['created_at'],
                last_login=user['last_login']
            )
        return None


def get_all_users():
    db = get_db()
    users = db.select('Users', to_dict=True)
    return {user['name']: Dict(user) for user in users}


def get_one_user(name):
    db = get_db()
    users = db.search_by_dict('Users', {'name': name}, to_dict=True)
    return Dict(users[0]) if users else None


def save_one_user(userdata: dict):
    db = get_db()
    userdata['created_at'] = datetime.utcnow()
    db.insert('Users', userdata)


def update_user(user_id: int, update_data: dict):
    db = get_db()
    db.update('Users', {'id': user_id}, update_data)


def delete_user(user_id: int):
    db = get_db()
    db.delete('Users', {'id': user_id})


def update_last_login(user_id: int):
    db = get_db()
    db.update('Users', {'id': user_id}, {'last_login': datetime.utcnow()})


def login_user(username, password, request):
    # ... 现有的登录验证代码 ...

    if user and verify_password(password, user.hashed_password):
        # 登录成功，记录登录信息
        db = SessionLocal()
        ip_address = request.client.host
        ip_location = get_ip_location(ip_address)
        user_agent = request.headers.get("user-agent", "Unknown")

        login_record = LoginRecord(
            user_id=user.id,
            ip_address=ip_address,
            ip_location=ip_location,
            user_agent=user_agent
        )
        db.add(login_record)
        db.commit()
        db.close()

        # ... 返回登录成功的代码 ...

    # ... 返回登录失败的代码 ...
