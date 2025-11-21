# 座位锁定系统测试

## 项目简介
简洁的座位锁定系统，支持座位锁定、解锁和超时自动释放功能。

## 功能特性
- **座位锁定**: 支持多用户锁定不同座位
- **超时管理**: 60秒自动释放（可配置）
- **冲突检测**: 防止重复锁定
- **自动清理**: 过期锁自动删除

## 文件结构
```
├── app/
│   └── seat_lock.py      # 核心系统类 (35行)
├── tests/
│   └── test_seat_lock.py # pytest测试 (30行)
├── run_tests.py          # 独立测试脚本 (55行)
└── report.html           # HTML测试报告
```

## 运行测试

### 方式1: 独立脚本
```bash
python run_tests.py
```

### 方式2: pytest
```bash
pytest tests/test_seat_lock.py -v
```

### 方式3: 生成HTML报告
```bash
pytest tests/test_seat_lock.py -v --html=report.html --self-contained-html
```

## 测试用例

| 编号 | 测试名称 | 测试内容 |
|------|---------|---------|
| 1 | test_lock_and_expire | 锁定座位并验证超时自动解锁 |
| 2 | test_relock_after_expire | 验证过期后可重新锁定 |
| 3 | test_unlock | 测试手动解锁功能 |
| 4 | test_lock_already_locked | 验证不能重复锁定同一座位 |
| 5 | test_multiple_seats | 测试多座位并发管理 |

## API使用

```python
from app.seat_lock import SeatLockSystem

# 创建系统实例
system = SeatLockSystem(timeout=60)

# 锁定座位
system.lock("A1", "user1")  # 返回True表示成功

# 检查状态
system.is_locked("A1")  # 返回True/False

# 获取信息
info = system.get_lock_info("A1")  # 返回{"user": "user1", "expire": timestamp}

# 解锁
system.unlock("A1")  # 返回True表示成功
```

## 测试结果
✅ 所有测试通过 (5/5)
⏱️ 测试时间: 0.04s

## 技术栈
- Python 3.14
- pytest 8.4.2
- 纯Python标准库（无额外依赖）
