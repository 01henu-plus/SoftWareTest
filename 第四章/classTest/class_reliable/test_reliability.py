"""
可靠性测试 - 长时间运行测试
测试系统在长时间运行下的稳定性
"""
import time
import requests

def test_reliability():
    """长时间运行可靠性测试"""
    print("\n" + "=" * 60)
    print("  可靠性测试：长时间运行")
    print("=" * 60)
    
    url = "http://127.0.0.1:5000/order"
    total_requests = 1000
    success_count = 0
    error_count = 0
    response_times = []
    
    print(f"\n将执行 {total_requests} 次订单请求...")
    print("测试开始时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    start = time.time()
    
    for i in range(total_requests):
        try:
            request_start = time.time()
            res = requests.post(
                url,
                json={"item": "book", "qty": 1},
                timeout=10
            )
            request_time = time.time() - request_start
            response_times.append(request_time)
            
            # 判断请求是否成功
            if res.status_code == 200 or res.status_code == 400:
                # 200 是成功，400 可能是库存不足（也算预期行为）
                success_count += 1
            else:
                error_count += 1
                print(f"\n✗ 请求 {i+1} 失败: 状态码 {res.status_code}")
            
            # 每100次请求显示进度
            if (i + 1) % 100 == 0:
                elapsed = time.time() - start
                avg_time = sum(response_times[-100:]) / 100
                print(f"进度: {i+1}/{total_requests} "
                      f"| 成功: {success_count} "
                      f"| 失败: {error_count} "
                      f"| 平均响应时间: {avg_time:.3f}秒")
        
        except requests.exceptions.RequestException as e:
            error_count += 1
            if error_count <= 5:  # 只显示前5个错误
                print(f"\n✗ 请求 {i+1} 异常: {e}")
        
        except Exception as e:
            error_count += 1
            if error_count <= 5:
                print(f"\n✗ 请求 {i+1} 发生错误: {e}")
    
    end = time.time()
    total_time = end - start
    
    # 计算统计数据
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
    else:
        avg_response_time = 0
        min_response_time = 0
        max_response_time = 0
    
    # 输出测试报告
    print("\n" + "=" * 60)
    print("  测试报告")
    print("=" * 60)
    print(f"\n测试结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总运行时间: {total_time:.2f} 秒")
    print(f"\n请求统计:")
    print(f"  总请求数: {total_requests}")
    print(f"  成功请求: {success_count}")
    print(f"  失败请求: {error_count}")
    print(f"  成功率: {(success_count/total_requests*100):.2f}%")
    
    print(f"\n响应时间统计:")
    print(f"  平均响应时间: {avg_response_time*1000:.2f} 毫秒")
    print(f"  最小响应时间: {min_response_time*1000:.2f} 毫秒")
    print(f"  最大响应时间: {max_response_time*1000:.2f} 毫秒")
    print(f"  吞吐量: {total_requests/total_time:.2f} 请求/秒")
    
    # 断言测试结果
    print(f"\n测试验证:")
    
    # 成功率应该大于 95%
    success_rate = success_count / total_requests * 100
    if success_rate >= 95:
        print(f"  ✓ 成功率 {success_rate:.2f}% >= 95% (通过)")
    else:
        print(f"  ✗ 成功率 {success_rate:.2f}% < 95% (未通过)")
    
    # 平均响应时间应该小于 1 秒
    if avg_response_time < 1:
        print(f"  ✓ 平均响应时间 {avg_response_time*1000:.2f}ms < 1000ms (通过)")
    else:
        print(f"  ✗ 平均响应时间 {avg_response_time*1000:.2f}ms >= 1000ms (未通过)")
    
    # 断言
    assert res.status_code == 200 or res.status_code == 400, \
        "系统应该能识别出错误（200成功或400库存不足）"
    
    print("\n" + "=" * 60)
    print("  结论")
    print("=" * 60)
    
    if success_rate >= 95 and avg_response_time < 1:
        print("\n✓ 可靠性测试通过")
        print("系统在长时间运行下表现稳定，能够可靠地处理大量请求")
    else:
        print("\n⚠️  可靠性测试存在问题")
        print("系统在长时间运行下出现了性能或稳定性问题")
    
    print("=" * 60)

if __name__ == "__main__":
    test_reliability()
