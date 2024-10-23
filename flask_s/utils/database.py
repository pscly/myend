from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app, g
from contextlib import contextmanager

Base = declarative_base()

class Database:
    def __init__(self):
        self.engine = None
        self.session_factory = None

    def init_app(self, app):
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self):
        if 'db_session' not in g:
            g.db_session = self.session_factory()
        return g.db_session

    @contextmanager
    def session_scope(self):
        session = self.get_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

db = Database()

def init_db(app):
    db.init_app(app)
    Base.metadata.create_all(db.engine)

def get_db():
    return db

@contextmanager
def db_session():
    return db.session_scope()
