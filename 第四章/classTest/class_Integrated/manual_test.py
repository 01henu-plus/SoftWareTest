"""
手动测试脚本 - 用于验证 Flask 服务是否正常运行
"""
import requests
import time

def test_server():
    """测试服务器连接"""
    print("正在测试 Flask 服务器...")
    time.sleep(1)  # 等待服务器完全启动
    
    try:
        # 测试 1: 正常下单
        print("\n[测试 1] 正常下单 (book, qty=2)")
        url = "http://127.0.0.1:5000/order"
        response = requests.post(url, json={"item": "book", "qty": 2}, timeout=5)
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 200 and response.json().get("success"):
            print("  ✓ 测试通过")
        else:
            print("  ✗ 测试失败")
        
        # 测试 2: 不存在的商品
        print("\n[测试 2] 不存在的商品 (phone, qty=1)")
        response = requests.post(url, json={"item": "phone", "qty": 1}, timeout=5)
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 400 and "不存在的商品" in response.json().get("error", ""):
            print("  ✓ 测试通过")
        else:
            print("  ✗ 测试失败")
        
        # 测试 3: 库存不足
        print("\n[测试 3] 库存不足 (book, qty=100)")
        response = requests.post(url, json={"item": "book", "qty": 100}, timeout=5)
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 400 and "库存不足" in response.json().get("error", ""):
            print("  ✓ 测试通过")
        else:
            print("  ✗ 测试失败")
        
        print("\n" + "="*50)
        print("所有测试完成！")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ 错误: 无法连接到服务器")
        print("请确保已经运行: python app.py")
    except Exception as e:
        print(f"\n✗ 错误: {e}")

if __name__ == "__main__":
    test_server()
