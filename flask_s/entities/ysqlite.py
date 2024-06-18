"""
python 简单操作sqlite

高级点的:  https://docs.sqlalchemy.org/en/20/tutorial/engine.html

"""

import sqlite3
from sqlite3 import Error, OperationalError  


class YSqlite1:
    """
    用于管理 SQLite 数据库的类。

    提供连接数据库、创建表格、以及执行 CRUD 操作的方法。
    """

    def __init__(self, db_path='y_database.db'):
        """
        初始化 SQLiteManager 对象。

        Args:
            db_path (str): 数据库文件的路径。
        """

        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        建立数据库连接。

        Returns:
            SQLiteManager: 返回自身，以便在 with 语句中使用。
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return self
        except OperationalError as e:
            print(f"数据库连接错误: {e}")
            raise  # 重新抛出异常，以便外部捕获处理

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        关闭数据库连接。
        """
        if exc_type:    # 遇到异常就回滚 
            print(f"事务被打断: {exc_val}")
            self.conn.rollback()  # 回滚事务
        else:
            self.conn.commit()  # 提交事务
        self.conn.close()

        
    
    def transaction(self):
        """
        创建一个上下文管理器，用于手动控制事务。

        可以通过抛出 异常来打断事务。

        Yields:
            SQLiteManager: 返回自身，以便在 with 语句中使用。
        """
        self.conn.isolation_level = None  # 关闭自动提交
        try:
            yield self  # 返回自身，以便在 with 语句块中执行数据库操作
            self.conn.commit()  # 提交事务
        except Exception as e:  # 捕获数据库操作错误
            print(f"事务执行失败: {e}")
            self.conn.rollback()  # 回滚事务
            raise



    def create_table(self, table_name, columns):
        """
        创建数据表。

        Args:
            table_name (str): 表格名称。
            columns (dict): 表格列定义，格式为 {'列名': '数据类型'}。
        """

        try:
            column_defs = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
            self.cursor.execute(sql)
            self.conn.commit()
        except OperationalError as e:
            print(f"创建表格错误: {e}")
            self.conn.rollback()  # 回滚事务，防止数据异常
            raise

    def insert(self, table_name, data):
        """
        插入数据到表格。

        Args:
            table_name (str): 表格名称。
            data (dict): 要插入的数据，格式为 {'列名': '值'}。
        """

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, tuple(data.values()))
        # self.conn.commit()

    def like_search(self, table_name, column, keyword, columns='*'):
        """
        在指定列中进行模糊查询。

        Args:
            table_name (str): 表格名称。
            column (str): 要进行模糊查询的列名。
            keyword (str): 查询关键字。
            columns (str, optional): 要查询的列，默认为 '*' (所有列)。

        Returns:
            list: 查询结果。
        """

        sql = f"SELECT {columns} FROM {table_name} WHERE {column} LIKE ?"
        self.cursor.execute(sql, (f'%{keyword}%',))
        return self.cursor.fetchall()

    
    def select(self, table_name, columns='*', where=None):
        """
        从表格中查询数据。

        Args:
            table_name (str): 表格名称。
            columns (str, optional): 要查询的列，默认为 '*' (所有列)。
            where (str, optional): WHERE 子句，用于过滤数据。

        Returns:
            list: 查询结果。
        """

        sql = f"SELECT {columns} FROM {table_name}"
        if where:
            sql += f" WHERE {where}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self, table_name, data, where):
        """
        更新表格中的数据。

        Args:
            table_name (str): 表格名称。
            data (dict): 要更新的数据，格式为 {'列名': '值'}。
            where (str): WHERE 子句，用于指定要更新的行。
        """

        set_clause = ', '.join([f"{col} = ?" for col in data.keys()])
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
        self.cursor.execute(sql, tuple(data.values()))
        # self.conn.commit()

    def exact_search(self, table_name, column, value, columns='*'):
        """
        在指定列中进行精准查询。

        Args:
            table_name (str): 表格名称。
            column (str): 要进行精准查询的列名。
            value (str): 查询值。
            columns (str, optional): 要查询的列，默认为 '*' (所有列)。

        Returns:
            list: 查询结果。
        """

        sql = f"SELECT {columns} FROM {table_name} WHERE {column} = ?"
        self.cursor.execute(sql, (value,))
        return self.cursor.fetchall()

    def search_by_dict(self, table_name, query_dict, columns='*'):
        """
        使用字典进行多条件精准查询，返回字典列表。

        Args:
            table_name (str): 表格名称。
            query_dict (dict): 查询条件字典，格式为 {'列名': '值'}。
            columns (str, optional): 要查询的列，默认为 '*' (所有列)。

        Returns:
            list: 查询结果，每个元素都是一个字典，键为列名，值为对应值。
        """

        where_clause = " AND ".join([f"{col} = ?" for col in query_dict.keys()])
        sql = f"SELECT {columns} FROM {table_name} WHERE {where_clause}"
        self.cursor.execute(sql, tuple(query_dict.values()))
        results = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return [dict(zip(column_names, row)) for row in results]


    def like_search_by_dict(self, table_name, query_dict, columns='*'):
        """
        使用字典进行多条件模糊查询，返回字典列表。

        Args:
            table_name (str): 表格名称。
            query_dict (dict): 查询条件字典，格式为 {'列名': '值'}。
            columns (str, optional): 要查询的列，默认为 '*' (所有列)。

        Returns:
            list: 查询结果，每个元素都是一个字典，键为列名，值为对应值。
        """

        where_clause = " AND ".join([f"{col} LIKE ?" for col in query_dict.keys()])
        values = tuple([f"%{val}%" for val in query_dict.values()])
        sql = f"SELECT {columns} FROM {table_name} WHERE {where_clause}"
        self.cursor.execute(sql, values)
        results = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return [dict(zip(column_names, row)) for row in results]


    def find(self, table_name, query_dict, columns='*'):
        return self.search_by_dict(table_name, query_dict, columns)

    def find_all(self, table_name):
        """
        拿到一个表中所有的值
        """
        sql = f"SELECT * FROM {table_name}"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return [dict(zip(column_names, row)) for row in results]

    def save(self, table_name, data, p_key='id'):
        """
        保存数据到表格中。

        Args:
            table_name (str): 表格名称。
            data (dict or list): 要保存的数据，可以是字典格式 {'列名': '值'} 
                                  或者列表套字典 [{'列名': '值'}, {'列名': '值'}]。
            p_key (str, optional): 主键列名，默认为 'id'。

        如果 data 中包含主键值，并且该值在数据库中存在，则更新数据；
        否则，插入新数据。
        """

        if isinstance(data, list):  # 处理列表套字典的情况
            for item in data:
                self._save_single_item(table_name, item, p_key)
        elif isinstance(data, dict):  # 处理单个字典的情况
            self._save_single_item(table_name, data, p_key)
        else:
            raise ValueError("data 参数必须是字典或字典列表")

    def _save_single_item(self, table_name, data, p_key):
        """
        保存单个数据项到表格中。

        Args:
            table_name (str): 表格名称。
            data (dict): 要保存的单个数据项，格式为 {'列名': '值'}。
            p_key (str): 主键列名。
        """
        if p_key in data:
            # 如果主键值存在，尝试更新数据
            existing_data = self.search_by_dict(table_name, {p_key: data[p_key]})
            if existing_data:
                self._update_data(table_name, data, p_key)
            else:
                self._insert_data(table_name, data)
        else:
            # 如果主键值不存在，插入新数据
            self._insert_data(table_name, data)

    def _insert_data(self, table_name, data):
        """
        插入数据到表格。

        Args:
            table_name (str): 表格名称。
            data (dict): 要插入的数据，格式为 {'列名': '值'}。
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, tuple(data.values()))
        # try:
        #     columns = ', '.join(data.keys())
        #     placeholders = ', '.join(['?'] * len(data))
        #     sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        #     self.cursor.execute(sql, tuple(data.values()))
        #     self.conn.commit()
        # except OperationalError as e:
        #     print(f"插入数据错误: {e}")
        #     self.conn.rollback()
        #     raise

    def _update_data(self, table_name, data, p_key):
        """
        更新表格中的数据。

        Args:
            table_name (str): 表格名称。
            data (dict): 要更新的数据，格式为 {'列名': '值'}。
            p_key (str): 主键列名。
        """
        update_fields = ', '.join([f"{key} = ?" for key in data if key != p_key])
        sql = f"UPDATE {table_name} SET {update_fields} WHERE {p_key} = ?"
        values = list(data.values())
        values.append(data[p_key])  # 将主键值添加到 values 的末尾
        self.cursor.execute(sql, tuple(values))
        # try:
        #     update_fields = ', '.join([f"{key} = ?" for key in data if key != p_key])
        #     sql = f"UPDATE {table_name} SET {update_fields} WHERE {p_key} = ?"
        #     values = list(data.values())
        #     values.append(data[p_key])  # 将主键值添加到 values 的末尾
        #     self.cursor.execute(sql, tuple(values))
        #     self.conn.commit()
        # except OperationalError as e:
        #     print(f"更新数据错误: {e}")
        #     self.conn.rollback()
        #     raise

        
    def delete(self, table_name, where):
        """
        从表格中删除数据。

        Args:
            table_name (str): 表格名称。
            where (str): WHERE 子句，用于指定要删除的行。
        """

        sql = f"DELETE FROM {table_name} WHERE {where}"
        self.cursor.execute(sql)
        # self.conn.commit()

if __name__ == '__main__':
            
    # 创建 SQLiteManager 对象
    db_manager = YSqlite1('y_database.db')

    # 使用 with 语句自动管理数据库连接
    with db_manager:
        # 创建表格
        db_manager.create_table('users', {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT', 'email': 'TEXT'})

    #     # 插入数据
    #     db_manager.insert('users', {'name': 'Pscly', 'email': 'Pscly@qq.com'})
    #     db_manager.insert('users', {'name': 'Pslsy1', 'email': 'Pslsy1@qq.com'})
    #     db_manager.insert('users', {'name': 'Ps111', 'email': 'Pslsy1@qq.com'})

    #     # 查询数据
    #     users = db_manager.select('users')
    #     users = db_manager.search_by_dict('users', {'name': 'Pscly'})
    #     users = db_manager.like_search_by_dict('users', {'name': 'Ps'})
    #     print(users)

    #     # 更新数据
    #     db_manager.update('users', {'email': 'john.doe@example.com'}, 'id = 1')

    #     # 删除数据
    #     db_manager.delete('users', 'id = 1')
    a = 1
    #  db_manager.transaction()
    with db_manager:
        db_manager.insert('users', {'name': '1231', 'email': 'Pscly@qq.com'})
        # if a == 1:
        #     raise Exception("a 等于 1，触发事务回滚！")

        

