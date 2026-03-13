@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
set /p TOKEN=<C:\Users\INTEL3\Desktop\token.txt
echo Removing old remote...
git remote remove origin
echo Adding remote with token...
git remote add origin https://%TOKEN%@github.com/zhangxiaobiao/chip-etf-monitor.git
echo Verifying configuration...
git remote -v
echo.
echo ========================================
echo   配置完成！
echo ========================================
echo.
echo 现在执行推送命令...
git branch -M main
git push -u origin main
pause
