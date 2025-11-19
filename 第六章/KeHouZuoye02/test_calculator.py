"""
计算器模块的测试用例
演示 GitHub Actions 持续集成
"""
import pytest
from calculator import add, subtract, multiply, divide, power


def test_add():
    """测试加法"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    print("✅ 加法测试通过")


def test_subtract():
    """测试减法"""
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5
    print("✅ 减法测试通过")


def test_multiply():
    """测试乘法"""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0
    print("✅ 乘法测试通过")


def test_divide():
    """测试除法"""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
    assert divide(5, 2) == 2.5
    print("✅ 除法测试通过")


def test_divide_by_zero():
    """测试除零异常"""
    with pytest.raises(ValueError, match="除数不能为零"):
        divide(10, 0)
    print("✅ 除零异常测试通过")


def test_power():
    """测试幂运算"""
    assert power(2, 3) == 8
    assert power(5, 2) == 25
    assert power(10, 0) == 1
    print("✅ 幂运算测试通过")


def test_edge_cases():
    """测试边界情况"""
    # 大数计算
    assert add(999999, 1) == 1000000
    
    # 小数计算
    assert abs(divide(1, 3) - 0.333333) < 0.00001
    
    # 负数
    assert multiply(-5, -5) == 25
    
    print("✅ 边界情况测试通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
