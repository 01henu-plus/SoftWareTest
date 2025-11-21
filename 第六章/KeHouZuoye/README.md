# 购物车结算微服务测试

## 项目简介
Flask购物车结算API的自动化测试项目。

## 功能特性
- **结算API**: POST /checkout 计算购物车总价
- **输入验证**: 空购物车检测
- **多商品支持**: 批量计算

## 文件说明
- `app/checkout_service.py` - Flask微服务 (16行)
- `test_checkout.py` - pytest测试套件 (26行)
- `report.html` - HTML测试报告

## 运行测试

```bash
# 方式1: pytest
pytest test_checkout.py -v

# 方式2: 生成HTML报告
pytest test_checkout.py -v --html=report.html --self-contained-html
```

## API示例

```python
# 请求
POST http://127.0.0.1:5000/checkout
{
  "items": [
    {"price": 20, "quantity": 3},
    {"price": 15, "quantity": 2}
  ]
}

# 响应
{"total": 90, "status": "ok"}
```

## 测试用例

| 测试 | 场景 | 预期 |
|------|------|------|
| test_checkout_total | 单商品 | 200, total=60 |
| test_checkout_empty_cart | 空购物车 | 400, error |
| test_checkout_multiple_items | 多商品 | 200, total=100 |

## 测试结果
✅ 3 passed in 0.12s

## 技术栈
- Flask (Web框架)
- pytest (测试框架)
- Python 3.14
