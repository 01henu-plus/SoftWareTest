"""座位锁定系统"""
import time

class SeatLockSystem:
    """座位锁定系统 - 支持座位锁定、解锁和超时功能"""
    
    def __init__(self, timeout=60):
        self.locked_seats = {}  # {seat_id: {"user": user, "expire": timestamp}}
        self.timeout = timeout
    
    def lock(self, seat_id, user):
        """锁定座位，返回True表示成功，False表示已被锁定"""
        now = time.time()
        if seat_id in self.locked_seats and self.locked_seats[seat_id]["expire"] > now:
            return False
        self.locked_seats[seat_id] = {"user": user, "expire": now + self.timeout}
        return True
    
    def is_locked(self, seat_id):
        """检查座位是否锁定，自动清理过期锁"""
        if seat_id not in self.locked_seats:
            return False
        if self.locked_seats[seat_id]["expire"] <= time.time():
            del self.locked_seats[seat_id]
            return False
        return True
    
    def unlock(self, seat_id):
        """解锁座位"""
        if seat_id in self.locked_seats:
            del self.locked_seats[seat_id]
            return True
        return False
    
    def get_lock_info(self, seat_id):
        """获取座位锁定信息"""
        return self.locked_seats.get(seat_id, {}).copy() if seat_id in self.locked_seats else None
