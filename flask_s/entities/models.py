# pgmodels.py
import os
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session


def get_session():
    return os.y.Session()


class Base(DeclarativeBase):
    pass

class AppConfig(Base):
    __tablename__ = 'AppConfig'
    key = Column(String, primary_key=True)
    value = Column(String)
    text = Column(String, default="")

class Users(Base, UserMixin):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    pwd = Column(String(255), nullable=False)
    user_type = Column(Integer, default=0)
    is_ban = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)   # 如果是 False 则不能登录 (似乎flask默认有这个判断？)
    created_at = Column(DateTime, default=lambda: datetime.now())
    last_login = Column(DateTime, default=lambda: datetime.now())

    login_records = relationship("LoginRecord", back_populates="user")

    def __init__(self, name, pwd, user_type=0, is_ban=False, is_active=True):
        self.name = name
        self.set_password(pwd)
        self.user_type = user_type
        self.is_ban = is_ban
        self.is_active = is_active

    def set_password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)

    @classmethod
    def get(cls, user_id):
        session = get_session()
        return session.query(cls).get(int(user_id))

    @classmethod
    def get_by_name(cls, name):
        session = get_session()
        return session.query(cls).filter_by(name=name).first()

    def update_last_login(self):
        self.last_login = datetime.now()
        session = get_session()
        session.commit()
        session.close()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_type': self.user_type,
            'is_ban': self.is_ban,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'last_login': self.last_login
        }

class LoginRecord(Base):
    __tablename__ = 'LoginRecord'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    ip_address = Column(String)
    ip_location = Column(String)
    login_time = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String)

    user = relationship("Users", back_populates="login_records")
