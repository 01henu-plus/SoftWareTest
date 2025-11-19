"""
Web 登录功能自动化测试
使用 pytest + Selenium 进行自动化测试
"""
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# 测试配置
BASE_URL = "http://127.0.0.1:5000"
API_URL = f"{BASE_URL}/api/login"

class TestLoginAPI:
    """登录 API 测试类"""
    
    def test_successful_login(self):
        """测试用例1: 正常登录"""
        payload = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(API_URL, json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert 'admin' in data['message']
        print("✓ 测试通过: 正常登录成功")
    
    def test_wrong_password(self):
        """测试用例2: 错误密码"""
        payload = {
            "username": "admin",
            "password": "wrongpassword"
        }
        response = requests.post(API_URL, json=payload)
        
        assert response.status_code == 401
        data = response.json()
        assert data['status'] == 'error'
        assert '密码错误' in data['message']
        print("✓ 测试通过: 错误密码被拒绝")
    
    def test_nonexistent_user(self):
        """测试用例3: 不存在的用户"""
        payload = {
            "username": "nonexistent",
            "password": "anypassword"
        }
        response = requests.post(API_URL, json=payload)
        
        assert response.status_code == 401
        data = response.json()
        assert data['status'] == 'error'
        assert '用户名不存在' in data['message']
        print("✓ 测试通过: 不存在的用户被拒绝")
    
    def test_empty_username(self):
        """测试用例4: 空用户名"""
        payload = {
            "username": "",
            "password": "admin123"
        }
        response = requests.post(API_URL, json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert data['status'] == 'error'
        assert '不能为空' in data['message']
        print("✓ 测试通过: 空用户名被拒绝")
    
    def test_empty_password(self):
        """测试用例5: 空密码"""
        payload = {
            "username": "admin",
            "password": ""
        }
        response = requests.post(API_URL, json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert data['status'] == 'error'
        assert '不能为空' in data['message']
        print("✓ 测试通过: 空密码被拒绝")
    
    def test_short_username(self):
        """测试用例6: 用户名过短"""
        payload = {
            "username": "ab",
            "password": "password123"
        }
        response = requests.post(API_URL, json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert data['status'] == 'error'
        assert '用户名长度' in data['message']
        print("✓ 测试通过: 过短用户名被拒绝")
    
    def test_long_username(self):
        """测试用例7: 用户名过长"""
        payload = {
            "username": "a" * 21,
            "password": "password123"
        }
        response = requests.post(API_URL, json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert data['status'] == 'error'
        assert '用户名长度' in data['message']
        print("✓ 测试通过: 过长用户名被拒绝")
    
    def test_short_password(self):
        """测试用例8: 密码过短"""
        payload = {
            "username": "admin",
            "password": "12345"
        }
        response = requests.post(API_URL, json=payload)
        
        assert response.status_code == 400
        data = response.json()
        assert data['status'] == 'error'
        assert '密码长度' in data['message']
        print("✓ 测试通过: 过短密码被拒绝")

class TestLoginUI:
    """登录 UI 测试类（使用 Selenium）"""
    
    @pytest.fixture
    def driver(self):
        """初始化 Chrome 驱动"""
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    def test_ui_successful_login(self, driver):
        """测试用例9: UI 正常登录"""
        driver.get(BASE_URL)
        
        # 输入用户名和密码
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        
        username_input.send_keys("admin")
        password_input.send_keys("admin123")
        
        # 点击登录按钮
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # 等待成功消息
        time.sleep(2)
        message = driver.find_element(By.ID, "message")
        
        assert message.is_displayed()
        assert "欢迎回来" in message.text
        assert "success" in message.get_attribute("class")
        print("✓ 测试通过: UI 登录成功")
    
    def test_ui_wrong_password(self, driver):
        """测试用例10: UI 错误密码"""
        driver.get(BASE_URL)
        
        # 输入错误密码
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        
        username_input.send_keys("admin")
        password_input.send_keys("wrongpass")
        
        # 点击登录按钮
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # 等待错误消息
        time.sleep(2)
        message = driver.find_element(By.ID, "message")
        
        assert message.is_displayed()
        assert "密码错误" in message.text
        assert "error" in message.get_attribute("class")
        print("✓ 测试通过: UI 错误密码提示正确")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
