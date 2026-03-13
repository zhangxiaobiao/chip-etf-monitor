#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
技能包测试脚本
验证股票监控技能包的功能完整性
"""

import os
import sys
import subprocess
from pathlib import Path

def test_skill_structure():
    """测试技能包结构完整性"""
    print("🔍 测试技能包结构...")
    
    skill_dir = Path(__file__).parent.parent
    required_files = [
        'SKILL.md',
        'scripts/create_monitor_project.py',
        'references/technical_indicators.md',
        'references/api_reference.md',
        'assets/project-structure.txt'
    ]
    
    missing_files = []
    for file in required_files:
        file_path = skill_dir / file
        if not file_path.exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少文件: {missing_files}")
        return False
    
    print("✅ 技能包结构完整")
    return True

def test_python_environment():
    """测试Python环境"""
    print("\n🔍 测试Python环境...")
    
    try:
        # 检查Python版本
        result = subprocess.run(
            [sys.executable, '--version'],
            capture_output=True,
            text=True
        )
        print(f"✅ Python版本: {result.stdout.strip()}")
        
        # 检查必要依赖
        required_packages = ['pandas', 'numpy', 'yfinance', 'streamlit', 'plotly']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✓ {package} 已安装")
            except ImportError:
                missing_packages.append(package)
                print(f"  ✗ {package} 未安装")
        
        if missing_packages:
            print(f"⚠️  缺少依赖包: {missing_packages}")
            print("   运行: pip install " + " ".join(missing_packages))
            return False
        
        print("✅ Python环境正常")
        return True
        
    except Exception as e:
        print(f"❌ Python环境测试失败: {e}")
        return False

def test_project_creation():
    """测试项目创建功能"""
    print("\n🔍 测试项目创建功能...")
    
    try:
        # 导入项目创建脚本
        skill_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(skill_dir / 'scripts'))
        
        from create_monitor_project import create_project
        
        # 创建测试项目
        test_project_dir = Path.cwd() / "test_monitor_project"
        
        # 如果目录已存在，先删除
        if test_project_dir.exists():
            import shutil
            shutil.rmtree(test_project_dir)
        
        # 创建项目
        success = create_project(
            str(test_project_dir),
            "588200.SS",
            "科创芯片ETF"
        )
        
        if success:
            # 检查创建的文件
            required_project_files = [
                'config.py',
                'requirements.txt',
                '.env.example',
                'README.md',
                'start_project.bat'
            ]
            
            missing_files = []
            for file in required_project_files:
                if not (test_project_dir / file).exists():
                    missing_files.append(file)
            
            if missing_files:
                print(f"❌ 项目创建不完整，缺少文件: {missing_files}")
                return False
            
            print("✅ 项目创建功能正常")
            
            # 清理测试项目
            import shutil
            shutil.rmtree(test_project_dir)
            print("✅ 测试项目清理完成")
            
            return True
        else:
            print("❌ 项目创建失败")
            return False
            
    except Exception as e:
        print(f"❌ 项目创建测试失败: {e}")
        return False

def test_documentation():
    """测试文档完整性"""
    print("\n🔍 测试文档完整性...")
    
    try:
        skill_dir = Path(__file__).parent.parent
        
        # 检查SKILL.md
        skill_md = skill_dir / 'SKILL.md'
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            'name:',
            'description:',
            '使用场景',
            '核心功能',
            '使用方法'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ SKILL.md缺少部分: {missing_sections}")
            return False
        
        print("✅ 文档完整性检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 文档测试失败: {e}")
        return False

def test_references():
    """测试参考资料"""
    print("\n🔍 测试参考资料...")
    
    try:
        skill_dir = Path(__file__).parent.parent
        
        # 检查技术指标文档
        tech_file = skill_dir / 'references' / 'technical_indicators.md'
        if not tech_file.exists():
            print("❌ 缺少技术指标文档")
            return False
        
        with open(tech_file, 'r', encoding='utf-8') as f:
            tech_content = f.read()
        
        tech_sections = ['MACD', 'RSI', '布林带', '移动平均线']
        missing_tech = []
        for section in tech_sections:
            if section not in tech_content:
                missing_tech.append(section)
        
        if missing_tech:
            print(f"⚠️  技术指标文档不完整: {missing_tech}")
        
        # 检查API文档
        api_file = skill_dir / 'references' / 'api_reference.md'
        if not api_file.exists():
            print("❌ 缺少API文档")
            return False
        
        print("✅ 参考资料检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 参考资料测试失败: {e}")
        return False

def test_assets():
    """测试资产文件"""
    print("\n🔍 测试资产文件...")
    
    try:
        skill_dir = Path(__file__).parent.parent
        
        # 检查项目结构文档
        struct_file = skill_dir / 'assets' / 'project-structure.txt'
        if not struct_file.exists():
            print("❌ 缺少项目结构文档")
            return False
        
        # 检查项目模板生成器
        template_file = skill_dir / 'assets' / 'complete_project_template.py'
        if not template_file.exists():
            print("❌ 缺少完整项目模板")
            return False
        
        print("✅ 资产文件检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 资产文件测试失败: {e}")
        return False

def generate_test_report():
    """生成测试报告"""
    print("\n" + "="*60)
    print("📋 技能包测试报告")
    print("="*60)
    
    tests = [
        ("技能包结构", test_skill_structure),
        ("Python环境", test_python_environment),
        ("项目创建", test_project_creation),
        ("文档完整性", test_documentation),
        ("参考资料", test_references),
        ("资产文件", test_assets)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success, ""))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    # 显示结果
    print("\n测试结果:")
    print("-" * 40)
    
    all_passed = True
    for test_name, success, error in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status} {test_name}")
        if error:
            print(f"   错误: {error}")
        if not success:
            all_passed = False
    
    print("-" * 40)
    
    if all_passed:
        print("🎉 所有测试通过！技能包准备就绪。")
    else:
        print("⚠️  部分测试失败，请修复问题。")
    
    # 生成使用建议
    print("\n💡 使用建议:")
    print("1. 技能包路径: .codebuddy/skills/stock-monitor/")
    print("2. 创建新项目:")
    print("   python scripts/create_monitor_project.py")
    print("3. 查看文档:")
    print("   SKILL.md - 核心文档")
    print("   references/ - 参考资料")
    print("   assets/ - 项目模板")
    
    return all_passed

def main():
    """主函数"""
    print("="*60)
    print("   股票监控技能包 - 功能测试")
    print("="*60)
    
    # 运行测试
    success = generate_test_report()
    
    # 退出状态
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()