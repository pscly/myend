import importlib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base


class YSqlTool:
    _instance = None

    def __new__(cls, db_url: str = None):
        if cls._instance is None:
            cls._instance = super(YSqlTool, cls).__new__(cls)
            cls._instance.initialize(db_url)
        return cls._instance

    def initialize(self, db_url: str):
        if not hasattr(self, 'engine'):
            try:
                self.error = None
                self.engine = create_engine(db_url)
                self.Session = sessionmaker(bind=self.engine)
                self.models = {}
                self.load_models()
            except Exception as e:
                print(f"数据库连接失败: {e}")
                self.error = True


    def load_models(self):
        """动态加载模型类并自动创建表"""
        models_module = importlib.import_module('pgmodels')
        Base = models_module.Base

        for name, cls in models_module.__dict__.items():
            if  'app'  in  name.lower():
                print()
            if isinstance(cls, type) and issubclass(cls, Base) and cls != Base:
                self.models[name] = cls
                
                # 检查表是否存在，如果不存在则创建
                if not inspect(self.engine).has_table(cls.__tablename__):
                    cls.__table__.create(self.engine)
                    print(f"自动创建了表: {cls.__tablename__}")
                else:
                    print(f"表已存在: {cls.__tablename__}")


    def get_session(self):
        """获取会话"""
        return self.Session()

    def execute_query(self, query, params=None):
        """执行查询并返回结果"""
        session = self.get_session()
        try:
            result = session.execute(text(query), params)
            return result.fetchall()
        finally:
            session.close()

    def execute_update(self, query, params=None):
        """执行更新操作"""
        session = self.get_session()
        try:
            result = session.execute(text(query), params)
            session.commit()
            return result.rowcount
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def insert(self, table_name, data):
        """插入数据"""
        model = self.models.get(table_name)
        if not model:
            raise ValueError(f"Model {table_name} not found")
        session = self.get_session()
        try:
            instance = model(**data)
            session.add(instance)
            session.commit()
            return instance
        finally:
            session.close()

    def update(self, table_name, filter_by, update_data):
        """更新数据"""
        model = self.models.get(table_name)
        if not model:
            raise ValueError(f"Model {table_name} not found")
        session = self.get_session()
        try:
            instances = session.query(model).filter_by(**filter_by).all()
            for instance in instances:
                for key, value in update_data.items():
                    setattr(instance, key, value)
            session.commit()
            return instances
        finally:
            session.close()

    def select(self, table_name, to_dict=False):
        """查询所有数据"""
        model = self.models.get(table_name)
        if not model:
            raise ValueError(f"Model {table_name} not found")
        session = self.get_session()
        try:
            if to_dict:
                return self.dbdata_to_dict(session.query(model).all())
            else:
                return session.query(model).all()
        finally:
            session.close()

    def search_by_dict(self, table_name, filter_by, to_dict=False):
        """按字典条件查询数据"""
        model = self.models.get(table_name)
        if not model:
            raise ValueError(f"Model {table_name} not found")
        session = self.get_session()
        try:
            if to_dict:
                return self.dbdata_to_dict(session.query(model).filter_by(**filter_by).all())
            else:
                return session.query(model).filter_by(**filter_by).all()
        finally:
            session.close()
            
    def dbdata_to_dict(self, data):
        """
        将数据库数据转换为字典
        """
        if not data:
            return []
        if isinstance(data, list):
            return [self._object_to_dict(item) for item in data]
        else:
            return self._object_to_dict(data)
        return []

    def _object_to_dict(self, obj):
        """
        将单个对象转换为字典
        """
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}


    def delete(self, table_name, filter_by):
        """删除数据"""
        model = self.models.get(table_name)
        if not model:
            raise ValueError(f"Model {table_name} not found")
        session = self.get_session()
        try:
            instances = session.query(model).filter_by(**filter_by).all()
            for instance in instances:
                session.delete(instance)
            session.commit()
            return len(instances)
        finally:
            session.close()

    def close(self):
        """关闭数据库连接"""
        self.engine.dispose()



if __name__ == '__main__':
    pgsql = YSqlTool('postgresql://pscly:111111@192.168.3.5:5432/yend')
    # pgsql.insert('Users', {'name': 'pscly', 'pwd': '12345'})
    # print(pgsql.search_by_dict('Users', {'name': 'pscly'}))
    # print(pgsql.select('Users', to_dict=True))
    # pgsql.insert('Users', {'name': 'pscly', 'pwd': '12345'})
    

