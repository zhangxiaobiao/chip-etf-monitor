#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全的GitHub发布辅助脚本
支持使用Personal Access Token进行安全的Git操作
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """执行命令并显示结果"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=r"c:\Users\INTEL3\WorkBuddy\Claw"
        )
        if result.returncode == 0:
            print(f"✅ {description} 成功")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} 失败")
            if result.stderr:
                print(f"错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False

def check_git_installed():
    """检查Git是否已安装"""
    return run_command("git --version", "检查Git安装")

def init_git_repo():
    """初始化Git仓库"""
    if Path(r"c:\Users\INTEL3\WorkBuddy\Claw\.git").exists():
        print("✅ Git仓库已存在")
        return True
    return run_command("git init", "初始化Git仓库")

def add_files():
    """添加所有文件到暂存区"""
    return run_command("git add .", "添加文件到暂存区")

def create_initial_commit():
    """创建初始提交"""
    commit_msg = 'Initial commit: 科创芯片ETF实时监控系统\n\n- 完整的ETF监控和分析功能\n- 专业级技术指标分析\n- Web可视化界面\n- WorkBuddy Skill包集成'
    
    # 使用Git配置的提交信息
    cmd = f'git commit -m "{commit_msg}"'
    return run_command(cmd, "创建初始提交")

def configure_git_user():
    """配置Git用户信息"""
    print("\n📝 配置Git用户信息...")
    
    name = input("请输入你的GitHub用户名: ").strip()
    email = input("请输入你的GitHub邮箱: ").strip()
    
    if not name or not email:
        print("❌ 用户名和邮箱不能为空")
        return False
    
    success = True
    success &= run_command(f'git config user.name "{name}"', "设置Git用户名")
    success &= run_command(f'git config user.email "{email}"', "设置Git邮箱")
    
    return success

def setup_remote_repo(token_method=True):
    """设置远程仓库"""
    print("\n🌐 设置GitHub远程仓库...")
    
    username = input("请输入你的GitHub用户名: ").strip()
    repo_name = input("请输入仓库名称 (默认: chip-etf-monitor): ").strip()
    
    if not repo_name:
        repo_name = "chip-etf-monitor"
    
    # 设置远程仓库URL
    if token_method:
        print("\n📝 使用Personal Access Token认证")
        print("⚠️  请先按照 SECURE_GITHUB_GUIDE.md 创建Token")
        
        token = input("请输入你的GitHub Personal Access Token: ").strip()
        
        if not token:
            print("❌ Token不能为空")
            return False
        
        remote_url = f"https://{token}@github.com/{username}/{repo_name}.git"
        print("🔒 Token已配置，将被保存在Windows凭据管理器中")
    else:
        print("\n🔑 使用SSH密钥认证")
        remote_url = f"git@github.com:{username}/{repo_name}.git"
    
    # 添加远程仓库
    return run_command(f'git remote add origin "{remote_url}"', "添加远程仓库")

def push_to_github():
    """推送到GitHub"""
    # 重命名分支为main
    run_command("git branch -M main", "重命名分支为main")
    
    # 推送
    print("\n🚀 开始推送到GitHub...")
    return run_command("git push -u origin main", "推送到GitHub远程仓库")

def check_remote_exists():
    """检查远程仓库是否已配置"""
    try:
        result = subprocess.run(
            "git remote -v",
            shell=True,
            capture_output=True,
            text=True,
            cwd=r"c:\Users\INTEL3\WorkBuddy\Claw"
        )
        return "origin" in result.stdout
    except:
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 科创芯片ETF监控系统 - GitHub发布辅助工具")
    print("=" * 60)
    
    # 步骤1: 检查Git
    print("\n【步骤 1/7】检查Git安装")
    if not check_git_installed():
        print("❌ 请先安装Git: https://git-scm.com/downloads")
        return False
    
    # 步骤2: 初始化仓库
    print("\n【步骤 2/7】初始化Git仓库")
    if not init_git_repo():
        return False
    
    # 步骤3: 配置用户信息
    print("\n【步骤 3/7】配置Git用户信息")
    if not configure_git_user():
        return False
    
    # 步骤4: 添加文件
    print("\n【步骤 4/7】添加文件到暂存区")
    if not add_files():
        return False
    
    # 步骤5: 创建提交
    print("\n【步骤 5/7】创建初始提交")
    if not create_initial_commit():
        return False
    
    # 步骤6: 设置远程仓库
    print("\n【步骤 6/7】设置GitHub远程仓库")
    
    if check_remote_exists():
        print("⚠️  检测到远程仓库已配置")
        choice = input("是否重新配置远程仓库? (y/N): ").strip().lower()
        if choice == 'y':
            run_command("git remote remove origin", "移除现有远程仓库")
            if not setup_remote_repo():
                return False
    else:
        if not setup_remote_repo():
            return False
    
    # 步骤7: 推送到GitHub
    print("\n【步骤 7/7】推送到GitHub")
    
    print("\n⚠️  重要提示：")
    print("在推送之前，请确保：")
    print("1. 已在GitHub上创建了仓库: https://github.com/new")
    print("2. 已准备好Personal Access Token（如使用Token认证）")
    print("3. 已配置SSH密钥（如使用SSH认证）")
    
    choice = input("\n是否继续推送? (Y/n): ").strip().lower()
    if choice != 'n':
        if push_to_github():
            print("\n" + "=" * 60)
            print("🎉 恭喜！项目已成功发布到GitHub！")
            print("=" * 60)
            print("\n📍 下一步：")
            print("1. 访问你的GitHub仓库验证文件")
            print("2. 检查README.md显示效果")
            print("3. 确认Skill包目录完整")
            print("4. 分享仓库链接给团队成员")
            return True
    
    print("\n⏸️  发布已暂停，你可以稍后手动执行：")
    print("   git push -u origin main")
    return False

if __name__ == "__main__":
    try:
        main()
        input("\n按任意键退出...")
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
        sys.exit(1)
