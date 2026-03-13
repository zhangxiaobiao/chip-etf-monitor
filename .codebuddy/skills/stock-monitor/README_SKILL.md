# 📊 股票监控技能包

## 概述

**stock-monitor** 技能包是一个用于快速创建专业股票和ETF实时监控系统的完整解决方案。该技能包提供了从数据获取、技术分析、信号生成到可视化界面和通知系统的全套工具。

## 功能特性

### 🚀 核心功能
- **实时行情监控**: 支持多数据源实时数据获取
- **技术指标分析**: MACD、RSI、布林带、移动平均线等
- **智能信号生成**: 多指标综合判断，提供买卖信号
- **可视化界面**: Streamlit Web应用，Plotly交互图表
- **价格警报**: Telegram通知，自定义阈值
- **数据分析**: 历史数据回测，报告生成

### 🛠️ 技术栈
- **后端**: Python 3.7+
- **数据处理**: Pandas, NumPy, yfinance
- **技术指标**: TA-Lib (ta库)
- **可视化**: Streamlit, Plotly
- **通知**: Telegram Bot API
- **任务调度**: schedule

## 快速开始

### 1. 使用技能包创建项目

```bash
# 进入技能包目录
cd .codebuddy/skills/stock-monitor

# 使用项目创建脚本
python scripts/create_monitor_project.py
```

### 2. 手动创建项目结构

技能包提供完整的项目模板：
- **SKILL.md**: 核心使用文档
- **scripts/**: 核心Python脚本
- **references/**: 技术文档和API参考
- **assets/**: 项目模板和示例

## 项目结构

```
stock-monitor-project/
├── app.py                 # Streamlit Web界面
├── monitor.py             # 后台监控服务
├── analyzer.py            # 数据分析工具
├── config.py              # 配置文件
├── data_fetcher.py        # 数据获取模块
├── signals.py             # 信号生成模块
├── utils.py               # 工具函数
├── requirements.txt       # Python依赖
├── .env.example           # 环境变量模板
├── README.md              # 项目文档
├── start_project.bat      # Windows启动脚本
├── data_cache/            # 数据缓存目录
└── analysis_output/       # 分析输出目录
```

## 配置说明

### 基础配置
编辑 `config.py` 或 `.env` 文件：

```python
# 股票配置
STOCK_SYMBOL = "588200.SS"  # 股票代码
STOCK_NAME = "科创芯片ETF"   # 股票名称

# 监控配置
MONITORING_INTERVAL = 60     # 监控间隔(秒)
ALERT_THRESHOLD = 2.0        # 价格警报阈值(%)

# 技术指标配置
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_SIGNAL = 9
MACD_FAST = 12
MACD_SLOW = 26
```

### Telegram通知配置
1. 创建Telegram Bot (@BotFather)
2. 获取Bot Token和Chat ID
3. 在 `.env` 文件中配置：
```bash
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## 使用示例

### 创建科创芯片ETF监控系统
```bash
# 运行项目创建向导
python scripts/create_monitor_project.py

# 输入项目信息
项目名称: chip-monitor
股票代码: 588200.SS
股票名称: 科创芯片ETF

# 安装依赖
cd chip-monitor
pip install -r requirements.txt

# 启动系统
streamlit run app.py
```

### 监控其他股票
修改 `config.py` 中的配置：
```python
STOCK_SYMBOL = "000001.SZ"  # 平安银行
STOCK_NAME = "平安银行"
```

## 技术文档

### 核心模块说明

#### 1. DataFetcher (数据获取)
- 实时行情数据获取
- 历史数据下载和缓存
- 多数据源支持
- 错误处理和降级

#### 2. SignalGenerator (信号生成)
- 多种技术指标计算
- 综合信号评分机制
- 风险等级评估
- 投资建议生成

#### 3. NotificationManager (通知管理)
- Telegram消息发送
- 价格变动警报
- 买卖信号通知
- 系统状态报告

### 技术指标
- **MACD**: 趋势跟踪指标
- **RSI**: 超买超卖指标
- **布林带**: 波动性指标
- **移动平均线**: 趋势判断指标

## 扩展功能

### 添加新的数据源
1. 在 `data_fetcher.py` 中添加新的数据源类
2. 实现相同接口方法
3. 在配置中添加切换选项

### 添加新的技术指标
1. 在 `signals.py` 中添加指标计算方法
2. 在 `generate_signals` 中集成新指标
3. 在配置中添加参数设置

### 多股票监控
1. 修改数据获取模块支持多股票
2. 在界面中添加股票切换功能
3. 调整信号生成逻辑

## 故障排除

### 常见问题

#### 1. 数据获取失败
- 检查网络连接
- 验证股票代码格式
- 查看数据源API状态

#### 2. 依赖包安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用用户安装
python -m pip install -r requirements.txt --user

# 单独安装问题包
python -m pip install yfinance --user
```

#### 3. Streamlit启动失败
- 检查端口8501是否被占用
- 确保Streamlit正确安装
- 查看浏览器控制台错误

### 日志文件
- **monitor.log**: 后台监控日志
- **data_cache/**: 数据缓存文件
- **analysis_output/**: 分析输出文件

## 最佳实践

### 1. 配置管理
- 使用环境变量存储敏感信息
- 配置文件与代码分离
- 提供配置示例文件

### 2. 错误处理
- 为API调用添加重试机制
- 实现数据降级方案
- 详细日志记录

### 3. 性能优化
- 使用数据缓存减少API调用
- 合理设置监控频率
- 及时清理历史数据

### 4. 安全考虑
- 不要硬编码API密钥
- 验证用户输入数据
- 限制敏感信息输出

## 测试验证

### 运行技能包测试
```bash
python scripts/test_skill.py
```

### 测试项目创建
```bash
# 创建测试项目
python scripts/create_monitor_project.py

# 验证项目文件
cd test_project
python -m pytest tests/
```

### 功能测试
1. 数据获取功能测试
2. 信号生成准确性测试
3. 通知系统可靠性测试
4. 界面响应性测试

## 维护计划

### 定期维护
1. **每周**: 检查数据源连接状态
2. **每月**: 更新依赖包版本
3. **每季度**: 验证技术指标准确性
4. **每年**: 系统架构评审

### 版本更新
- **v1.0.0**: 基础功能版本
- **v1.1.0**: 增加多股票支持
- **v1.2.0**: 添加更多技术指标
- **v2.0.0**: 重构架构，支持插件化

## 相关资源

### 文档资料
- **SKILL.md**: 技能包核心文档
- **references/technical_indicators.md**: 技术指标详解
- **references/api_reference.md**: API接口文档
- **assets/project-structure.txt**: 项目结构说明

### 外部资源
- [Yahoo Finance API文档](https://pypi.org/project/yfinance/)
- [TA-Lib技术指标库](https://github.com/mrjbq7/ta-lib)
- [Streamlit文档](https://docs.streamlit.io/)
- [Plotly文档](https://plotly.com/python/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 贡献指南

### 报告问题
1. 在GitHub Issues中创建问题
2. 提供详细的重现步骤
3. 包含错误日志和配置信息

### 提交改进
1. Fork项目仓库
2. 创建功能分支
3. 提交Pull Request
4. 添加测试用例

### 代码规范
- 遵循PEP 8编码规范
- 添加必要的注释
- 编写单元测试
- 更新相关文档

## 许可证

本项目基于MIT许可证开源，详情见LICENSE文件。

## 支持与联系

如有问题或建议，请通过以下方式联系：

- GitHub Issues: [项目问题跟踪](https://github.com/your-repo/issues)
- 电子邮件: support@example.com
- 文档网站: https://docs.example.com

---

**💡 提示**: 技能包提供了完整的股票监控解决方案，可根据具体需求灵活定制和扩展。建议先从基础功能开始，逐步添加高级特性。