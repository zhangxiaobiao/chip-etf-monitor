@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
echo ========================================
echo   使用新Token推送到GitHub
echo ========================================
echo.
echo [1/3] 读取新Token...
set /p TOKEN=<C:\Users\INTEL3\Desktop\token.txt
echo Token已加载
echo.
echo [2/3] 配置远程仓库...
git remote remove origin
git remote add origin https://%TOKEN%@github.com/zhangxiaobiao/chip-etf-monitor.git
echo 远程仓库已配置
echo.
echo [3/3] 推送到GitHub...
echo 正在推送，请稍候...
git push -u origin main
echo.
echo ========================================
if errorlevel 1 (
    echo   推送失败！
    echo.
    echo 可能的原因：
    echo 1. GitHub仓库不存在
    echo 2. Token权限不足
    echo 3. 用户名不正确
    echo.
    echo 请检查：
    echo - 仓库地址: https://github.com/zhangxiaobiao/chip-etf-monitor
    echo - Token权限: https://github.com/settings/tokens
) else (
    echo   推送成功！
    echo.
    echo 访问你的仓库：
    echo https://github.com/zhangxiaobiao/chip-etf-monitor
)
echo ========================================
pause
