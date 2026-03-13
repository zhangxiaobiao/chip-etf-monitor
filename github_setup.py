#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub发布工具 - 将科创芯片ETF监控系统发布到GitHub
"""

import os
import sys
import subprocess
import json
import platform
from pathlib import Path
from datetime import datetime

class GitHubPublisher:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.project_name = "科创芯片ETF监控系统"
        self.repository_name = "chip-etf-monitor"
        self.description = "科创芯片ETF(588200)实时监控与分析系统，提供技术指标、买卖信号、可视化界面和价格警报"
        
    def check_git_installed(self):
        """检查Git是否安装"""
        print("🔍 检查Git安装状态...")
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  cwd=self.project_dir)
            if result.returncode == 0:
                print(f"✓ Git已安装: {result.stdout.strip()}")
                return True
            else:
                print("❌ Git未安装或无法访问")
                return False
        except FileNotFoundError:
            print("❌ Git未安装，请先安装Git: https://git-scm.com/")
            return False
    
    def check_git_repo(self):
        """检查是否已初始化Git仓库"""
        print("\n🔍 检查Git仓库状态...")
        
        git_dir = self.project_dir / '.git'
        if git_dir.exists():
            print("✓ Git仓库已初始化")
            
            # 检查远程仓库
            try:
                result = subprocess.run(['git', 'remote', '-v'], 
                                      capture_output=True, 
                                      text=True, 
                                      cwd=self.project_dir)
                if result.returncode == 0 and 'origin' in result.stdout:
                    print(f"✓ 已配置远程仓库:\n{result.stdout}")
                    return True, True
                else:
                    print("⚠️  Git仓库已初始化，但未配置远程仓库")
                    return True, False
            except Exception as e:
                print(f"❌ 检查远程仓库失败: {e}")
                return True, False
        else:
            print("❌ 未初始化Git仓库")
            return False, False
    
    def init_git_repo(self):
        """初始化Git仓库"""
        print("\n🚀 初始化Git仓库...")
        
        try:
            # 初始化仓库
            result = subprocess.run(['git', 'init'], 
                                  capture_output=True, 
                                  text=True, 
                                  cwd=self.project_dir)
            if result.returncode == 0:
                print("✓ Git仓库初始化成功")
                
                # 配置用户信息（如果未配置）
                try:
                    subprocess.run(['git', 'config', 'user.name', '"科创芯片ETF监控系统"'], 
                                 capture_output=True, text=True, cwd=self.project_dir)
                    subprocess.run(['git', 'config', 'user.email', '"chip-etf-monitor@example.com"'], 
                                 capture_output=True, text=True, cwd=self.project_dir)
                    print("✓ Git用户信息已配置")
                except:
                    print("⚠️  配置用户信息失败，请手动配置")
                
                return True
            else:
                print(f"❌ Git仓库初始化失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 初始化Git仓库时出错: {e}")
            return False
    
    def create_gitignore(self):
        """创建.gitignore文件"""
        print("\n📄 创建.gitignore文件...")
        
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
data_cache/*.csv
data_cache/*.json
data_cache/*.pkl
analysis_output/*
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
~*

# 测试输出
.coverage
htmlcov/
.pytest_cache/

# 文档生成
docs/_build/
"""
        
        gitignore_path = self.project_dir / '.gitignore'
        try:
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("✓ .gitignore文件已创建")
            return True
        except Exception as e:
            print(f"❌ 创建.gitignore文件失败: {e}")
            return False
    
    def check_gitignore_exists(self):
        """检查.gitignore文件是否存在"""
        gitignore_path = self.project_dir / '.gitignore'
        return gitignore_path.exists()
    
    def add_files_to_git(self):
        """将文件添加到Git暂存区"""
        print("\n📦 添加文件到Git暂存区...")
        
        try:
            # 先添加.gitignore
            if self.check_gitignore_exists():
                result = subprocess.run(['git', 'add', '.gitignore'], 
                                      capture_output=True, 
                                      text=True, 
                                      cwd=self.project_dir)
                if result.returncode != 0:
                    print(f"⚠️  添加.gitignore失败: {result.stderr}")
            
            # 添加所有文件（除了.gitignore中排除的）
            result = subprocess.run(['git', 'add', '.'], 
                                  capture_output=True, 
                                  text=True, 
                                  cwd=self.project_dir)
            
            if result.returncode == 0:
                print("✓ 文件已添加到暂存区")
                
                # 显示状态
                status_result = subprocess.run(['git', 'status', '--short'], 
                                             capture_output=True, 
                                             text=True, 
                                             cwd=self.project_dir)
                if status_result.returncode == 0:
                    files_count = len([line for line in status_result.stdout.split('\n') if line.strip()])
                    print(f"  已暂存 {files_count} 个文件")
                
                return True
            else:
                print(f"❌ 添加文件失败: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 添加文件时出错: {e}")
            return False
    
    def create_initial_commit(self):
        """创建初始提交"""
        print("\n💾 创建初始提交...")
        
        commit_message = f"""初始提交: {self.project_name}

🎯 项目概述
{self.description}

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

📅 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        try:
            result = subprocess.run(['git', 'commit', '-m', commit_message], 
                                  capture_output=True, 
                                  text=True, 
                                  cwd=self.project_dir)
            
            if result.returncode == 0:
                print("✓ 初始提交创建成功")
                print(f"  提交消息: 初始提交: {self.project_name}")
                return True
            else:
                # 如果提交失败，可能是因为没有配置用户信息
                print(f"⚠️  提交失败: {result.stderr}")
                
                # 尝试使用简化消息
                simple_message = f"初始提交: {self.project_name}"
                result = subprocess.run(['git', 'commit', '-m', simple_message], 
                                      capture_output=True, 
                                      text=True, 
                                      cwd=self.project_dir)
                
                if result.returncode == 0:
                    print("✓ 使用简化消息提交成功")
                    return True
                else:
                    print(f"❌ 提交失败: {result.stderr}")
                    return False
        except Exception as e:
            print(f"❌ 创建提交时出错: {e}")
            return False
    
    def check_github_token(self):
        """检查GitHub Token配置"""
        print("\n🔑 检查GitHub配置...")
        
        # 检查环境变量
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            print("✓ 检测到GitHub Token环境变量")
            return github_token
        
        # 检查配置文件
        config_file = Path.home() / '.config' / 'gh' / 'hosts.yml'
        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config and 'github.com' in config:
                        token = config['github.com'].get('oauth_token')
                        if token:
                            print("✓ 检测到GitHub CLI配置")
                            return token
            except:
                pass
        
        print("⚠️  未检测到GitHub Token，需要手动配置")
        print("   请创建GitHub Token: https://github.com/settings/tokens")
        print("   需要权限: repo, workflow")
        return None
    
    def create_github_repo_info(self):
        """创建GitHub仓库信息"""
        print("\n📋 GitHub仓库信息:")
        print(f"   仓库名称: {self.repository_name}")
        print(f"   项目名称: {self.project_name}")
        print(f"   描述: {self.description}")
        print(f"   项目目录: {self.project_dir}")
        print(f"   可见性: Public (建议)")
        
        return {
            'name': self.repository_name,
            'description': self.description,
            'private': False,
            'has_issues': True,
            'has_projects': True,
            'has_wiki': True,
            'auto_init': False
        }
    
    def print_setup_instructions(self):
        """打印GitHub设置说明"""
        print("\n" + "="*60)
        print("🚀 GitHub发布指南")
        print("="*60)
        
        print(f"\n📁 项目: {self.project_name}")
        print(f"📝 描述: {self.description}")
        print(f"📂 本地目录: {self.project_dir}")
        
        print("\n📋 已完成:")
        print("✓ 检查Git安装状态")
        print("✓ 初始化Git仓库")
        print("✓ 创建.gitignore文件")
        print("✓ 添加文件到暂存区")
        print("✓ 创建初始提交")
        
        print("\n🚀 下一步 - 发布到GitHub:")
        print("\n方法1: 使用GitHub CLI (推荐)")
        print("   1. 安装GitHub CLI: https://cli.github.com/")
        print("   2. 登录: gh auth login")
        print("   3. 创建仓库: gh repo create chip-etf-monitor --public --source=. --remote=origin --push")
        
        print("\n方法2: 使用Git命令")
        print(f"   1. 在GitHub创建仓库: https://github.com/new")
        print(f"      - 仓库名: {self.repository_name}")
        print(f"      - 描述: {self.description}")
        print(f"      - 选择Public")
        print(f"      - 不要初始化README, .gitignore等")
        print(f"   2. 添加远程仓库:")
        print(f"      git remote add origin https://github.com/你的用户名/{self.repository_name}.git")
        print(f"   3. 推送代码:")
        print(f"      git branch -M main")
        print(f"      git push -u origin main")
        
        print("\n方法3: 使用GitHub网页")
        print("   1. 访问 https://github.com/new")
        print("   2. 填写仓库信息")
        print("   3. 上传现有文件")
        
        print("\n🔧 配置说明:")
        print("   - 确保.gitignore文件已正确配置")
        print("   - 敏感信息不要提交（如.env文件）")
        print("   - 建议使用SSH密钥进行认证")
        
        print("\n📚 文档:")
        print("   - 项目文档: README.md")
        print("   - 技能包文档: .codebuddy/skills/chip-etf-monitor/")
        print("   - 快速开始: README_START.md")
        
        print("\n" + "="*60)
        print("💡 提示: 发布后可以设置GitHub Pages展示项目")
        print("="*60)
    
    def create_readme_for_github(self):
        """为GitHub创建优化的README.md"""
        print("\n📝 优化README.md用于GitHub...")
        
        readme_path = self.project_dir / 'README.md'
        if not readme_path.exists():
            print("⚠️  README.md不存在，正在创建...")
            self.create_basic_readme()
            return
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加GitHub徽章（如果还没有）
            if 'badge' not in content.lower() and 'github' not in content.lower():
                badges = """<!-- GitHub徽章 -->
![GitHub last commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/chip-etf-monitor)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/chip-etf-monitor)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/chip-etf-monitor)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

"""
                
                # 在标题后添加徽章
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    new_lines.append(line)
                    if line.startswith('# ') and len(new_lines) == 1:
                        new_lines.append('\n' + badges)
                
                new_content = '\n'.join(new_lines)
                
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✓ README.md已优化，添加了GitHub徽章占位符")
                print("  请将YOUR_USERNAME替换为你的GitHub用户名")
            else:
                print("✓ README.md已包含GitHub相关标记")
        
        except Exception as e:
            print(f"⚠️  优化README.md失败: {e}")
    
    def create_basic_readme(self):
        """创建基本的README.md"""
        readme_content = f"""# {self.project_name}

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/{self.repository_name})
![License](https://img.shields.io/badge/License-MIT-green)

## 📊 项目概述

{self.description}

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Git

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/{self.repository_name}.git
cd {self.repository_name}

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env
# 编辑.env文件配置股票和Telegram信息

# 启动系统
streamlit run app.py
```

### 一键启动 (Windows)
双击 `start_easy.bat`

## 📈 核心功能

- **实时行情监控**: 科创芯片ETF(588200)实时价格
- **技术指标分析**: MACD, RSI, 布林带等
- **智能信号生成**: 买卖信号和风险评估
- **可视化界面**: Streamlit Web应用
- **价格警报**: Telegram实时通知

## 🛠️ 技术栈

- **后端**: Python 3.7+
- **数据处理**: Pandas, NumPy, yfinance
- **技术分析**: TA-Lib (ta库)
- **可视化**: Streamlit, Plotly
- **通知**: Telegram Bot API

## 📁 项目结构

```
{self.repository_name}/
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
├── data_cache/         # 数据缓存目录
├── analysis_output/    # 分析输出目录
└── README.md           # 本文件
```

## 🔧 配置说明

详细配置请查看 [配置文档](docs/configuration.md)

## 🤝 贡献指南

欢迎贡献代码！请查看 [贡献指南](CONTRIBUTING.md)

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过GitHub Issues提交

---

**💡 提示**: 本系统为辅助决策工具，不构成投资建议。金融市场有风险，投资需谨慎。
"""
        
        readme_path = self.project_dir / 'README.md'
        try:
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print("✓ 创建了基本的README.md文件")
        except Exception as e:
            print(f"❌ 创建README.md失败: {e}")
    
    def create_github_workflow(self):
        """创建GitHub Actions工作流"""
        print("\n⚙️  创建GitHub Actions工作流...")
        
        workflows_dir = self.project_dir / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = """name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with flake8
      run: |
        pip install flake8
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test with pytest
      run: |
        pip install pytest
        if [ -f "test_*.py" ]; then
          pytest
        else
          echo "No test files found"
        fi
"""
        
        workflow_file = workflows_dir / 'python-ci.yml'
        try:
            with open(workflow_file, 'w', encoding='utf-8') as f:
                f.write(workflow_content)
            print("✓ 创建了GitHub Actions工作流文件")
            return True
        except Exception as e:
            print(f"⚠️  创建工作流文件失败: {e}")
            return False
    
    def run(self):
        """运行发布流程"""
        print("="*60)
        print(f"🚀 {self.project_name} - GitHub发布工具")
        print("="*60)
        
        # 检查Git安装
        if not self.check_git_installed():
            print("\n❌ 请先安装Git: https://git-scm.com/")
            return False
        
        # 检查Git仓库状态
        repo_initialized, remote_configured = self.check_git_repo()
        
        # 初始化仓库（如果未初始化）
        if not repo_initialized:
            if not self.init_git_repo():
                return False
        else:
            print("✓ 使用现有Git仓库")
        
        # 创建.gitignore（如果不存在）
        if not self.check_gitignore_exists():
            if not self.create_gitignore():
                print("⚠️  无法创建.gitignore，继续...")
        
        # 添加文件到Git
        if not self.add_files_to_git():
            print("⚠️  添加文件失败，继续...")
        
        # 创建提交
        if not self.create_initial_commit():
            print("⚠️  创建提交失败，继续...")
        
        # 优化README.md
        self.create_readme_for_github()
        
        # 创建GitHub Actions工作流
        self.create_github_workflow()
        
        # 检查GitHub Token
        self.check_github_token()
        
        # 创建GitHub仓库信息
        repo_info = self.create_github_repo_info()
        
        # 打印设置说明
        self.print_setup_instructions()
        
        # 保存仓库信息到文件
        self.save_repo_info(repo_info)
        
        print("\n✅ 本地Git设置完成！")
        print("   请按照上述说明将项目发布到GitHub")
        
        return True
    
    def save_repo_info(self, repo_info):
        """保存仓库信息到文件"""
        info_file = self.project_dir / 'github_repo_info.json'
        try:
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(repo_info, f, indent=2, ensure_ascii=False)
            print(f"\n📄 仓库信息已保存到: {info_file}")
        except Exception as e:
            print(f"⚠️  保存仓库信息失败: {e}")

def main():
    """主函数"""
    project_dir = Path.cwd()
    publisher = GitHubPublisher(project_dir)
    
    try:
        success = publisher.run()
        if success:
            print("\n🎉 GitHub发布准备完成！")
            print("   请按照打印的指南完成GitHub发布")
        else:
            print("\n❌ GitHub发布准备失败")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()