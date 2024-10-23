# pgmodels.py
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
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
