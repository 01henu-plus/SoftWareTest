"""
测试用户注册流程
测试场景：前端界面调用 -> 用户服务（创建账户）-> 数据库（保存数据）

测试点：
1. 用户服务是否能正确接收前端数据并成功写入数据库？
2. 写入失败时是否会向前端返回错误信息？
"""
import os
from user_service import UserService


def test_user_registration_flow():
    """测试用户注册流程"""
    
    print("=" * 60)
    print("测试用户注册流程")
    print("=" * 60)
    
    # 创建用户服务实例（使用测试数据库）
    service = UserService("test_users.db")
    service.clear_database()  # 清空测试数据
    
    # 测试1: 正常注册流程
    print("\n【测试1】正常注册流程")
    print("步骤: 前端界面 -> 用户服务 -> 数据库")
    result = service.register_user("testuser", "password123", "test@example.com")
    
    assert result["success"] == True, "注册应该成功"
    assert result["message"] == "注册成功", "应该返回成功消息"
    assert "user_id" in result, "应该返回用户ID"
    print(f"✅ 测试通过: {result['message']}")
    print(f"   用户ID: {result['user_id']}")
    
    # 验证数据是否写入数据库
    user = service.get_user_by_username("testuser")
    assert user is not None, "用户应该存在于数据库中"
    assert user["username"] == "testuser", "用户名应该正确"
    print(f"✅ 验证通过: 数据已成功保存到数据库")
    print(f"   查询结果: ID={user['id']}, 用户名={user['username']}, 邮箱={user['email']}")
    
    # 测试2: 写入失败 - 用户名为空
    print("\n【测试2】写入失败 - 用户名为空")
    result = service.register_user("", "password123")
    
    assert result["success"] == False, "注册应该失败"
    assert "用户名" in result["message"], "应该返回错误信息"
    print(f"✅ 测试通过: 正确返回错误信息")
    print(f"   错误消息: {result['message']}")
    
    # 测试3: 写入失败 - 密码为空
    print("\n【测试3】写入失败 - 密码为空")
    result = service.register_user("user2", "")
    
    assert result["success"] == False, "注册应该失败"
    assert "密码" in result["message"], "应该返回错误信息"
    print(f"✅ 测试通过: 正确返回错误信息")
    print(f"   错误消息: {result['message']}")
    
    # 测试4: 写入失败 - 用户名太短
    print("\n【测试4】写入失败 - 用户名太短")
    result = service.register_user("ab", "password123")
    
    assert result["success"] == False, "注册应该失败"
    assert "长度" in result["message"], "应该返回长度错误信息"
    print(f"✅ 测试通过: 正确返回错误信息")
    print(f"   错误消息: {result['message']}")
    
    # 测试5: 写入失败 - 密码太短
    print("\n【测试5】写入失败 - 密码太短")
    result = service.register_user("user3", "12345")
    
    assert result["success"] == False, "注册应该失败"
    assert "密码" in result["message"] and "长度" in result["message"], "应该返回密码长度错误"
    print(f"✅ 测试通过: 正确返回错误信息")
    print(f"   错误消息: {result['message']}")
    
    # 测试6: 写入失败 - 用户名已存在
    print("\n【测试6】写入失败 - 用户名已存在")
    result = service.register_user("testuser", "newpassword")
    
    assert result["success"] == False, "注册应该失败"
    assert "已存在" in result["message"], "应该返回用户名已存在错误"
    print(f"✅ 测试通过: 正确返回错误信息")
    print(f"   错误消息: {result['message']}")
    
    # 测试7: 成功注册多个用户
    print("\n【测试7】成功注册多个用户")
    users = [
        ("user_zhang", "pass123456", "zhang@test.com"),
        ("user_wang", "pass789012", "wang@test.com"),
        ("user_li", "pass345678", "li@test.com")
    ]
    
    for username, password, email in users:
        result = service.register_user(username, password, email)
        assert result["success"] == True, f"用户 {username} 注册应该成功"
        print(f"✅ 用户注册成功: {username}")
    
    # 测试8: 验证所有数据都在数据库中
    print("\n【测试8】验证所有用户数据")
    all_usernames = ["testuser", "user_zhang", "user_wang", "user_li"]
    for username in all_usernames:
        user = service.get_user_by_username(username)
        assert user is not None, f"用户 {username} 应该在数据库中"
        print(f"✅ 验证通过: {username} 存在于数据库")
    
    # 清理测试数据
    service.close()
    
    print("\n" + "=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)
    print("\n测试总结:")
    print("✓ 用户服务能正确接收前端数据")
    print("✓ 数据能成功写入数据库")
    print("✓ 写入失败时正确返回错误信息")
    print("✓ 所有验证规则正常工作")


if __name__ == "__main__":
    test_user_registration_flow()
