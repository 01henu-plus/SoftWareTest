"""
用户登录系统 - SQL注入漏洞演示
"""
import sqlite3


class LoginSystem:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        test_users = [('admin', 'admin123'), ('user1', 'password1')]
        for username, password in test_users:
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            except sqlite3.IntegrityError:
                pass
        conn.commit()
        conn.close()
    
    def login_vulnerable(self, username, password):
        """不安全：直接拼接SQL"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            return {'success': bool(result), 'message': '登录成功' if result else '登录失败'}
        except Exception as e:
            conn.close()
            return {'success': False, 'message': f'错误: {str(e)}'}
    
    def login_secure(self, username, password):
        """安全：使用参数化查询"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=? AND password=?"
        try:
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            conn.close()
            return {'success': bool(result), 'message': '登录成功' if result else '登录失败'}
        except Exception as e:
            conn.close()
            return {'success': False, 'message': f'错误: {str(e)}'}
    
    def cleanup(self):
        import os
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
