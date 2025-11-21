"""
年龄验证系统 - 边界值分析
"""


def validate_age(age):
    """
    验证年龄是否有效
    有效范围：18-60岁
    
    返回：
        True: 有效年龄
        False: 无效年龄
        错误信息: 当输入类型错误时
    """
    # 类型检查
    if not isinstance(age, (int, float)):
        return "错误：非数字类型"
    
    # 负数检查
    if age < 0:
        return "错误：负数"
    
    # 浮点数检查
    if isinstance(age, float) and age != int(age):
        return "错误：浮点数"
    
    # 转换为整数
    age = int(age)
    
    # 边界值判断
    if age >= 18 and age <= 60:
        return True
    else:
        return False


if __name__ == "__main__":
    # 简单演示
    test_values = [17, 18, 19, 59, 60, 61, "abc", -5, 18.5]
    
    print("年龄验证演示：")
    for val in test_values:
        result = validate_age(val)
        print(f"年龄 {val}: {result}")
