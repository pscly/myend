from flask_login import UserMixin
from utils.db import get_db
from addict import Dict
from datetime import datetime
from utils.ip_location import get_ip_location
from entities.models import LoginRecord, Users as DBUsers
from utils.database import get_session
from flask import request
from flask_login import login_user as flask_login_user
from werkzeug.security import check_password_hash


class UserLogin(UserMixin):
    def __init__(self, id, name, user_type, is_ban, is_active, created_at, last_login):
        self.id = id
        self.name = name
        self.user_type = user_type
        self.is_ban = is_ban
        self.is_active = is_active
        self.created_at = created_at
        self.last_login = last_login

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.search_by_dict('Users', {'id': user_id}, to_dict=True)
        if user:
            user = user[0]
            return UserLogin(
                id=user['id'],
                name=user['name'],
                user_type=user['user_type'],
                is_ban=user['is_ban'],
                is_active=user['is_active'],
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


def login_user(username, password):
    # 获取用户
    user = DBUsers.query.filter_by(name=username).first()

    if user and check_password_hash(user.pwd, password):
        # 登录成功，记录登录信息
        try:
            session = get_session()
            ip_address = request.remote_addr
            ip_location = get_ip_location(ip_address)
            user_agent = request.headers.get("User-Agent", "Unknown")

            login_record = LoginRecord(
                user_id=user.id,
                ip_address=ip_address,
                ip_location=ip_location,
                user_agent=user_agent
            )
            session.add(login_record)
            session.commit()

            # 创建UserLogin对象并使用Flask-Login的login_user函数
            user_login = UserLogin(
                id=user.id,
                name=user.name,
                user_type=user.user_type,
                is_ban=user.is_ban,
                created_at=user.created_at,
                last_login=user.last_login
            )
            flask_login_user(user_login)

            return {"message": "Login successful", "user_id": user.id}, 200
        except Exception as e:
            session.rollback()
            return {"message": f"Login failed: {str(e)}"}, 500
        finally:
            session.close()
    else:
        # 登录失败
        return {"message": "Invalid username or password"}, 401
