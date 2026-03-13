#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
股票监控项目创建脚本
快速创建基于技能包的项目模板
"""

import os
import shutil
import sys
from datetime import datetime

def create_project(project_name: str, stock_symbol: str = "588200.SS", stock_name: str = "科创芯片ETF"):
    """创建股票监控项目"""
    
    print(f"正在创建项目: {project_name}")
    print(f"监控股票: {stock_name} ({stock_symbol})")
    print("=" * 60)
    
    # 项目目录
    project_dir = os.path.join(os.getcwd(), project_name)
    
    # 检查目录是否存在
    if os.path.exists(project_dir):
        print(f"错误: 目录 '{project_name}' 已存在")
        return False
    
    # 创建目录结构
    directories = [
        project_dir,
        os.path.join(project_dir, "data_cache"),
        os.path.join(project_dir, "analysis_output")
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # 复制核心文件
    core_files = {
        'config.py': """import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 股票配置
STOCK_SYMBOL = os.getenv('STOCK_SYMBOL', '{stock_symbol}')
STOCK_NAME = "{stock_name}"

# 监控配置
MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', 60))
ALERT_THRESHOLD = float(os.getenv('ALERT_THRESHOLD', 2.0))
CHECK_HISTORY_DAYS = int(os.getenv('CHECK_HISTORY_DAYS', 30))

# 技术指标配置
RSI_OVERBOUGHT = int(os.getenv('RSI_OVERBOUGHT', 70))
RSI_OVERSOLD = int(os.getenv('RSI_OVERSOLD', 30))
MACD_SIGNAL = int(os.getenv('MACD_SIGNAL', 9))
MACD_FAST = int(os.getenv('MACD_FAST', 12))
MACD_SLOW = int(os.getenv('MACD_SLOW', 26))
BBANDS_PERIOD = int(os.getenv('BBANDS_PERIOD', 20))
BBANDS_STD = float(os.getenv('BBANDS_STD', 2.0))

# 通知配置
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
ENABLE_TELEGRAM = TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID

# 数据源配置
YAHOO_FINANCE_ENABLED = True
DATA_CACHE_DIR = "data_cache"
DATA_CACHE_TTL = 300

def get_config_summary():
    return {{
        "stock_symbol": STOCK_SYMBOL,
        "stock_name": STOCK_NAME,
        "monitoring_interval": MONITORING_INTERVAL,
        "alert_threshold": ALERT_THRESHOLD,
        "check_history_days": CHECK_HISTORY_DAYS,
        "telegram_enabled": ENABLE_TELEGRAM
    }}""".format(stock_symbol=stock_symbol, stock_name=stock_name),
        
        'requirements.txt': """pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.38
ta>=0.10.2
streamlit>=1.28.0
plotly>=5.18.0
python-telegram-bot>=20.6
schedule>=1.2.0
python-dotenv>=1.0.0
requests>=2.31.0
tqdm>=4.66.0""",
        
        '.env.example': """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Stock Monitoring Settings
STOCK_SYMBOL={stock_symbol}
MONITORING_INTERVAL=60
ALERT_THRESHOLD=2.0
CHECK_HISTORY_DAYS=30

# Technical Indicators Settings
RSI_OVERBOUGHT=70
RSI_OVERSOLD=30
MACD_SIGNAL=9
MACD_FAST=12
MACD_SLOW=26
BBANDS_PERIOD=20
BBANDS_STD=2.0""".format(stock_symbol=stock_symbol),
        
        'README.md': """# {stock_name} ({stock_symbol}) 实时监控系统

## 项目概述
实时监控{stock_name}行情数据，提供技术分析和买卖信号。

## 功能特点
- 📈 实时行情获取
- 🔍 多指标技术分析
- 🚦 智能买卖信号
- 🌐 Web监控界面
- 🔔 价格警报通知

## 快速启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境
```bash
cp .env.example .env
# 编辑 .env 文件配置您的设置
```

### 3. 启动系统
```bash
# Web界面
streamlit run app.py

# 后台监控
python monitor.py

# 数据分析
python analyzer.py
```

## 技术架构
- **语言**: Python 3.7+
- **数据处理**: Pandas, NumPy
- **数据源**: Yahoo Finance
- **可视化**: Streamlit, Plotly
- **通知**: Telegram Bot

## 配置说明
编辑 `config.py` 或 `.env` 文件调整：
- 监控股票代码
- 检查间隔时间
- 警报阈值
- 技术指标参数

## 使用说明
1. 配置Telegram Bot接收实时通知
2. 启动监控系统
3. 访问 http://localhost:8501 查看实时界面
4. 查看 `monitor.log` 获取运行日志

## 注意事项
- 本系统为辅助决策工具，不构成投资建议
- 定期检查数据源连接状态
- 配置合适的监控频率避免API限制

---
*项目基于股票监控技能包创建*
*生成时间: {timestamp}*""".format(
            stock_name=stock_name,
            stock_symbol=stock_symbol,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ),
        
        'start_project.bat': """@echo off
chcp 65001 >nul

echo ====================================================
echo  🚀 {stock_name} 监控系统启动
echo ====================================================
echo.

echo 请选择启动方式:
echo.
echo  1. 🌐 Web监控界面 (推荐)
echo  2. 🔄 后台监控服务
echo  3. 📊 数据分析工具
echo  4. ❌ 退出
echo.

set /p choice=请输入选项(1-4): 

if "%choice%"=="1" (
    echo.
    echo 正在启动Web监控界面...
    echo 请访问: http://localhost:8501
    echo.
    python -m streamlit run app.py
) else if "%choice%"=="2" (
    echo.
    echo 正在启动后台监控服务...
    echo.
    python monitor.py
) else if "%choice%"=="3" (
    echo.
    echo 正在启动数据分析工具...
    echo.
    python analyzer.py
) else if "%choice%"=="4" (
    echo 退出
) else (
    echo 无效选项
)

pause""".format(stock_name=stock_name)
    }
    
    # 写入文件
    for filename, content in core_files.items():
        filepath = os.path.join(project_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 创建: {filename}")
    
    # 复制Python脚本文件
    script_files_needed = ['app.py', 'monitor.py', 'analyzer.py', 'data_fetcher.py', 'signals.py', 'utils.py', 'run.py']
    
    # 创建基础文件
    for script in script_files_needed:
        if script == 'app.py':
            content = """import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="{stock_name}监控系统", layout="wide")
st.title("📈 {stock_name} ({stock_symbol}) 实时监控系统")

st.write("项目已创建完成！请安装依赖后启动系统。")
st.info("运行: pip install -r requirements.txt")
st.success("启动命令: streamlit run app.py")""".format(
                stock_name=stock_name, 
                stock_symbol=stock_symbol
            )
        elif script == 'monitor.py':
            content = """#!/usr/bin/env python
print("后台监控服务")
print("请先安装依赖包: pip install -r requirements.txt")"""
        elif script == 'analyzer.py':
            content = """#!/usr/bin/env python
print("数据分析工具")
print("请先安装依赖包: pip install -r requirements.txt")"""
        else:
            content = """#!/usr/bin/env python
print("{filename} - 请从技能包复制完整内容")""".format(filename=script)
        
        filepath = os.path.join(project_dir, script)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("=" * 60)
    print(f"✅ 项目 '{project_name}' 创建成功！")
    print("=" * 60)
    print("\n下一步操作:")
    print(f"1. 进入项目目录: cd {project_name}")
    print("2. 安装依赖包: pip install -r requirements.txt")
    print("3. 复制 .env.example 为 .env 并编辑配置")
    print("4. 启动系统: python start_project.bat")
    print("\n详细说明请查看 README.md")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("      股票监控项目创建向导")
    print("=" * 60)
    
    # 获取用户输入
    print("\n请填写项目信息:")
    
    project_name = input("项目名称 (默认: stock-monitor): ").strip()
    if not project_name:
        project_name = "stock-monitor"
    
    stock_symbol = input("股票代码 (默认: 588200.SS): ").strip()
    if not stock_symbol:
        stock_symbol = "588200.SS"
    
    stock_name = input("股票名称 (默认: 科创芯片ETF): ").strip()
    if not stock_name:
        stock_name = "科创芯片ETF"
    
    print("\n" + "=" * 60)
    print("确认信息:")
    print(f"  项目名称: {project_name}")
    print(f"  股票代码: {stock_symbol}")
    print(f"  股票名称: {stock_name}")
    print("=" * 60)
    
    confirm = input("\n是否创建项目? (y/n): ").strip().lower()
    if confirm != 'y':
        print("操作取消")
        return
    
    # 创建项目
    success = create_project(project_name, stock_symbol, stock_name)
    
    if success:
        print(f"\n🎉 项目 '{project_name}' 已成功创建！")
        print("请按照上述步骤完成后续操作。")
    else:
        print("\n❌ 项目创建失败，请检查错误信息。")

if __name__ == "__main__":
    main()