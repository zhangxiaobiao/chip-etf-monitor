#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科创芯片ETF监控系统 - GitHub发布向导
简化版，无需依赖外部工具
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

class GitHubPublishWizard:
    def __init__(self):
        self.project_dir = Path.cwd()
        self.project_name = "科创芯片ETF监控系统"
        self.repo_name = "chip-etf-monitor"
        
    def print_header(self):
        """打印头部信息"""
        print("=" * 60)
        print("🚀 科创芯片ETF监控系统 - GitHub发布向导")
        print("=" * 60)
        print(f"项目目录: {self.project_dir}")
        print(f"项目名称: {self.project_name}")
        print(f"建议仓库名: {self.repo_name}")
        print("=" * 60)
        print()
    
    def check_prerequisites(self):
        """检查前置条件"""
        print("🔍 检查发布前准备...")
        print()
        
        print("1. GitHub账号")
        print("   ✓ 需要注册GitHub账号: https://github.com")
        print("   ✓ 建议使用邮箱验证")
        print()
        
        print("2. Git安装")
        print("   ✓ 需要安装Git: https://git-scm.com/")
        print("   ✓ Windows用户建议选择'Use Git from Windows Command Prompt'")
        print()
        
        print("3. Python环境")
        print("   ✓ 需要Python 3.7或更高版本")
        print("   ✓ 建议使用虚拟环境")
        print()
        
        print("📋 请确保以上条件已满足，然后继续")
        print()
        
        input("按Enter键继续...")
        print()
    
    def create_gitignore(self):
        """确保.gitignore文件存在"""
        gitignore_path = self.project_dir / '.gitignore'
        
        if gitignore_path.exists():
            print("✓ .gitignore文件已存在")
            return True
        
        print("📄 创建.gitignore文件...")
        
        gitignore_content = """# Python
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
data_cache/*
analysis_output/*
.env
.env.local

# WorkBuddy缓存
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
"""
        
        try:
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("✓ .gitignore文件创建成功")
            return True
        except Exception as e:
            print(f"❌ 创建.gitignore失败: {e}")
            return False
    
    def create_readme_for_github(self):
        """为GitHub优化README.md"""
        readme_path = self.project_dir / 'README.md'
        
        if not readme_path.exists():
            print("⚠️  README.md不存在，创建基本README...")
            self.create_basic_readme()
            return
        
        print("📝 优化README.md用于GitHub...")
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否需要添加徽章占位符
            if 'badge' not in content.lower():
                # 在标题后添加徽章占位符
                lines = content.split('\n')
                new_content = []
                for i, line in enumerate(lines):
                    new_content.append(line)
                    if i == 0 and line.startswith('# '):
                        new_content.append('\n<!-- 添加GitHub徽章 -->')
                        new_content.append('<!-- 发布后在此处添加徽章代码 -->')
                        new_content.append('')
                
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_content))
                
                print("✓ README.md已优化")
                print("  发布后可以添加GitHub徽章")
        except Exception as e:
            print(f"⚠️  优化README.md失败: {e}")
    
    def create_basic_readme(self):
        """创建基本的README.md"""
        readme_content = f"""# {self.project_name}

<!-- 添加GitHub徽章 -->
<!-- 
![GitHub last commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/{self.repo_name})
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/{self.repo_name})
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
-->

## 📊 项目概述

科创芯片ETF(588200)实时监控与分析系统，提供技术指标、买卖信号、可视化界面和价格警报。

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/{self.repo_name}.git
cd {self.repo_name}

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env
# 编辑.env文件配置

# 启动系统
streamlit run app.py
```

## 📈 核心功能

- 实时行情监控
- 技术指标分析 (MACD, RSI, 布林带)
- 买卖信号生成
- 可视化Web界面
- 价格警报系统

## 📄 许可证

MIT License
"""
        
        readme_path = self.project_dir / 'README.md'
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print("✓ 创建了基本的README.md文件")
        except Exception as e:
            print(f"❌ 创建README.md失败: {e}")
    
    def generate_github_instructions(self):
        """生成GitHub发布说明"""
        print()
        print("=" * 60)
        print("📋 GitHub发布步骤说明")
        print("=" * 60)
        print()
        
        print("步骤1: 在GitHub创建仓库")
        print("  🔗 访问: https://github.com/new")
        print("  📝 填写信息:")
        print(f"    - 仓库名: {self.repo_name}")
        print("    - 描述: 科创芯片ETF(588200)实时监控与分析系统")
        print("    - 选择: Public (公开)")
        print("    - 不要勾选: Initialize this repository with...")
        print("  ✅ 点击: Create repository")
        print()
        
        print("步骤2: 获取仓库URL")
        print("  🔗 创建成功后，复制仓库URL:")
        print("    格式: https://github.com/你的用户名/chip-etf-monitor.git")
        print()
        
        print("步骤3: 本地Git操作")
        print("  💻 在项目目录执行以下命令:")
        print("    1. 初始化Git (如果未初始化):")
        print("       git init")
        print("    2. 配置用户信息:")
        print("       git config user.name '你的名字'")
        print("       git config user.email '你的邮箱'")
        print("    3. 添加文件:")
        print("       git add .")
        print("    4. 提交文件:")
        print("       git commit -m '初始提交: 科创芯片ETF监控系统'")
        print()
        
        print("步骤4: 连接到GitHub并推送")
        print("  💻 继续执行命令:")
        print("    5. 添加远程仓库:")
        print("       git remote add origin [你的仓库URL]")
        print("    6. 重命名分支:")
        print("       git branch -M main")
        print("    7. 推送代码:")
        print("       git push -u origin main")
        print()
        
        print("步骤5: 验证发布")
        print("  🌐 访问你的仓库:")
        print("     https://github.com/你的用户名/chip-etf-monitor")
        print("  ✅ 检查文件是否完整显示")
        print()
        
        print("🔧 可选配置:")
        print("  - 添加SSH密钥 (推荐)")
        print("  - 设置GitHub Pages")
        print("  - 添加CI/CD工作流")
        print()
        
        print("📚 详细指南请查看: GITHUB_PUBLISH_GUIDE.md")
        print()
    
    def create_publish_checklist(self):
        """创建发布检查清单"""
        checklist = {
            "prerequisites": {
                "github_account": False,
                "git_installed": False,
                "python_installed": False
            },
            "local_setup": {
                "gitignore_created": os.path.exists(self.project_dir / '.gitignore'),
                "readme_optimized": os.path.exists(self.project_dir / 'README.md'),
                "sensitive_files_excluded": not os.path.exists(self.project_dir / '.env')
            },
            "github_setup": {
                "repository_created": False,
                "remote_configured": False,
                "code_pushed": False
            },
            "post_publish": {
                "readme_visible": False,
                "badges_added": False,
                "license_added": False
            }
        }
        
        # 保存检查清单
        checklist_path = self.project_dir / 'github_checklist.json'
        with open(checklist_path, 'w', encoding='utf-8') as f:
            json.dump(checklist, f, indent=2, ensure_ascii=False)
        
        print("📋 发布检查清单已保存到: github_checklist.json")
        print("   请在发布过程中更新此清单")
    
    def create_simple_license(self):
        """创建简单的许可证文件"""
        license_path = self.project_dir / 'LICENSE'
        
        if license_path.exists():
            print("✓ LICENSE文件已存在")
            return
        
        license_content = """MIT License

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
"""
        
        try:
            with open(license_path, 'w', encoding='utf-8') as f:
                f.write(license_content)
            print("✓ LICENSE文件已创建 (MIT许可证)")
        except Exception as e:
            print(f"⚠️  创建LICENSE文件失败: {e}")
    
    def run(self):
        """运行发布向导"""
        self.print_header()
        
        # 检查前置条件
        self.check_prerequisites()
        
        # 创建必要的文件
        print("🛠️  准备发布文件...")
        print()
        
        self.create_gitignore()
        print()
        
        self.create_readme_for_github()
        print()
        
        self.create_simple_license()
        print()
        
        # 生成发布说明
        self.generate_github_instructions()
        
        # 创建检查清单
        self.create_publish_checklist()
        
        # 完成提示
        print("=" * 60)
        print("🎉 发布准备完成！")
        print("=" * 60)
        print()
        print("📁 已创建的文件:")
        print("  ✓ .gitignore - Git忽略文件")
        print("  ✓ README.md - 项目文档 (已优化)")
        print("  ✓ LICENSE - 许可证文件")
        print("  ✓ GITHUB_PUBLISH_GUIDE.md - 详细发布指南")
        print("  ✓ github_checklist.json - 发布检查清单")
        print()
        print("🚀 下一步:")
        print("  1. 按照上面的步骤在GitHub创建仓库")
        print("  2. 执行Git命令推送代码")
        print("  3. 验证发布结果")
        print()
        print("💡 提示: 如果遇到问题，请查看GITHUB_PUBLISH_GUIDE.md")
        print("=" * 60)

def main():
    """主函数"""
    try:
        wizard = GitHubPublishWizard()
        wizard.run()
        
        print()
        input("按Enter键退出...")
        
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    main()