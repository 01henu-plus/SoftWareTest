# 浏览器兼容性测试项目

## 项目说明
本项目使用 Selenium 进行浏览器兼容性测试，测试登录页面在不同浏览器中的表现。

## 文件说明
- `login.html` - 简单的登录页面
- `app.py` - Flask 服务器，托管登录页面
- `test_browser.py` - Selenium 测试脚本，测试 Chrome、Firefox、Edge 浏览器

## 测试环境要求
1. Python 3.x
2. 已安装的浏览器：Chrome、Firefox、Edge
3. 必要的 Python 包：
   - selenium
   - webdriver-manager
   - flask

## 安装依赖
```bash
pip install selenium webdriver-manager flask
```

## 运行步骤

### 1. 启动 Flask 服务器
在一个终端中运行：
```bash
cd class_compatible
python app.py
```
服务器将在 http://127.0.0.1:5000 启动

### 2. 运行浏览器兼容性测试
在另一个终端中运行：
```bash
cd class_compatible
python test_browser.py
```

## 测试内容
测试脚本将自动：
1. 在 Chrome、Firefox、Edge 浏览器中打开登录页面
2. 验证页面元素是否正确加载
3. 填写用户名和密码
4. 点击登录按钮
5. 验证登录功能

## 预期结果
所有浏览器应该能够：
- 正确显示登录页面
- 找到所有表单元素
- 成功提交表单
- 显示登录成功提示

## 注意事项
- 首次运行时，webdriver-manager 会自动下载对应的浏览器驱动
- 确保系统中已安装对应的浏览器
- 测试过程中会自动打开和关闭浏览器窗口
