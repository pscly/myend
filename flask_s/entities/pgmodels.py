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
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class LoginRecord(Base):
    __tablename__ = 'login_records'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String)
    ip_location = Column(String)
    login_time = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String)

    user = relationship("User", back_populates="login_records")

# 在 User 类中添加关系
User.login_records = relationship("LoginRecord", back_populates="user")
