@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
set /p TOKEN=<C:\Users\INTEL3\Desktop\token.txt
git remote remove origin
git remote add origin https://%TOKEN%@github.com/zhangxiaobiao/chip-etf-monitor.git
echo Remote updated with new token
git remote -v
