"""购物车结算微服务测试"""
import pytest
from app.checkout_service import app

@pytest.fixture
def client():
    """Flask测试客户端"""
    app.config['TESTING'] = True
    return app.test_client()

def test_checkout_total(client):
    """测试1: 单商品结算"""
    res = client.post('/checkout', json={"items": [{"price": 20, "quantity": 3}]})
    assert res.status_code == 200
    assert res.json["total"] == 60
    assert res.json["status"] == "ok"

def test_checkout_empty_cart(client):
    """测试2: 空购物车"""
    res = client.post('/checkout', json={"items": []})
    assert res.status_code == 400
    assert res.json["error"] == "empty cart"

def test_checkout_multiple_items(client):
    """测试3: 多商品结算"""
    data = {"items": [{"price": 20, "quantity": 3}, {"price": 15, "quantity": 2}, {"price": 10, "quantity": 1}]}
    res = client.post('/checkout', json=data)
    assert res.status_code == 200
    assert res.json["total"] == 100
