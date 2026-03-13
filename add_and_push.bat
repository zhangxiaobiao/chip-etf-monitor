@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
echo ========================================
echo   添加新文件并推送到GitHub
echo ========================================
echo.
echo [1/3] 添加新文件...
git add .
echo.
echo [2/3] 提交更改...
git commit -m "Add GitHub publishing scripts and documentation"
echo.
echo [3/3] 推送到GitHub...
git push -u origin main
echo.
echo ========================================
if errorlevel 1 (
    echo   推送失败
    echo.
    echo 权限问题？请检查Token权限：
    echo https://github.com/settings/tokens
) else (
    echo   推送成功！
)
echo ========================================
pause
