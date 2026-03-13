@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
echo ========================================
echo   Git配置检查
echo ========================================
echo.
echo [1] 当前Git用户配置:
git config user.name
git config user.email
echo.
echo [2] 远程仓库配置:
git remote -v
echo.
echo [3] 当前分支:
git branch
echo.
pause
