"""
SQL注入攻击安全测试
"""
from login_system import LoginSystem


def test_sql_injection():
    """SQL注入测试"""
    system = LoginSystem("test.db")
    
    print("="*60)
    print("SQL注入攻击安全测试")
    print("="*60)
    
    # 测试1：正常登录
    print("\n【测试1】正常登录")
    result = system.login_vulnerable("admin", "admin123")
    print(f"结果: {result['message']}")
    
    # 测试2：SQL注入攻击 - ' OR '1'='1
    print("\n【测试2】SQL注入攻击 - 密码: ' OR '1'='1")
    print("原理: 构造永真条件绕过密码验证")
    result = system.login_vulnerable("admin", "' OR '1'='1")
    if result['success']:
        print("⚠️ 漏洞存在：SQL注入攻击成功！")
    else:
        print("✅ 安全：攻击被阻止")
    
    # 测试3：安全方法防御
    print("\n【测试3】安全方法 - 参数化查询")
    result = system.login_secure("admin", "' OR '1'='1")
    if not result['success']:
        print("✅ 防御成功：注入被阻止")
    else:
        print("❌ 防御失败")
    
    # 测试4：对比
    print("\n【测试4】对比测试")
    print("-"*60)
    print(f"{'测试场景':<20} {'不安全方法':<15} {'安全方法':<15}")
    print("-"*60)
    
    tests = [
        ("正常登录", "admin", "admin123"),
        ("SQL注入攻击", "admin", "' OR '1'='1"),
    ]
    
    for name, user, pwd in tests:
        r1 = system.login_vulnerable(user, pwd)
        r2 = system.login_secure(user, pwd)
        s1 = "✅成功" if r1['success'] else "❌失败"
        s2 = "✅成功" if r2['success'] else "❌失败"
        print(f"{name:<20} {s1:<15} {s2:<15}")
    
    print("-"*60)
    print("\n结论:")
    print("• 不安全方法：SQL注入可绕过验证 ⚠️")
    print("• 安全方法：参数化查询成功防御 ✅")
    print("="*60)
    
    system.cleanup()


if __name__ == "__main__":
    test_sql_injection()
