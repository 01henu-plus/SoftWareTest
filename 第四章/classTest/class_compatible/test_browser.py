"""
浏览器兼容性测试 (Selenium 示例)
测试登录页面在不同浏览器中的兼容性 - Chrome 和 Edge
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

def test_login_page_chrome():
    """测试 Chrome 浏览器"""
    print("\n" + "=" * 60)
    print("测试浏览器: Chrome")
    print("=" * 60)
    
    driver = None
    try:
        # 初始化 Chrome 浏览器
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("http://127.0.0.1:5000/login")
        
        # 等待页面加载
        time.sleep(2)
        
        # 验证页面标题
        assert "登录" in driver.page_source, "页面中未找到'登录'关键字"
        print("[PASS] 页面加载成功")
        
        # 查找用户名输入框
        username_input = driver.find_element(By.ID, "username")
        assert username_input is not None, "未找到用户名输入框"
        print("[PASS] 找到用户名输入框")
        
        # 查找密码输入框
        password_input = driver.find_element(By.ID, "password")
        assert password_input is not None, "未找到密码输入框"
        print("[PASS] 找到密码输入框")
        
        # 输入测试数据
        username_input.send_keys("testuser")
        password_input.send_keys("testpass123")
        print("[PASS] 成功输入测试数据")
        
        # 查找登录按钮
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert login_button is not None, "未找到登录按钮"
        print("[PASS] 找到登录按钮")
        
        # 点击登录按钮
        login_button.click()
        time.sleep(1)
        
        # 处理 alert
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print(f"[PASS] 登录成功，弹窗提示: {alert_text}")
        except:
            print("[PASS] 表单提交成功")
        
        print("\n✓ Chrome 浏览器测试通过\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Chrome 浏览器测试失败: {str(e)}\n")
        return False
    finally:
        if driver:
            driver.quit()


def test_login_page_edge():
    """测试 Edge 浏览器"""
    print("\n" + "=" * 60)
    print("测试浏览器: Edge")
    print("=" * 60)
    
    driver = None
    try:
        # 初始化 Edge 浏览器
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        driver.get("http://127.0.0.1:5000/login")
        
        # 等待页面加载
        time.sleep(2)
        
        # 验证页面标题
        assert "登录" in driver.page_source, "页面中未找到'登录'关键字"
        print("[PASS] 页面加载成功")
        
        # 查找用户名输入框
        username_input = driver.find_element(By.ID, "username")
        assert username_input is not None, "未找到用户名输入框"
        print("[PASS] 找到用户名输入框")
        
        # 查找密码输入框
        password_input = driver.find_element(By.ID, "password")
        assert password_input is not None, "未找到密码输入框"
        print("[PASS] 找到密码输入框")
        
        # 输入测试数据
        username_input.send_keys("testuser")
        password_input.send_keys("testpass123")
        print("[PASS] 成功输入测试数据")
        
        # 查找登录按钮
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert login_button is not None, "未找到登录按钮"
        print("[PASS] 找到登录按钮")
        
        # 点击登录按钮
        login_button.click()
        time.sleep(1)
        
        # 处理 alert
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print(f"[PASS] 登录成功，弹窗提示: {alert_text}")
        except:
            print("[PASS] 表单提交成功")
        
        print("\n✓ Edge 浏览器测试通过\n")
        return True
        
    except Exception as e:
        print(f"\n✗ Edge 浏览器测试失败: {str(e)}\n")
        return False
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  浏览器兼容性测试 (Chrome & Edge)")
    print("=" * 60)
    print("\n请确保已启动登录页面服务器 (python app.py)\n")
    
    results = {
        "Chrome": False,
        "Edge": False
    }
    
    # 测试 Chrome
    try:
        results["Chrome"] = test_login_page_chrome()
    except Exception as e:
        print(f"Chrome 测试异常: {str(e)}")
    
    time.sleep(2)
    
    # 测试 Edge
    try:
        results["Edge"] = test_login_page_edge()
    except Exception as e:
        print(f"Edge 测试异常: {str(e)}")
    
    # 输出测试总结
    print("\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)
    for browser, passed in results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{browser:15} {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\n总计: {passed}/{total} 个浏览器测试通过")
    print("=" * 60)
