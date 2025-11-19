import os
import requests
import pytest


def test_api_login_success():
    """简单的 API 登录示例。通过 `API_BASE_URL` 环境变量指定基地址。

    默认会 POST 到 `/api/login`，并断言返回码为 200 且包含 `token` 字段或类似成功标志。
    如果响应不是 JSON，则跳过测试（便于在未配置真实服务时运行）。
    """
    base = os.getenv('API_BASE_URL', 'http://example.com')
    url = base.rstrip('/') + '/api/login'
    payload = {'username': 'testuser', 'password': 'password'}

    resp = requests.post(url, json=payload, timeout=10)
    assert resp.status_code == 200

    try:
        data = resp.json()
    except Exception:
        pytest.skip('响应不是 JSON，跳过断言')

    assert ('token' in data) or (data.get('success', False)) or (data.get('status') in ('ok', 'success'))
