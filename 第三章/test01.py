def isValidPassword(s: str) -> bool:
    """
    检查密码是否有效。
    要求：
    - 长度为6到12位。
    - 必须包含数字和字母。
    """
    if not (6 <= len(s) <= 12):
        return False
    has_digit = any(char.isdigit() for char in s)
    has_alpha = any(char.isalpha() for char in s)
    return has_digit and has_alpha

class TestIsValidPassword:
    """
    测试类，用于测试 isValidPassword 函数。
    """

    @staticmethod
    def run_tests():
        test_cases = [
            ("123456", False),  # 仅数字
            ("abcdef", False),  # 仅字母
            ("abc123", True),   # 数字和字母，长度符合
            ("a1", False),      # 长度不足
            ("a1b2c3d4e5f6", True),  # 边界值，长度12
            ("a1b2c3d4e5f6g", False), # 超过长度
            ("", False),       # 空字符串
        ]

        print("测试 isValidPassword 函数")
        for i, (password, expected) in enumerate(test_cases, 1):
            result = isValidPassword(password)
            print(f"测试用例 {i}: 输入: '{password}' | 期望: {expected} | 实际: {result} | {'通过' if result == expected else '失败'}")

# 运行测试
if __name__ == "__main__":
    TestIsValidPassword.run_tests()