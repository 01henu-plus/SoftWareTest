from main import is_palindrome

def test_palindrome():
    # 测试标准回文
    assert is_palindrome("level") is True
    # 测试非回文
    assert is_palindrome("hello") is False
    # 测试含空格和大小写的回文
    assert is_palindrome("A man a plan a canal Panama") is True