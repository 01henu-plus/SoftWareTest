# SQL 注入安全测试项目

## 项目说明
本项目演示了 SQL 注入漏洞的检测和测试方法。**仅用于教学目的！**

## ⚠️ 重要警告
- 本项目中的代码**故意包含**安全漏洞
- **切勿在生产环境中使用**
- 仅用于学习和理解 SQL 注入攻击原理

## 文件说明
- `app.py` - 存在 SQL 注入漏洞的 Flask 登录系统
- `test_sql_injection.py` - SQL 注入测试脚本
- `users.db` - SQLite 数据库（自动生成）
- `README.md` - 本文档

## 安全漏洞说明

### 漏洞代码示例
```python
# 危险的做法 - 直接拼接用户输入
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
```

### 攻击示例
输入以下用户名可以绕过身份验证：
```
用户名: ' OR 1=1 --
密码: 任意值
```

实际执行的 SQL 语句：
```sql
SELECT * FROM users WHERE username='' OR 1=1 --' AND password='xxx'
```
- `OR 1=1` 使条件永远为真
- `--` 注释掉后面的密码验证

## 运行步骤

### 1. 安装依赖
```bash
pip install flask requests
```

### 2. 启动 Flask 服务器
```bash
cd class_safe
python app.py
```

服务器将在 http://127.0.0.1:5000 启动

### 3. 运行 SQL 注入测试（在新终端中）
```bash
cd class_safe
python test_sql_injection.py
```

## 测试用例

### 测试 1: 正常登录
```json
{
    "username": "admin",
    "password": "admin123"
}
```
**预期结果**: 登录成功

### 测试 2: SQL 注入攻击
```json
{
    "username": "' OR 1=1 --",
    "password": "xxx"
}
```
**预期结果**: 绕过身份验证（漏洞存在）

### 测试 3: 错误凭据
```json
{
    "username": "admin",
    "password": "wrongpass"
}
```
**预期结果**: 登录失败

### 测试 4: 另一种注入方式
```json
{
    "username": "admin' --",
    "password": "anything"
}
```
**预期结果**: 绕过身份验证（漏洞存在）

## 安全修复方案

### 方案 1: 使用参数化查询
```python
# 安全的做法 - 使用参数化查询
query = "SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, password))
```

### 方案 2: 输入验证
```python
import re

def validate_input(input_str):
    # 只允许字母和数字
    if not re.match("^[a-zA-Z0-9]+$", input_str):
        raise ValueError("Invalid input")
    return input_str
```

### 方案 3: 使用 ORM
```python
from flask_sqlalchemy import SQLAlchemy

user = User.query.filter_by(username=username, password=password).first()
```

## 学习要点

1. **SQL 注入原理**: 通过构造特殊的输入，改变 SQL 语句的逻辑
2. **危险操作**: 直接拼接用户输入到 SQL 语句中
3. **防御方法**: 
   - 参数化查询（最重要）
   - 输入验证
   - 使用 ORM
   - 最小权限原则
   - WAF 防护

## 参考资料
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQLite 参数化查询文档](https://docs.python.org/3/library/sqlite3.html)

## 测试数据

系统预置用户：
- admin / admin123
- user1 / pass123
- test / test456

## 注意事项
1. 本项目仅用于教学演示
2. 理解漏洞原理有助于写出更安全的代码
3. 在实际开发中必须使用安全的编码实践
4. 定期进行安全测试和代码审查
