import yfinance as yf
import pandas as pd
import numpy as np
import os
import time
import pickle
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import requests
from config import STOCK_SYMBOL, CHECK_HISTORY_DAYS, DATA_CACHE_DIR, DATA_CACHE_TTL

class DataFetcher:
    """股票数据获取器"""
    
    def __init__(self, symbol: str = STOCK_SYMBOL):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self.cache_dir = DATA_CACHE_DIR
        
        # 创建缓存目录
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def get_cache_file(self, data_type: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.cache_dir, f"{self.symbol}_{data_type}.pkl")
    
    def is_cache_valid(self, cache_file: str, ttl: int = DATA_CACHE_TTL) -> bool:
        """检查缓存是否有效"""
        if not os.path.exists(cache_file):
            return False
        
        file_mtime = os.path.getmtime(cache_file)
        current_time = time.time()
        return (current_time - file_mtime) < ttl
    
    def save_to_cache(self, data, data_type: str):
        """保存数据到缓存"""
        cache_file = self.get_cache_file(data_type)
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'data': data,
                'timestamp': datetime.now()
            }, f)
    
    def load_from_cache(self, data_type: str):
        """从缓存加载数据"""
        cache_file = self.get_cache_file(data_type)
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                cached = pickle.load(f)
                return cached['data']
        return None
    
    def get_realtime_data(self) -> Dict:
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
                
                # 添加基本信息
                if 'marketCap' in data:
                    realtime_data['market_cap'] = data['marketCap']
                if 'volume' in data:
                    realtime_data['avg_volume'] = data['volume']
                if 'fiftyTwoWeekHigh' in data:
                    realtime_data['52w_high'] = data['fiftyTwoWeekHigh']
                if 'fiftyTwoWeekLow' in data:
                    realtime_data['52w_low'] = data['fiftyTwoWeekLow']
                
                return realtime_data
            else:
                # 如果无法获取分钟数据，使用日数据
                return self.get_daily_data()
                
        except Exception as e:
            print(f"获取实时数据失败: {e}")
            return self.get_fallback_data()
    
    def get_daily_data(self) -> Dict:
        """获取日线数据（备用）"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1)
            
            history = self.ticker.history(start=start_date, end=end_date)
            if not history.empty:
                latest_price = history['Close'].iloc[-1]
                prev_close = history['Close'].iloc[0] if len(history) > 1 else latest_price
                
                change = latest_price - prev_close
                change_percent = (change / prev_close * 100) if prev_close != 0 else 0
                
                return {
                    'symbol': self.symbol,
                    'price': round(latest_price, 3),
                    'prev_close': round(prev_close, 3),
                    'change': round(change, 3),
                    'change_percent': round(change_percent, 2),
                    'volume': int(history['Volume'].iloc[-1]) if 'Volume' in history.columns else 0,
                    'high': round(history['High'].iloc[-1], 3) if 'High' in history.columns else latest_price,
                    'low': round(history['Low'].iloc[-1], 3) if 'Low' in history.columns else latest_price,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'open': round(history['Open'].iloc[-1], 3) if 'Open' in history.columns else latest_price
                }
        except Exception as e:
            print(f"获取日线数据失败: {e}")
        
        return self.get_fallback_data()
    
    def get_fallback_data(self) -> Dict:
        """获取降级数据（当所有API都失败时）"""
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
    
    def get_historical_data(self, days: int = CHECK_HISTORY_DAYS) -> pd.DataFrame:
        """获取历史数据"""
        cache_key = f"history_{days}d"
        
        # 检查缓存
        if self.is_cache_valid(self.get_cache_file(cache_key)):
            cached_data = self.load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # 获取历史数据
            history = self.ticker.history(start=start_date, end=end_date)
            
            if not history.empty:
                # 清理数据
                history = history[['Open', 'High', 'Low', 'Close', 'Volume']]
                history.columns = ['open', 'high', 'low', 'close', 'volume']
                
                # 保存到缓存
                self.save_to_cache(history, cache_key)
                
                return history
            else:
                print("获取历史数据为空")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"获取历史数据失败: {e}")
            return pd.DataFrame()
    
    def get_intraday_data(self, interval: str = '5m', days: int = 5) -> pd.DataFrame:
        """获取日内数据"""
        cache_key = f"intraday_{interval}_{days}d"
        
        # 检查缓存
        if self.is_cache_valid(self.get_cache_file(cache_key)):
            cached_data = self.load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        try:
            # 获取日内数据
            history = self.ticker.history(period=f'{days}d', interval=interval)
            
            if not history.empty:
                # 清理数据
                history = history[['Open', 'High', 'Low', 'Close', 'Volume']]
                history.columns = ['open', 'high', 'low', 'close', 'volume']
                
                # 保存到缓存
                self.save_to_cache(history, cache_key)
                
                return history
            else:
                print("获取日内数据为空")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"获取日内数据失败: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self) -> Dict:
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
                'avg_volume': info.get('averageVolume', 0),
                '52w_high': info.get('fiftyTwoWeekHigh', 0),
                '52w_low': info.get('fiftyTwoWeekLow', 0),
                'beta': info.get('beta', 0)
            }
            
            return basic_info
        except Exception as e:
            print(f"获取股票信息失败: {e}")
            return {}