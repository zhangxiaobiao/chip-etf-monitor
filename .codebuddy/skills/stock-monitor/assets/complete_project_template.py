#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完整项目模板生成器
从技能包生成完整的股票监控项目
"""

import os
import shutil
import sys
from datetime import datetime

def copy_template_files(src_dir, dst_dir, stock_symbol="588200.SS", stock_name="科创芯片ETF"):
    """复制模板文件并替换配置"""
    
    # 文件映射：源文件 -> 目标文件
    file_mapping = {
        'config.py': 'config.py',
        'requirements.txt': 'requirements.txt',
        '.env.example': '.env.example',
        'README.md': 'README.md',
        'app_template.py': 'app.py',
        'monitor_template.py': 'monitor.py',
        'analyzer_template.py': 'analyzer.py',
        'data_fetcher_template.py': 'data_fetcher.py',
        'signals_template.py': 'signals.py',
        'utils_template.py': 'utils.py',
        'run_template.py': 'run.py'
    }
    
    # 创建目录结构
    os.makedirs(os.path.join(dst_dir, 'data_cache'), exist_ok=True)
    os.makedirs(os.path.join(dst_dir, 'analysis_output'), exist_ok=True)
    
    # 替换变量
    replacements = {
        '{STOCK_SYMBOL}': stock_symbol,
        '{STOCK_NAME}': stock_name,
        '{TIMESTAMP}': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 复制并处理文件
    for src_file, dst_file in file_mapping.items():
        src_path = os.path.join(src_dir, src_file)
        dst_path = os.path.join(dst_dir, dst_file)
        
        if os.path.exists(src_path):
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换变量
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ 创建: {dst_file}")
        else:
            # 创建基础模板
            if dst_file == 'app.py':
                content = create_basic_app(stock_symbol, stock_name)
            elif dst_file == 'config.py':
                content = create_basic_config(stock_symbol, stock_name)
            elif dst_file == 'requirements.txt':
                content = create_requirements()
            else:
                content = f"# {dst_file} - 请从技能包复制完整内容"
            
            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"ⓘ 创建基础: {dst_file}")

def create_basic_config(symbol, name):
    """创建基础配置文件"""
    return f'''import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 股票配置
STOCK_SYMBOL = os.getenv('STOCK_SYMBOL', '{symbol}')
STOCK_NAME = "{name}"

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
    }}
'''

def create_basic_app(symbol, name):
    """创建基础Web应用"""
    return f'''import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="{name}监控系统",
    page_icon="📈",
    layout="wide"
)

st.title("📈 {name} ({symbol}) 实时监控系统")
st.markdown("---")

st.success("✅ 项目创建成功！")

st.subheader("📋 下一步操作")
st.write("""
1. **安装依赖包**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件配置您的设置
   ```

3. **启动系统**
   ```bash
   # Web界面
   streamlit run app.py
   
   # 后台监控
   python monitor.py
   
   # 数据分析
   python analyzer.py
   ```
""")

st.subheader("🌐 访问地址")
st.write("Web界面启动后访问: http://localhost:8501")

st.subheader("📞 技术支持")
st.write("如需帮助，请参考技能包文档或联系技术支持。")

st.markdown("---")
st.caption(f"项目生成时间: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
'''

def create_requirements():
    """创建依赖文件"""
    return '''pandas>=2.0.0
numpy>=1.24.0
yfinance>=0.2.38
ta>=0.10.2
streamlit>=1.28.0
plotly>=5.18.0
python-telegram-bot>=20.6
schedule>=1.2.0
python-dotenv>=1.0.0
requests>=2.31.0
tqdm>=4.66.0'''

def create_start_scripts(dst_dir, stock_name):
    """创建启动脚本"""
    
    # Windows批处理文件
    bat_content = f'''@echo off
chcp 65001 >nul

echo ====================================================
echo  🚀 {stock_name}监控系统启动
echo ====================================================
echo.

echo 请选择启动方式:
echo.
echo  1. 🌐 Web监控界面 (推荐)
echo  2. 🔄 后台监控服务
echo  3. 📊 数据分析工具
echo  4. ⚙️  安装依赖包
echo  5. ❌ 退出
echo.

set /p choice=请输入选项(1-5): 

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
    echo.
    echo 正在安装依赖包...
    echo.
    python -m pip install -r requirements.txt --user
    echo.
    echo ✓ 依赖包安装完成
    pause
    goto :eof
) else if "%choice%"=="5" (
    echo 退出
) else (
    echo 无效选项
)

pause'''
    
    with open(os.path.join(dst_dir, 'start_project.bat'), 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    print("✓ 创建: start_project.bat")
    
    # Linux/Mac Shell脚本
    sh_content = f'''#!/bin/bash

echo "===================================================="
echo "  🚀 {stock_name}监控系统启动"
echo "===================================================="
echo ""

echo "请选择启动方式:"
echo ""
echo "  1. 🌐 Web监控界面 (推荐)"
echo "  2. 🔄 后台监控服务"
echo "  3. 📊 数据分析工具"
echo "  4. ⚙️  安装依赖包"
echo "  5. ❌ 退出"
echo ""

read -p "请输入选项(1-5): " choice

case $choice in
    1)
        echo ""
        echo "正在启动Web监控界面..."
        echo "请访问: http://localhost:8501"
        echo ""
        python -m streamlit run app.py
        ;;
    2)
        echo ""
        echo "正在启动后台监控服务..."
        echo ""
        python monitor.py
        ;;
    3)
        echo ""
        echo "正在启动数据分析工具..."
        echo ""
        python analyzer.py
        ;;
    4)
        echo ""
        echo "正在安装依赖包..."
        echo ""
        pip install -r requirements.txt --user
        echo ""
        echo "✓ 依赖包安装完成"
        ;;
    5)
        echo "退出"
        ;;
    *)
        echo "无效选项"
        ;;
esac'''
    
    with open(os.path.join(dst_dir, 'start_project.sh'), 'w', encoding='utf-8') as f:
        f.write(sh_content)
    
    # 设置执行权限
    os.chmod(os.path.join(dst_dir, 'start_project.sh'), 0o755)
    print("✓ 创建: start_project.sh")

def main():
    """主函数"""
    print("=" * 60)
    print("      股票监控项目模板生成器")
    print("=" * 60)
    
    # 获取用户输入
    project_name = input("\n项目名称 (默认: stock-monitor): ").strip()
    if not project_name:
        project_name = "stock-monitor"
    
    stock_symbol = input("股票代码 (默认: 588200.SS): ").strip()
    if not stock_symbol:
        stock_symbol = "588200.SS"
    
    stock_name = input("股票名称 (默认: 科创芯片ETF): ").strip()
    if not stock_name:
        stock_name = "科创芯片ETF"
    
    # 创建项目目录
    project_dir = os.path.join(os.getcwd(), project_name)
    
    if os.path.exists(project_dir):
        print(f"\n❌ 错误: 目录 '{project_name}' 已存在")
        return
    
    print(f"\n正在创建项目: {project_name}")
    print(f"监控股票: {stock_name} ({stock_symbol})")
    print("-" * 40)
    
    # 创建项目
    try:
        # 创建目录
        os.makedirs(project_dir)
        
        # 复制模板文件
        copy_template_files(
            os.path.dirname(__file__),  # 当前目录
            project_dir,
            stock_symbol,
            stock_name
        )
        
        # 创建启动脚本
        create_start_scripts(project_dir, stock_name)
        
        print("-" * 40)
        print(f"✅ 项目 '{project_name}' 创建成功！")
        print("=" * 60)
        
        # 显示后续步骤
        print("\n🎉 项目创建完成！")
        print("\n下一步操作:")
        print(f"1. 进入项目目录: cd {project_name}")
        print("2. 安装依赖包:")
        print("   - 方法A: python -m pip install -r requirements.txt")
        print("   - 方法B: 运行 start_project.bat 选择选项4")
        print("3. 配置环境变量:")
        print("   - 复制 .env.example 为 .env")
        print("   - 编辑 .env 文件设置您的配置")
        print("4. 启动系统:")
        print("   - Web界面: streamlit run app.py")
        print("   - 或运行: start_project.bat")
        print("\n详细说明请查看 README.md 文件")
        
    except Exception as e:
        print(f"\n❌ 创建项目时出错: {e}")
        # 清理已创建的目录
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)

if __name__ == "__main__":
    main()