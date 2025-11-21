"""座位锁定系统测试"""
from app.seat_lock import SeatLockSystem
import time

def test_lock_and_expire():
    """测试1: 锁定和过期"""
    s = SeatLockSystem()
    assert s.lock("A1", "user1")
    assert s.is_locked("A1")
    s.locked_seats["A1"]["expire"] = time.time() - 1
    assert not s.is_locked("A1")

def test_relock_after_expire():
    """测试2: 过期后重新锁定"""
    s = SeatLockSystem()
    s.lock("A1", "user1")
    s.locked_seats["A1"]["expire"] = time.time() - 1
    assert s.lock("A1", "user2")
    assert s.is_locked("A1")

def test_unlock():
    """测试3: 解锁功能"""
    s = SeatLockSystem()
    s.lock("A1", "user1")
    assert s.is_locked("A1")
    assert s.unlock("A1")
    assert not s.is_locked("A1")

def test_lock_already_locked():
    """测试4: 锁定已占用座位"""
    s = SeatLockSystem()
    assert s.lock("A1", "user1")
    assert not s.lock("A1", "user2")
    assert s.get_lock_info("A1")["user"] == "user1"

def test_multiple_seats():
    """测试5: 多座位管理"""
    s = SeatLockSystem()
    assert s.lock("A1", "user1") and s.lock("B2", "user2") and s.lock("C3", "user3")
    assert s.is_locked("A1") and s.is_locked("B2") and s.is_locked("C3")
    s.unlock("B2")
    assert s.is_locked("A1") and not s.is_locked("B2") and s.is_locked("C3")
