#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的启动脚本
"""

import subprocess
import sys
import os

def check_python():
    """检查Python环境"""
    try:
        version = sys.version_info
        print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print("错误: 需要Python 3.7或更高版本")
            return False
        
        return True
    except Exception as e:
        print(f"检查Python时出错: {e}")
        return False

def install_dependencies():
    """安装依赖包"""
    try:
        import pip
        packages = [
            'pandas',
            'numpy', 
            'yfinance',
            'ta',
            'streamlit',
            'plotly',
            'python-telegram-bot',
            'schedule',
            'python-dotenv',
            'requests',
            'tqdm'
        ]
        
        print("正在安装依赖包...")
        for package in packages:
            try:
                __import__(package.replace('-', '_'))
                print(f"  ✓ {package} 已安装")
            except ImportError:
                print(f"  📦 正在安装 {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"  ✓ {package} 安装成功")
        
        return True
    except Exception as e:
        print(f"安装依赖包时出错: {e}")
        return False

def run_web_interface():
    """运行Web界面"""
    try:
        print("\n正在启动Web监控界面...")
        print("请稍等，Streamlit正在启动...")
        print("启动完成后，会在浏览器中自动打开界面")
        print("如果没有自动打开，请访问: http://localhost:8501")
        print("\n按 Ctrl+C 停止运行")
        
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        return True
    except KeyboardInterrupt:
        print("\nWeb界面已关闭")
        return True
    except Exception as e:
        print(f"启动Web界面时出错: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("🚀 科创芯片ETF (588200) 实时监控系统")
    print("="*60)
    
    # 检查Python
    if not check_python():
        return
    
    # 安装依赖
    if not install_dependencies():
        print("是否继续? (y/n): ", end="")
        choice = input().strip().lower()
        if choice != 'y':
            return
    
    # 运行Web界面
    run_web_interface()

if __name__ == "__main__":
    main()