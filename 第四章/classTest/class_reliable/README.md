# 容错性和可靠性测试项目

## 项目说明
本项目演示了系统的容错性（数据库中断恢复）和可靠性（长时间运行）测试。

## 文件说明
- `app.py` - Flask 订单系统服务器
- `test_resilience.py` - 容错性测试（数据库中断恢复）
- `test_reliability.py` - 可靠性测试（长时间运行 1000 次请求）
- `orders.db` - SQLite 数据库（自动生成）
- `README.md` - 本文档

## 测试场景

### 1. 容错性测试（Resilience Testing）
测试系统在数据库故障时的表现和恢复能力。

**测试步骤**:
1. 正常创建订单 - 验证系统正常运行
2. 模拟数据库中断 - 移除数据库文件
3. 尝试创建订单 - 系统应该能识别故障
4. 恢复数据库 - 恢复数据库连接
5. 再次创建订单 - 验证系统恢复正常

**Docker 模拟方式**:
```bash
# 停止数据库容器（模拟故障）
docker stop mysql_db

# 启动数据库容器（恢复）
docker start mysql_db
```

### 2. 可靠性测试（Reliability Testing）
测试系统长时间运行的稳定性。

**测试指标**:
- 执行 1000 次订单请求
- 统计成功率（应 >= 95%）
- 统计平均响应时间（应 < 1秒）
- 计算吞吐量（请求/秒）

## 运行步骤

### 方式一：自动化测试（推荐）

#### 1. 启动 Flask 服务器
在一个终端中运行：
```bash
cd class_reliable
python app.py
```

#### 2. 运行容错性测试
在另一个终端中运行：
```bash
cd class_reliable
python test_resilience.py
```

#### 3. 运行可靠性测试
```bash
cd class_reliable
python test_reliability.py
```

### 方式二：使用浏览器测试

访问 http://127.0.0.1:5000 查看 API 文档

#### 使用 Chrome 控制台测试：

```javascript
// 创建订单
fetch('http://127.0.0.1:5000/order', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({item: 'book', qty: 1})
})
.then(r => r.json())
.then(console.log);

// 查看所有订单
fetch('http://127.0.0.1:5000/orders')
  .then(r => r.json())
  .then(console.log);

// 查看库存
fetch('http://127.0.0.1:5000/inventory')
  .then(r => r.json())
  .then(console.log);

// 健康检查
fetch('http://127.0.0.1:5000/health')
  .then(r => r.json())
  .then(console.log);
```

## API 接口

### POST /order
创建订单

**请求体**:
```json
{
  "item": "book",
  "qty": 1
}
```

**响应 200**:
```json
{
  "status": "success",
  "message": "Order created",
  "order_id": 1,
  "item": "book",
  "qty": 1
}
```

**响应 400** (库存不足):
```json
{
  "status": "error",
  "message": "Insufficient stock"
}
```

**响应 503** (数据库故障):
```json
{
  "status": "error",
  "message": "Database connection failed"
}
```

### GET /orders
查看最近10个订单

### GET /inventory
查看库存状态

### GET /health
健康检查

## 测试数据

### 预置库存
- book: 100
- pen: 200
- notebook: 150

## 测试报告

### 容错性测试预期结果
- ✓ 正常情况下系统运行正常
- ✓ 数据库故障时返回 503 错误
- ✓ 数据库恢复后系统继续正常工作

### 可靠性测试预期结果
- ✓ 1000 次请求成功率 >= 95%
- ✓ 平均响应时间 < 1000ms
- ✓ 系统持续稳定运行

## 性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 成功率 | >= 95% | 系统可靠性指标 |
| 平均响应时间 | < 1000ms | 性能指标 |
| 最大响应时间 | < 5000ms | 极端情况容忍度 |
| 吞吐量 | > 10 req/s | 处理能力指标 |

## 故障模拟方法

### SQLite 数据库
- 移动/删除数据库文件模拟数据库不可用
- 恢复文件模拟数据库恢复

### Docker 数据库（可选）
```bash
# 模拟故障
docker stop mysql_db

# 恢复
docker start mysql_db
```

## 注意事项

1. **容错性测试**会短暂移动数据库文件，测试完成后会自动恢复
2. **可靠性测试**会执行 1000 次请求，需要几分钟时间
3. 确保端口 5000 未被占用
4. 建议在测试环境运行，不要在生产环境测试

## 学习要点

### 容错性（Resilience）
- **定义**: 系统在故障发生时的恢复能力
- **关键**: 
  - 故障检测
  - 优雅降级
  - 快速恢复
  - 数据一致性

### 可靠性（Reliability）
- **定义**: 系统长时间稳定运行的能力
- **关键**:
  - 高成功率
  - 稳定性能
  - 无内存泄漏
  - 资源管理

## 改进建议

1. **连接池**: 使用数据库连接池提高性能
2. **重试机制**: 实现自动重试失败的请求
3. **熔断器**: 实现断路器模式防止级联故障
4. **监控**: 添加系统监控和告警
5. **日志**: 完善日志记录便于问题排查

## 参考资料
- [12-Factor App - Disposability](https://12factor.net/disposability)
- [Chaos Engineering](https://principlesofchaos.org/)
- [Site Reliability Engineering](https://sre.google/)
