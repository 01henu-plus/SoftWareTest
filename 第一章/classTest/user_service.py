"""
用户注册服务 - 模拟用户注册流程
"""
import sqlite3
import os


class UserService:
    """用户服务类"""
    
    def __init__(self, db_path="users.db"):
        """初始化用户服务"""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def register_user(self, username, password, email=None):
        """
        注册用户
        :param username: 用户名
        :param password: 密码
        :param email: 邮箱（可选）
        :return: dict - 包含success和message的字典
        """
        # 数据验证
        if not username or not password:
            return {
                "success": False,
                "message": "用户名和密码不能为空"
            }
        
        if len(username) < 3:
            return {
                "success": False,
                "message": "用户名长度至少3个字符"
            }
        
        if len(password) < 6:
            return {
                "success": False,
                "message": "密码长度至少6个字符"
            }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 检查用户名是否已存在
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                return {
                    "success": False,
                    "message": "用户名已存在"
                }
            
            # 插入新用户
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, password, email)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return {
                "success": True,
                "message": "注册成功",
                "user_id": user_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"注册失败: {str(e)}"
            }
    
    def get_user_by_username(self, username):
        """根据用户名查询用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2]
            }
        return None
    
    def clear_database(self):
        """清空数据库（用于测试）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        conn.close()
    
    def close(self):
        """关闭并删除测试数据库"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
