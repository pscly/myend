from entities.mypgsql import YSqlTool
from flask import current_app

def get_db():
    if not hasattr(current_app, 'db'):
        db_url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
        if not db_url:
            raise ValueError("SQLALCHEMY_DATABASE_URI not set in configuration")
        current_app.db = YSqlTool(db_url)
    return current_app.db

def get_session():
    return get_db().get_session()

SessionLocal = get_session
