#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Python环境 - Python 2兼容版本
"""

import sys

print("="*60)
print("Python环境测试")
print("="*60)

print("Python版本: {}".format(sys.version))
print("Python路径: {}".format(sys.executable))

# 检查必要的包
required_packages = [
    'pandas',
    'numpy',
    'yfinance',
    'ta',
    'streamlit',
    'plotly',
    'schedule',
    'dotenv',
    'requests',
    'tqdm'
]

print("\n检查依赖包:")
for package in required_packages:
    try:
        __import__(package.replace('-', '_'))
        print("  ✓ {}".format(package))
    except ImportError:
        print("  ✗ {} (未安装)".format(package))

print("\n" + "="*60)
print("如果所有包都显示✓，系统可以正常运行")
print("如果有✗，请运行: python -m pip install 包名")
print("="*60)