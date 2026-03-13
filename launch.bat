@echo off
chcp 65001 >nul
echo ============================================================
echo   🚀 科创芯片ETF (588200) 实时监控系统
echo ============================================================
echo.

REM 尝试使用不同的Python命令
set PYTHON_CMD=python
where python >nul 2>nul || set PYTHON_CMD=py
where py >nul 2>nul || set PYTHON_CMD=python3
where python3 >nul 2>nul || (
    echo ❌ 错误：未找到Python，请先安装Python 3.7+
    echo.
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ 找到Python: %PYTHON_CMD%
echo.

REM 创建必要的目录
if not exist data_cache mkdir data_cache
if not exist analysis_output mkdir analysis_output
echo ✓ 创建必要目录

echo.
echo 请选择启动方式：
echo   1. 🌐 启动Web监控界面（推荐）
echo   2. 🔄 启动后台监控服务
echo   3. 📊 启动数据分析工具
echo   4. ℹ️  查看系统信息
echo   5. ❌ 退出
echo.

set /p choice=请输入选项(1-5): 

if "%choice%"=="1" (
    echo.
    echo 正在启动Web监控界面...
    echo 请稍等，Streamlit正在启动...
    echo.
    echo 启动完成后会自动在浏览器中打开
    echo 如果没有自动打开，请访问：http://localhost:8501
    echo.
    echo 按 Ctrl+C 停止运行
    echo ============================================================
    %PYTHON_CMD% -m streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo 正在启动后台监控服务...
    echo 按 Ctrl+C 停止运行
    echo ============================================================
    %PYTHON_CMD% monitor.py
) else if "%choice%"=="3" (
    echo.
    echo 正在启动数据分析工具...
    echo ============================================================
    %PYTHON_CMD% analyzer.py
) else if "%choice%"=="4" (
    echo.
    echo 系统信息：
    echo --------------------------------------------
    %PYTHON_CMD% -c "import sys; print('Python版本:', sys.version.split()[0]); print('系统平台:', sys.platform)"
    echo --------------------------------------------
    echo 项目文件：11个文件已就绪
    echo 数据目录：data_cache/, analysis_output/
    echo 配置文件：.env.example (请复制为.env并编辑)
    echo.
    pause
) else if "%choice%"=="5" (
    echo.
    echo 退出系统
) else (
    echo.
    echo 无效选项
    pause
)

if not "%choice%"=="5" (
    echo.
    pause
)