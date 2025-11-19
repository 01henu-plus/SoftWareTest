"""
座位锁定系统测试脚本
测试锁定、解锁和过期功能
"""
from app.seat_lock import SeatLockSystem
import time


def test_lock_and_expire():
    """测试用例1: 锁定座位并测试过期"""
    s = SeatLockSystem()
    
    # 锁定座位A1，用户user1
    assert s.lock("A1", "user1")
    
    # 检查座位是否被锁定
    assert s.is_locked("A1")
    
    # 修改过期时间为当前时间-1秒（模拟过期）
    s.locked_seats["A1"]["expire"] = time.time() - 1
    
    # 检查过期后座位应该未锁定
    assert s.is_locked("A1") is False
    
    print("✅ 测试通过: test_lock_and_expire")


def test_relock_after_expire():
    """测试用例2: 过期后重新锁定座位"""
    s = SeatLockSystem()
    
    # 用户user1锁定座位A1
    s.lock("A1", "user1")
    
    # 设置过期时间
    s.locked_seats["A1"]["expire"] = time.time() - 1
    
    # 用户user2尝试锁定同一座位
    s.lock("A1", "user2")
    
    # 验证座位现在是被锁定的
    assert s.is_locked("A1")
    
    print("✅ 测试通过: test_relock_after_expire")


def test_unlock():
    """测试用例3: 解锁座位功能"""
    s = SeatLockSystem()
    
    # 锁定座位A1
    s.lock("A1", "user1")
    
    # 验证座位已锁定
    assert s.is_locked("A1")
    
    # 解锁座位
    assert s.unlock("A1")
    
    # 验证座位已解锁
    assert s.is_locked("A1") is False
    
    print("✅ 测试通过: test_unlock")


def test_lock_already_locked():
    """测试用例4: 尝试锁定已锁定的座位"""
    s = SeatLockSystem()
    
    # 用户user1锁定座位A1
    assert s.lock("A1", "user1")
    
    # 用户user2尝试锁定同一座位（应该失败）
    assert s.lock("A1", "user2") is False
    
    # 验证座位仍被user1锁定
    info = s.get_lock_info("A1")
    assert info is not None
    assert info["user"] == "user1"
    
    print("✅ 测试通过: test_lock_already_locked")


def test_multiple_seats():
    """测试用例5: 多个座位同时锁定"""
    s = SeatLockSystem()
    
    # 锁定多个座位
    assert s.lock("A1", "user1")
    assert s.lock("B2", "user2")
    assert s.lock("C3", "user3")
    
    # 验证所有座位都已锁定
    assert s.is_locked("A1")
    assert s.is_locked("B2")
    assert s.is_locked("C3")
    
    # 解锁B2
    s.unlock("B2")
    
    # 验证B2已解锁，其他座位仍锁定
    assert s.is_locked("A1")
    assert s.is_locked("B2") is False
    assert s.is_locked("C3")
    
    print("✅ 测试通过: test_multiple_seats")


if __name__ == "__main__":
    print("=" * 60)
    print("  座位锁定系统测试")
    print("=" * 60)
    print()
    
    # 运行所有测试
    test_lock_and_expire()
    test_relock_after_expire()
    test_unlock()
    test_lock_already_locked()
    test_multiple_seats()
    
    print()
    print("=" * 60)
    print("  所有测试通过! ✅")
    print("=" * 60)
