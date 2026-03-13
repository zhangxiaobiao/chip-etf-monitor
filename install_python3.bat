@echo off
chcp 65001 >nul

echo ====================================================
echo  Python 3.7 安装助手
echo ====================================================
echo.

REM 检查是否已安装Python 3.7+
where python >nul 2>nul
if %errorlevel%==0 (
    python -c "import sys; v=sys.version_info; exit(0) if v.major==3 and v.minor>=7 else exit(1)" >nul 2>nul
    if %errorlevel%==0 (
        echo ✓ 已安装Python 3.7或更高版本
        python -c "import sys; print('当前版本: {}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))"
        echo.
        goto :start_system
    )
)

echo 当前Python版本:
where python
echo.

echo 检测到需要安装Python 3.7
echo.
echo 请选择安装方式:
echo   1. 自动下载并安装Python 3.7.9 (推荐)
echo   2. 手动下载安装 (显示下载链接)
echo   3. 使用Python 3.8+ (如果已安装)
echo   4. 退出
echo.

set /p choice=请选择(1-4): 

if "%choice%"=="1" (
    echo.
    echo 正在下载Python 3.7.9安装程序...
    
    REM 创建临时目录
    set TEMP_DIR=%TEMP%\python_install
    if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
    
    REM 下载Python 3.7.9
    echo 正在从Python官网下载...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe' -OutFile '%TEMP_DIR%\python-3.7.9.exe'"
    
    if exist "%TEMP_DIR%\python-3.7.9.exe" (
        echo 下载完成，开始安装...
        echo 请按照安装向导完成安装
        echo 重要: 安装时请勾选 "Add Python 3.7 to PATH"
        echo.
        "%TEMP_DIR%\python-3.7.9.exe"
        
        echo.
        echo 安装完成，请重新启动命令行窗口
        pause
        exit /b 0
    ) else (
        echo 下载失败，请手动下载
        goto :manual_download
    )
    
) else if "%choice%"=="2" (
    :manual_download
    echo.
    echo 请手动下载Python 3.7.9:
    echo.
    echo 下载链接: https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe
    echo.
    echo 安装注意事项:
    echo   1. 运行下载的安装程序
    echo   2. 勾选 "Add Python 3.7 to PATH"
    echo   3. 选择 "Install Now" 或自定义安装
    echo   4. 安装完成后重启命令行窗口
    echo.
    pause
    exit /b 0
    
) else if "%choice%"=="3" (
    echo.
    echo 请确保已安装Python 3.8或更高版本
    where python3
    where py
    echo.
    echo 如果已安装，请使用以下命令启动系统:
    echo   python3 run.py
    echo   或
    echo   py run.py
    echo.
    pause
    exit /b 0
    
) else if "%choice%"=="4" (
    echo 退出安装
    exit /b 0
) else (
    echo 无效选择
    pause
    exit /b 1
)

:start_system
echo ====================================================
echo  启动科创芯片ETF监控系统
echo ====================================================
echo.

REM 检查依赖
echo 检查Python依赖包...
python -c "import pandas" >nul 2>nul
if %errorlevel% neq 0 (
    echo 正在安装必要依赖包...
    python -m pip install pandas numpy yfinance ta streamlit plotly python-telegram-bot schedule python-dotenv requests tqdm --user
    if %errorlevel% neq 0 (
        echo 依赖包安装失败，请手动安装
        echo 命令: python -m pip install pandas numpy yfinance ta streamlit plotly python-telegram-bot schedule python-dotenv requests tqdm
        pause
    )
)

echo.
echo 请选择启动方式:
echo   1. 🌐 启动Web监控界面 (推荐)
echo   2. 🔄 启动后台监控服务
echo   3. 📊 启动数据分析工具
echo   4. ❌ 退出
echo.

set /p choice=请输入选项(1-4): 

if "%choice%"=="1" (
    echo.
    echo 正在启动Web监控界面...
    echo 请稍等，系统正在启动...
    echo.
    echo 启动完成后会自动打开浏览器
    echo 如果没有打开，请访问: http://localhost:8501
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
    echo 退出系统
) else (
    echo 无效选项
)

if not "%choice%"=="4" (
    echo.
    pause
)