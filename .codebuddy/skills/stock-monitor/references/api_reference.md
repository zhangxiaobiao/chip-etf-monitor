# API参考手册

## 数据源API

### Yahoo Finance API

#### 基础用法
```python
import yfinance as yf

# 创建股票对象
ticker = yf.Ticker("588200.SS")

# 获取实时信息
info = ticker.info

# 获取历史数据
history = ticker.history(period="1d", interval="1m")
```

#### 可用参数

**时间段 (period)**
- `1d`: 1天
- `5d`: 5天
- `1mo`: 1个月
- `3mo`: 3个月
- `6mo`: 6个月
- `1y`: 1年
- `2y`: 2年
- `5y`: 5年
- `10y`: 10年
- `ytd`: 年初至今
- `max`: 最大历史数据

**时间间隔 (interval)**
- `1m`: 1分钟 (仅限最近7天)
- `2m`: 2分钟
- `5m`: 5分钟
- `15m`: 15分钟
- `30m`: 30分钟
- `60m`: 60分钟
- `90m`: 90分钟
- `1h`: 1小时
- `1d`: 1天
- `5d`: 5天
- `1wk`: 1周
- `1mo`: 1个月
- `3mo`: 3个月

#### 股票代码格式
- A股: `000001.SZ`, `600000.SS`
- 港股: `0700.HK`
- 美股: `AAPL`, `GOOGL`
- ETF: `588200.SS` (科创芯片ETF)

#### 数据字段说明
```python
# 基本信息字段
{
    'symbol': '股票代码',
    'longName': '公司全称',
    'shortName': '公司简称',
    'sector': '行业板块',
    'industry': '细分行业',
    'marketCap': '市值',
    'trailingPE': '市盈率',
    'priceToBook': '市净率',
    'dividendYield': '股息率',
    'averageVolume': '平均成交量',
    'fiftyTwoWeekHigh': '52周最高',
    'fiftyTwoWeekLow': '52周最低',
    'beta': '贝塔系数'
}

# 历史数据字段
{
    'Open': '开盘价',
    'High': '最高价',
    'Low': '最低价',
    'Close': '收盘价',
    'Volume': '成交量',
    'Dividends': '股息',
    'Stock Splits': '股票分割'
}
```

## Telegram Bot API

### 配置方法

#### 1. 创建Telegram Bot
1. 在Telegram中搜索 `@BotFather`
2. 发送 `/newbot` 创建新机器人
3. 设置机器人名称和用户名
4. 获取API Token

#### 2. 获取Chat ID
1. 在Telegram中搜索 `@userinfobot`
2. 发送 `/start`
3. 获取您的Chat ID

#### 3. 配置环境变量
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### API使用方法

#### 发送消息
```python
import requests

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200
```

#### 消息格式
支持HTML格式：
- `<b>粗体</b>`
- `<i>斜体</i>`
- `<u>下划线</u>`
- `<code>代码</code>`
- `<pre>预格式化文本</pre>`

## 系统内部API

### DataFetcher类

#### 方法列表
```python
class DataFetcher:
    def __init__(self, symbol: str = "588200.SS")
    def get_realtime_data(self) -> dict
    def get_historical_data(self, days: int = 30) -> pd.DataFrame
    def get_stock_info(self) -> dict
    def get_fallback_data(self) -> dict
```

#### 返回数据结构
```python
# get_realtime_data() 返回
{
    'symbol': '股票代码',
    'price': 当前价格,
    'prev_close': 昨日收盘价,
    'change': 涨跌额,
    'change_percent': 涨跌幅百分比,
    'volume': 成交量,
    'high': 最高价,
    'low': 最低价,
    'timestamp': '时间戳',
    'open': '开盘价'
}

# get_historical_data() 返回
DataFrame with columns:
- 'open': 开盘价
- 'high': 最高价
- 'low': 最低价
- 'close': 收盘价
- 'volume': 成交量
```

### SignalGenerator类

#### 方法列表
```python
class SignalGenerator:
    def __init__(self)
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame
    def generate_signals(self, df: pd.DataFrame, current_price: float) -> dict
```

#### 返回数据结构
```python
{
    'timestamp': '生成时间',
    'price': 当前价格,
    'overall_signal': '总体信号(买入/卖出/中性)',
    'signal_strength': 信号强度(0-100),
    'signals': [
        {
            'type': '指标类型',
            'signal': '具体信号',
            'confidence': 置信度(0-100),
            'description': '信号描述'
        }
    ],
    'recommendation': '操作建议',
    'risk_level': '风险等级'
}
```

### NotificationManager类

#### 方法列表
```python
class NotificationManager:
    def __init__(self, telegram_bot_token: str = None, telegram_chat_id: str = None)
    def send_telegram_message(self, message: str) -> bool
    def send_alert(self, alert_type: str, data: dict, threshold: float = None) -> bool
```

#### 警报类型
- `price_change`: 价格变动警报
- `signal`: 买卖信号警报
- `system`: 系统状态警报

## 配置API

### Config模块

#### 配置参数
```python
# 股票配置
STOCK_SYMBOL = "588200.SS"
STOCK_NAME = "科创芯片ETF"

# 监控配置
MONITORING_INTERVAL = 60  # 秒
ALERT_THRESHOLD = 2.0     # %
CHECK_HISTORY_DAYS = 30   # 天

# 技术指标配置
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_SIGNAL = 9
MACD_FAST = 12
MACD_SLOW = 26
BBANDS_PERIOD = 20
BBANDS_STD = 2.0

# 通知配置
TELEGRAM_BOT_TOKEN = None
TELEGRAM_CHAT_ID = None
ENABLE_TELEGRAM = False
```

#### 配置方法
```python
from config import get_config_summary

# 获取配置摘要
config = get_config_summary()
print(config)
```

## 扩展API

### 添加新的数据源

#### 实现步骤
1. 创建新的数据获取类
2. 实现与DataFetcher相同的接口
3. 在config.py中添加配置选项
4. 在数据获取模块中添加切换逻辑

#### 示例代码
```python
class AlternativeDataFetcher:
    def __init__(self, symbol: str):
        self.symbol = symbol
    
    def get_realtime_data(self) -> dict:
        # 实现新的数据获取逻辑
        pass
    
    def get_historical_data(self, days: int) -> pd.DataFrame:
        # 实现新的历史数据获取逻辑
        pass
```

### 添加新的技术指标

#### 实现步骤
1. 在signals.py中添加指标计算方法
2. 在generate_signals方法中集成新指标
3. 在config.py中添加配置参数
4. 在utils.py中添加可视化支持

#### 示例代码
```python
def calculate_new_indicator(df: pd.DataFrame) -> pd.DataFrame:
    """计算新指标"""
    df = df.copy()
    # 计算逻辑
    df['new_indicator'] = ...
    return df

def get_new_indicator_signal(value: float) -> dict:
    """生成新指标信号"""
    signal = {
        'type': '新指标',
        'signal': '中性',
        'confidence': 0,
        'description': ''
    }
    # 信号逻辑
    return signal
```

## 错误处理API

### 异常类型
```python
class DataSourceError(Exception):
    """数据源异常"""
    pass

class IndicatorError(Exception):
    """技术指标计算异常"""
    pass

class NotificationError(Exception):
    """通知发送异常"""
    pass

class ConfigError(Exception):
    """配置异常"""
    pass
```

### 错误处理策略
```python
try:
    data = data_fetcher.get_realtime_data()
except DataSourceError as e:
    # 降级处理
    data = data_fetcher.get_fallback_data()
    logger.error(f"数据源异常: {e}")
except Exception as e:
    # 通用异常处理
    logger.error(f"未知异常: {e}")
    raise
```

## 性能监控API

### 监控指标
```python
class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            'data_fetch_time': [],
            'signal_generation_time': [],
            'notification_send_time': []
        }
    
    def record_metric(self, metric_name: str, value: float):
        """记录性能指标"""
        pass
    
    def get_performance_report(self) -> dict:
        """获取性能报告"""
        pass
```

### 使用示例
```python
monitor = PerformanceMonitor()

# 记录数据获取时间
start_time = time.time()
data = data_fetcher.get_realtime_data()
end_time = time.time()
monitor.record_metric('data_fetch_time', end_time - start_time)

# 获取报告
report = monitor.get_performance_report()
```

## 日志API

### 日志配置
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 日志级别
- `DEBUG`: 调试信息
- `INFO`: 常规信息
- `WARNING`: 警告信息
- `ERROR`: 错误信息
- `CRITICAL`: 严重错误

### 使用示例
```python
logger.info("开始监控股票: %s", stock_symbol)
logger.warning("价格变动超过阈值: %.2f%%", change_percent)
logger.error("数据获取失败: %s", str(e))
```

## 测试API

### 单元测试
```python
import unittest

class TestDataFetcher(unittest.TestCase):
    def test_get_realtime_data(self):
        fetcher = DataFetcher("588200.SS")
        data = fetcher.get_realtime_data()
        self.assertIn('price', data)
        self.assertIn('timestamp', data)
    
    def test_get_historical_data(self):
        fetcher = DataFetcher("588200.SS")
        df = fetcher.get_historical_data(days=7)
        self.assertFalse(df.empty)
```

### 集成测试
```python
class TestIntegration(unittest.TestCase):
    def test_full_monitoring_cycle(self):
        # 测试完整监控周期
        fetcher = DataFetcher("588200.SS")
        generator = SignalGenerator()
        
        data = fetcher.get_realtime_data()
        df = fetcher.get_historical_data(days=30)
        signals = generator.generate_signals(df, data['price'])
        
        self.assertIn('overall_signal', signals)
        self.assertIn('recommendation', signals)
```

---
*API版本: 1.0.0*
*最后更新: 2024年*