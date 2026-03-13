# 科创芯片ETF (588200) 实时监控系统

这是一个实时监控科创芯片ETF (588200)并给出买卖信号的系统。

## 功能特点

- 📈 实时获取科创芯片ETF (588200)行情数据
- 🔍 多技术指标分析（MACD, RSI, 布林带等）
- ⚡ 实时买卖信号生成
- 📊 交互式可视化图表
- 🔔 多种通知方式（Telegram, 控制台）
- ⏰ 定时监控和自动更新

## 安装步骤

1. 克隆或下载项目
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量：
   ```bash
   cp .env.example .env
   ```
   编辑 `.env` 文件，填入您的Telegram Bot Token和Chat ID

## 使用方法

### 启动Web监控界面
```bash
streamlit run app.py
```

### 启动后台监控服务
```bash
python monitor.py
```

### 单独运行数据分析
```bash
python analyzer.py
```

## 项目结构

```
.
├── app.py              # Streamlit Web界面
├── monitor.py          # 后台监控服务
├── analyzer.py         # 数据分析模块
├── data_fetcher.py     # 数据获取模块
├── signals.py          # 信号生成模块
├── utils.py            # 工具函数
├── config.py           # 配置文件
├── requirements.txt    # 依赖包
├── .env.example        # 环境变量示例
└── README.md           # 说明文档
```

## 技术指标

系统使用以下技术指标生成买卖信号：

1. **MACD (移动平均收敛发散)**
   - 金叉：买入信号
   - 死叉：卖出信号

2. **RSI (相对强弱指数)**
   - RSI < 30：超卖，买入信号
   - RSI > 70：超买，卖出信号

3. **布林带 (Bollinger Bands)**
   - 价格触及下轨：买入信号
   - 价格触及上轨：卖出信号

4. **移动平均线**
   - 价格突破均线：趋势确认

## 配置说明

### Telegram通知
1. 创建Telegram Bot并获取Token
2. 获取Chat ID
3. 在 `.env` 文件中配置

### 监控参数
- `MONITORING_INTERVAL`: 监控间隔（秒）
- `ALERT_THRESHOLD`: 涨跌幅报警阈值（%）
- `CHECK_HISTORY_DAYS`: 历史数据天数

## 注意事项

1. 本系统为辅助决策工具，不构成投资建议
2. 金融市场有风险，投资需谨慎
3. 建议结合基本面分析和其他技术指标
4. 定期检查和更新策略参数