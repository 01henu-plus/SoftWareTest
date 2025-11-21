"""Web登录API自动化测试"""
import requests
import pytest

API_URL = "http://127.0.0.1:5000/api/login"

class TestLoginAPI:
    """API测试套件"""
    
    def test_01_successful_login(self):
        """正常登录"""
        response = requests.post(API_URL, json={"username": "admin", "password": "admin123"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "admin" in response.json()["user"]
    
    def test_02_wrong_password(self):
        """密码错误"""
        response = requests.post(API_URL, json={"username": "admin", "password": "wrongpass"})
        assert response.status_code == 401
        assert response.json()["status"] == "error"
    
    def test_03_nonexistent_user(self):
        """用户不存在"""
        response = requests.post(API_URL, json={"username": "nobody", "password": "pass123456"})
        assert response.status_code == 401
    
    def test_04_empty_username(self):
        """用户名为空"""
        response = requests.post(API_URL, json={"username": "", "password": "pass123456"})
        assert response.status_code == 400
    
    def test_05_empty_password(self):
        """密码为空"""
        response = requests.post(API_URL, json={"username": "admin", "password": ""})
        assert response.status_code == 400
    
    def test_06_short_username(self):
        """用户名过短"""
        response = requests.post(API_URL, json={"username": "ab", "password": "pass123456"})
        assert response.status_code == 400
    
    def test_07_long_username(self):
        """用户名过长"""
        response = requests.post(API_URL, json={"username": "a" * 21, "password": "pass123456"})
        assert response.status_code == 400
    
    def test_08_short_password(self):
        """密码过短"""
        response = requests.post(API_URL, json={"username": "admin", "password": "12345"})
        assert response.status_code == 400
