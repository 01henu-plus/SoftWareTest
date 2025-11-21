from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# 测试账户
USERS = {
    "admin": "0192023a7bbd73250516f069df18b500",      # admin123
    "user1": "482c811da5d5b4bc6d497ffa98491e38",      # password123  
    "test": "05a671c66aefea124cc08b76ea6d30bb"        # test123
}

@app.route("/")
def index():
    return """<h1>登录API</h1>
    <p>POST /api/login</p>
    <p>测试账户: admin/admin123, user1/password123, test/test123</p>"""

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "无效请求"}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # 验证空值
    if not username or not password:
        return jsonify({"status": "error", "message": "用户名和密码不能为空"}), 400
    
    # 验证长度
    if len(username) < 3 or len(username) > 20:
        return jsonify({"status": "error", "message": "用户名长度应为3-20个字符"}), 400
    
    if len(password) < 6:
        return jsonify({"status": "error", "message": "密码长度不能少于6个字符"}), 400
    
    # 验证用户存在
    if username not in USERS:
        return jsonify({"status": "error", "message": "用户名不存在"}), 401
    
    # 验证密码
    pwd_hash = hashlib.md5(password.encode()).hexdigest()
    if USERS[username] != pwd_hash:
        return jsonify({"status": "error", "message": "密码错误"}), 401
    
    return jsonify({"status": "success", "message": f"欢迎回来，{username}！", "user": username}), 200

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
