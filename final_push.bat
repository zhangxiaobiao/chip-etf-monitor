@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
echo ========================================
echo   推送到GitHub
echo ========================================
echo.
echo 目标仓库: https://github.com/zhangxiaobiao/chip-etf-monitor.git
echo.
echo 步骤 1/2: 重命名分支为main...
git branch -M main
if errorlevel 1 (
    echo [错误] 分支重命名失败
    pause
    exit /b 1
)
echo [成功] 分支已重命名为main
echo.
echo 步骤 2/2: 推送到GitHub...
git push -u origin main
if errorlevel 1 (
    echo.
    echo [错误] 推送失败！
    echo.
    echo 可能的原因：
    echo 1. GitHub上还没有创建 zhangxiaobiao/chip-etf-monitor 仓库
    echo 2. Token权限不足
    echo 3. 网络连接问题
    echo.
    echo 请先访问以下链接创建仓库：
    echo https://github.com/new
    echo.
    echo 仓库名称: chip-etf-monitor
    echo.
    pause
    exit /b 1
)
echo.
echo ========================================
echo   推送成功！
echo ========================================
echo.
echo 访问你的仓库：
echo https://github.com/zhangxiaobiao/chip-etf-monitor
echo.
pause
