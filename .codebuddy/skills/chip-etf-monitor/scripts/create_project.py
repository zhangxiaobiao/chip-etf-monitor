#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科创芯片ETF监控系统项目创建脚本
自动创建完整的监控系统项目结构
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

def print_header():
    """打印脚本头部信息"""
    print("=" * 60)
    print("科创芯片ETF(588200)监控系统项目创建工具")
    print("=" * 60)
    print("版本: 1.0.0")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_requirements():
    """检查系统要求"""
    print("\n[1/6] 检查系统要求...")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 错误: Python版本需要3.7或更高")
        print(f"当前版本: {sys.version}")
        return False
    
    print(f"✓ Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # 检查必要目录
    required_dirs = ['assets', 'references', 'scripts']
    for dir_name in required_dirs:
        dir_path = Path(__file__).parent.parent / dir_name
        if not dir_path.exists():
            print(f"❌ 错误: 缺少必要目录 {dir_name}")
            return False
    
    print("✓ 所有系统要求检查通过")
    return True

def get_user_input():
    """获取用户输入配置"""
    print("\n[2/6] 项目配置")
    
    config = {}
    
    # 项目名称
    default_name = "chip-etf-monitor"
    project_name = input(f"请输入项目名称 [{default_name}]: ").strip()
    config['project_name'] = project_name if project_name else default_name
    
    # 项目目录
    default_dir = Path.cwd() / config['project_name']
    project_dir = input(f"请输入项目目录 [{default_dir}]: ").strip()
    config['project_dir'] = Path(project_dir) if project_dir else default_dir
    
    # 股票配置
    print("\n股票配置:")
    config['stock_symbol'] = input(f"股票代码 [588200.SS]: ").strip() or "588200.SS"
    config['stock_name'] = input(f"股票名称 [科创芯片ETF]: ").strip() or "科创芯片ETF"
    
    # 监控配置
    print("\n监控配置:")
    config['monitoring_interval'] = input(f"监控间隔(秒) [60]: ").strip() or "60"
    config['alert_threshold'] = input(f"价格警报阈值(%) [2.0]: ").strip() or "2.0"
    config['history_days'] = input(f"历史数据天数 [30]: ").strip() or "30"
    
    # Telegram配置
    print("\nTelegram通知配置 (可选):")
    enable_telegram = input(f"启用Telegram通知? (y/n) [n]: ").strip().lower()
    config['enable_telegram'] = enable_telegram in ['y', 'yes', '是']
    
    if config['enable_telegram']:
        config['telegram_token'] = input(f"Telegram Bot Token: ").strip()
        config['telegram_chat_id'] = input(f"Telegram Chat ID: ").strip()
    else:
        config['telegram_token'] = ""
        config['telegram_chat_id'] = ""
    
    return config

def create_project_structure(config):
    """创建项目目录结构"""
    print(f"\n[3/6] 创建项目目录结构: {config['project_dir']}")
    
    project_dir = config['project_dir']
    
    # 如果目录已存在，询问是否覆盖
    if project_dir.exists():
        print(f"⚠️  目录 {project_dir} 已存在")
        overwrite = input("是否覆盖? (y/n) [n]: ").strip().lower()
        if overwrite not in ['y', 'yes', '是']:
            print("❌ 用户取消操作")
            return False
        # 删除现有目录
        shutil.rmtree(project_dir)
    
    # 创建主目录
    project_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ 创建项目目录: {project_dir}")
    
    # 创建子目录
    subdirs = [
        'analysis_output/reports',
        'analysis_output/charts', 
        'analysis_output/logs',
        'data_cache/historical',
        'data_cache/realtime',
        'data_cache/metadata',
        'tests'
    ]
    
    for subdir in subdirs:
        dir_path = project_dir / subdir
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建子目录: {subdir}")
    
    print(f"✓ 目录结构创建完成")
    return True

def copy_template_files(config):
    """从skill包复制模板文件"""
    print("\n[4/6] 复制模板文件")
    
    skill_dir = Path(__file__).parent.parent
    project_dir = config['project_dir']
    
    # 定义需要复制的文件映射
    file_mapping = {
        # 从skill assets目录复制
        skill_dir / 'assets' / 'app_template.py': project_dir / 'app.py',
        skill_dir / 'assets' / 'monitor_template.py': project_dir / 'monitor.py',
        skill_dir / 'assets' / 'analyzer_template.py': project_dir / 'analyzer.py',
        skill_dir / 'assets' / 'config_template.py': project_dir / 'config.py',
        skill_dir / 'assets' / 'data_fetcher_template.py': project_dir / 'data_fetcher.py',
        skill_dir / 'assets' / 'signals_template.py': project_dir / 'signals.py',
        skill_dir / 'assets' / 'utils_template.py': project_dir / 'utils.py',
        skill_dir / 'assets' / 'requirements_template.txt': project_dir / 'requirements.txt',
        skill_dir / 'assets' / 'env_template': project_dir / '.env.example',
        
        # 从skill根目录复制文档
        skill_dir / 'SKILL.md': project_dir / 'SKILL_REFERENCE.md',
        skill_dir / 'README_SKILL.md': project_dir / 'README_SKILL_REFERENCE.md',
        
        # 从references复制技术文档
        skill_dir / 'references' / 'technical_indicators.md': project_dir / 'docs' / 'technical_indicators.md',
    }
    
    # 检查模板文件是否存在，如果不存在则创建默认文件
    for src_template, dst_file in list(file_mapping.items()):
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        
        if src_template.exists():
            shutil.copy2(src_template, dst_file)
            print(f"✓ 复制: {src_template.name} → {dst_file.name}")
        else:
            # 如果模板不存在，创建默认文件
            create_default_file(dst_file, config)
            print(f"✓ 创建默认: {dst_file.name}")
    
    # 创建启动脚本
    create_startup_scripts(project_dir)
    
    print(f"✓ 文件复制完成")
    return True

def create_default_file(file_path, config):
    """创建默认文件内容"""
    
    if file_path.name == 'app.py':
        content = f'''# 科创芯片ETF监控系统 - Web界面
# 项目: {config['project_name']}
# 股票: {config['stock_name']} ({config['stock_symbol']})
# 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

import streamlit as st

st.set_page_config(
    page_title="{config['stock_name']}监控系统",
    page_icon="📈",
    layout="wide"
)

st.title(f"📈 {{config['stock_name']}} 实时监控系统")
st.info("这是一个自动生成的监控系统模板，请根据实际需求进行修改。")
'''
    elif file_path.name == 'config.py':
        content = f'''# 科创芯片ETF监控系统配置
# 项目: {config['project_name']}

# 股票配置
STOCK_SYMBOL = "{config['stock_symbol']}"
STOCK_NAME = "{config['stock_name']}"

# 监控配置
MONITORING_INTERVAL = {config['monitoring_interval']}
ALERT_THRESHOLD = {config['alert_threshold']}
CHECK_HISTORY_DAYS = {config['history_days']}

# Telegram配置
ENABLE_TELEGRAM = {str(config['enable_telegram']).lower()}
TELEGRAM_BOT_TOKEN = "{config['telegram_token']}"
TELEGRAM_CHAT_ID = "{config['telegram_chat_id']}"

# 技术指标配置
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BOLLINGER_WINDOW = 20
BOLLINGER_STD = 2
'''
    elif file_path.name == 'requirements.txt':
        content = '''# 科创芯片ETF监控系统依赖包

# 核心依赖
pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.38
ta>=0.10.2

# 可视化
streamlit>=1.28.0
plotly>=5.18.0

# 通知和工具
python-telegram-bot>=20.6
schedule>=1.2.0
python-dotenv>=1.0.0
requests>=2.31.0
tqdm>=4.66.0

# 开发工具
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
'''
    elif file_path.name == '.env.example':
        content = f'''# 科创芯片ETF监控系统环境变量配置
# 复制此文件为 .env 并修改配置

# 股票配置
STOCK_SYMBOL={config['stock_symbol']}
STOCK_NAME={config['stock_name']}

# 监控配置
MONITORING_INTERVAL={config['monitoring_interval']}
ALERT_THRESHOLD={config['alert_threshold']}
CHECK_HISTORY_DAYS={config['history_days']}

# Telegram配置 (可选)
ENABLE_TELEGRAM={str(config['enable_telegram']).lower()}
TELEGRAM_BOT_TOKEN={config['telegram_token']}
TELEGRAM_CHAT_ID={config['telegram_chat_id']}

# 数据源配置
YAHOO_FINANCE_ENABLED=true
CACHE_ENABLED=true
CACHE_EXPIRE_HOURS=24
'''
    else:
        # 其他文件创建简单模板
        content = f'''# {file_path.name}
# 科创芯片ETF监控系统
# 项目: {config['project_name']}
# 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# TODO: 实现具体功能
print("这是一个自动生成的文件模板，请根据实际需求进行修改。")
'''
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_startup_scripts(project_dir):
    """创建启动脚本"""
    
    # Windows批处理脚本
    bat_content = '''@echo off
echo ========================================
echo 科创芯片ETF监控系统启动脚本
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.7+
    pause
    exit /b 1
)

echo ✓ 检查Python... 通过

REM 检查依赖
if not exist "requirements.txt" (
    echo ❌ 错误: 缺少requirements.txt文件
    pause
    exit /b 1
)

echo ✓ 检查依赖文件... 通过

REM 安装依赖
echo.
echo [1/3] 安装Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ⚠️  警告: 依赖安装可能有问题，请手动检查
)

REM 检查环境配置
echo.
echo [2/3] 检查环境配置...
if not exist ".env" (
    echo ⚠️  警告: 缺少.env文件，使用示例配置
    copy .env.example .env >nul
    echo ✓ 已创建.env文件，请编辑配置
)

REM 启动系统
echo.
echo [3/3] 启动监控系统...
echo.
echo 选择启动方式:
echo 1. Web界面 (Streamlit)
echo 2. 后台监控服务
echo 3. 数据分析工具
echo 4. 退出
echo.

set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" (
    echo 启动Web界面...
    streamlit run app.py
) else if "%choice%"=="2" (
    echo 启动后台监控...
    python monitor.py
) else if "%choice%"=="3" (
    echo 启动数据分析...
    python analyzer.py
) else (
    echo 退出
    pause
)
'''
    
    # 创建批处理脚本
    bat_files = {
        'start.bat': bat_content,
        'start_easy.bat': '''@echo off
echo 科创芯片ETF监控系统 - 简易启动
echo.
echo 启动Web界面...
streamlit run app.py
''',
        'start_simple.bat': '''@echo off
echo 科创芯片ETF监控系统 - 快速启动
echo.
python monitor.py
''',
        'launch.bat': '''@echo off
echo 科创芯片ETF监控系统启动器
echo.
call start.bat
''',
        'QUICK_START.bat': '''@echo off
echo ========================================
echo 科创芯片ETF监控系统快速开始指南
echo ========================================
echo.
echo 1. 安装依赖: pip install -r requirements.txt
echo 2. 配置环境: copy .env.example .env
echo 3. 编辑.env文件，配置股票和Telegram信息
echo 4. 启动系统: streamlit run app.py
echo.
echo 详细说明请查看README.md
echo.
pause
''',
        'install_python3.bat': '''@echo off
echo Python 3安装助手
echo.
echo 请访问 https://www.python.org/downloads/ 下载Python 3.7+
echo.
echo 安装时请务必勾选 "Add Python to PATH"
echo.
pause
'''
    }
    
    for filename, content in bat_files.items():
        file_path = project_dir / filename
        with open(file_path, 'w', encoding='gbk') as f:  # Windows使用GBK编码
            f.write(content)
        print(f"✓ 创建启动脚本: {filename}")
    
    # 创建Python测试脚本
    test_scripts = {
        'test_env.py': '''#!/usr/bin/env python3
# 环境测试脚本

import sys
import platform

print("=" * 50)
print("科创芯片ETF监控系统 - 环境测试")
print("=" * 50)

# Python版本
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")

# 系统信息
print(f"操作系统: {platform.system()} {platform.release()}")
print(f"系统架构: {platform.machine()}")

# 检查核心包
required_packages = ['pandas', 'numpy', 'yfinance', 'streamlit', 'plotly']
print("\\n检查核心依赖包:")

for package in required_packages:
    try:
        __import__(package)
        print(f"✓ {package}: 已安装")
    except ImportError:
        print(f"✗ {package}: 未安装")

print("\\n" + "=" * 50)
print("测试完成")
print("=" * 50)
''',
        'test_env2.py': '''#!/usr/bin/env python3
# 高级环境测试脚本

import sys
import subprocess
import json

def run_command(cmd):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def main():
    print("🔍 高级环境测试")
    print("=" * 50)
    
    tests = [
        ("Python版本", "python --version"),
        ("Pip版本", "pip --version"),
        ("Streamlit版本", "streamlit --version"),
        ("Pandas版本", "python -c \"import pandas; print(pandas.__version__)\""),
        ("网络连接", "ping -n 2 api.finance.yahoo.com"),
    ]
    
    for test_name, cmd in tests:
        print(f"\\n测试: {test_name}")
        print(f"命令: {cmd}")
        
        success, output = run_command(cmd)
        if success:
            print(f"结果: ✓ 成功")
            if output:
                print(f"输出: {output[:100]}{'...' if len(output) > 100 else ''}")
        else:
            print(f"结果: ✗ 失败")
            print(f"错误: {output}")
    
    print("\\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    main()
'''
    }
    
    for filename, content in test_scripts.items():
        file_path = project_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 创建测试脚本: {filename}")

def create_documentation(config):
    """创建项目文档"""
    print("\n[5/6] 创建项目文档")
    
    project_dir = config['project_dir']
    
    # README.md
    readme_content = f'''# {config['stock_name']}监控系统

## 📊 项目概述

本项目是一个专门针对**{config['stock_name']} ({config['stock_symbol']})** 的实时监控系统，提供技术指标分析、买卖信号生成、可视化界面和价格警报功能。

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置股票和Telegram信息
```

### 2. 启动系统

#### 启动Web界面
```bash
streamlit run app.py
```
访问 http://localhost:8501

#### 启动后台监控
```bash
python monitor.py
```

#### 快速启动 (Windows)
双击 `start_easy.bat` 或 `start.bat`

### 3. 配置说明

编辑 `config.py` 或 `.env` 文件：

```python
# 股票配置
STOCK_SYMBOL = "{config['stock_symbol']}"
STOCK_NAME = "{config['stock_name']}"

# 监控配置
MONITORING_INTERVAL = {config['monitoring_interval']}
ALERT_THRESHOLD = {config['alert_threshold']}
CHECK_HISTORY_DAYS = {config['history_days']}
```

## 📈 核心功能

### 1. 实时行情监控
- 实时价格和涨跌幅
- 成交量和价格区间
- 多数据源支持

### 2. 技术指标分析
- MACD趋势分析
- RSI超买超卖判断
- 布林带波动性分析
- 移动平均线趋势确认

### 3. 智能信号生成
- 多指标综合评分
- 买卖信号建议
- 风险等级评估
- 操作建议

### 4. 可视化界面
- Streamlit Web应用
- Plotly交互图表
- 实时仪表盘
- 技术指标展示

### 5. 智能通知
- Telegram实时通知
- 价格变动警报
- 买卖信号提醒
- 系统状态报告

## 🗂️ 项目结构

```
{config['project_name']}/
├── app.py              # Streamlit Web界面
├── monitor.py          # 后台监控服务
├── analyzer.py         # 数据分析工具
├── config.py           # 系统配置
├── data_fetcher.py     # 数据获取模块
├── signals.py          # 信号生成模块
├── utils.py            # 工具函数
├── requirements.txt    # Python依赖
├── .env.example        # 环境变量模板
├── start.bat           # Windows启动脚本
├── start_easy.bat      # 简易启动脚本
├── data_cache/         # 数据缓存目录
├── analysis_output/    # 分析输出目录
└── README.md           # 本文件
```

## 🔧 配置详解

### 基础配置
- **STOCK_SYMBOL**: 监控的股票代码
- **MONITORING_INTERVAL**: 监控间隔（秒）
- **ALERT_THRESHOLD**: 价格警报阈值（%）
- **CHECK_HISTORY_DAYS**: 历史数据天数

### 技术指标配置
- **RSI参数**: 周期、超买超卖阈值
- **MACD参数**: 快线、慢线、信号线周期
- **布林带参数**: 窗口、标准差倍数

### Telegram通知配置
1. 创建Telegram Bot (@BotFather)
2. 获取Bot Token和Chat ID
3. 在 `.env` 文件中配置

## 🚨 故障排除

### 常见问题

#### 1. 数据获取失败
- 检查网络连接
- 验证股票代码格式
- 查看数据源API状态

#### 2. 依赖包安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3. Streamlit启动失败
- 检查端口8501是否被占用
- 确保Streamlit正确安装
- 查看防火墙设置

### 日志文件
- **monitor.log**: 后台监控日志
- **data_cache/**: 数据缓存文件
- **analysis_output/**: 分析输出文件

## 📊 技术栈

- **后端**: Python 3.7+
- **数据处理**: Pandas, NumPy, yfinance
- **技术分析**: TA-Lib (ta库)
- **可视化**: Streamlit, Plotly
- **通知**: python-telegram-bot
- **调度**: schedule

## 🔄 维护计划

### 日常维护
- **每日**: 检查系统运行状态
- **每周**: 清理缓存数据
- **每月**: 更新依赖包版本
- **每季度**: 审核技术指标参数

### 定期备份
- 实时数据: 每小时备份
- 配置文件: 每次修改后备份
- 完整系统: 每周备份

## ⚠️ 免责声明

1. 本系统为辅助决策工具，不构成投资建议
2. 金融市场有风险，投资需谨慎
3. 建议结合基本面分析和其他技术指标
4. 系统提供的数据仅供参考，不保证准确性

## 📞 技术支持

如有问题或建议，请参考：
- 项目文档: SKILL_REFERENCE.md
- 技术指标详解: docs/technical_indicators.md
- GitHub Issues: 提交问题和功能请求

---

**💡 提示**: 建议先从基础监控开始，逐步探索高级功能。定期回顾和调整监控参数，以适应市场变化。

**项目创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
    
    with open(project_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✓ 创建README.md")
    
    # README_START.md - 简化版开始指南
    readme_start = f'''# {config['stock_name']}监控系统 - 快速开始

## 🎯 三步快速启动

### 第一步：安装依赖
```bash
pip install -r requirements.txt
```

### 第二步：配置系统
1. 复制环境变量文件：
   ```bash
   copy .env.example .env
   ```
2. 编辑 `.env` 文件，配置股票代码和Telegram信息

### 第三步：启动系统
- **Web界面**: `streamlit run app.py`
- **后台监控**: `python monitor.py`
- **一键启动**: 双击 `start_easy.bat`

## 📞 遇到问题？

### 常见问题快速解决

#### 1. Python未安装
- 下载地址: https://www.python.org/downloads/
- 安装时勾选 "Add Python to PATH"

#### 2. 依赖安装失败
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 3. 启动失败
- 检查端口8501是否被占用
- 运行测试脚本: `python test_env.py`

## 🆘 紧急帮助

如果以上方法无法解决问题：
1. 查看详细文档: README.md
2. 运行环境测试: `python test_env2.py`
3. 检查错误日志: `data_cache/error.log`

---

**开始时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**股票代码**: {config['stock_symbol']}
**监控间隔**: {config['monitoring_interval']}秒
'''

    with open(project_dir / 'README_START.md', 'w', encoding='utf-8') as f:
        f.write(readme_start)
    print("✓ 创建README_START.md")

def finalize_project(config):
    """完成项目创建"""
    print("\n[6/6] 完成项目创建")
    
    project_dir = config['project_dir']
    
    # 创建.gitignore文件
    gitignore_content = '''# Python
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
!data_cache/.gitkeep
analysis_output/*
!analysis_output/.gitkeep

# 环境配置
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

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
'''
    
    with open(project_dir / '.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print("✓ 创建.gitignore")
    
    # 创建.gitkeep文件确保空目录被版本控制
    for root, dirs, files in os.walk(project_dir):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if not any((dir_path / f).is_file() for f in os.listdir(dir_path)):
                (dir_path / '.gitkeep').touch()
    
    # 创建LICENSE文件
    license_content = '''MIT License

Copyright (c) 2023 科创芯片ETF监控系统

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    
    with open(project_dir / 'LICENSE', 'w', encoding='utf-8') as f:
        f.write(license_content)
    print("✓ 创建LICENSE")
    
    # 创建简单的监控和分析脚本
    simple_scripts = {
        'simple_monitor.py': '''#!/usr/bin/env python3
# 简化监控脚本

import time
from datetime import datetime

def main():
    print(f"{'='*50}")
    print(f"科创芯片ETF简化监控系统")
    print(f"{'='*50}")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        while True:
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"[{current_time}] 监控运行中...")
            time.sleep(60)  # 60秒间隔
    except KeyboardInterrupt:
        print("\\n监控已停止")
    except Exception as e:
        print(f"监控错误: {e}")

if __name__ == "__main__":
    main()
''',
        'simple_start.py': '''#!/usr/bin/env python3
# 简化启动脚本

import subprocess
import sys
import os

def check_python():
    """检查Python环境"""
    try:
        import pandas
        import streamlit
        return True, "Python环境检查通过"
    except ImportError as e:
        return False, f"缺少依赖: {e}"

def main():
    print("🚀 科创芯片ETF监控系统 - 简化启动")
    print("=" * 50)
    
    # 检查环境
    print("1. 检查Python环境...")
    success, message = check_python()
    if success:
        print(f"   ✓ {message}")
    else:
        print(f"   ✗ {message}")
        print("   请运行: pip install -r requirements.txt")
        return
    
    # 检查配置文件
    print("2. 检查配置文件...")
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("   ✓ 已创建.env文件，请编辑配置")
        else:
            print("   ✗ 缺少.env.example文件")
            return
    else:
        print("   ✓ .env文件已存在")
    
    # 启动选项
    print("\\n3. 选择启动方式:")
    print("   1. Web界面 (推荐)")
    print("   2. 后台监控")
    print("   3. 退出")
    
    choice = input("请输入选项 (1-3): ").strip()
    
    if choice == "1":
        print("启动Web界面...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    elif choice == "2":
        print("启动后台监控...")
        subprocess.run([sys.executable, "monitor.py"])
    else:
        print("退出")

if __name__ == "__main__":
    main()
''',
        'run.py': '''#!/usr/bin/env python3
# 主运行脚本

import sys
import os

def main():
    """主函数"""
    print("科创芯片ETF监控系统")
    print("=" * 40)
    
    # 添加项目根目录到Python路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # 检查必要的模块
    try:
        from config import STOCK_SYMBOL, STOCK_NAME
        print(f"股票: {STOCK_NAME} ({STOCK_SYMBOL})")
    except ImportError:
        print("警告: 无法导入配置，请检查config.py")
    
    # 显示可用命令
    print("\\n可用命令:")
    print("  python monitor.py    - 启动后台监控")
    print("  streamlit run app.py - 启动Web界面")
    print("  python analyzer.py   - 运行数据分析")
    print("  python test_env.py   - 测试环境")
    
    print("\\n详细说明请查看README.md")

if __name__ == "__main__":
    main()
'''
    }
    
    for filename, content in simple_scripts.items():
        file_path = project_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 创建脚本: {filename}")
    
    return True

def print_summary(config):
    """打印项目创建总结"""
    print("\n" + "=" * 60)
    print("🎉 项目创建完成!")
    print("=" * 60)
    
    project_dir = config['project_dir']
    
    print(f"\n📁 项目目录: {project_dir}")
    print(f"📈 监控股票: {config['stock_name']} ({config['stock_symbol']})")
    print(f"⏰ 监控间隔: {config['monitoring_interval']}秒")
    print(f"🚨 警报阈值: {config['alert_threshold']}%")
    
    print("\n🚀 启动方式:")
    print(f"1. Web界面:   cd \"{project_dir}\" && streamlit run app.py")
    print(f"2. 后台监控:  cd \"{project_dir}\" && python monitor.py")
    print(f"3. 一键启动:  双击 {project_dir}/start_easy.bat")
    
    print("\n📋 下一步:")
    print("1. 安装依赖: pip install -r requirements.txt")
    print("2. 配置环境: 编辑 .env 文件")
    print("3. 启动测试: python test_env.py")
    print("4. 开始监控: 选择上述启动方式之一")
    
    if not config['enable_telegram']:
        print("\n💡 提示: Telegram通知未启用，如需启用请编辑 .env 文件")
    
    print("\n" + "=" * 60)
    print("💡 更多信息请查看项目目录中的文档:")
    print(f"   - README.md: 完整文档")
    print(f"   - README_START.md: 快速开始指南")
    print(f"   - SKILL_REFERENCE.md: 技能包参考")
    print("=" * 60)

def main():
    """主函数"""
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='创建科创芯片ETF监控系统项目')
    parser.add_argument('--name', help='项目名称')
    parser.add_argument('--dir', help='项目目录')
    parser.add_argument('--symbol', help='股票代码')
    parser.add_argument('--quick', action='store_true', help='快速模式')
    args = parser.parse_args()
    
    # 打印头部信息
    print_header()
    
    # 检查系统要求
    if not check_requirements():
        sys.exit(1)
    
    # 获取配置
    if args.quick and args.name and args.symbol:
        # 快速模式使用命令行参数
        config = {
            'project_name': args.name,
            'project_dir': Path(args.dir) if args.dir else Path.cwd() / args.name,
            'stock_symbol': args.symbol,
            'stock_name': '科创芯片ETF',
            'monitoring_interval': '60',
            'alert_threshold': '2.0',
            'history_days': '30',
            'enable_telegram': False,
            'telegram_token': '',
            'telegram_chat_id': ''
        }
    else:
        # 交互式获取配置
        config = get_user_input()
    
    # 创建项目
    try:
        if not create_project_structure(config):
            sys.exit(1)
        
        if not copy_template_files(config):
            sys.exit(1)
        
        create_documentation(config)
        
        if not finalize_project(config):
            sys.exit(1)
        
        # 打印总结
        print_summary(config)
        
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()