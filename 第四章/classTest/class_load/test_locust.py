"""
简单负载测试脚本（替代Locust）
模拟100用户并发请求/order接口
"""
import requests
import threading
import time
from datetime import datetime


class LoadTester:
    def __init__(self, host, users=100, duration=10):
        self.host = host
        self.users = users
        self.duration = duration
        self.results = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "times": []
        }
        self.lock = threading.Lock()
    
    def request_order(self):
        """发送订单请求"""
        end_time = time.time() + self.duration
        while time.time() < end_time:
            start = time.time()
            try:
                res = requests.post(
                    f"{self.host}/order",
                    json={"item": "book", "qty": 1},
                    timeout=5
                )
                elapsed = (time.time() - start) * 1000
                
                with self.lock:
                    self.results["total"] += 1
                    self.results["times"].append(elapsed)
                    if res.status_code == 200:
                        self.results["success"] += 1
                    else:
                        self.results["failed"] += 1
            except Exception:
                with self.lock:
                    self.results["total"] += 1
                    self.results["failed"] += 1
            
            time.sleep(1)  # 模拟用户思考时间
    
    def run(self):
        """运行负载测试"""
        print("="*60)
        print("负载测试 - 订单系统")
        print("="*60)
        print(f"目标: {self.host}")
        print(f"用户数: {self.users}")
        print(f"持续时间: {self.duration}秒")
        print(f"开始时间: {datetime.now().strftime('%H:%M:%S')}")
        print("\n启动用户...")
        
        # 创建线程
        threads = []
        for i in range(self.users):
            t = threading.Thread(target=self.request_order)
            t.daemon = True
            threads.append(t)
            t.start()
        
        print(f"✅ {self.users}个用户已启动\n")
        
        # 等待完成
        for t in threads:
            t.join()
        
        # 输出结果
        self.print_results()
    
    def print_results(self):
        """打印测试结果"""
        print("\n" + "="*60)
        print("测试结果")
        print("="*60)
        print(f"结束时间: {datetime.now().strftime('%H:%M:%S')}")
        print(f"\n总请求数: {self.results['total']}")
        print(f"成功: {self.results['success']}")
        print(f"失败: {self.results['failed']}")
        
        if self.results['times']:
            times = self.results['times']
            print(f"\n响应时间:")
            print(f"  平均: {sum(times)/len(times):.2f} ms")
            print(f"  最小: {min(times):.2f} ms")
            print(f"  最大: {max(times):.2f} ms")
            
            rps = self.results['total'] / self.duration
            print(f"\n吞吐量: {rps:.2f} RPS")
        
        print("="*60)


if __name__ == "__main__":
    tester = LoadTester(
        host="http://localhost:8089",
        users=100,
        duration=10
    )
    tester.run()
