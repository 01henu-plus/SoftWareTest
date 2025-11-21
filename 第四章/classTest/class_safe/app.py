from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_FILE = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    cursor.execute("DELETE FROM users")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user', 'pass123')")
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    # SQL注入漏洞 - 直接拼接用户输入
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"SQL: {query}")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        
        if result:
            return jsonify({"status": "success", "message": "登录成功"}), 200
        else:
            return jsonify({"status": "error", "message": "用户名或密码错误"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    init_db()
    print("服务启动: http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
