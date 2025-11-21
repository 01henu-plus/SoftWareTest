"""运行测试脚本"""
import subprocess
import sys
import time
from multiprocessing import Process
from app.checkout_service import app

def start_server():
    app.run(port=5000, debug=False, use_reloader=False)

def main():
    print("="*60)
    print(" 购物车结算微服务测试")
    print("="*60)
    
    # 启动服务器
    print("\n启动服务器...")
    server = Process(target=start_server)
    server.start()
    time.sleep(2)
    
    try:
        # 运行pytest
        print("运行测试...\n")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "test_checkout.py", "-v", "--tb=short"],
            capture_output=False
        )
        return result.returncode
    finally:
        print("\n关闭服务器...")
        server.terminate()
        server.join()

if __name__ == "__main__":
    sys.exit(main())
