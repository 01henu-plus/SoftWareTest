# 快速启动脚本
# 运行此脚本会自动测试 API（假设 Flask 已在另一终端运行）

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  订单系统集成测试 - 快速演示" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Flask 服务是否运行
Write-Host "步骤 1: 检查 Flask 服务..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/order" -Method POST -ContentType "application/json" -Body '{"item":"book","qty":1}' -ErrorAction Stop
    Write-Host "✓ Flask 服务正在运行" -ForegroundColor Green
} catch {
    Write-Host "✗ Flask 服务未运行" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先在另一个终端运行:" -ForegroundColor Yellow
    Write-Host "  python app.py" -ForegroundColor White
    Write-Host "或" -ForegroundColor Yellow
    Write-Host "  E:/python3.14/python.exe app.py" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "步骤 2: 运行集成测试..." -ForegroundColor Yellow
Write-Host ""

# 运行测试
& E:/python3.14/python.exe manual_test.py

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "提示: 使用 Ctrl+C 停止 Flask 服务" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
