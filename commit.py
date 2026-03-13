#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Git发布脚本"""
import subprocess

# 执行Git提交
subprocess.run([
    'git', '-C', r'c:\Users\INTEL3\WorkBuddy\Claw',
    'commit', '-m', 'Initial commit: 科创芯片ETF实时监控系统'
])
