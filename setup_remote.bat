@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
set /p TOKEN=<C:\Users\INTEL3\Desktop\token.txt
git remote add origin https://%TOKEN%@github.com/645702352/chip-etf-monitor.git
echo Remote repository added successfully
