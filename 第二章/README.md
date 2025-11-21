# 第二章：SQL注入攻击安全测试

## 项目说明

本项目演示了SQL注入漏洞及其防御方法，包含：
- 存在SQL注入漏洞的登录系统
- 安全的登录系统（使用参数化查询）
- 完整的安全测试用例

## 文件结构

```
第二章/
├── README.md                          # 项目说明文档
├── SQA_Checklist_用户登录注册模块.md  # SQA检查表
├── login_system.py                    # 登录系统实现
└── test_sql_injection.py              # SQL注入安全测试
```

## SQL注入漏洞说明

### 什么是SQL注入？

SQL注入是一种代码注入技术，攻击者通过在应用程序的输入字段中插入恶意SQL代码，欺骗应用程序执行非预期的数据库操作。

### 案例演示

**漏洞代码：**
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
```

**正常登录：**
- 用户名：`admin`
- 密码：`admin123`
- SQL语句：`SELECT * FROM users WHERE username='admin' AND password='admin123'`

**SQL注入攻击：**
- 用户名：`admin`
- 密码：`' OR '1'='1`
- SQL语句：`SELECT * FROM users WHERE username='admin' AND password='' OR '1'='1'`
- 结果：由于 `'1'='1'` 永远为真，绕过了密码验证

## 运行测试

```powershell
# 运行SQL注入安全测试
python test_sql_injection.py
```

## 测试用例

| 测试编号 | 测试场景 | 预期结果 |
|---------|---------|---------|
| 测试1 | 正常登录（正确用户名密码） | 登录成功 ✅ |
| 测试2 | 错误密码 | 登录失败 ❌ |
| 测试3 | SQL注入：`' OR '1'='1` | 不安全方法：成功 ⚠️<br>安全方法：失败 ✅ |
| 测试4 | SQL注入：`admin'--` | 不安全方法：成功 ⚠️<br>安全方法：失败 ✅ |
| 测试5 | 参数化查询防御 | 阻止注入攻击 ✅ |
| 测试6 | 对比测试 | 验证安全方法有效性 |

## 防御措施

### 1. 使用参数化查询（最重要）

**不安全：**
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
```

**安全：**
```python
query = "SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, password))
```

### 2. 其他防御措施

- ✅ **输入验证**：限制输入格式和长度
- ✅ **最小权限原则**：数据库账户只授予必要的权限
- ✅ **错误处理**：不要在错误信息中暴露SQL语句
- ✅ **使用ORM框架**：如SQLAlchemy会自动处理SQL注入
- ✅ **Web应用防火墙（WAF）**：过滤恶意请求

## SQA视角

从软件质量保证（SQA）角度，SQL注入属于：
- **功能性缺陷**：保密安全性问题
- **测试要求**：
  - 需求阶段：定义安全标准
  - 设计阶段：规划防护手段
  - 编码阶段：避免拼接SQL字符串
  - 测试阶段：进行专项安全测试（反向测试）

## 测试数据

系统预置了以下测试用户：
- 用户名：`admin`，密码：`admin123`
- 用户名：`user1`，密码：`password1`
- 用户名：`user2`，密码：`password2`

## 学习目标

通过本项目，你将学习：
1. ✅ 理解SQL注入的原理和危害
2. ✅ 识别代码中的SQL注入漏洞
3. ✅ 掌握参数化查询的使用方法
4. ✅ 编写安全测试用例
5. ✅ 了解SQA在安全测试中的作用

## 注意事项

⚠️ **警告**：本项目仅用于教学目的，不要在生产环境中使用存在漏洞的代码！

---

**创建日期**：2025年11月20日  
**适用课程**：软件测试 - 第二章
