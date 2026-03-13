@echo off
chcp 65001 >nul

echo ====================================================
echo  🚀 科创芯片ETF监控系统 - 启动助手
echo ====================================================
echo.

echo 步骤1: 检查Python环境
echo.

REM 检查Python 3
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 未找到Python
    echo.
    echo 请先安装Python 3.7或更高版本:
    echo   1. 访问 https://www.python.org/downloads/
    echo   2. 下载Windows安装程序
    echo   3. 安装时务必勾选 "Add Python to PATH"
    echo   4. 安装完成后重新运行此脚本
    echo.
    pause
    exit /b 1
)

REM 检查Python版本
python -c "import sys; v=sys.version_info; print('Python {}.{}.{}'.format(v.major, v.minor, v.micro))"
python -c "import sys; v=sys.version_info; exit(0) if v.major==3 else exit(1)" >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 需要Python 3，当前是Python 2
    echo.
    echo 请安装Python 3.7或更高版本
    echo 下载: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ Python 3 已就绪
echo.

echo 步骤2: 检查依赖包
echo.

REM 创建简单的Python脚本来检查依赖
echo import sys > check_deps.py
echo print("检查依赖包...") >> check_deps.py
echo deps = ['pandas', 'numpy', 'yfinance', 'streamlit', 'plotly', 'requests'] >> check_deps.py
echo for dep in deps: >> check_deps.py
echo     try: >> check_deps.py
echo         __import__(dep) >> check_deps.py
echo         print(f'    ✓ {dep}') >> check_deps.py
echo     except ImportError: >> check_deps.py
echo         print(f'    ✗ {dep} (未安装)') >> check_deps.py

python check_deps.py
del check_deps.py

echo.
echo 步骤3: 选择启动方式
echo ====================================================
echo.
echo  1. 🌐 Web监控界面 (推荐)
echo  2. 🔄 后台监控服务  
echo  3. 📊 数据分析工具
echo  4. ⚙️  安装依赖包
echo  5. ❌ 退出
echo.

set /p choice=请选择(1-5): 

if "%choice%"=="1" (
    echo.
    echo 正在启动Web监控界面...
    echo.
    echo 请稍等，系统正在启动...
    echo 启动完成后会自动打开浏览器
    echo 如果未打开，请访问: http://localhost:8501
    echo.
    echo 按 Ctrl+C 停止运行
    echo ====================================================
    python -m streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo 正在启动后台监控服务...
    echo 按 Ctrl+C 停止运行
    echo ====================================================
    python monitor.py
) else if "%choice%"=="3" (
    echo.
    echo 正在启动数据分析工具...
    echo ====================================================
    python analyzer.py
) else if "%choice%"=="4" (
    echo.
    echo 正在安装依赖包...
    echo 这可能需要几分钟，请耐心等待...
    echo.
    python -m pip install pandas numpy yfinance ta streamlit plotly python-telegram-bot schedule python-dotenv requests tqdm --user
    echo.
    echo ✓ 依赖包安装完成
    echo 请重新运行此脚本启动系统
    echo.
    pause
) else if "%choice%"=="5" (
    echo 退出系统
    exit /b 0
) else (
    echo 无效选项
)

if not "%choice%"=="5" (
    echo.
    pause
)