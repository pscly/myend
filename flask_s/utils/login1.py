from flask_login import UserMixin
from utils.database import db_session
from entities.pgmodels import Users
from datetime import datetime


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
        with db_session() as session:
            user = session.query(Users).filter_by(id=user_id).first()
            if user:
                return User(
                    id=user.id,
                    name=user.name,
                    user_type=user.user_type,
                    is_ban=user.is_ban,
                    created_at=user.created_at,
                    last_login=user.last_login
                )
        return None


def get_all_users():
    with db_session() as session:
        return {user.name: user for user in session.query(Users).all()}


def get_one_user(name):
    with db_session() as session:
        return session.query(Users).filter_by(name=name).first()


def save_one_user(userdata: dict):
    with db_session() as session:
        user = Users(**userdata)
        session.add(user)


def update_user(user_id: int, update_data: dict):
    with db_session() as session:
        session.query(Users).filter_by(id=user_id).update(update_data)


def delete_user(user_id: int):
    with db_session() as session:
        session.query(Users).filter_by(id=user_id).delete()


def update_last_login(user_id: int):
    with db_session() as session:
        session.query(Users).filter_by(id=user_id).update({'last_login': datetime.utcnow()})
