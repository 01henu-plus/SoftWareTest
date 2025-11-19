"""
座位锁定系统 (SeatLockSystem)
实现座位的锁定、解锁和过期检查功能
"""
import time

class SeatLockSystem:
    """座位锁定系统类"""
    
    def __init__(self):
        """初始化系统，设置锁定座位字典和超时时间"""
        self.locked_seats = {}  # 存储锁定的座位信息 {seat_id: {"user": user, "expire": timestamp}}
        self.timeout = 60  # 默认超时时间为60秒
    
    def lock(self, seat_id, user):
        """
        锁定座位
        
        参数:
            seat_id: 座位ID (如 "A1", "B2")
            user: 用户名
            
        返回:
            True: 锁定成功
            False: 座位已被锁定
        """
        now = time.time()
        
        # 检查座位是否已被锁定且未过期
        if seat_id in self.locked_seats and self.locked_seats[seat_id]["expire"] > now:
            return False
        
        # 锁定座位，设置过期时间
        self.locked_seats[seat_id] = {
            "user": user,
            "expire": now + self.timeout
        }
        return True
    
    def is_locked(self, seat_id):
        """
        检查座位是否被锁定
        
        参数:
            seat_id: 座位ID
            
        返回:
            True: 座位已锁定且未过期
            False: 座位未锁定或已过期
        """
        if seat_id not in self.locked_seats:
            return False
        
        now = time.time()
        
        # 如果锁已过期，删除锁定记录
        if self.locked_seats[seat_id]["expire"] <= now:
            del self.locked_seats[seat_id]
            return False
        
        return True
    
    def unlock(self, seat_id):
        """
        解锁座位
        
        参数:
            seat_id: 座位ID
            
        返回:
            True: 解锁成功
            False: 座位未被锁定
        """
        if seat_id in self.locked_seats:
            del self.locked_seats[seat_id]
            return True
        return False
    
    def get_lock_info(self, seat_id):
        """
        获取座位锁定信息
        
        参数:
            seat_id: 座位ID
            
        返回:
            dict: 包含user和expire的字典，如果未锁定返回None
        """
        if seat_id in self.locked_seats:
            return self.locked_seats[seat_id].copy()
        return None
