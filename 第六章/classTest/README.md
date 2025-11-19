# 座位锁定系统 - 课堂案例

## 项目说明
实现一个简单的座位锁定系统，用于演示 pytest 测试框架的使用。

## 功能特性
- ✅ 座位锁定功能
- ✅ 座位解锁功能
- ✅ 锁定超时检查
- ✅ 多座位管理

## 项目结构
```
classTest/
├── venv/                  # Python 虚拟环境
├── app/                   # 应用代码
│   ├── __init__.py
│   └── seat_lock.py      # 座位锁定系统类
├── tests/                 # 测试代码
│   ├── __init__.py
│   └── test_seat_lock.py # 测试脚本
├── requirements.txt       # 依赖清单
├── pytest.ini            # pytest 配置
└── README.md             # 本文件
```

## 环境配置

### 1. 创建虚拟环境
```bash
python -m venv venv
```

### 2. 激活虚拟环境
Windows:
```bash
.\venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install pytest pytest-html
```

## 运行测试

### 方法1: 使用 pytest (推荐)
```bash
# VS Code 中运行
Ctrl+Shift+P → Python: Configure Tests → pytest → tests/

# 生成 HTML 报告
pytest --html=report.html --self-contained-html
```

### 方法2: 直接运行测试文件
```bash
python tests/test_seat_lock.py
```

## 测试用例

| 测试ID | 测试场景 | 验证点 |
|--------|----------|--------|
| test_lock_and_expire | 锁定座位并测试过期 | 座位锁定后过期自动解锁 |
| test_relock_after_expire | 过期后重新锁定 | 过期后其他用户可以重新锁定 |
| test_unlock | 解锁座位 | 手动解锁功能正常工作 |
| test_lock_already_locked | 锁定已锁定座位 | 已锁定座位不能被其他用户锁定 |
| test_multiple_seats | 多座位管理 | 系统可以同时管理多个座位 |

## 核心代码

### SeatLockSystem 类
```python
class SeatLockSystem:
    def __init__(self):
        self.locked_seats = {}
        self.timeout = 60
    
    def lock(self, seat_id, user):
        # 锁定座位
        pass
    
    def is_locked(self, seat_id):
        # 检查座位是否锁定
        pass
    
    def unlock(self, seat_id):
        # 解锁座位
        pass
```

## 预期输出

```
============================================================
  座位锁定系统测试
============================================================

✅ 测试通过: test_lock_and_expire
✅ 测试通过: test_relock_after_expire
✅ 测试通过: test_unlock
✅ 测试通过: test_lock_already_locked
✅ 测试通过: test_multiple_seats

============================================================
  所有测试通过! ✅
============================================================
```

## 学习要点

1. **Python 虚拟环境**: 使用 venv 创建独立的项目环境
2. **pytest 框架**: 现代化的 Python 测试框架
3. **单元测试**: 测试单个功能模块
4. **断言验证**: 使用 assert 进行结果验证
5. **测试报告**: 生成 HTML 格式的测试报告

## 参考资料
- [pytest 官方文档](https://docs.pytest.org/)
- [Python 官方文档](https://docs.python.org/zh-cn/3/)
