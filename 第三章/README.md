# 第三章：实验室访问控制系统

## 项目说明

本项目实现了一个高安全级别实验室的访问控制系统，基于复杂的逻辑条件判断是否授权人员进入实验室。

## 授权逻辑

一个人员（person）请求进入实验室，授权结果（grant_access）由以下复杂逻辑决定：

### 必要条件
1. **该人员必须是内部员工**（`is_employee == True`）

### 充分条件（满足其一即可）
2. 并且，需要满足以下**任一**条件：
   - **a. 拥有高级别安全许可**（`has_high_clearance == True`）
   - **b. 正在访问期内**（`is_within_visit_window == True`）**并且** 有内部员工陪同（`is_escorted == True`）

## 文件结构

```
第三章/
├── README.md                # 项目说明文档
├── lab_access_control.py    # 访问控制系统实现
└── test_lab_access.py       # 测试用例
```

## 运行测试

```powershell
python test_lab_access.py
```

## 测试用例

| 测试编号 | 场景 | is_employee | has_high_clearance | is_within_visit_window | is_escorted | 预期结果 |
|---------|------|-------------|-------------------|----------------------|-------------|---------|
| 测试1 | 非员工访问 | False | - | - | - | ❌ 拒绝 |
| 测试2 | 员工+高级许可 | True | True | - | - | ✅ 授权 |
| 测试3 | 员工+访问期+陪同 | True | False | True | True | ✅ 授权 |
| 测试4 | 员工+访问期(无陪同) | True | False | True | False | ❌ 拒绝 |
| 测试5 | 员工(无特殊权限) | True | False | False | False | ❌ 拒绝 |

## 逻辑公式

```
grant_access = is_employee AND (has_high_clearance OR (is_within_visit_window AND is_escorted))
```

## 决策表

| 规则 | is_employee | has_high_clearance | is_within_visit_window | is_escorted | grant_access |
|-----|-------------|-------------------|----------------------|-------------|--------------|
| 1 | False | - | - | - | ❌ False |
| 2 | True | True | - | - | ✅ True |
| 3 | True | False | True | True | ✅ True |
| 4 | True | False | True | False | ❌ False |
| 5 | True | False | False | True | ❌ False |
| 6 | True | False | False | False | ❌ False |

## 测试结果示例

```
======================================================================
高安全级别实验室访问控制测试
======================================================================

【测试1】非员工访问
is_employee = False
结果: ❌ 拒绝

【测试2】员工 + 高级别安全许可
is_employee = True, has_high_clearance = True
结果: ✅ 授权

【测试3】员工 + 访问期内 + 有陪同
is_employee = True, is_within_visit_window = True, is_escorted = True
结果: ✅ 授权

【测试4】员工 + 访问期内 + 无陪同
is_employee = True, is_within_visit_window = True, is_escorted = False
结果: ❌ 拒绝

【测试5】员工 + 无特殊权限
is_employee = True, has_high_clearance = False
结果: ❌ 拒绝
```

## 核心代码

**访问控制逻辑：**
```python
def grant_access(person):
    # 条件1：必须是内部员工
    if not person.is_employee:
        return False
    
    # 条件2a：拥有高级别安全许可
    if person.has_high_clearance:
        return True
    
    # 条件2b：在访问期内且有员工陪同
    if person.is_within_visit_window and person.is_escorted:
        return True
    
    return False
```

## 学习目标

通过本项目，你将学习：
1. ✅ 理解复杂逻辑条件的实现
2. ✅ 掌握决策表测试方法
3. ✅ 编写完整的条件覆盖测试用例
4. ✅ 理解AND/OR逻辑组合
5. ✅ 实现访问控制系统

---

**创建日期**：2025年11月20日  
**适用课程**：软件测试 - 第三章
