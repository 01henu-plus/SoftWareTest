import time
import requests

def test_reliability():
    url = "http://127.0.0.1:5000/order"
    total = 100
    success = 0
    times = []
    
    print(f"\n=== 可靠性测试: {total}次请求 ===\n")
    start = time.time()
    
    for i in range(total):
        try:
            t1 = time.time()
            res = requests.post(url, json={"item": "book", "qty": 1}, timeout=10)
            t2 = time.time()
            times.append(t2 - t1)
            
            if res.status_code in [200, 400]:
                success += 1
            
            if (i + 1) % 20 == 0:
                print(f"进度: {i+1}/{total} | 成功: {success}")
        except:
            pass
    
    total_time = time.time() - start
    avg_time = sum(times) / len(times) if times else 0
    success_rate = success / total * 100
    
    print(f"\n结果:")
    print(f"总请求数: {total}")
    print(f"成功: {success} ({success_rate:.1f}%)")
    print(f"平均响应时间: {avg_time*1000:.2f}ms")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"吞吐量: {total/total_time:.2f} req/s")
    
    if success_rate >= 95:
        print("\n✓ 测试通过")
    else:
        print("\n✗ 测试未通过")

if __name__ == "__main__":
    test_reliability()
