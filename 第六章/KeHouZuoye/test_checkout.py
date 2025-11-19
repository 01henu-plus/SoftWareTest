"""
Checkout 微服务测试脚本
使用 pytest + requests + multiprocessing 进行测试
"""
import requests
import multiprocessing
import time
from app.checkout_service import app


def run_server():
    """在子进程中运行 Flask 服务器"""
    app.run(port=5000, debug=False)


def test_checkout_total():
    """测试用例: 计算购物车总价"""
    # 启动服务器
    p = multiprocessing.Process(target=run_server)
    p.start()
    
    # 等待服务器启动
    time.sleep(1)
    
    try:
        # 准备测试数据
        data = {"items": [{"price": 20, "quantity": 3}]}
        
        # 发送请求
        res = requests.post("http://127.0.0.1:5000/checkout", json=data)
        
        # 验证状态码
        assert res.status_code == 200, f"期望状态码 200，实际 {res.status_code}"
        
        # 验证返回数据
        json_data = res.json()
        assert json_data["total"] == 60, f"期望总价 60，实际 {json_data['total']}"
        assert json_data["status"] == "ok", f"期望状态 ok，实际 {json_data['status']}"
        
        print("✅ 测试通过: test_checkout_total")
        print(f"   请求数据: {data}")
        print(f"   响应数据: {json_data}")
        print(f"   状态码: {res.status_code}")
        
    finally:
        # 终止服务器进程
        p.terminate()
        p.join()


def test_checkout_empty_cart():
    """测试用例: 空购物车"""
    # 启动服务器
    p = multiprocessing.Process(target=run_server)
    p.start()
    
    # 等待服务器启动
    time.sleep(1)
    
    try:
        # 准备测试数据（空购物车）
        data = {"items": []}
        
        # 发送请求
        res = requests.post("http://127.0.0.1:5000/checkout", json=data)
        
        # 验证状态码
        assert res.status_code == 400, f"期望状态码 400，实际 {res.status_code}"
        
        # 验证返回数据
        json_data = res.json()
        assert "error" in json_data, "期望返回 error 字段"
        assert json_data["error"] == "empty cart", f"期望错误信息 'empty cart'，实际 {json_data['error']}"
        
        print("✅ 测试通过: test_checkout_empty_cart")
        print(f"   请求数据: {data}")
        print(f"   响应数据: {json_data}")
        print(f"   状态码: {res.status_code}")
        
    finally:
        # 终止服务器进程
        p.terminate()
        p.join()


def test_checkout_multiple_items():
    """测试用例: 多个商品"""
    # 启动服务器
    p = multiprocessing.Process(target=run_server)
    p.start()
    
    # 等待服务器启动
    time.sleep(1)
    
    try:
        # 准备测试数据（多个商品）
        data = {
            "items": [
                {"price": 20, "quantity": 3},
                {"price": 15, "quantity": 2},
                {"price": 10, "quantity": 1}
            ]
        }
        
        # 发送请求
        res = requests.post("http://127.0.0.1:5000/checkout", json=data)
        
        # 验证状态码
        assert res.status_code == 200, f"期望状态码 200，实际 {res.status_code}"
        
        # 验证返回数据
        json_data = res.json()
        expected_total = 20*3 + 15*2 + 10*1  # 60 + 30 + 10 = 100
        assert json_data["total"] == expected_total, f"期望总价 {expected_total}，实际 {json_data['total']}"
        
        print("✅ 测试通过: test_checkout_multiple_items")
        print(f"   请求数据: {data}")
        print(f"   响应数据: {json_data}")
        print(f"   计算验证: 20*3 + 15*2 + 10*1 = {expected_total}")
        
    finally:
        # 终止服务器进程
        p.terminate()
        p.join()


if __name__ == "__main__":
    print("=" * 70)
    print("  Checkout 微服务测试")
    print("=" * 70)
    print()
    
    # 运行所有测试
    test_checkout_total()
    print()
    test_checkout_empty_cart()
    print()
    test_checkout_multiple_items()
    
    print()
    print("=" * 70)
    print("  🎉 所有测试通过! (3/3)")
    print("=" * 70)
