# Web 登录功能测试项目

## 项目说明
基于 VSCode 的软件测试全流程教学案例，完成 Web 登录功能的完整测试流程。

## 任务目标
1. ✅ 设计并执行测试用例
2. ✅ 自动化执行测试
3. ✅ 提交缺陷报告
4. ✅ 生成测试报告

## 项目结构
```
classTest/
├── app.py              # Flask 登录系统
├── test_login.py       # pytest 自动化测试
├── README.md           # 项目文档
├── 测试用例.md         # 测试用例设计
├── 缺陷报告.md         # 缺陷跟踪
└── requirements.txt    # 依赖包
```

## 测试用例设计

### API 测试用例（8个）

| ID | 测试场景 | 输入 | 预期结果 | 优先级 |
|----|----------|------|----------|--------|
| TC01 | 正常登录 | admin/admin123 | 200, 登录成功 | P0 |
| TC02 | 错误密码 | admin/wrongpass | 401, 密码错误 | P0 |
| TC03 | 不存在用户 | nouser/pass | 401, 用户不存在 | P0 |
| TC04 | 空用户名 | 空/admin123 | 400, 不能为空 | P1 |
| TC05 | 空密码 | admin/空 | 400, 不能为空 | P1 |
| TC06 | 用户名过短 | ab/pass123 | 400, 长度错误 | P2 |
| TC07 | 用户名过长 | 21字符/pass | 400, 长度错误 | P2 |
| TC08 | 密码过短 | admin/12345 | 400, 长度错误 | P2 |

### UI 测试用例（2个）

| ID | 测试场景 | 操作步骤 | 预期结果 | 优先级 |
|----|----------|----------|----------|--------|
| TC09 | UI 正常登录 | 输入正确凭据并提交 | 显示成功消息 | P0 |
| TC10 | UI 错误密码 | 输入错误密码并提交 | 显示错误消息 | P0 |

## 安装依赖

```bash
pip install flask pytest requests selenium webdriver-manager
```

或使用 requirements.txt:

```bash
pip install -r requirements.txt
```

## 运行步骤

### 1. 启动 Web 应用

```bash
cd classTest
python app.py
```

应用将在 http://127.0.0.1:5000 启动

### 2. 使用 Chrome 浏览器手动测试

在 Chrome 中打开: http://127.0.0.1:5000

测试账号:
- admin / admin123
- user1 / password123
- test / test123

### 3. 运行自动化测试

在新终端中运行:

```bash
cd classTest
pytest test_login.py -v
```

### 4. 生成 HTML 测试报告

```bash
pytest test_login.py -v --html=test_report.html --self-contained-html
```

## 测试报告

### 测试统计
- **总用例数**: 10
- **通过数**: 10
- **失败数**: 0
- **通过率**: 100%

### 测试覆盖

#### 功能覆盖
- ✅ 正常登录流程
- ✅ 错误处理（密码错误、用户不存在）
- ✅ 输入验证（空值、长度限制）
- ✅ UI 交互测试

#### 边界值测试
- ✅ 用户名最小长度: 3
- ✅ 用户名最大长度: 20
- ✅ 密码最小长度: 6

## 缺陷报告

### 发现的问题

暂无缺陷发现 - 所有测试用例通过 ✅

## 技术栈

- **后端**: Flask 3.1.2
- **测试框架**: pytest 8.4.2
- **UI 测试**: Selenium 4.x
- **浏览器驱动**: Chrome + webdriver-manager
- **报告生成**: pytest-html

## 学习要点

### 1. 测试用例设计
- 等价类划分
- 边界值分析
- 错误猜测法

### 2. 自动化测试
- pytest 框架使用
- Selenium WebDriver
- 断言和验证

### 3. 测试报告
- 测试结果统计
- 缺陷跟踪
- HTML 报告生成

## Chrome 浏览器测试

### 手动测试步骤
1. 打开 Chrome 浏览器
2. 访问 http://127.0.0.1:5000
3. 按照测试用例进行测试
4. 记录测试结果

### 使用开发者工具
按 F12 打开 Chrome 开发者工具

#### Network 面板
- 查看 API 请求
- 检查响应状态码
- 分析请求/响应数据

#### Console 面板
```javascript
// 测试 API
fetch('http://127.0.0.1:5000/api/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
})
.then(r => r.json())
.then(console.log);
```

## 最佳实践

1. **测试独立性**: 每个测试用例相互独立
2. **清晰命名**: 测试方法名描述测试内容
3. **断言准确**: 使用精确的断言条件
4. **日志记录**: 记录测试过程和结果
5. **持续集成**: 集成到 CI/CD 流程

## 参考资料

- [pytest 文档](https://docs.pytest.org/)
- [Selenium 文档](https://www.selenium.dev/documentation/)
- [Flask 文档](https://flask.palletsprojects.com/)
- [软件测试方法](https://www.guru99.com/software-testing.html)

## 项目总结

本项目完整演示了 Web 应用测试的全流程：
1. ✅ 需求分析和测试计划
2. ✅ 测试用例设计和编写
3. ✅ 自动化测试实施
4. ✅ 测试执行和结果记录
5. ✅ 缺陷报告和跟踪
6. ✅ 测试报告生成

通过本项目，学习者可以掌握：
- 测试用例设计方法
- pytest 自动化测试框架
- Selenium UI 测试技术
- 测试报告编写规范
- 软件测试完整流程
