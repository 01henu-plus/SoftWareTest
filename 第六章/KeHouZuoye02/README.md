# CI 配置与评分标准 - 课后作业

## 项目说明
使用 GitHub Actions 实现 Python 项目的持续集成（CI），自动运行测试并生成报告。

## GitHub Actions 配置

### Workflow 文件
位置: `.github/workflows/python-test.yml`

```yaml
name: Python Test

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - run: pip install -r requirements.txt
      
      - run: pytest --html=report.html --self-contained-html
```

### 配置说明

**触发条件:**
- `on: [push]` - 每次代码推送时触发

**运行环境:**
- `runs-on: ubuntu-latest` - 使用最新的 Ubuntu 环境

**执行步骤:**
1. **检出代码** - `actions/checkout@v4`
2. **设置 Python** - `actions/setup-python@v5` (Python 3.11)
3. **安装依赖** - `pip install -r requirements.txt`
4. **运行测试** - `pytest --html=report.html --self-contained-html`

## 项目结构

```
KeHouZuoye02/
├── .github/
│   └── workflows/
│       └── python-test.yml   # GitHub Actions 配置
├── calculator.py             # 计算器模块
├── test_calculator.py        # 测试用例
├── requirements.txt          # 依赖清单
└── README.md                 # 本文件
```

## 本地测试

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行测试
```bash
# 基本测试
pytest test_calculator.py -v

# 生成 HTML 报告
pytest test_calculator.py --html=report.html --self-contained-html
```

### 3. 直接运行测试文件
```bash
python test_calculator.py
```

## 测试用例

### 测试覆盖

| 测试用例 | 功能 | 验证点 |
|---------|------|--------|
| test_add | 加法运算 | 正数、负数、零 |
| test_subtract | 减法运算 | 正数、负数、零 |
| test_multiply | 乘法运算 | 正数、负数、零 |
| test_divide | 除法运算 | 整除、小数 |
| test_divide_by_zero | 除零异常 | 异常处理 |
| test_power | 幂运算 | 指数计算 |
| test_edge_cases | 边界情况 | 大数、小数、负数 |

### 预期输出

```
======================================================================
测试结果
======================================================================

test_calculator.py::test_add PASSED                              [ 14%]
✅ 加法测试通过

test_calculator.py::test_subtract PASSED                         [ 28%]
✅ 减法测试通过

test_calculator.py::test_multiply PASSED                         [ 42%]
✅ 乘法测试通过

test_calculator.py::test_divide PASSED                           [ 57%]
✅ 除法测试通过

test_calculator.py::test_divide_by_zero PASSED                   [ 71%]
✅ 除零异常测试通过

test_calculator.py::test_power PASSED                            [ 85%]
✅ 幂运算测试通过

test_calculator.py::test_edge_cases PASSED                       [100%]
✅ 边界情况测试通过

======================================================================
7 passed in 0.05s
======================================================================
```

## GitHub Actions 使用流程

### 1. 创建 GitHub 仓库
```bash
git init
git add .
git commit -m "Initial commit: Add CI configuration"
```

### 2. 推送到 GitHub
```bash
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main
git push -u origin main
```

### 3. 查看 Actions
1. 访问 GitHub 仓库
2. 点击 "Actions" 标签
3. 查看 workflow 运行状态
4. 点击具体的 workflow 查看详细日志

### 4. 触发方式
- **自动触发**: 每次 push 代码时自动运行
- **手动触发**: 在 Actions 页面手动触发
- **Pull Request**: PR 时自动运行（可配置）

## CI/CD 优势

### 持续集成优点
1. ✅ **自动化测试** - 每次提交自动运行测试
2. ✅ **快速反馈** - 及时发现代码问题
3. ✅ **质量保证** - 确保代码质量
4. ✅ **团队协作** - 统一的测试标准

### GitHub Actions 特点
1. ✅ **免费额度** - 公开仓库免费使用
2. ✅ **易于配置** - YAML 文件配置
3. ✅ **丰富生态** - 大量可用 Actions
4. ✅ **多平台支持** - Linux, Windows, macOS

## 评分标准

### CI 配置质量
- ✅ Workflow 文件配置正确
- ✅ 触发条件设置合理
- ✅ 步骤顺序正确
- ✅ Python 版本指定

### 测试质量
- ✅ 测试用例覆盖全面
- ✅ 断言准确
- ✅ 异常处理测试
- ✅ 边界情况测试

### 文档质量
- ✅ README 完整
- ✅ 配置说明清晰
- ✅ 使用步骤详细
- ✅ 代码注释完善

## 扩展配置

### 添加代码覆盖率
```yaml
- run: pip install pytest-cov
- run: pytest --cov=calculator --cov-report=html
```

### 多 Python 版本测试
```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11", "3.12"]
```

### 上传测试报告
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: test-report
    path: report.html
```

### 添加徽章
在 README 中添加状态徽章：
```markdown
![Python Test](https://github.com/username/repo/workflows/Python%20Test/badge.svg)
```

## 常见问题

### Q1: Workflow 不触发？
**A**: 检查 `.github/workflows/` 路径是否正确，YAML 语法是否有误。

### Q2: 测试失败？
**A**: 查看 Actions 日志，定位失败原因。确保依赖已正确安装。

### Q3: 报告无法查看？
**A**: 使用 `actions/upload-artifact` 上传报告，或配置 GitHub Pages。

### Q4: 如何调试？
**A**: 在本地运行相同命令，使用 `pytest -v` 查看详细输出。

## 最佳实践

### 1. 版本管理
- 使用固定版本号（如 @v4, @v5）
- 定期更新 Actions 版本
- 指定 Python 版本

### 2. 缓存依赖
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 3. 矩阵测试
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.9", "3.10", "3.11"]
```

### 4. 条件执行
```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: echo "Deploying..."
```

## 学习资源

1. **GitHub Actions 文档**: https://docs.github.com/actions
2. **pytest 文档**: https://docs.pytest.org/
3. **Python CI/CD 最佳实践**: https://testdriven.io/
4. **Actions Marketplace**: https://github.com/marketplace?type=actions

## 总结

### 项目特点
- ✅ 完整的 CI 配置
- ✅ 自动化测试流程
- ✅ 专业的项目结构
- ✅ 详细的文档说明

### 学习目标
- ✅ 理解 CI/CD 概念
- ✅ 掌握 GitHub Actions 配置
- ✅ 学会自动化测试
- ✅ 提升代码质量意识

---

**项目完成时间**: 2025年11月19日  
**适用平台**: GitHub  
**Python 版本**: 3.11  
**状态**: ✅ 就绪
