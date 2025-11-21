"""
高安全级别实验室访问控制系统
"""


class Person:
    """人员类"""
    def __init__(self, name, is_employee=False, has_high_clearance=False, 
                 is_within_visit_window=False, is_escorted=False):
        self.name = name
        self.is_employee = is_employee
        self.has_high_clearance = has_high_clearance
        self.is_within_visit_window = is_within_visit_window
        self.is_escorted = is_escorted


class LabAccessControl:
    """实验室访问控制"""
    
    @staticmethod
    def grant_access(person):
        """
        判断是否授权进入实验室
        
        授权逻辑：
        1. 必须是内部员工 (is_employee == True)
        2. 并且满足以下任一条件：
           a. 拥有高级别安全许可 (has_high_clearance == True)
           b. 正在访问期内 (is_within_visit_window == True) 并且 有内部员工陪同 (is_escorted == True)
        
        返回：True(授权) 或 False(拒绝)
        """
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