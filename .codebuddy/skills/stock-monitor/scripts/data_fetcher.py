import yfinance as yf
import pandas as pd
import os
import time
import pickle
from datetime import datetime, timedelta

class DataFetcher:
    """股票数据获取器 - 核心模块"""
    
    def __init__(self, symbol: str = "588200.SS"):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.cache_dir = "data_cache"
        
        # 创建缓存目录
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def get_realtime_data(self) -> dict:
        """获取实时行情数据"""
        try:
            # 获取实时数据
            data = self.ticker.info
            
            # 获取当前价格
            history = self.ticker.history(period='1d', interval='1m')
            if not history.empty:
                latest_price = history['Close'].iloc[-1]
                prev_close = history['Close'].iloc[0] if len(history) > 1 else latest_price
                
                change = latest_price - prev_close
                change_percent = (change / prev_close * 100) if prev_close != 0 else 0
                
                realtime_data = {
                    'symbol': self.symbol,
                    'price': round(latest_price, 3),
                    'prev_close': round(prev_close, 3),
                    'change': round(change, 3),
                    'change_percent': round(change_percent, 2),
                    'volume': int(history['Volume'].sum()) if 'Volume' in history.columns else 0,
                    'high': round(history['High'].max(), 3) if 'High' in history.columns else latest_price,
                    'low': round(history['Low'].min(), 3) if 'Low' in history.columns else latest_price,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'open': round(history['Open'].iloc[0], 3) if 'Open' in history.columns else latest_price
                }
                
                return realtime_data
                
        except Exception as e:
            print(f"获取实时数据失败: {e}")
        
        return self.get_fallback_data()
    
    def get_historical_data(self, days: int = 30) -> pd.DataFrame:
        """获取历史数据"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            history = self.ticker.history(start=start_date, end=end_date)
            
            if not history.empty:
                # 清理数据
                history = history[['Open', 'High', 'Low', 'Close', 'Volume']]
                history.columns = ['open', 'high', 'low', 'close', 'volume']
                
                return history
                
        except Exception as e:
            print(f"获取历史数据失败: {e}")
        
        return pd.DataFrame()
    
    def get_fallback_data(self) -> dict:
        """获取降级数据"""
        return {
            'symbol': self.symbol,
            'price': 0.0,
            'prev_close': 0.0,
            'change': 0.0,
            'change_percent': 0.0,
            'volume': 0,
            'high': 0.0,
            'low': 0.0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'open': 0.0,
            'error': '数据获取失败'
        }
    
    def get_stock_info(self) -> dict:
        """获取股票基本信息"""
        try:
            info = self.ticker.info
            
            basic_info = {
                'symbol': self.symbol,
                'name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'avg_volume': info.get('averageVolume', 0)
            }
            
            return basic_info
        except Exception as e:
            print(f"获取股票信息失败: {e}")
            return {}