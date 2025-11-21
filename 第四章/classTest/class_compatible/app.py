from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
@app.route('/login')
def login():
    html_path = os.path.join(os.path.dirname(__file__), 'login.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    print("登录页面服务器启动: http://127.0.0.1:5000/login")
    app.run(debug=False, port=5000)
