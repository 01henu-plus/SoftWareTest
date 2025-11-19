"""
Web 登录功能测试项目
基于 VSCode 的软件测试全流程教学案例
"""
from flask import Flask, request, jsonify, render_template_string
import hashlib

app = Flask(__name__)

# 模拟用户数据库
USERS = {
    'admin': hashlib.md5('admin123'.encode()).hexdigest(),
    'user1': hashlib.md5('password123'.encode()).hexdigest(),
    'test': hashlib.md5('test123'.encode()).hexdigest(),
}

# 登录页面HTML
LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录页面 - 测试系统</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            width: 400px;
        }
        
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
        }
        
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        .message {
            margin-top: 20px;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            display: none;
        }
        
        .message.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .message.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .test-info {
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            font-size: 12px;
        }
        
        .test-info h4 {
            margin-bottom: 10px;
            color: #667eea;
        }
        
        .test-info ul {
            list-style: none;
            padding-left: 0;
        }
        
        .test-info li {
            margin-bottom: 5px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>登录系统</h2>
        <form id="loginForm">
            <div class="form-group">
                <label for="username">用户名：</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">密码：</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">登录</button>
        </form>
        <div class="message" id="message"></div>
        
        <div class="test-info">
            <h4>测试账号</h4>
            <ul>
                <li>👤 admin / admin123</li>
                <li>👤 user1 / password123</li>
                <li>👤 test / test123</li>
            </ul>
        </div>
    </div>
    
    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const messageDiv = document.getElementById('message');
            
            fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data => {
                messageDiv.style.display = 'block';
                if (data.status === 'success') {
                    messageDiv.className = 'message success';
                    messageDiv.textContent = '✓ ' + data.message;
                } else {
                    messageDiv.className = 'message error';
                    messageDiv.textContent = '✗ ' + data.message;
                }
            })
            .catch(error => {
                messageDiv.style.display = 'block';
                messageDiv.className = 'message error';
                messageDiv.textContent = '✗ 请求失败: ' + error.message;
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """登录页面"""
    return render_template_string(LOGIN_PAGE)

@app.route('/api/login', methods=['POST'])
def login():
    """登录API接口"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # 验证输入
        if not username or not password:
            return jsonify({
                'status': 'error',
                'message': '用户名和密码不能为空'
            }), 400
        
        # 用户名长度验证
        if len(username) < 3 or len(username) > 20:
            return jsonify({
                'status': 'error',
                'message': '用户名长度应为3-20个字符'
            }), 400
        
        # 密码长度验证
        if len(password) < 6:
            return jsonify({
                'status': 'error',
                'message': '密码长度不能少于6个字符'
            }), 400
        
        # 检查用户是否存在
        if username not in USERS:
            return jsonify({
                'status': 'error',
                'message': '用户名不存在'
            }), 401
        
        # 验证密码
        password_hash = hashlib.md5(password.encode()).hexdigest()
        if USERS[username] != password_hash:
            return jsonify({
                'status': 'error',
                'message': '密码错误'
            }), 401
        
        # 登录成功
        return jsonify({
            'status': 'success',
            'message': f'欢迎回来，{username}！',
            'user': username
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """获取用户列表（测试用）"""
    return jsonify({
        'status': 'success',
        'users': list(USERS.keys())
    })

if __name__ == '__main__':
    print("=" * 60)
    print("  Web 登录功能测试系统")
    print("=" * 60)
    print(f"\n🌐 访问地址: http://127.0.0.1:5000")
    print(f"📖 API 文档: POST /api/login")
    print(f"\n测试账号:")
    print(f"  - admin / admin123")
    print(f"  - user1 / password123")
    print(f"  - test / test123")
    print(f"\n按 Ctrl+C 停止服务器\n")
    
    app.run(debug=True, port=5000)
