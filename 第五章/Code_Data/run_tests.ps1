# 快速启动脚本 - 运行所有测试
# 使用方法: .\run_tests.ps1

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "电商平台登录模块自动化测试" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 是否安装
Write-Host "[1/6] 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python 未安装或未添加到 PATH" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host ""
Write-Host "[2/6] 安装 Python 依赖..." -ForegroundColor Yellow
pip install -r requirements.txt -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "✗ 依赖安装失败" -ForegroundColor Red
    exit 1
}

# 运行 API 测试
Write-Host ""
Write-Host "[3/6] 运行 API 测试..." -ForegroundColor Yellow
pytest tests\test_api_login.py -v --tb=short
$apiTestResult = $LASTEXITCODE

# 运行 UI 测试
Write-Host ""
Write-Host "[4/6] 运行 UI 测试..." -ForegroundColor Yellow
pytest tests\login_ui_test.py -v --tb=short
$uiTestResult = $LASTEXITCODE

# 生成综合报告
Write-Host ""
Write-Host "[5/6] 生成测试报告..." -ForegroundColor Yellow
pytest tests\ --html=test-report.html --self-contained-html --junitxml=test-results.xml -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 报告生成完成: test-report.html" -ForegroundColor Green
} else {
    Write-Host "⚠ 部分测试失败，报告已生成" -ForegroundColor Yellow
}

# 测试集成脚本
Write-Host ""
Write-Host "[6/6] 测试集成脚本..." -ForegroundColor Yellow
Write-Host "→ TestLink 同步（演示模式）" -ForegroundColor Gray
python scripts\sync_to_testlink.py --results test-results.xml
Write-Host ""
Write-Host "→ Jira 集成（演示模式）" -ForegroundColor Gray
python scripts\create_jira_issues.py --results test-results.xml

# 总结
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "测试执行完成" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 测试报告: test-report.html" -ForegroundColor White
Write-Host "📄 JUnit XML: test-results.xml" -ForegroundColor White
Write-Host ""
Write-Host "提示:" -ForegroundColor Yellow
Write-Host "  - 设置环境变量以连接真实服务器" -ForegroundColor Gray
Write-Host "  - 查看 README.md 了解详细配置" -ForegroundColor Gray
Write-Host "  - 配置 TestLink/Jira 凭据以启用自动同步" -ForegroundColor Gray
Write-Host ""

# 打开报告
$openReport = Read-Host "是否打开测试报告? (Y/N)"
if ($openReport -eq 'Y' -or $openReport -eq 'y') {
    Start-Process test-report.html
}
