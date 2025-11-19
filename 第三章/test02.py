def reverse_string(s: str) -> str:
    """反转字符串"""
    return s[::-1]

def is_palindrome(s: str) -> bool:
    """检查字符串是否是回文"""
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def count_vowels(s: str) -> int:
    """统计字符串中的元音字母数量"""
    vowels = "aeiou"
    return sum(1 for char in s.lower() if char in vowels)

# 编写基于 pytest 的单元测试用例
import pytest

def test_reverse_string():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"

def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("A man a plan a canal Panama") is True

def test_count_vowels():
    assert count_vowels("hello") == 2
    assert count_vowels("HELLO") == 2
    assert count_vowels("xyz") == 0
    assert count_vowels("") == 0

if __name__ == "__main__":
    # 使用 pytest.main() 来运行测试并显示结果
    pytest.main(["-v", "--capture=no", __file__])