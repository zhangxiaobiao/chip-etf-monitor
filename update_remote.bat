@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
set /p TOKEN=<C:\Users\INTEL3\Desktop\token.txt
echo Removing old remote...
git remote remove origin
echo Adding new remote repository...
git remote add origin https://%TOKEN%@github.com/zhangxiaobiao/chip-etf-monitor.git
echo Remote repository updated successfully!
git remote -v
