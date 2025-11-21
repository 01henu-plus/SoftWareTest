"""
转账函数 - 单元测试案例
测试点：余额不足、负数金额、跨用户正常转账
"""


class Account:
    """账户类"""
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
    
    def deposit(self, amount):
        """存款"""
        if amount < 0:
            raise ValueError("金额不能为负数")
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount):
        """取款"""
        if amount < 0:
            raise ValueError("金额不能为负数")
        if amount > self.balance:
            raise ValueError("余额不足")
        self.balance -= amount
        return self.balance


def transfer(from_account, to_account, amount):
    """
    转账函数
    
    参数:
        from_account: 转出账户
        to_account: 转入账户
        amount: 转账金额
    
    返回:
        True: 转账成功
    
    异常:
        ValueError: 金额无效或余额不足
    """
    if amount <= 0:
        raise ValueError("转账金额必须大于0")
    
    # 从转出账户扣款
    from_account.withdraw(amount)
    
    # 向转入账户存款
    to_account.deposit(amount)
    
    return True


if __name__ == "__main__":
    # 简单演示
    account_a = Account("用户A", 1000)
    account_b = Account("用户B", 500)
    
    print(f"转账前: {account_a.name}={account_a.balance}, {account_b.name}={account_b.balance}")
    
    transfer(account_a, account_b, 200)
    
    print(f"转账后: {account_a.name}={account_a.balance}, {account_b.name}={account_b.balance}")

