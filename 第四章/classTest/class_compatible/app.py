"""
登录页面服务器
提供简单的 HTTP 服务来托管登录页面
"""
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
@app.route('/login')
def login():
    """返回登录页面"""
    # 读取 HTML 文件内容
    html_path = os.path.join(os.path.dirname(__file__), 'login.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    print("=" * 60)
    print("  登录页面服务器")
    print("=" * 60)
    print(f"\n🌐 访问登录页面: http://127.0.0.1:5000/login")
    print(f"\n按 Ctrl+C 停止服务器\n")
    app.run(debug=True, port=5000)
