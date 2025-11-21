"""座位锁定系统测试运行器"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.seat_lock import SeatLockSystem
import time

def test_lock_and_expire():
    """测试1: 锁定和过期"""
    print("\n[1/5] 测试锁定和过期...")
    s = SeatLockSystem()
    assert s.lock("A1", "user1"), "锁定失败"
    assert s.is_locked("A1"), "座位未锁定"
    s.locked_seats["A1"]["expire"] = time.time() - 1
    assert not s.is_locked("A1"), "过期座位未自动解锁"
    print("  ✅ 通过")

def test_relock_after_expire():
    """测试2: 过期后重新锁定"""
    print("\n[2/5] 测试过期后重新锁定...")
    s = SeatLockSystem()
    s.lock("A1", "user1")
    s.locked_seats["A1"]["expire"] = time.time() - 1
    assert s.lock("A1", "user2"), "无法重新锁定过期座位"
    assert s.is_locked("A1"), "重新锁定失败"
    print("  ✅ 通过")

def test_unlock():
    """测试3: 解锁功能"""
    print("\n[3/5] 测试解锁功能...")
    s = SeatLockSystem()
    s.lock("A1", "user1")
    assert s.unlock("A1"), "解锁失败"
    assert not s.is_locked("A1"), "解锁后座位仍被锁定"
    print("  ✅ 通过")

def test_lock_already_locked():
    """测试4: 锁定已占用座位"""
    print("\n[4/5] 测试锁定已占用座位...")
    s = SeatLockSystem()
    assert s.lock("A1", "user1"), "首次锁定失败"
    assert not s.lock("A1", "user2"), "不应允许重复锁定"
    assert s.get_lock_info("A1")["user"] == "user1", "锁定用户错误"
    print("  ✅ 通过")

def test_multiple_seats():
    """测试5: 多座位管理"""
    print("\n[5/5] 测试多座位管理...")
    s = SeatLockSystem()
    assert all([s.lock("A1", "user1"), s.lock("B2", "user2"), s.lock("C3", "user3")]), "批量锁定失败"
    assert all([s.is_locked("A1"), s.is_locked("B2"), s.is_locked("C3")]), "部分座位未锁定"
    s.unlock("B2")
    assert s.is_locked("A1") and not s.is_locked("B2") and s.is_locked("C3"), "解锁B2后状态错误"
    print("  ✅ 通过")

if __name__ == "__main__":
    print("="*60)
    print(" 座位锁定系统测试")
    print("="*60)
    
    try:
        test_lock_and_expire()
        test_relock_after_expire()
        test_unlock()
        test_lock_already_locked()
        test_multiple_seats()
        
        print("\n" + "="*60)
        print(" 🎉 全部测试通过 (5/5) ✅")
        print("="*60)
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
