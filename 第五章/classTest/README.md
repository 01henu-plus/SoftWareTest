# Web登录功能测试

## 项目简介
简化的Web登录API测试系统，包含完整的输入验证和自动化测试。

## 功能特性
- **登录API**: `/api/login` POST接口
- **输入验证**: 用户名长度、密码强度检查
- **测试覆盖**: 8个自动化测试用例
- **测试报告**: 自动生成HTML报告

## 文件说明
- `app.py` - Flask登录服务（40行）
- `test_login.py` - pytest测试套件（8个测试）
- `run_tests.py` - 自动化测试运行脚本
- `test_report.html` - HTML测试报告

## 运行方式

### 方式1: 使用运行脚本（推荐）
```bash
python run_tests.py
```

### 方式2: 手动运行
```bash
# 启动服务器
python app.py

# 新终端运行测试
python -m pytest test_login.py -v

# 生成HTML报告
python -m pytest test_login.py -v --html=test_report.html --self-contained-html
```

## 测试用例

| 编号 | 测试场景 | 预期结果 |
|------|---------|---------|
| 01 | 正常登录 | 200 成功 |
| 02 | 密码错误 | 401 拒绝 |
| 03 | 用户不存在 | 401 拒绝 |
| 04 | 用户名为空 | 400 错误 |
| 05 | 密码为空 | 400 错误 |
| 06 | 用户名过短(<3) | 400 错误 |
| 07 | 用户名过长(>20) | 400 错误 |
| 08 | 密码过短(<6) | 400 错误 |

## 测试账户
- admin / admin123
- user1 / password123
- test / test123

## 技术栈
- Python 3.14
- Flask (Web框架)
- pytest (测试框架)
- requests (HTTP客户端)
