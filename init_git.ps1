# 科创芯片ETF监控系统 - Git初始化脚本
# 运行方式: 右键点击此文件，选择"使用 PowerShell 运行"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "科创芯片ETF监控系统 - Git初始化工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Git是否安装
try {
    $gitVersion = git --version
    Write-Host "✓ Git已安装: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git未安装或无法访问" -ForegroundColor Red
    Write-Host "请先安装Git: https://git-scm.com/" -ForegroundColor Yellow
    Write-Host "按任意键退出..."
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    exit 1
}

# 检查是否已初始化Git仓库
if (Test-Path .git) {
    Write-Host "✓ Git仓库已存在" -ForegroundColor Green
} else {
    Write-Host "🚀 初始化Git仓库..." -ForegroundColor Yellow
    git init
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Git仓库初始化成功" -ForegroundColor Green
    } else {
        Write-Host "❌ Git仓库初始化失败" -ForegroundColor Red
        exit 1
    }
}

# 配置Git用户信息
Write-Host ""
Write-Host "🔧 配置Git用户信息..." -ForegroundColor Yellow
git config user.name "科创芯片ETF监控系统"
git config user.email "chip-etf-monitor@example.com"

Write-Host "✓ Git用户信息已配置" -ForegroundColor Green

# 创建.gitignore文件（如果不存在）
Write-Host ""
Write-Host "📄 检查.gitignore文件..." -ForegroundColor Yellow
if (Test-Path .gitignore) {
    Write-Host "✓ .gitignore文件已存在" -ForegroundColor Green
} else {
    Write-Host "创建.gitignore文件..." -ForegroundColor Yellow
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 项目特定
data_cache/*.csv
data_cache/*.json
data_cache/*.pkl
analysis_output/*
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# WorkBuddy技能包缓存
.codebuddy/cache/

# 日志文件
*.log
logs/

# 系统文件
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# 临时文件
*.tmp
*.temp
~*

# 测试输出
.coverage
htmlcov/
.pytest_cache/

# 文档生成
docs/_build/
"@ | Out-File -FilePath .gitignore -Encoding UTF8
    Write-Host "✓ .gitignore文件已创建" -ForegroundColor Green
}

# 添加文件到暂存区
Write-Host ""
Write-Host "📦 添加文件到Git暂存区..." -ForegroundColor Yellow
git add .

# 显示状态
Write-Host ""
Write-Host "📊 Git状态:" -ForegroundColor Cyan
git status --short

# 创建初始提交
Write-Host ""
Write-Host "💾 创建初始提交..." -ForegroundColor Yellow
$commitMessage = @"
初始提交: 科创芯片ETF监控系统

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

📅 创建时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
"@

git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 初始提交创建成功" -ForegroundColor Green
} else {
    Write-Host "⚠️ 使用简化提交消息..." -ForegroundColor Yellow
    git commit -m "初始提交: 科创芯片ETF监控系统"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 提交失败" -ForegroundColor Red
        Write-Host "请检查Git配置:" -ForegroundColor Yellow
        Write-Host "  git config --global user.name '你的名字'" -ForegroundColor Gray
        Write-Host "  git config --global user.email '你的邮箱'" -ForegroundColor Gray
        exit 1
    }
    Write-Host "✓ 使用简化消息提交成功" -ForegroundColor Green
}

# 显示Git日志
Write-Host ""
Write-Host "📋 提交历史:" -ForegroundColor Cyan
git log --oneline -5

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 本地Git设置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 显示后续步骤
Write-Host "🚀 下一步 - 发布到GitHub:" -ForegroundColor Yellow
Write-Host ""
Write-Host "方法1: 使用GitHub CLI (推荐)" -ForegroundColor White
Write-Host "  1. 安装GitHub CLI: https://cli.github.com/" -ForegroundColor Gray
Write-Host "  2. 登录: gh auth login" -ForegroundColor Gray
Write-Host "  3. 创建仓库: gh repo create chip-etf-monitor --public --source=. --remote=origin --push" -ForegroundColor Gray
Write-Host ""
Write-Host "方法2: 使用Git命令" -ForegroundColor White
Write-Host "  1. 在GitHub创建仓库: https://github.com/new" -ForegroundColor Gray
Write-Host "     - 仓库名: chip-etf-monitor" -ForegroundColor Gray
Write-Host "     - 描述: 科创芯片ETF(588200)实时监控与分析系统" -ForegroundColor Gray
Write-Host "     - 选择Public" -ForegroundColor Gray
Write-Host "     - 不要初始化README, .gitignore等" -ForegroundColor Gray
Write-Host "  2. 添加远程仓库:" -ForegroundColor Gray
Write-Host "     git remote add origin https://github.com/你的用户名/chip-etf-monitor.git" -ForegroundColor Gray
Write-Host "  3. 推送代码:" -ForegroundColor Gray
Write-Host "     git branch -M main" -ForegroundColor Gray
Write-Host "     git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "📋 GitHub仓库信息:" -ForegroundColor Cyan
Write-Host "  仓库名称: chip-etf-monitor" -ForegroundColor Gray
Write-Host "  项目名称: 科创芯片ETF监控系统" -ForegroundColor Gray
Write-Host "  描述: 科创芯片ETF(588200)实时监控与分析系统，提供技术指标、买卖信号、可视化界面和价格警报" -ForegroundColor Gray
Write-Host "  建议: Public仓库" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 配置说明:" -ForegroundColor White
Write-Host "  - 确保.gitignore文件已正确配置" -ForegroundColor Gray
Write-Host "  - 敏感信息不要提交（如.env文件）" -ForegroundColor Gray
Write-Host "  - 建议使用SSH密钥进行认证" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "💡 提示: 发布后可以设置GitHub Pages展示项目" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')