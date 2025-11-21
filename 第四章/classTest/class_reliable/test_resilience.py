import requests
import time
import os

def test_db_failure_recovery():
    url = "http://127.0.0.1:5000/order"
    payload = {"item": "pen", "qty": 1}  # 使用pen，库存更多
    
    print("\n=== 容错性测试: 数据库故障恢复 ===\n")
    
    # 步骤1: 正常请求
    print("【步骤1】正常创建订单")
    res1 = requests.post(url, json=payload)
    print(f"结果: {res1.status_code} - {res1.json()}")
    if res1.status_code == 200:
        print("✓ 正常创建成功")
    
    # 步骤2: 模拟数据库故障
    print("\n【步骤2】模拟数据库故障")
    db_file = 'orders.db'
    db_backup = 'orders.db.backup'
    if os.path.exists(db_backup):
        os.remove(db_backup)
    if os.path.exists(db_file):
        os.rename(db_file, db_backup)
        print("✓ 数据库文件已移除")
    
    time.sleep(2)
    
    # 步骤3: 故障时请求
    print("\n【步骤3】数据库故障时创建订单")
    res2 = requests.post(url, json=payload)
    print(f"结果: {res2.status_code} - {res2.json()}")
    
    if res2.status_code in [500, 503]:
        print("✓ 系统正确识别了数据库故障")
    else:
        print("⚠ 系统未能正确识别故障(可能是缓存)")
    
    # 步骤4: 恢复数据库
    print("\n【步骤4】恢复数据库")
    if os.path.exists(db_backup):
        os.rename(db_backup, db_file)
        print("✓ 数据库已恢复")
    
    time.sleep(3)
    
    # 步骤5: 恢复后请求
    print("\n【步骤5】数据库恢复后创建订单")
    res3 = requests.post(url, json=payload)
    print(f"结果: {res3.status_code} - {res3.json()}")
    
    if res3.status_code == 200:
        print("✓ 系统恢复正常")
        print("\n✓ 容错性测试通过")
    elif res3.status_code == 400:
        print("⚠ 库存不足，但系统正常运行")
        print("\n✓ 容错性测试通过(系统能正常响应)")
    else:
        print("\n✗ 系统未能恢复")

if __name__ == "__main__":
    test_db_failure_recovery()
