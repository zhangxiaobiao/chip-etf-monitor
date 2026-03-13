@echo off
echo 正在启动科创芯片ETF监控系统...
echo.

REM 检查Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误：未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

REM 检查依赖
echo 检查Python依赖包...
python -c "import pandas, numpy, yfinance, ta, streamlit, plotly, schedule, dotenv, requests, tqdm" >nul 2>nul
if %errorlevel% neq 0 (
    echo 正在安装依赖包...
    python -m pip install pandas numpy yfinance ta streamlit plotly python-telegram-bot schedule python-dotenv requests tqdm --user
    if %errorlevel% neq 0 (
        echo 依赖包安装失败
        pause
        exit /b 1
    )
    echo 依赖包安装成功
)

echo.
echo 请选择启动方式：
echo 1. 启动Web监控界面
echo 2. 启动后台监控服务
echo 3. 启动数据分析工具
echo 4. 查看使用说明
echo 5. 退出
echo.

set /p choice=请输入选项(1-5): 

if "%choice%"=="1" (
    echo 正在启动Web监控界面...
    start streamlit run app.py
) else if "%choice%"=="2" (
    echo 正在启动后台监控服务...
    python monitor.py
) else if "%choice%"=="3" (
    echo 正在启动数据分析工具...
    python analyzer.py
) else if "%choice%"=="4" (
    echo 正在显示使用说明...
    python -c "import sys; sys.path.append('.'); exec(open('run.py').read())" --help
    pause
) else if "%choice%"=="5" (
    echo 退出系统
) else (
    echo 无效选项
)

pause