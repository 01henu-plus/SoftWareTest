import requests
import json

def test_sql_injection():
    url = "http://127.0.0.1:5000/login"
    
    print("\n=== SQL注入安全测试 ===\n")
    
    # 测试1: 正常登录
    print("【测试1】正常登录")
    payload1 = {"username": "admin", "password": "admin123"}
    res1 = requests.post(url, json=payload1)
    print(f"请求: {json.dumps(payload1, ensure_ascii=False)}")
    print(f"结果: {res1.status_code} - {res1.json()}\n")
    
    # 测试2: SQL注入攻击
    print("【测试2】SQL注入攻击 (' OR 1=1 --)")
    payload2 = {"username": "' OR 1=1 --", "password": "xxx"}
    res2 = requests.post(url, json=payload2)
    print(f"请求: {json.dumps(payload2, ensure_ascii=False)}")
    print(f"结果: {res2.status_code} - {res2.json()}")
    
    if res2.status_code == 200:
        print("✗ 漏洞存在: SQL注入攻击成功！\n")
    else:
        print("✓ 系统安全: 攻击被阻止\n")
    
    # 测试3: 错误凭据
    print("【测试3】错误的登录凭据")
    payload3 = {"username": "admin", "password": "wrong"}
    res3 = requests.post(url, json=payload3)
    print(f"请求: {json.dumps(payload3, ensure_ascii=False)}")
    print(f"结果: {res3.status_code} - {res3.json()}\n")

if __name__ == "__main__":
    test_sql_injection()
