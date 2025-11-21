"""运行测试脚本"""
import subprocess
import sys
import time

def start_server():
    """启动Flask服务器"""
    print("启动Flask服务器...")
    server = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # 等待服务器启动
    return server

def run_tests():
    """运行测试"""
    print("\n运行测试...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "test_login.py", "-v", "--tb=short"],
        capture_output=False
    )
    return result.returncode

def main():
    server = None
    try:
        server = start_server()
        exit_code = run_tests()
        sys.exit(exit_code)
    finally:
        if server:
            print("\n关闭服务器...")
            server.terminate()
            server.wait()

if __name__ == "__main__":
    main()
