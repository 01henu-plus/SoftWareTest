"""
SQL 注入安全测试脚本
测试 Flask 登录接口的 SQL 注入漏洞
"""
import requests
import json

def test_sql_injection():
    """测试 SQL 注入漏洞"""
    url = "http://127.0.0.1:5000/login"
    
    print("\n" + "=" * 60)
    print("  SQL 注入安全测试")
    print("=" * 60)
    
    # 测试用例 1: 正常登录
    print("\n【测试用例 1】正常登录")
    print("-" * 60)
    payload1 = {
        "username": "admin",
        "password": "admin123"
    }
    print(f"请求数据: {json.dumps(payload1, ensure_ascii=False)}")
    
    try:
        res1 = requests.post(url, json=payload1)
        print(f"响应状态码: {res1.status_code}")
        print(f"响应内容: {res1.json()}")
        
        if res1.status_code == 200:
            print("✓ 测试结果: 正常登录成功")
        else:
            print("✗ 测试结果: 正常登录失败")
    except Exception as e:
        print(f"✗ 请求失败: {e}")
    
    # 测试用例 2: SQL 注入攻击
    print("\n【测试用例 2】SQL 注入攻击 (' OR 1=1 --)")
    print("-" * 60)
    payload2 = {
        "username": "' OR 1=1 --",
        "password": "xxx"
    }
    print(f"请求数据: {json.dumps(payload2, ensure_ascii=False)}")
    print(f"注入原理: 将 SQL 查询变为 'SELECT * FROM users WHERE username='' OR 1=1 --' AND password='xxx'")
    print(f"         其中 1=1 永远为真，-- 注释掉后面的密码验证")
    
    try:
        res2 = requests.post(url, json=payload2)
        print(f"响应状态码: {res2.status_code}")
        print(f"响应内容: {res2.json()}")
        
        if res2.status_code == 200:
            print("✗ 漏洞存在: SQL 注入攻击成功，绕过了身份验证！")
        else:
            print("✓ 系统安全: SQL 注入攻击被阻止")
            
        # 断言：检查是否存在漏洞
        assert res2.status_code == 400 or "error" in res2.text.lower(), "SQL 注入漏洞存在！"
        
    except AssertionError as e:
        print(f"\n⚠️  安全警报: {e}")
    except Exception as e:
        print(f"✗ 请求失败: {e}")
    
    # 测试用例 3: 错误的登录凭据
    print("\n【测试用例 3】错误的登录凭据")
    print("-" * 60)
    payload3 = {
        "username": "admin",
        "password": "wrongpass"
    }
    print(f"请求数据: {json.dumps(payload3, ensure_ascii=False)}")
    
    try:
        res3 = requests.post(url, json=payload3)
        print(f"响应状态码: {res3.status_code}")
        print(f"响应内容: {res3.json()}")
        
        if res3.status_code == 400:
            print("✓ 测试结果: 正确拒绝了错误凭据")
        else:
            print("✗ 测试结果: 应该拒绝错误凭据")
    except Exception as e:
        print(f"✗ 请求失败: {e}")
    
    # 测试用例 4: 另一种 SQL 注入尝试
    print("\n【测试用例 4】另一种 SQL 注入尝试 (admin' --)")
    print("-" * 60)
    payload4 = {
        "username": "admin' --",
        "password": "anything"
    }
    print(f"请求数据: {json.dumps(payload4, ensure_ascii=False)}")
    print(f"注入原理: 将 SQL 查询变为 'SELECT * FROM users WHERE username='admin' --' AND password='anything'")
    print(f"         -- 注释掉后面的密码验证部分")
    
    try:
        res4 = requests.post(url, json=payload4)
        print(f"响应状态码: {res4.status_code}")
        print(f"响应内容: {res4.json()}")
        
        if res4.status_code == 200:
            print("✗ 漏洞存在: SQL 注入攻击成功！")
        else:
            print("✓ 系统安全: SQL 注入攻击被阻止")
    except Exception as e:
        print(f"✗ 请求失败: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)
    print("\n⚠️  发现的安全问题:")
    print("1. 系统存在 SQL 注入漏洞")
    print("2. 未对用户输入进行过滤和验证")
    print("3. 使用了字符串拼接构造 SQL 查询")
    print("\n📝 修复建议:")
    print("1. 使用参数化查询（预编译语句）")
    print("2. 对用户输入进行严格验证和过滤")
    print("3. 使用 ORM 框架（如 SQLAlchemy）")
    print("4. 实施最小权限原则")
    print("5. 添加 WAF（Web 应用防火墙）")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_sql_injection()
