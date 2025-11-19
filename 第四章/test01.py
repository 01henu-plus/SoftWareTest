import pytest

# 模拟数据库
users_db = {'user1', 'user2', 'user3'}
books_db = {
    'book1': {'available': True, 'stock': 5},
    'book2': {'available': True, 'stock': 2},
    'book3': {'available': False, 'stock': 0}
}


def borrow_book(user, book):
    """
    借书函数
    参数:
        user: 用户名
        book: 图书名
    返回:
        成功返回 True 和剩余库存
        失败返回 False 和错误信息
    """
    # 1. 用户是否存在
    if user not in users_db:
        return False, "用户不存在"
    
    # 2. 图书是否可借
    if book not in books_db:
        return False, "书不存在"
    
    if not books_db[book]['available']:
        return False, "图书不可借"
    
    # 3. 借书后库存减少
    if books_db[book]['stock'] <= 0:
        return False, "库存为0"
    
    books_db[book]['stock'] -= 1
    
    # 如果库存为0，设置为不可借
    if books_db[book]['stock'] == 0:
        books_db[book]['available'] = False
    
    return True, f"借书成功，剩余库存: {books_db[book]['stock']}"


# ==================== 单元测试用例 ====================

class TestBorrowBook:
    """借书功能单元测试类"""
    
    def setup_method(self):
        """每个测试前重置数据"""
        global books_db
        books_db = {
            'book1': {'available': True, 'stock': 5},
            'book2': {'available': True, 'stock': 2},
            'book3': {'available': False, 'stock': 0}
        }
    
    def test_normal_borrow(self):
        """测试用例1: 正常借书 - 用户存在，图书可借，库存充足"""
        result, message = borrow_book('user1', 'book1')
        assert result == True, "正常借书应该成功"
        assert books_db['book1']['stock'] == 4, "库存应该减少1"
        assert "借书成功" in message
        print(f"✓ 测试用例1通过: {message}")
    
    def test_user_not_exist(self):
        """测试用例2: 异常情况 - 用户不存在"""
        result, message = borrow_book('user_invalid', 'book1')
        assert result == False, "用户不存在应该借书失败"
        assert message == "用户不存在"
        assert books_db['book1']['stock'] == 5, "库存不应该改变"
        print(f"✓ 测试用例2通过: {message}")
    
    def test_book_not_exist(self):
        """测试用例3: 异常情况 - 书不存在"""
        result, message = borrow_book('user1', 'book_invalid')
        assert result == False, "书不存在应该借书失败"
        assert message == "书不存在"
        print(f"✓ 测试用例3通过: {message}")
    
    def test_book_unavailable(self):
        """测试用例4: 异常情况 - 图书不可借"""
        result, message = borrow_book('user1', 'book3')
        assert result == False, "图书不可借应该借书失败"
        assert message == "图书不可借"
        assert books_db['book3']['stock'] == 0, "库存不应该改变"
        print(f"✓ 测试用例4通过: {message}")
    
    def test_stock_becomes_zero(self):
        """测试用例5: 边界情况 - 借书后库存为0"""
        # 先借一本，使库存变为1
        borrow_book('user1', 'book2')
        assert books_db['book2']['stock'] == 1
        
        # 再借一本，库存应该变为0，且图书变为不可借
        result, message = borrow_book('user2', 'book2')
        assert result == True, "库存为1时应该可以借"
        assert books_db['book2']['stock'] == 0, "库存应该变为0"
        assert books_db['book2']['available'] == False, "库存为0时图书应该变为不可借"
        print(f"✓ 测试用例5通过: 借书成功，库存变为0，图书状态变为不可借")
    
    def test_zero_stock_cannot_borrow(self):
        """测试用例6: 异常情况 - 库存为0时不能借书"""
        # 手动设置库存为0但状态为可借（边界异常情况）
        books_db['book1']['stock'] = 0
        
        result, message = borrow_book('user1', 'book1')
        assert result == False, "库存为0应该不能借书"
        assert message == "库存为0"
        print(f"✓ 测试用例6通过: {message}")
    
    def test_multiple_borrows(self):
        """测试用例7: 正常情况 - 多次借书，库存逐步减少"""
        initial_stock = books_db['book1']['stock']
        
        # 第一次借书
        result1, message1 = borrow_book('user1', 'book1')
        assert result1 == True
        assert books_db['book1']['stock'] == initial_stock - 1
        
        # 第二次借书
        result2, message2 = borrow_book('user2', 'book1')
        assert result2 == True
        assert books_db['book1']['stock'] == initial_stock - 2
        
        # 第三次借书
        result3, message3 = borrow_book('user3', 'book1')
        assert result3 == True
        assert books_db['book1']['stock'] == initial_stock - 3
        
        print(f"✓ 测试用例7通过: 连续3次借书成功，库存从{initial_stock}减少到{books_db['book1']['stock']}")


# ==================== 运行测试并显示结果 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("图书借阅系统单元测试")
    print("=" * 60)
    print()
    
    # 运行 pytest 并显示详细结果
    pytest.main([
        __file__,
        '-v',  # 详细模式
        '-s',  # 显示print输出
        '--tb=short',  # 简短的traceback
        '--color=yes'  # 彩色输出
    ])
