@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
echo ========================================
echo   正在推送到GitHub...
echo ========================================
echo 目标仓库: https://github.com/zhangxiaobiao/chip-etf-monitor.git
echo ========================================
git push -u origin main
echo ========================================
echo   推送完成！
echo ========================================
pause
