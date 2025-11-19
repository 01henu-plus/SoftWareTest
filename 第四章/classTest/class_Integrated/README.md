# 课堂作业运行说明

## 项目介绍
这是一个订单系统的集成测试案例，包含：
- Flask API 服务（订单模块 + 库存模块）
- 使用 requests 库进行 API 集成测试

## 文件说明
- `app.py`: Flask 应用，提供订单 API
- `test_integration.py`: 集成测试文件
- `课堂作业.py`: 项目说明文档
- `README.md`: 本文件

## 运行步骤

### 方法一：手动运行（推荐用于学习）

**步骤 1: 启动 Flask 服务**
```powershell
python app.py
```
或
```powershell
E:/python3.14/python.exe app.py
```

服务将在 http://127.0.0.1:5000 启动

**步骤 2: 在新终端运行测试**
打开新的终端窗口，执行：
```powershell
python test_integration.py
```
或使用 pytest：
```powershell
pytest -v test_integration.py
```

### 方法二：使用 VS Code REST Client 插件
1. 安装 REST Client 插件
2. 创建 `test.http` 文件
3. 编写 HTTP 请求并直接在 VS Code 中测试

### 方法三：使用 Postman
1. 启动 app.py
2. 在 Postman 中创建 POST 请求
3. URL: http://127.0.0.1:5000/order
4. Body (JSON):
   ```json
   {
     "item": "book",
     "qty": 2
   }
   ```

## API 接口文档

### POST /order
创建订单

**请求体:**
```json
{
  "item": "商品名称",
  "qty": 数量
}
```

**成功响应 (200):**
```json
{
  "success": true,
  "剩余库存": 8
}
```

**失败响应 (400):**
```json
{
  "error": "不存在的商品"
}
```
或
```json
{
  "error": "库存不足"
}
```

## 测试案例覆盖

1. ✓ 正常下单流程测试
2. ✓ 不存在的商品异常测试
3. ✓ 库存不足异常测试

## 课堂练习建议

### 练习 1: 修改接口参数
在 `app.py` 中，将第 11 行的 `item` 改为 `product`：
```python
item = request.json.get("product")  # 原来是 "item"
```
然后重新运行测试，观察集成测试能否发现这个接口不匹配问题。

### 练习 2: 增加新的测试用例
在 `test_integration.py` 中添加：
- 测试数量为 0 的情况
- 测试数量为负数的情况
- 测试缺少必填参数的情况

### 练习 3: 扩展功能
添加以下功能并编写对应的集成测试：
- GET /inventory - 查询当前库存
- POST /refund - 退货（增加库存）

## 故障排查

**问题：启动 app.py 时提示端口被占用**
解决：更改 app.py 最后一行的端口号
```python
app.run(debug=True, port=5001)  # 改为 5001 或其他端口
```

**问题：测试失败，提示连接拒绝**
解决：确保 Flask 服务已经启动并正在运行

**问题：Flask 未安装**
解决：运行 `pip install flask requests`

## 学习要点

1. **集成测试 vs 单元测试**：集成测试关注多个模块协作是否正常
2. **API 测试**：使用 requests 库模拟 HTTP 请求
3. **断言验证**：验证响应状态码和响应体内容
4. **接口契约**：前后端需要对接口参数达成一致
