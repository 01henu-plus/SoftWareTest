"""
Flask 登录接口 - 用于 SQL 注入安全测试
警告: 此代码包含 SQL 注入漏洞，仅用于教学演示！
"""
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# 数据库文件路径
DB_FILE = 'users.db'

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # 插入测试数据
    cursor.execute("DELETE FROM users")  # 清空旧数据
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'pass123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('test', 'test456')")
    
    conn.commit()
    conn.close()
    print("✓ 数据库初始化完成")

@app.route('/')
def index():
    """主页"""
    return '''
    <h1>SQL 注入测试系统</h1>
    <h2>登录接口: POST /login</h2>
    <h3>正常登录请求示例:</h3>
    <pre>
    {
        "username": "admin",
        "password": "admin123"
    }
    </pre>
    <h3>SQL 注入测试示例:</h3>
    <pre>
    {
        "username": "' OR 1=1 --",
        "password": "xxx"
    }
    </pre>
    <p style="color: red;">⚠️ 警告: 此系统存在 SQL 注入漏洞，仅用于安全测试演示！</p>
    '''

@app.route('/login', methods=['POST'])
def login():
    """
    登录接口 - 存在 SQL 注入漏洞！
    """
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    # 危险的 SQL 查询 - 直接拼接用户输入，存在 SQL 注入漏洞！
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    print(f"\n[SQL 查询] {query}")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        
        if result:
            print(f"[登录成功] 找到 {len(result)} 条记录")
            return jsonify({
                "status": "success",
                "message": "登录成功",
                "user_count": len(result),
                "data": result
            }), 200
        else:
            print("[登录失败] 未找到匹配用户")
            return jsonify({
                "status": "error",
                "message": "用户名或密码错误"
            }), 400
            
    except Exception as e:
        error_msg = str(e)
        print(f"[SQL 错误] {error_msg}")
        return jsonify({
            "status": "error",
            "message": error_msg
        }), 400

@app.route('/users', methods=['GET'])
def get_users():
    """查看所有用户（用于验证数据）"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return jsonify({
        "status": "success",
        "users": [{"id": u[0], "username": u[1]} for u in users]
    })

if __name__ == '__main__':
    print("=" * 60)
    print("  SQL 注入测试系统启动")
    print("=" * 60)
    
    # 初始化数据库
    init_db()
    
    print(f"\n🌐 访问地址: http://127.0.0.1:5000")
    print(f"📖 登录接口: POST http://127.0.0.1:5000/login")
    print(f"👥 查看用户: GET http://127.0.0.1:5000/users")
    print(f"\n⚠️  警告: 此系统存在 SQL 注入漏洞，仅用于教学演示！")
    print(f"\n按 Ctrl+C 停止服务器\n")
    
    app.run(debug=True, port=5000)
