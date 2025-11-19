# ==================== 待测试的程序代码 ====================

def divide(a, b):
    return a / b  # 缺陷1：未检查除数为0

def find_max(lst):
    max_val = 0  # 缺陷2：如果列表全是负数，返回结果错误
    for x in lst:
        if x > max_val:
            max_val = x
    return max_val

def get_item(lst, idx):
    return lst[idx]  # 缺陷3：未检查索引越界


# ==================== 测试用例设计 ====================

class TestCase:
    """测试用例类"""
    def __init__(self, case_id, function_name, input_data, expected_output, description):
        self.case_id = case_id
        self.function_name = function_name
        self.input_data = input_data
        self.expected_output = expected_output
        self.description = description
        self.actual_output = None
        self.status = None  # PASS / FAIL / ERROR
        self.error_message = None

# 定义测试用例
test_cases = [
    # divide() 函数测试用例
    TestCase(
        case_id="TC001",
        function_name="divide",
        input_data={"a": 10, "b": 2},
        expected_output=5.0,
        description="正常除法运算：10除以2"
    ),
    TestCase(
        case_id="TC002",
        function_name="divide",
        input_data={"a": 10, "b": 0},
        expected_output="应抛出异常或返回错误提示",
        description="边界测试：除数为0（缺陷1）"
    ),
    
    # find_max() 函数测试用例
    TestCase(
        case_id="TC003",
        function_name="find_max",
        input_data={"lst": [1, 5, 3, 9, 2]},
        expected_output=9,
        description="正常情况：正整数列表找最大值"
    ),
    TestCase(
        case_id="TC004",
        function_name="find_max",
        input_data={"lst": [-5, -2, -8, -1]},
        expected_output=-1,
        description="边界测试：全是负数的列表（缺陷2）"
    ),
    TestCase(
        case_id="TC005",
        function_name="find_max",
        input_data={"lst": [0, -3, -7, -2]},
        expected_output=0,
        description="边界测试：包含0的负数列表"
    ),
    
    # get_item() 函数测试用例
    TestCase(
        case_id="TC006",
        function_name="get_item",
        input_data={"lst": [10, 20, 30, 40], "idx": 2},
        expected_output=30,
        description="正常情况：获取列表中间元素"
    ),
    TestCase(
        case_id="TC007",
        function_name="get_item",
        input_data={"lst": [10, 20, 30], "idx": 5},
        expected_output="应抛出异常或返回错误提示",
        description="边界测试：索引超出范围（缺陷3）"
    ),
    TestCase(
        case_id="TC008",
        function_name="get_item",
        input_data={"lst": [10, 20, 30], "idx": -1},
        expected_output=30,
        description="边界测试：负数索引（Python支持）"
    ),
]


# ==================== 测试执行 ====================

def execute_tests():
    """执行所有测试用例"""
    print("=" * 80)
    print("测试执行报告".center(80))
    print("=" * 80)
    print()
    
    for tc in test_cases:
        print(f"【{tc.case_id}】{tc.description}")
        print(f"测试函数: {tc.function_name}")
        print(f"输入数据: {tc.input_data}")
        print(f"期望输出: {tc.expected_output}")
        
        try:
            # 根据函数名执行相应的测试
            if tc.function_name == "divide":
                result = divide(tc.input_data["a"], tc.input_data["b"])
                tc.actual_output = result
                
            elif tc.function_name == "find_max":
                result = find_max(tc.input_data["lst"])
                tc.actual_output = result
                
            elif tc.function_name == "get_item":
                result = get_item(tc.input_data["lst"], tc.input_data["idx"])
                tc.actual_output = result
            
            # 判断测试结果
            if tc.actual_output == tc.expected_output:
                tc.status = "✓ PASS"
            else:
                tc.status = "✗ FAIL"
                
        except Exception as e:
            tc.status = "✗ ERROR"
            tc.actual_output = None
            tc.error_message = f"{type(e).__name__}: {str(e)}"
        
        print(f"实际输出: {tc.actual_output if tc.actual_output is not None else tc.error_message}")
        print(f"测试结果: {tc.status}")
        print("-" * 80)
        print()


# ==================== 缺陷分析报告 ====================

def generate_bug_report():
    """生成缺陷分析报告"""
    print("=" * 80)
    print("缺陷分析报告".center(80))
    print("=" * 80)
    print()
    
    bugs = [
        {
            "id": "BUG-001",
            "function": "divide(a, b)",
            "type": "Error（错误）",
            "severity": "严重",
            "description": "除数为0时未进行检查",
            "test_case": "TC002",
            "phenomenon": "当b=0时，程序抛出ZeroDivisionError异常，导致程序崩溃",
            "detection_phase": "单元测试阶段",
            "fix_suggestion": """
建议修复代码：
def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b
            """,
            "prevention": "在代码审查阶段加强边界条件检查，确保所有可能导致异常的输入都被处理"
        },
        {
            "id": "BUG-002",
            "function": "find_max(lst)",
            "type": "Fault（故障）",
            "severity": "中等",
            "description": "初始化max_val=0导致全负数列表返回错误结果",
            "test_case": "TC004",
            "phenomenon": "当列表全是负数时（如[-5,-2,-8,-1]），期望返回-1，实际返回0",
            "detection_phase": "单元测试阶段（边界测试）",
            "fix_suggestion": """
建议修复代码：
def find_max(lst):
    if not lst:
        raise ValueError("列表不能为空")
    max_val = lst[0]  # 使用列表第一个元素初始化
    for x in lst[1:]:
        if x > max_val:
            max_val = x
    return max_val
            """,
            "prevention": "设计测试用例时应包含边界情况，如全负数、全零、空列表等特殊场景"
        },
        {
            "id": "BUG-003",
            "function": "get_item(lst, idx)",
            "type": "Error（错误）",
            "severity": "严重",
            "description": "索引越界时未进行检查",
            "test_case": "TC007",
            "phenomenon": "当idx=5超出列表范围[10,20,30]时，抛出IndexError异常",
            "detection_phase": "单元测试阶段（边界测试）",
            "fix_suggestion": """
建议修复代码：
def get_item(lst, idx):
    if idx < 0 or idx >= len(lst):
        raise IndexError(f"索引{idx}超出范围[0, {len(lst)-1}]")
    return lst[idx]
            """,
            "prevention": "在处理数组/列表索引操作时，必须进行边界检查。使用自动化测试工具进行边界值分析"
        }
    ]
    
    for bug in bugs:
        print(f"缺陷编号: {bug['id']}")
        print(f"缺陷函数: {bug['function']}")
        print(f"缺陷类型: {bug['type']}")
        print(f"严重程度: {bug['severity']}")
        print(f"缺陷描述: {bug['description']}")
        print(f"触发用例: {bug['test_case']}")
        print(f"现象说明: {bug['phenomenon']}")
        print(f"发现阶段: {bug['detection_phase']}")
        print(f"修复建议: {bug['fix_suggestion']}")
        print(f"预防措施: {bug['prevention']}")
        print("=" * 80)
        print()


# ==================== 测试总结 ====================

def generate_summary():
    """生成测试总结"""
    print("=" * 80)
    print("测试总结".center(80))
    print("=" * 80)
    print()
    
    total = len(test_cases)
    passed = sum(1 for tc in test_cases if tc.status == "✓ PASS")
    failed = sum(1 for tc in test_cases if tc.status == "✗ FAIL")
    errors = sum(1 for tc in test_cases if tc.status == "✗ ERROR")
    
    print(f"总测试用例数: {total}")
    print(f"通过: {passed} ({passed/total*100:.1f}%)")
    print(f"失败: {failed} ({failed/total*100:.1f}%)")
    print(f"错误: {errors} ({errors/total*100:.1f}%)")
    print()
    print("测试结论:")
    print("  该程序存在3个严重缺陷，需要立即修复后方可上线。")
    print("  所有缺陷都可以通过完善的单元测试在早期发现。")
    print()


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + "软件测试作业 - 缺陷分析与测试报告".center(76) + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # 执行测试
    execute_tests()
    
    # 生成缺陷报告
    generate_bug_report()
    
    # 生成测试总结
    generate_summary()
    
    print("=" * 80)
    print("报告生成完成！".center(80))
    print("=" * 80)
