"""
实验室访问控制测试
"""
from lab_access_control import Person, LabAccessControl


def test_lab_access():
    print("="*70)
    print("高安全级别实验室访问控制测试")
    print("="*70)
    
    # 测试1：非员工 - 拒绝
    print("\n【测试1】非员工访问")
    p1 = Person("访客", is_employee=False)
    r1 = LabAccessControl.grant_access(p1)
    print(f"is_employee = {p1.is_employee}")
    print(f"结果: {'✅ 授权' if r1 else '❌ 拒绝'}")
    
    # 测试2：员工 + 高级许可 - 授权
    print("\n【测试2】员工 + 高级别安全许可")
    p2 = Person("员工A", is_employee=True, has_high_clearance=True)
    r2 = LabAccessControl.grant_access(p2)
    print(f"is_employee = {p2.is_employee}, has_high_clearance = {p2.has_high_clearance}")
    print(f"结果: {'✅ 授权' if r2 else '❌ 拒绝'}")
    
    # 测试3：员工 + 访问期 + 陪同 - 授权
    print("\n【测试3】员工 + 访问期内 + 有陪同")
    p3 = Person("员工B", is_employee=True, is_within_visit_window=True, is_escorted=True)
    r3 = LabAccessControl.grant_access(p3)
    print(f"is_employee = {p3.is_employee}, is_within_visit_window = {p3.is_within_visit_window}, is_escorted = {p3.is_escorted}")
    print(f"结果: {'✅ 授权' if r3 else '❌ 拒绝'}")
    
    # 测试4：员工 + 访问期 + 无陪同 - 拒绝
    print("\n【测试4】员工 + 访问期内 + 无陪同")
    p4 = Person("员工C", is_employee=True, is_within_visit_window=True, is_escorted=False)
    r4 = LabAccessControl.grant_access(p4)
    print(f"is_employee = {p4.is_employee}, is_within_visit_window = {p4.is_within_visit_window}, is_escorted = {p4.is_escorted}")
    print(f"结果: {'✅ 授权' if r4 else '❌ 拒绝'}")
    
    # 测试5：员工 + 无权限 - 拒绝
    print("\n【测试5】员工 + 无特殊权限")
    p5 = Person("员工D", is_employee=True)
    r5 = LabAccessControl.grant_access(p5)
    print(f"is_employee = {p5.is_employee}, has_high_clearance = {p5.has_high_clearance}")
    print(f"结果: {'✅ 授权' if r5 else '❌ 拒绝'}")
    
    # 决策表总结
    print("\n" + "="*70)
    print("决策表测试总结")
    print("="*70)
    print(f"{'场景':<15} {'员工':<8} {'高级许可':<10} {'访问期':<10} {'陪同':<8} {'结果':<8}")
    print("-"*70)
    
    test_cases = [
        ("非员工", False, False, False, False, False),
        ("员工+高级许可", True, True, False, False, True),
        ("员工+访问期+陪同", True, False, True, True, True),
        ("员工+访问期", True, False, True, False, False),
        ("仅员工", True, False, False, False, False),
    ]
    
    for name, emp, clearance, visit, escort, expected in test_cases:
        p = Person(name, emp, clearance, visit, escort)
        result = LabAccessControl.grant_access(p)
        status = "✅授权" if result else "❌拒绝"
        check = "✅" if result == expected else "❌"
        print(f"{name:<15} {str(emp):<8} {str(clearance):<10} {str(visit):<10} {str(escort):<8} {status:<8} {check}")
    
    print("="*70)
    print("🎯 所有测试完成")
    print("="*70)


if __name__ == "__main__":
    test_lab_access()
