@echo off
chcp 65001 >nul

echo ====================================================
echo  🚀 科创芯片ETF监控系统 - 快速启动
echo ====================================================
echo.

echo 方案选择:
echo.
echo  1. 💡 使用现有Python 2.7启动简化版监控
echo  2. 🐍 安装Python 3.11并启动完整系统
echo  3. 📖 查看详细安装指南
echo  4. ❌ 退出
echo.

set /p choice=请选择(1-4): 

if "%choice%"=="1" (
    echo.
    echo 正在启动简化版监控系统...
    echo 使用Python 2.7运行，每30秒刷新
    echo.
    echo 按 Ctrl+C 停止运行
    echo ====================================================
    C:\Python27\python.exe simple_monitor.py
) else if "%choice%"=="2" (
    echo.
    echo 推荐安装Python 3.11:
    echo.
    echo 请访问: https://www.python.org/downloads/
    echo 下载Windows 64位安装程序
    echo.
    echo 安装时务必:
    echo   1. 勾选 "Add Python to PATH"
    echo   2. 选择 "Install Now"
    echo.
    echo 安装完成后，请重新运行此脚本
    echo.
    pause
) else if "%choice%"=="3" (
    echo.
    echo 详细安装步骤:
    echo ====================================================
    echo 1. 安装Python 3.11:
    echo    访问 https://www.python.org/downloads/
    echo    下载并安装，勾选 "Add Python to PATH"
    echo.
    echo 2. 安装依赖包:
    echo    打开命令行，运行:
    echo    python -m pip install pandas numpy yfinance ta streamlit plotly --user
    echo.
    echo 3. 启动系统:
    echo    在项目目录运行:
    echo    python -m streamlit run app.py
    echo.
    echo 4. 访问系统:
    echo    浏览器打开 http://localhost:8501
    echo.
    echo 详细说明见 README_START.md 文件
    echo ====================================================
    echo.
    pause
) else if "%choice%"=="4" (
    echo 退出
    exit /b 0
) else (
    echo 无效选择
)

pause