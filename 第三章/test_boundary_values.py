"""
黑盒测试 - 边界值分析测试
测试年龄验证功能（18-60岁有效）
"""
from age_validator import validate_age


def test_boundary_values():
    """边界值分析测试"""
    
    print("="*70)
    print("黑盒测试 - 边界值分析")
    print("需求：输入年龄（18-60岁）为有效")
    print("="*70)
    
    # 有效边界值测试
    print("\n【测试1】有效边界值")
    valid_boundaries = [18, 19, 59, 60]
    
    for age in valid_boundaries:
        result = validate_age(age)
        status = "✅" if result == True else "❌"
        print(f"{status} 年龄 {age}: {result} (预期: True)")
    
    # 无效边界值测试
    print("\n【测试2】无效边界值")
    invalid_boundaries = [17, 61]
    
    for age in invalid_boundaries:
        result = validate_age(age)
        status = "✅" if result == False else "❌"
        print(f"{status} 年龄 {age}: {result} (预期: False)")
    
    # 类型边界测试
    print("\n【测试3】类型边界值")
    type_boundaries = [
        ("abc", "错误：非数字类型"),
        (-5, "错误：负数"),
        (18.5, "错误：浮点数")
    ]
    
    for value, expected in type_boundaries:
        result = validate_age(value)
        status = "✅" if expected in str(result) else "❌"
        print(f"{status} 输入 {value}: {result}")
    
    # 边界值总结表
    print("\n" + "="*70)
    print("边界值测试总结")
    print("="*70)
    print(f"{'测试值':<15} {'类型':<15} {'预期结果':<15} {'实际结果':<15} {'状态'}")
    print("-"*70)
    
    test_cases = [
        (18, "有效边界", "True", validate_age(18)),
        (19, "有效边界", "True", validate_age(19)),
        (59, "有效边界", "True", validate_age(59)),
        (60, "有效边界", "True", validate_age(60)),
        (17, "无效边界", "False", validate_age(17)),
        (61, "无效边界", "False", validate_age(61)),
        ("abc", "类型边界", "错误", validate_age("abc")),
        (-5, "类型边界", "错误", validate_age(-5)),
        (18.5, "类型边界", "错误", validate_age(18.5)),
    ]
    
    for value, type_name, expected, actual in test_cases:
        check = "✅" if (expected == "True" and actual == True) or \
                       (expected == "False" and actual == False) or \
                       (expected == "错误" and isinstance(actual, str)) else "❌"
        print(f"{str(value):<15} {type_name:<15} {expected:<15} {str(actual):<15} {check}")
    
    print("="*70)
    print("🎯 边界值分析测试完成")
    print("="*70)


if __name__ == "__main__":
    test_boundary_values()
