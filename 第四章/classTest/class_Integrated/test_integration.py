# file: test_integration.py
import requests

def test_order_api():
    """测试订单 API 的集成测试"""
    url = "http://127.0.0.1:5000/order"
    res = requests.post(url, json={"item": "book", "qty": 2})
    assert res.status_code == 200
    assert res.json()["success"] == True
    print("✓ 测试通过: 订单 API 正常工作")
    print(f"  响应: {res.json()}")

def test_order_invalid_item():
    """测试不存在的商品"""
    url = "http://127.0.0.1:5000/order"
    res = requests.post(url, json={"item": "phone", "qty": 1})
    assert res.status_code == 400
    assert "不存在的商品" in res.json()["error"]
    print("✓ 测试通过: 正确处理不存在的商品")

def test_order_insufficient_stock():
    """测试库存不足的情况"""
    url = "http://127.0.0.1:5000/order"
    res = requests.post(url, json={"item": "book", "qty": 100})
    assert res.status_code == 400
    assert "库存不足" in res.json()["error"]
    print("✓ 测试通过: 正确处理库存不足")

if __name__ == "__main__":
    print("开始执行集成测试...\n")
    test_order_api()
    test_order_invalid_item()
    test_order_insufficient_stock()
    print("\n所有测试完成！")
