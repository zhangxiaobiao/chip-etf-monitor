@echo off
chcp 65001 >nul

echo ====================================================
echo  🚀 科创芯片ETF监控系统 - 快速启动
echo ====================================================
echo.

REM 首先尝试使用Python 3
echo 检查Python环境...
echo.

set PYTHON_CMD=
set PYTHON_VERSION=

REM 尝试不同的Python命令
for %%c in (python3 py python) do (
    where %%c >nul 2>nul
    if !errorlevel!==0 (
        %%c -c "import sys; v=sys.version_info; exit(0) if v.major==3 else exit(1)" >nul 2>nul
        if !errorlevel!==0 (
            set PYTHON_CMD=%%c
            goto :found_python3
        )
    )
)

:found_python3
if "%PYTHON_CMD%"=="" (
    echo ❌ 未找到Python 3
    echo.
    echo 请安装Python 3.7或更高版本:
    echo.
    echo 推荐安装Python 3.11+ (最新稳定版):
    echo   1. 访问 https://www.python.org/downloads/
    echo   2. 下载Windows安装程序
    echo   3. 安装时务必勾选 "Add Python to PATH"
    echo   4. 安装完成后重启命令行，重新运行此脚本
    echo.
    pause
    exit /b 1
)

REM 获取Python版本
%PYTHON_CMD% -c "import sys; print('Python {}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))" > python_version.txt
set /p PYTHON_VERSION= < python_version.txt
del python_version.txt

echo ✓ 找到: %PYTHON_VERSION%
echo.

REM 检查依赖
echo 检查必要依赖包...
%PYTHON_CMD% -c "
try:
    import pandas, numpy, yfinance, streamlit, plotly, requests
    print('✓ 核心依赖包已安装')
except ImportError as e:
    print('⚠️  部分依赖包未安装:')
    print('   正在尝试安装...')
    import subprocess, sys
    packages = ['pandas', 'numpy', 'yfinance', 'ta', 'streamlit', 'plotly', 'python-telegram-bot', 'schedule', 'python-dotenv', 'requests', 'tqdm']
    for pkg in packages:
        try:
            __import__(pkg.replace('-', '_'))
            print(f'    ✓ {pkg}')
        except:
            print(f'    📦 安装 {pkg}...')
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '--user'])
    print('✓ 依赖包安装完成')
"

echo.
echo ====================================================
echo  选择启动方式:
echo ====================================================
echo.
echo  1. 🌐 Web监控界面 (实时图表，推荐)
echo  2. 🔄 后台监控服务 (自动警报)
echo  3. 📊 数据分析工具 (历史分析)
echo  4. ⚙️  安装/更新依赖包
echo  5. ❌ 退出
echo.

set /p choice=请输入选项(1-5): 

if "%choice%"=="1" (
    echo.
    echo 正在启动Web监控界面...
    echo.
    echo 📡 请稍等，Streamlit正在启动...
    echo 🌐 启动后会自动打开浏览器
    echo 🔗 如果未自动打开，请访问: http://localhost:8501
    echo ⏹️  按 Ctrl+C 停止运行
    echo.
    echo ====================================================
    %PYTHON_CMD% -m streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo 正在启动后台监控服务...
    echo.
    echo 📡 开始监控科创芯片ETF (588200)...
    echo 🔔 价格变动超过阈值时会发送警报
    echo 📝 详细日志查看 monitor.log
    echo ⏹️  按 Ctrl+C 停止运行
    echo.
    echo ====================================================
    %PYTHON_CMD% monitor.py
) else if "%choice%"=="3" (
    echo.
    echo 正在启动数据分析工具...
    echo.
    echo 📊 加载历史数据分析...
    echo 📈 生成技术指标图表...
    echo 📄 输出分析报告...
    echo.
    echo ====================================================
    %PYTHON_CMD% analyzer.py
) else if "%choice%"=="4" (
    echo.
    echo 正在安装/更新依赖包...
    echo.
    %PYTHON_CMD% -m pip install --upgrade pip
    %PYTHON_CMD% -m pip install pandas numpy yfinance ta streamlit plotly python-telegram-bot schedule python-dotenv requests tqdm --user
    echo.
    echo ✓ 依赖包安装完成
    echo.
    pause
    goto :eof
) else if "%choice%"=="5" (
    echo 退出系统
    exit /b 0
) else (
    echo 无效选项，请重新运行
    pause
    exit /b 1
)

if not "%choice%"=="5" (
    echo.
    pause
)