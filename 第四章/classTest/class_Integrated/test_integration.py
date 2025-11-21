"""
集成测试 - 订单系统
测试下单模块、库存模块、支付模块的集成
"""
import requests


def test_order_success():
    """测试1：正常下单成功"""
    url = "http://127.0.0.1:5000/order"
    data = {
        "item": "book",
        "qty": 2,
        "user": "user1",
        "price": 10
    }
    res = requests.post(url, json=data)
    
    assert res.status_code == 200
    assert res.json()["success"] == True
    print(f"✅ 测试1通过: {res.json()}")


def test_stock_insufficient():
    """测试2：库存不足"""
    url = "http://127.0.0.1:5000/order"
    data = {
        "item": "book",
        "qty": 100,  # 库存不足
        "user": "user1",
        "price": 10
    }
    res = requests.post(url, json=data)
    
    assert res.status_code == 400
    assert "库存不足" in res.json()["error"]
    print(f"✅ 测试2通过: {res.json()}")


def test_balance_insufficient():
    """测试3：余额不足"""
    url = "http://127.0.0.1:5000/order"
    data = {
        "item": "book",
        "qty": 2,
        "user": "user2",  # user2余额500
        "price": 300  # 总价600，余额不足
    }
    res = requests.post(url, json=data)
    
    assert res.status_code == 400
    assert "余额不足" in res.json()["error"]
    print(f"✅ 测试3通过: {res.json()}")


if __name__ == "__main__":
    print("="*60)
    print("集成测试 - 订单系统")
    print("="*60)
    
    try:
        test_order_success()
        test_stock_insufficient()
        test_balance_insufficient()
        
        print("\n" + "="*60)
        print("🎉 所有集成测试通过")
        print("="*60)
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
    except requests.exceptions.ConnectionError:
        print("\n❌ 连接失败: 请先启动Flask服务 (flask run)")

