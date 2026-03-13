@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
echo ========================================
echo   重新配置并推送到GitHub
echo ========================================
echo.
echo [1/3] 读取Token...
set /p TOKEN=<C:\Users\INTEL3\Desktop\token.txt
echo Token: %TOKEN:~0,20%... (已隐藏)
echo.
echo [2/3] 配置远程仓库...
git remote remove origin
git remote add origin https://%TOKEN%@github.com/zhangxiaobiao/chip-etf-monitor.git
git remote -v
echo.
echo [3/3] 推送到GitHub...
git push -u origin main
echo.
echo ========================================
if errorlevel 1 (
    echo   推送失败！
    echo.
    echo 可能的原因：
    echo 1. Token权限不足（需要 repo 权限）
    echo 2. GitHub仓库不存在
    echo 3. Token已过期
    echo.
    echo 请访问以下链接检查：
    echo https://github.com/settings/tokens
) else (
    echo   推送成功！
)
echo ========================================
pause
