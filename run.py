#!/usr/bin/env python3
"""
科创芯片ETF (588200) 监控系统 - 启动脚本
"""

import sys
import os
import argparse

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'pandas',
        'numpy',
        'yfinance',
        'ta',
        'streamlit',
        'plotly',
        'python-telegram-bot',
        'schedule',
        'python-dotenv',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(missing_packages):
    """安装缺失的依赖包"""
    import subprocess
    
    print(f"正在安装缺失的依赖包: {', '.join(missing_packages)}")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ 依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def setup_environment():
    """设置环境"""
    print("🛠️  设置环境...")
    
    # 检查.env文件
    if not os.path.exists('.env'):
        print("⚠️  未找到.env文件，正在从.env.example创建...")
        
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ 已创建.env文件，请编辑该文件配置您的设置")
        else:
            print("❌ 未找到.env.example文件")
            return False
    
    # 检查数据缓存目录
    if not os.path.exists('data_cache'):
        os.makedirs('data_cache')
        print("✅ 已创建数据缓存目录")
    
    # 检查分析输出目录
    if not os.path.exists('analysis_output'):
        os.makedirs('analysis_output')
        print("✅ 已创建分析输出目录")
    
    return True

def show_menu():
    """显示主菜单"""
    print("\n" + "="*60)
    print("🚀 科创芯片ETF (588200) 实时监控系统")
    print("="*60)
    print("1. 启动Web监控界面")
    print("2. 启动后台监控服务")
    print("3. 运行数据分析工具")
    print("4. 检查系统状态")
    print("5. 安装/更新依赖包")
    print("6. 查看使用说明")
    print("0. 退出")
    print("="*60)

def run_web_interface():
    """运行Web界面"""
    print("🌐 正在启动Web监控界面...")
    
    try:
        import subprocess
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Web界面已关闭")
    except Exception as e:
        print(f"❌ 启动Web界面失败: {e}")

def run_monitor_service():
    """运行监控服务"""
    print("🔄 正在启动后台监控服务...")
    
    try:
        import monitor
        monitor.main()
    except KeyboardInterrupt:
        print("\n🛑 监控服务已关闭")
    except Exception as e:
        print(f"❌ 启动监控服务失败: {e}")

def run_analyzer():
    """运行数据分析工具"""
    print("📊 正在启动数据分析工具...")
    
    try:
        import analyzer
        analyzer.main()
    except KeyboardInterrupt:
        print("\n🛑 数据分析工具已关闭")
    except Exception as e:
        print(f"❌ 启动数据分析工具失败: {e}")

def check_system_status():
    """检查系统状态"""
    print("🔍 检查系统状态...")
    
    # 检查Python版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✅ Python版本: {python_version}")
    
    # 检查依赖包
    missing = check_dependencies()
    if missing:
        print(f"❌ 缺失依赖包: {', '.join(missing)}")
    else:
        print("✅ 所有依赖包已安装")
    
    # 检查环境文件
    if os.path.exists('.env'):
        print("✅ .env文件存在")
        
        # 读取配置
        try:
            from config import get_config_summary
            config = get_config_summary()
            print(f"✅ 配置加载成功")
            print(f"   监控股票: {config['stock_name']} ({config['stock_symbol']})")
            print(f"   监控间隔: {config['monitoring_interval']}秒")
            print(f"   警报阈值: {config['alert_threshold']}%")
        except Exception as e:
            print(f"⚠️  配置加载失败: {e}")
    else:
        print("❌ .env文件不存在")
    
    # 检查数据目录
    if os.path.exists('data_cache'):
        print("✅ 数据缓存目录存在")
        
        # 检查缓存文件数量
        cache_files = [f for f in os.listdir('data_cache') if f.endswith('.pkl')]
        print(f"   缓存文件数: {len(cache_files)}")
    else:
        print("❌ 数据缓存目录不存在")
    
    # 检查日志文件
    if os.path.exists('monitor.log'):
        file_size = os.path.getsize('monitor.log')
        print(f"✅ 监控日志文件存在 ({file_size:,} 字节)")
    else:
        print("⚠️  监控日志文件不存在")
    
    print("\n✅ 系统状态检查完成")

def show_instructions():
    """显示使用说明"""
    print("\n" + "="*60)
    print("📖 使用说明")
    print("="*60)
    print("\n1. 首次使用:")
    print("   a. 运行 'python run.py' 启动本程序")
    print("   b. 选择选项5安装依赖包")
    print("   c. 编辑 .env 文件配置Telegram通知等设置")
    print("   d. 选择选项4检查系统状态")
    
    print("\n2. 主要功能:")
    print("   a. Web监控界面 (选项1) - 实时图表和信号")
    print("   b. 后台监控服务 (选项2) - 自动监控和警报")
    print("   c. 数据分析工具 (选项3) - 历史数据分析和回测")
    
    print("\n3. 配置文件 (.env):")
    print("   - TELEGRAM_BOT_TOKEN: Telegram机器人令牌")
    print("   - TELEGRAM_CHAT_ID: Telegram聊天ID")
    print("   - MONITORING_INTERVAL: 监控间隔(秒)")
    print("   - ALERT_THRESHOLD: 价格警报阈值(%)")
    
    print("\n4. 数据文件:")
    print("   - data_cache/: 数据缓存目录")
    print("   - monitor.log: 监控日志文件")
    print("   - analysis_output/: 分析输出目录")
    
    print("\n5. 常用命令:")
    print("   - 直接启动Web界面: streamlit run app.py")
    print("   - 直接启动监控: python monitor.py")
    print("   - 直接运行分析: python analyzer.py")
    
    print("\n6. 注意事项:")
    print("   - 确保网络连接正常")
    print("   - 首次使用需要等待数据加载")
    print("   - 建议配置Telegram通知及时接收警报")
    
    print("\n7. 技术支持:")
    print("   - 查看项目README.md文件")
    print("   - 检查日志文件 monitor.log")
    print("   - 确保所有依赖包已正确安装")
    print("="*60)

def main():
    """主函数"""
    print("🔧 科创芯片ETF监控系统初始化...")
    
    # 检查工作目录
    if not os.path.exists('requirements.txt'):
        print("❌ 请在项目根目录运行此脚本")
        return
    
    # 设置环境
    if not setup_environment():
        print("❌ 环境设置失败")
        return
    
    # 主循环
    while True:
        show_menu()
        
        try:
            choice = input("\n请选择操作 (0-6): ").strip()
            
            if choice == '1':
                run_web_interface()
            elif choice == '2':
                run_monitor_service()
            elif choice == '3':
                run_analyzer()
            elif choice == '4':
                check_system_status()
            elif choice == '5':
                missing = check_dependencies()
                if missing:
                    install_dependencies(missing)
                else:
                    print("✅ 所有依赖包已安装")
            elif choice == '6':
                show_instructions()
            elif choice == '0':
                print("感谢使用，再见！")
                break
            else:
                print("❌ 无效选择，请重新输入")
        
        except KeyboardInterrupt:
            print("\n\n🛑 程序被用户中断")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser(description='科创芯片ETF监控系统')
    parser.add_argument('--web', action='store_true', help='直接启动Web界面')
    parser.add_argument('--monitor', action='store_true', help='直接启动监控服务')
    parser.add_argument('--analyze', action='store_true', help='直接运行数据分析')
    parser.add_argument('--check', action='store_true', help='检查系统状态')
    parser.add_argument('--install', action='store_true', help='安装依赖包')
    
    args = parser.parse_args()
    
    if args.web:
        run_web_interface()
    elif args.monitor:
        run_monitor_service()
    elif args.analyze:
        run_analyzer()
    elif args.check:
        check_system_status()
    elif args.install:
        missing = check_dependencies()
        if missing:
            install_dependencies(missing)
        else:
            print("✅ 所有依赖包已安装")
    else:
        main()