def is_palindrome(s):
    """判断字符串是否为回文"""
    s = s.lower().replace(" ", "")  # 统一小写并去除空格
    return s == s[::-1]