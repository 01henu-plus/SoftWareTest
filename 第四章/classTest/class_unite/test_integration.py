"""
单元测试 - 转账函数
使用 pytest + unittest.mock 进行测试
"""
import pytest
from unittest.mock import Mock
from app import Account, transfer


class TestTransferFunction:
    """转账函数单元测试"""
    
    def test_余额不足(self):
        """测试点1：余额不足"""
        account_a = Account("用户A", 100)
        account_b = Account("用户B", 500)
        
        with pytest.raises(ValueError, match="余额不足"):
            transfer(account_a, account_b, 200)
        
        # 验证账户余额未变化
        assert account_a.balance == 100
        assert account_b.balance == 500
    
    def test_负数金额(self):
        """测试点2：负数金额"""
        account_a = Account("用户A", 1000)
        account_b = Account("用户B", 500)
        
        with pytest.raises(ValueError, match="转账金额必须大于0"):
            transfer(account_a, account_b, -100)
        
        # 验证账户余额未变化
        assert account_a.balance == 1000
        assert account_b.balance == 500
    
    def test_跨用户正常转账(self):
        """测试点3：跨用户正常转账"""
        account_a = Account("用户A", 1000)
        account_b = Account("用户B", 500)
        
        result = transfer(account_a, account_b, 200)
        
        assert result == True
        assert account_a.balance == 800  # 1000 - 200
        assert account_b.balance == 700  # 500 + 200
    
    def test_使用mock验证调用(self):
        """测试点4：使用 unittest.mock 验证方法调用"""
        # 创建 mock 对象
        mock_from = Mock()
        mock_from.withdraw = Mock()
        mock_from.balance = 1000
        
        mock_to = Mock()
        mock_to.deposit = Mock()
        
        # 执行转账
        transfer(mock_from, mock_to, 300)
        
        # 验证方法被正确调用
        mock_from.withdraw.assert_called_once_with(300)
        mock_to.deposit.assert_called_once_with(300)


def test_零金额转账():
    """额外测试：零金额转账"""
    account_a = Account("用户A", 1000)
    account_b = Account("用户B", 500)
    
    with pytest.raises(ValueError, match="转账金额必须大于0"):
        transfer(account_a, account_b, 0)


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])

