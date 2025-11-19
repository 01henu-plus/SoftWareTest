"""
性能测试脚本 - 模拟 100 用户并发请求
由于 Locust 安装需要 C++ 编译器，这里使用 threading 模块实现简单的并发测试
"""
import requests
import threading
import time
from datetime import datetime

# 测试配置
HOST = "http://127.0.0.1:5000"
ENDPOINT = "/order"
NUM_USERS = 100  # 模拟用户数
DURATION = 20  # 测试持续时间（秒）

# 统计数据
results = {
    "total_requests": 0,
    "success": 0,
    "failed": 0,
    "response_times": [],
    "errors": []
}
lock = threading.Lock()

def make_request():
    """发送单个请求"""
    start_time = time.time()
    try:
        response = requests.post(
            f"{HOST}{ENDPOINT}",
            json={"item": "book", "qty": 1},
            timeout=5
        )
        elapsed = time.time() - start_time
        
        with lock:
            results["total_requests"] += 1
            results["response_times"].append(elapsed)
            if response.status_code == 200:
                results["success"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(f"Status {response.status_code}")
    except Exception as e:
        elapsed = time.time() - start_time
        with lock:
            results["total_requests"] += 1
            results["failed"] += 1
            results["errors"].append(str(e))

def user_behavior():
    """模拟单个用户的行为"""
    end_time = time.time() + DURATION
    while time.time() < end_time:
        make_request()
        time.sleep(1)  # 每次请求间隔1秒（模拟 wait_time）

def run_load_test():
    """运行负载测试"""
    print("="*70)
    print("  性能测试 - 订单系统")
    print("="*70)
    print(f"\n配置:")
    print(f"  目标地址: {HOST}")
    print(f"  测试端点: {ENDPOINT}")
    print(f"  并发用户: {NUM_USERS}")
    print(f"  测试时长: {DURATION} 秒")
    print(f"\n开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n正在启动用户...")
    
    # 创建并启动线程
    threads = []
    for i in range(NUM_USERS):
        t = threading.Thread(target=user_behavior)
        t.daemon = True
        threads.append(t)
        t.start()
        if (i + 1) % 10 == 0:
            print(f"  已启动 {i + 1} 个用户...")
    
    print(f"\n所有用户已启动，测试运行中...")
    print(f"测试将在 {DURATION} 秒后结束...\n")
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    # 输出结果
    print("\n" + "="*70)
    print("  测试结果")
    print("="*70)
    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n请求统计:")
    print(f"  总请求数: {results['total_requests']}")
    print(f"  成功: {results['success']} ({results['success']/max(results['total_requests'],1)*100:.1f}%)")
    print(f"  失败: {results['failed']} ({results['failed']/max(results['total_requests'],1)*100:.1f}%)")
    
    if results['response_times']:
        avg_time = sum(results['response_times']) / len(results['response_times'])
        min_time = min(results['response_times'])
        max_time = max(results['response_times'])
        
        print(f"\n响应时间:")
        print(f"  平均: {avg_time*1000:.2f} ms")
        print(f"  最小: {min_time*1000:.2f} ms")
        print(f"  最大: {max_time*1000:.2f} ms")
        
        # 计算请求速率
        rps = results['total_requests'] / DURATION
        print(f"\n吞吐量:")
        print(f"  RPS (每秒请求数): {rps:.2f}")
    
    if results['errors'] and len(set(results['errors'])) < 10:
        print(f"\n错误类型:")
        error_counts = {}
        for error in results['errors']:
            error_counts[error] = error_counts.get(error, 0) + 1
        for error, count in error_counts.items():
            print(f"  {error}: {count} 次")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        run_load_test()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
    except Exception as e:
        print(f"\n错误: {e}")
