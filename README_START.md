# 🚀 启动科创芯片ETF监控系统 - 快速指南

## 第1步：安装Python 3.7+

### 方法A：安装Python 3.11（推荐）
1. 访问 https://www.python.org/downloads/
2. 下载 **Python 3.11.x Windows installer** (64-bit)
3. 运行安装程序，**务必勾选**：
   - [x] Add Python to PATH
   - [x] Install for all users
4. 点击 "Install Now"
5. 安装完成后，**重启命令行窗口**

### 方法B：使用Microsoft Store安装（更简单）
1. 打开Microsoft Store
2. 搜索 "Python 3.11"
3. 点击获取并安装
4. 安装完成后即可使用

## 第2步：验证Python安装
打开新的命令行窗口，运行：
```cmd
python --version
```
应该显示：`Python 3.11.x`

## 第3步：启动系统

### 选项1：自动安装并启动（推荐）
双击运行 `start_easy.bat`，然后选择：
- **选项1**：启动Web监控界面
- **选项4**：先安装依赖包

### 选项2：手动命令启动
```cmd
# 1. 进入项目目录
cd c:\Users\INTEL3\WorkBuddy\Claw

# 2. 安装依赖包
python -m pip install pandas numpy yfinance ta streamlit plotly python-telegram-bot schedule python-dotenv requests tqdm --user

# 3. 启动Web界面
python -m streamlit run app.py
```

## 第4步：访问系统

### Web监控界面
- 启动后自动打开浏览器
- 访问地址：http://localhost:8501
- 功能：实时行情、技术图表、买卖信号

### 后台监控服务
```cmd
python monitor.py
```
- 自动监控价格变动
- 发送Telegram警报
- 日志文件：monitor.log

### 数据分析工具
```cmd
python analyzer.py
```
- 历史数据分析
- 技术指标回测
- 生成报告和图表

## 常见问题

### ❌ 错误：'python' 不是内部或外部命令
说明Python没有添加到PATH，请：
1. 重新安装Python，确保勾选 "Add Python to PATH"
2. 或手动添加Python安装目录到系统PATH

### ❌ 错误：ModuleNotFoundError
缺少依赖包，运行：
```cmd
python -m pip install 缺失的包名
```

### ❌ 错误：Python 2.x 版本
系统默认是Python 2，请：
1. 卸载Python 2（如果不需要）
2. 或使用 `python3` 命令
3. 或重新安装Python 3并确保在PATH中优先级更高

## 快速测试
运行以下命令测试环境：
```cmd
cd c:\Users\INTEL3\WorkBuddy\Claw
python test_env2.py
```

## 配置Telegram通知
1. 复制 `.env.example` 为 `.env`
2. 编辑 `.env` 文件，设置：
   - `TELEGRAM_BOT_TOKEN`：您的Telegram Bot令牌
   - `TELEGRAM_CHAT_ID`：您的Telegram聊天ID

## 技术支持
如果遇到问题：
1. 检查日志文件 `monitor.log`
2. 确保网络连接正常
3. Python版本 ≥ 3.7

---

**💡 提示**：建议先运行 `start_easy.bat` 选择选项4安装依赖包，然后选择选项1启动Web界面。