# pgmodels.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import DeclarativeBase

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
    name = Column(String, unique=True)  # unique 是唯一约束
    pwd = Column(String)
    user_type = Column(Integer, default=0)
    is_ban = Column(Integer, default=0)
