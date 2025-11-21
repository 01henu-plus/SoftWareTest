"""
Locust 负载测试文件
用 Python + Locust 在 VS Code 中模拟 100 用户同时请求 /order 接口，观察响应时间
"""
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    """网站用户类"""
    wait_time = between(1, 3)  # 每次请求间隔1-3秒
    
    @task
    def order_book(self):
        """下单任务"""
        self.client.post("/order", json={"item": "book", "qty": 1})

