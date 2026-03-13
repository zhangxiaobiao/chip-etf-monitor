@echo off
cd /d "c:\Users\INTEL3\WorkBuddy\Claw"
echo ========================================
echo   清理临时文件
echo ========================================
echo.

echo [1/4] 删除临时批处理脚本...
del add_and_push.bat 2>nul
del check_config.bat 2>nul
del check_remote.bat 2>nul
del commit.py 2>nul
del do_push.bat 2>nul
del final_push_command.bat 2>nul
del final_push.bat 2>nul
del fix_push.bat 2>nul
del git_commit.bat 2>nul
del push_to_github.bat 2>nul
del push_with_new_token.bat 2>nul
del rename_branch.bat 2>nul
del reset_remote.bat 2>nul
del setup_remote.bat 2>nul
del update_remote.bat 2>nul
del update_remote_only.bat 2>nul
echo 临时脚本已删除
echo.

echo [2/4] 删除临时GitHub发布指南...
del CREATE_REPO_GUIDE.md 2>nul
del DEBUG_PUSH.md 2>nul
del GITHUB_PUBLISH_GUIDE.md 2>nul
del MANUAL_PUSH.md 2>nul
del PUBLISH_COMPLETE_CHECKLIST.md 2>nul
del PUSH_READY.md 2>nul
del QUICK_GITHUB_GUIDE.md 2>nul
del SECURE_GITHUB_GUIDE.md 2>nul
del CLEANUP_PLAN.md 2>nul
echo 临时指南已删除
echo.

echo [3/4] 删除测试文件...
del test_env.py 2>nul
del test_env2.py 2>nul
echo 测试文件已删除
echo.

echo [4/4] 清理临时目录...
rmdir /s /q analysis_output 2>nul
rmdir /s /q data_cache 2>nul
rmdir /s /q -p 2>nul
echo 临时目录已清理
echo.

echo ========================================
echo   清理完成！
echo ========================================
echo.
echo 现在执行Git操作...
git add -A
git status
pause
