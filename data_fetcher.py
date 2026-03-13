import pandas as pd
import numpy as np
import os
import time
import pickle
from datetime import datetime, timedelta
from typing import Dict, Optional
from config import STOCK_SYMBOL, CHECK_HISTORY_DAYS, DATA_CACHE_DIR, DATA_CACHE_TTL

# 股票代码处理：去掉 .SS / .SZ 后缀，只保留6位数字
def _pure_code(symbol: str) -> str:
    return symbol.split('.')[0]

class DataFetcher:
    """股票数据获取器（基于 akshare，专为中国 A 股 / ETF 设计）"""

    def __init__(self, symbol: str = STOCK_SYMBOL):
        self.symbol = symbol
        self.code = _pure_code(symbol)   # 例: "588200"
        self.cache_dir = DATA_CACHE_DIR

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    # ──────────────────────────────
    # 缓存工具
    # ──────────────────────────────
    def _cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{self.code}_{key}.pkl")

    def _cache_valid(self, key: str, ttl: int = DATA_CACHE_TTL) -> bool:
        path = self._cache_path(key)
        if not os.path.exists(path):
            return False
        return (time.time() - os.path.getmtime(path)) < ttl

    def _save_cache(self, data, key: str):
        with open(self._cache_path(key), 'wb') as f:
            pickle.dump({'data': data, 'ts': datetime.now()}, f)

    def _load_cache(self, key: str):
        path = self._cache_path(key)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return pickle.load(f)['data']
        return None

    # ──────────────────────────────
    # 实时行情
    # ──────────────────────────────
    def get_realtime_data(self) -> Dict:
        """获取实时行情（akshare fund_etf_spot_em）"""
        try:
            import akshare as ak
            df = ak.fund_etf_spot_em()
            row = df[df['代码'] == self.code]
            if row.empty:
                raise ValueError(f"未找到代码 {self.code}")

            r = row.iloc[0]
            price      = float(r.get('最新价', 0) or 0)
            prev_close = float(r.get('昨收', 0) or price)
            change     = round(price - prev_close, 4)
            chg_pct    = round(change / prev_close * 100, 2) if prev_close else 0

            return {
                'symbol':         self.symbol,
                'price':          round(price, 4),
                'prev_close':     round(prev_close, 4),
                'change':         change,
                'change_percent': chg_pct,
                'volume':         int(float(r.get('成交量', 0) or 0)),
                'high':           float(r.get('最高', price) or price),
                'low':            float(r.get('最低', price) or price),
                'open':           float(r.get('今开', price) or price),
                'timestamp':      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        except Exception as e:
            print(f"[akshare 实时] 获取失败: {e}")
            return self._fallback()

    # ──────────────────────────────
    # 历史数据
    # ──────────────────────────────
    def get_historical_data(self, days: int = CHECK_HISTORY_DAYS) -> pd.DataFrame:
        """获取日线历史数据（akshare fund_etf_hist_em）"""
        key = f"history_{days}d"

        if self._cache_valid(key):
            cached = self._load_cache(key)
            if cached is not None:
                return cached

        try:
            import akshare as ak
            end   = datetime.now()
            start = end - timedelta(days=days + 10)   # 多取几天保证够用

            df = ak.fund_etf_hist_em(
                symbol=self.code,
                period="daily",
                start_date=start.strftime('%Y%m%d'),
                end_date=end.strftime('%Y%m%d'),
                adjust="qfq"           # 前复权
            )

            if df.empty:
                raise ValueError("历史数据为空")

            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
            })
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')[['open', 'high', 'low', 'close', 'volume']]
            df = df.sort_index().tail(days)

            self._save_cache(df, key)
            return df

        except Exception as e:
            print(f"[akshare 历史] 获取失败: {e}")
            return pd.DataFrame()

    # ──────────────────────────────
    # 日内分时数据（近 5 天 5 分钟）
    # ──────────────────────────────
    def get_intraday_data(self, interval: str = '5m', days: int = 5) -> pd.DataFrame:
        """获取分时数据（akshare fund_etf_hist_min_em）"""
        key = f"intraday_{interval}_{days}d"

        if self._cache_valid(key, ttl=60):
            cached = self._load_cache(key)
            if cached is not None:
                return cached

        try:
            import akshare as ak
            period_map = {'1m': '1', '5m': '5', '15m': '15', '30m': '30', '60m': '60'}
            period = period_map.get(interval, '5')

            df = ak.fund_etf_hist_min_em(symbol=self.code, period=period, adjust='qfq')

            if df.empty:
                raise ValueError("分时数据为空")

            df = df.rename(columns={
                '时间': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
            })
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')[['open', 'high', 'low', 'close', 'volume']]

            # 只保留最近 N 天
            cutoff = datetime.now() - timedelta(days=days)
            df = df[df.index >= cutoff]

            self._save_cache(df, key)
            return df

        except Exception as e:
            print(f"[akshare 分时] 获取失败: {e}")
            return pd.DataFrame()

    # ──────────────────────────────
    # 基本信息
    # ──────────────────────────────
    def get_stock_info(self) -> Dict:
        """获取 ETF 基本信息"""
        try:
            import akshare as ak
            # ETF 名称 / 规模等
            df = ak.fund_etf_spot_em()
            row = df[df['代码'] == self.code]
            if row.empty:
                raise ValueError("未找到 ETF 信息")

            r = row.iloc[0]
            # 尝试获取基金规模（可能字段不存在时用默认值）
            return {
                'symbol':        self.symbol,
                'name':          str(r.get('名称', '科创芯片ETF')),
                'sector':        '半导体/芯片',
                'industry':      'ETF基金',
                'market_cap':    float(r.get('总市值', 0) or 0),
                'pe_ratio':      0,
                'pb_ratio':      0,
                'dividend_yield':0,
                'avg_volume':    float(r.get('成交量', 0) or 0),
                '52w_high':      0,
                '52w_low':       0,
                'beta':          0,
            }
        except Exception as e:
            print(f"[akshare 基本信息] 获取失败: {e}")
            return {
                'symbol':   self.symbol,
                'name':     '科创芯片ETF (588200)',
                'sector':   '半导体/芯片',
                'industry': 'ETF基金',
            }

    # ──────────────────────────────
    # 降级兜底
    # ──────────────────────────────
    def _fallback(self) -> Dict:
        return {
            'symbol':         self.symbol,
            'price':          0.0,
            'prev_close':     0.0,
            'change':         0.0,
            'change_percent': 0.0,
            'volume':         0,
            'high':           0.0,
            'low':            0.0,
            'open':           0.0,
            'timestamp':      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error':          '数据获取失败，请检查网络或稍后重试',
        }

    # 保持旧接口兼容
    def get_fallback_data(self) -> Dict:
        return self._fallback()
