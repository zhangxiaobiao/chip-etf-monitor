@echo off
echo ========================================
echo 科创芯片ETF监控系统 - GitHub发布工具
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)
echo ✓ Python已安装

REM 检查Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Git，请先安装Git: https://git-scm.com/
    pause
    exit /b 1
)
echo ✓ Git已安装

echo.
echo 🔍 检查当前目录...
echo   项目目录: %CD%
echo.

REM 初始化Git仓库
if exist ".git" (
    echo ✓ Git仓库已存在
) else (
    echo 🚀 初始化Git仓库...
    git init
    if errorlevel 1 (
        echo ❌ Git仓库初始化失败
        pause
        exit /b 1
    )
    echo ✓ Git仓库初始化成功
    
    REM 配置用户信息
    echo   配置Git用户信息...
    git config user.name "科创芯片ETF监控系统"
    git config user.email "chip-etf-monitor@example.com"
)

REM 创建.gitignore文件
echo.
echo 📄 创建.gitignore文件...
if exist ".gitignore" (
    echo ✓ .gitignore文件已存在
) else (
    (
    echo # Python
    echo __pycache__/
    echo *.py[cod]
    echo *$py.class
    echo *.so
    echo .Python
    echo build/
    echo develop-eggs/
    echo dist/
    echo downloads/
    echo eggs/
    echo .eggs/
    echo lib/
    echo lib64/
    echo parts/
    echo sdist/
    echo var/
    echo wheels/
    echo *.egg-info/
    echo .installed.cfg
    echo *.egg
    echo.
    echo # 项目特定
    echo data_cache/*.csv
    echo data_cache/*.json
    echo data_cache/*.pkl
    echo analysis_output/*
    echo .env
    echo .env.local
    echo .env.development.local
    echo .env.test.local
    echo .env.production.local
    echo.
    echo # 日志文件
    echo *.log
    echo logs/
    echo.
    echo # 系统文件
    echo .DS_Store
    echo Thumbs.db
    echo.
    echo # IDE
    echo .vscode/
    echo .idea/
    echo *.swp
    echo *.swo
    echo.
    echo # 临时文件
    echo *.tmp
    echo *.temp
    echo ~*
    ) > .gitignore
    echo ✓ .gitignore文件已创建
)

REM 添加文件到Git
echo.
echo 📦 添加文件到Git...
git add .
if errorlevel 1 (
    echo ⚠️  添加文件时出现问题
    echo   尝试单独添加文件...
    git add *.py *.md *.txt *.bat
    git add .gitignore
)

REM 显示状态
echo.
echo 📊 Git状态:
git status --short

REM 创建提交
echo.
echo 💾 创建初始提交...
git commit -m "初始提交: 科创芯片ETF监控系统

🎯 项目概述
科创芯片ETF(588200)实时监控与分析系统，提供技术指标、买卖信号、可视化界面和价格警报

📦 包含功能:
- 实时行情监控 (科创芯片ETF 588200)
- 技术指标分析 (MACD, RSI, 布林带)
- 买卖信号生成和风险评估
- Streamlit可视化界面
- Telegram价格警报系统
- 完整的技术文档和Skill包

🛠️ 技术栈:
- Python 3.7+
- Pandas, NumPy, yfinance
- Streamlit, Plotly
- TA-Lib技术分析库
- Telegram Bot API

📅 创建时间: %DATE% %TIME%"
if errorlevel 1 (
    echo ⚠️  提交失败，尝试简化提交消息...
    git commit -m "初始提交: 科创芯片ETF监控系统"
    if errorlevel 1 (
        echo ❌ 提交失败，请检查Git配置
        echo   运行: git config --global user.name '你的名字' 
        echo   运行: git config --global user.email '你的邮箱'
        pause
        exit /b 1
    )
)

echo ✓ 提交创建成功

echo.
echo ========================================
echo 🎉 本地Git设置完成！
echo ========================================
echo.

echo 🚀 下一步 - 发布到GitHub:
echo.
echo 方法1: 使用GitHub CLI (推荐)
echo   1. 安装GitHub CLI: https://cli.github.com/
echo   2. 登录: gh auth login
echo   3. 创建仓库: gh repo create chip-etf-monitor --public --source=. --remote=origin --push
echo.
echo 方法2: 使用Git命令
echo   1. 在GitHub创建仓库: https://github.com/new
echo      - 仓库名: chip-etf-monitor
echo      - 描述: 科创芯片ETF(588200)实时监控与分析系统
echo      - 选择Public
echo      - 不要初始化README, .gitignore等
echo   2. 添加远程仓库:
echo      git remote add origin https://github.com/你的用户名/chip-etf-monitor.git
echo   3. 推送代码:
echo      git branch -M main
echo      git push -u origin main
echo.
echo 方法3: 使用GitHub网页
echo   1. 访问 https://github.com/new
echo   2. 填写仓库信息
echo   3. 上传现有文件
echo.
echo 📋 GitHub仓库信息:
echo   仓库名称: chip-etf-monitor
echo   项目名称: 科创芯片ETF监控系统
echo   描述: 科创芯片ETF(588200)实时监控与分析系统，提供技术指标、买卖信号、可视化界面和价格警报
echo   建议: Public仓库
echo.
echo 🔧 配置说明:
echo   - 确保.gitignore文件已正确配置
echo   - 敏感信息不要提交（如.env文件）
echo   - 建议使用SSH密钥进行认证
echo.
echo 📚 文档:
echo   - 项目文档: README.md
echo   - 技能包文档: .codebuddy/skills/chip-etf-monitor/
echo   - 快速开始: README_START.md
echo.
echo ========================================
echo 💡 提示: 发布后可以设置GitHub Pages展示项目
echo ========================================
echo.

REM 创建仓库信息文件
(
echo {
echo   "repository_name": "chip-etf-monitor",
echo   "project_name": "科创芯片ETF监控系统",
echo   "description": "科创芯片ETF(588200)实时监控与分析系统，提供技术指标、买卖信号、可视化界面和价格警报",
echo   "private": false,
echo   "has_issues": true,
echo   "has_projects": true,
echo   "has_wiki": true,
echo   "setup_time": "%DATE% %TIME%"
echo }
) > github_repo_info.json

echo 📄 GitHub仓库信息已保存到: github_repo_info.json
echo.

pause