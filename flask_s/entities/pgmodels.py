# pgmodels.py
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from datetime import datetime

class Base(DeclarativeBase):
    pass

class AppConfig(Base):
    __tablename__ = 'AppConfig'
    key = Column(String, primary_key=True)
    value = Column(String)
    text = Column(String)

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    pwd = Column(String, nullable=False)
    user_type = Column(Integer, default=0)
    is_ban = Column(Integer, default=0)
    is_active = Column(Integer, default=1)
    is_active2 = Column(Integer, default=1)
    is_active4 = Column(Integer, default=1)
    is_active5 = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class LoginRecord(Base):
    __tablename__ = 'LoginRecord'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    ip_address = Column(String)
    ip_location = Column(String)
    login_time = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String)

    user = relationship("Users", back_populates="LoginRecord")

# 在 User 类中添加关系
Users.LoginRecord = relationship("LoginRecord", back_populates="user")
