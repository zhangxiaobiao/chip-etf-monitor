import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 股票配置
STOCK_SYMBOL = os.getenv('STOCK_SYMBOL', '588200.SS')  # 科创芯片ETF
STOCK_NAME = "科创芯片ETF (588200)"

# 监控配置
MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', 60))  # 监控间隔（秒）
ALERT_THRESHOLD = float(os.getenv('ALERT_THRESHOLD', 2.0))  # 涨跌幅报警阈值（%）
CHECK_HISTORY_DAYS = int(os.getenv('CHECK_HISTORY_DAYS', 30))  # 历史数据天数

# 技术指标配置
RSI_OVERBOUGHT = int(os.getenv('RSI_OVERBOUGHT', 70))
RSI_OVERSOLD = int(os.getenv('RSI_OVERSOLD', 30))
MACD_SIGNAL = int(os.getenv('MACD_SIGNAL', 9))
MACD_FAST = int(os.getenv('MACD_FAST', 12))
MACD_SLOW = int(os.getenv('MACD_SLOW', 26))
BBANDS_PERIOD = int(os.getenv('BBANDS_PERIOD', 20))
BBANDS_STD = float(os.getenv('BBANDS_STD', 2.0))

# 通知配置
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
ENABLE_TELEGRAM = TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID

# 数据源配置
YAHOO_FINANCE_ENABLED = True
DATA_CACHE_DIR = "data_cache"
DATA_CACHE_TTL = 300  # 数据缓存时间（秒）

def get_config_summary():
    """获取配置摘要"""
    return {
        "stock_symbol": STOCK_SYMBOL,
        "stock_name": STOCK_NAME,
        "monitoring_interval": MONITORING_INTERVAL,
        "alert_threshold": ALERT_THRESHOLD,
        "check_history_days": CHECK_HISTORY_DAYS,
        "telegram_enabled": ENABLE_TELEGRAM,
        "rsi_overbought": RSI_OVERBOUGHT,
        "rsi_oversold": RSI_OVERSOLD,
        "macd_fast": MACD_FAST,
        "macd_slow": MACD_SLOW,
        "macd_signal": MACD_SIGNAL,
        "bbands_period": BBANDS_PERIOD,
        "bbands_std": BBANDS_STD
    }