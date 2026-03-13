import pandas as pd
import numpy as np
import os
import time
import pickle
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
from config import STOCK_SYMBOL, CHECK_HISTORY_DAYS, DATA_CACHE_DIR, DATA_CACHE_TTL


def _pure_code(symbol: str) -> str:
    """去掉 .SS / .SZ 后缀，只保留 6 位数字"""
    return symbol.split('.')[0]


class DataFetcher:
    """
    股票数据获取器
    优先级：akshare ETF接口 → akshare 通用行情 → 东方财富 HTTP → 静态兜底
    """

    def __init__(self, symbol: str = STOCK_SYMBOL):
        self.symbol = symbol
        self.code = _pure_code(symbol)   # 例: "588200"
        self.cache_dir = DATA_CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)

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
        try:
            with open(self._cache_path(key), 'wb') as f:
                pickle.dump({'data': data, 'ts': datetime.now()}, f)
        except Exception:
            pass

    def _load_cache(self, key: str):
        path = self._cache_path(key)
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)['data']
            except Exception:
                pass
        return None

    # ──────────────────────────────
    # 实时行情
    # ──────────────────────────────
    def get_realtime_data(self) -> Dict:
        """获取实时行情，多接口容错"""
        # 1. 尝试 akshare ETF 实时接口
        result = self._fetch_realtime_akshare_etf()
        if result and result.get('price', 0) > 0:
            return result

        # 2. 尝试 akshare 通用 A 股实时接口
        result = self._fetch_realtime_akshare_stock()
        if result and result.get('price', 0) > 0:
            return result

        # 3. 尝试东方财富 HTTP 接口
        result = self._fetch_realtime_eastmoney()
        if result and result.get('price', 0) > 0:
            return result

        # 4. 返回带提示的兜底数据
        print("[DataFetcher] 所有实时接口均失败，返回兜底数据")
        return self._fallback()

    def _fetch_realtime_akshare_etf(self) -> Optional[Dict]:
        """akshare fund_etf_spot_em 接口"""
        try:
            import akshare as ak
            df = ak.fund_etf_spot_em()
            # 统一列名（不同版本可能略有差异）
            df.columns = [str(c).strip() for c in df.columns]

            row = df[df['代码'] == self.code]
            if row.empty:
                return None

            r = row.iloc[0]
            price = self._to_float(r, ['最新价', '现价', '价格'], 0)
            prev_close = self._to_float(r, ['昨收', '昨日收盘', '昨收价'], price)
            if prev_close == 0:
                prev_close = price
            change = round(price - prev_close, 4)
            chg_pct = round(change / prev_close * 100, 2) if prev_close else 0

            return {
                'symbol':         self.symbol,
                'price':          round(price, 4),
                'prev_close':     round(prev_close, 4),
                'change':         change,
                'change_percent': chg_pct,
                'volume':         int(self._to_float(r, ['成交量', '手数'], 0)),
                'amount':         self._to_float(r, ['成交额', '成交量(元)'], 0),
                'high':           self._to_float(r, ['最高', '今日最高', '高'], price),
                'low':            self._to_float(r, ['最低', '今日最低', '低'], price),
                'open':           self._to_float(r, ['今开', '开盘', '开'], price),
                'timestamp':      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_source':    'akshare-etf',
            }
        except Exception as e:
            print(f"[akshare ETF 实时] 失败: {e}")
            return None

    def _fetch_realtime_akshare_stock(self) -> Optional[Dict]:
        """akshare stock_zh_a_spot_em 通用行情接口"""
        try:
            import akshare as ak
            df = ak.stock_zh_a_spot_em()
            df.columns = [str(c).strip() for c in df.columns]

            row = df[df['代码'] == self.code]
            if row.empty:
                return None

            r = row.iloc[0]
            price = self._to_float(r, ['最新价', '现价', '价格'], 0)
            prev_close = self._to_float(r, ['昨收', '昨日收盘'], price)
            if prev_close == 0:
                prev_close = price
            change = round(price - prev_close, 4)
            chg_pct = round(change / prev_close * 100, 2) if prev_close else 0

            return {
                'symbol':         self.symbol,
                'price':          round(price, 4),
                'prev_close':     round(prev_close, 4),
                'change':         change,
                'change_percent': chg_pct,
                'volume':         int(self._to_float(r, ['成交量', '手数'], 0)),
                'amount':         self._to_float(r, ['成交额'], 0),
                'high':           self._to_float(r, ['最高', '高'], price),
                'low':            self._to_float(r, ['最低', '低'], price),
                'open':           self._to_float(r, ['今开', '开盘', '开'], price),
                'timestamp':      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_source':    'akshare-stock',
            }
        except Exception as e:
            print(f"[akshare 通用行情 实时] 失败: {e}")
            return None

    def _fetch_realtime_eastmoney(self) -> Optional[Dict]:
        """东方财富 HTTP 接口（无需 akshare）"""
        try:
            # secid: 1=上海, 0=深圳  588200 是上交所
            secid = f"1.{self.code}"
            url = (
                f"https://push2.eastmoney.com/api/qt/stock/get"
                f"?secid={secid}&fields=f43,f57,f58,f169,f170,f44,f45,f46,f60,f47"
            )
            resp = requests.get(url, timeout=8,
                                headers={'User-Agent': 'Mozilla/5.0'})
            data = resp.json().get('data', {})
            if not data:
                return None

            price      = data.get('f43', 0) / 100.0
            prev_close = data.get('f60', 0) / 100.0
            high       = data.get('f44', 0) / 100.0
            low        = data.get('f45', 0) / 100.0
            open_      = data.get('f46', 0) / 100.0
            volume     = data.get('f47', 0)
            change     = data.get('f169', 0) / 100.0
            chg_pct    = data.get('f170', 0) / 100.0

            if price <= 0:
                return None

            return {
                'symbol':         self.symbol,
                'price':          round(price, 4),
                'prev_close':     round(prev_close, 4),
                'change':         round(change, 4),
                'change_percent': round(chg_pct, 2),
                'volume':         int(volume),
                'amount':         0,
                'high':           round(high, 4),
                'low':            round(low, 4),
                'open':           round(open_, 4),
                'timestamp':      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_source':    'eastmoney-http',
            }
        except Exception as e:
            print(f"[东方财富 HTTP 实时] 失败: {e}")
            return None

    # ──────────────────────────────
    # 历史数据
    # ──────────────────────────────
    def get_historical_data(self, days: int = CHECK_HISTORY_DAYS) -> pd.DataFrame:
        """获取日线历史数据，多接口容错"""
        key = f"history_{days}d"

        if self._cache_valid(key):
            cached = self._load_cache(key)
            if cached is not None and not cached.empty:
                return cached

        # 1. akshare ETF 历史接口
        df = self._fetch_hist_akshare_etf(days)
        if df is not None and not df.empty:
            self._save_cache(df, key)
            return df

        # 2. akshare 通用行情历史接口
        df = self._fetch_hist_akshare_stock(days)
        if df is not None and not df.empty:
            self._save_cache(df, key)
            return df

        # 3. 东方财富 HTTP 历史接口
        df = self._fetch_hist_eastmoney(days)
        if df is not None and not df.empty:
            self._save_cache(df, key)
            return df

        print("[DataFetcher] 所有历史数据接口均失败")
        return pd.DataFrame()

    def _fetch_hist_akshare_etf(self, days: int) -> Optional[pd.DataFrame]:
        """akshare fund_etf_hist_em"""
        try:
            import akshare as ak
            end   = datetime.now()
            start = end - timedelta(days=days + 30)

            df = ak.fund_etf_hist_em(
                symbol=self.code,
                period="daily",
                start_date=start.strftime('%Y%m%d'),
                end_date=end.strftime('%Y%m%d'),
                adjust="qfq"
            )

            if df is None or df.empty:
                return None

            df.columns = [str(c).strip() for c in df.columns]
            # 兼容不同版本列名
            col_map = {}
            for c in df.columns:
                if c in ('日期', 'date', 'Date'):
                    col_map[c] = 'date'
                elif c in ('开盘', 'open', 'Open'):
                    col_map[c] = 'open'
                elif c in ('收盘', 'close', 'Close'):
                    col_map[c] = 'close'
                elif c in ('最高', 'high', 'High'):
                    col_map[c] = 'high'
                elif c in ('最低', 'low', 'Low'):
                    col_map[c] = 'low'
                elif c in ('成交量', 'volume', 'Volume'):
                    col_map[c] = 'volume'

            df = df.rename(columns=col_map)

            required = ['date', 'open', 'close', 'high', 'low', 'volume']
            missing = [c for c in required if c not in df.columns]
            if missing:
                print(f"[akshare ETF 历史] 列名缺失: {missing}，实际列: {list(df.columns)}")
                return None

            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')[['open', 'high', 'low', 'close', 'volume']]
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna().sort_index().tail(days)

            return df if not df.empty else None

        except Exception as e:
            print(f"[akshare ETF 历史] 失败: {e}")
            return None

    def _fetch_hist_akshare_stock(self, days: int) -> Optional[pd.DataFrame]:
        """akshare stock_zh_a_hist"""
        try:
            import akshare as ak
            end   = datetime.now()
            start = end - timedelta(days=days + 30)

            df = ak.stock_zh_a_hist(
                symbol=self.code,
                period="daily",
                start_date=start.strftime('%Y%m%d'),
                end_date=end.strftime('%Y%m%d'),
                adjust="qfq"
            )

            if df is None or df.empty:
                return None

            df.columns = [str(c).strip() for c in df.columns]
            col_map = {}
            for c in df.columns:
                lc = c.lower()
                if '日期' in c or lc == 'date':
                    col_map[c] = 'date'
                elif '开盘' in c or lc == 'open':
                    col_map[c] = 'open'
                elif '收盘' in c or lc == 'close':
                    col_map[c] = 'close'
                elif '最高' in c or lc == 'high':
                    col_map[c] = 'high'
                elif '最低' in c or lc == 'low':
                    col_map[c] = 'low'
                elif '成交量' in c or lc == 'volume':
                    col_map[c] = 'volume'

            df = df.rename(columns=col_map)

            required = ['date', 'open', 'close', 'high', 'low', 'volume']
            if any(c not in df.columns for c in required):
                return None

            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')[['open', 'high', 'low', 'close', 'volume']]
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.dropna().sort_index().tail(days)

            return df if not df.empty else None

        except Exception as e:
            print(f"[akshare 通用历史] 失败: {e}")
            return None

    def _fetch_hist_eastmoney(self, days: int) -> Optional[pd.DataFrame]:
        """东方财富 HTTP K线接口"""
        try:
            end_dt   = datetime.now()
            start_dt = end_dt - timedelta(days=days + 30)

            url = (
                f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
                f"?secid=1.{self.code}"
                f"&fields1=f1,f2,f3,f4,f5,f6"
                f"&fields2=f51,f52,f53,f54,f55,f56,f57"
                f"&klt=101&fqt=1"
                f"&beg={start_dt.strftime('%Y%m%d')}"
                f"&end={end_dt.strftime('%Y%m%d')}"
            )
            resp = requests.get(url, timeout=10,
                                headers={'User-Agent': 'Mozilla/5.0'})
            klines = resp.json().get('data', {}).get('klines', [])
            if not klines:
                return None

            records = []
            for line in klines:
                parts = line.split(',')
                if len(parts) >= 6:
                    records.append({
                        'date':   parts[0],
                        'open':   float(parts[1]),
                        'close':  float(parts[2]),
                        'high':   float(parts[3]),
                        'low':    float(parts[4]),
                        'volume': float(parts[5]),
                    })

            if not records:
                return None

            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')[['open', 'high', 'low', 'close', 'volume']]
            df = df.sort_index().tail(days)

            return df if not df.empty else None

        except Exception as e:
            print(f"[东方财富 HTTP 历史] 失败: {e}")
            return None

    # ──────────────────────────────
    # 分时数据（近 N 天 5 分钟）
    # ──────────────────────────────
    def get_intraday_data(self, interval: str = '5m', days: int = 5) -> pd.DataFrame:
        """获取分时数据，多接口容错"""
        key = f"intraday_{interval}_{days}d"

        if self._cache_valid(key, ttl=60):
            cached = self._load_cache(key)
            if cached is not None and not cached.empty:
                return cached

        df = self._fetch_intraday_akshare(interval, days)
        if df is not None and not df.empty:
            self._save_cache(df, key)
            return df

        df = self._fetch_intraday_eastmoney(interval, days)
        if df is not None and not df.empty:
            self._save_cache(df, key)
            return df

        return pd.DataFrame()

    def _fetch_intraday_akshare(self, interval: str, days: int) -> Optional[pd.DataFrame]:
        try:
            import akshare as ak
            period_map = {'1m': '1', '5m': '5', '15m': '15', '30m': '30', '60m': '60'}
            period = period_map.get(interval, '5')

            df = ak.fund_etf_hist_min_em(symbol=self.code, period=period, adjust='qfq')
            if df is None or df.empty:
                return None

            df.columns = [str(c).strip() for c in df.columns]
            col_map = {}
            for c in df.columns:
                if '时间' in c or c.lower() in ('time', 'date', 'datetime'):
                    col_map[c] = 'date'
                elif '开盘' in c:
                    col_map[c] = 'open'
                elif '收盘' in c:
                    col_map[c] = 'close'
                elif '最高' in c:
                    col_map[c] = 'high'
                elif '最低' in c:
                    col_map[c] = 'low'
                elif '成交量' in c:
                    col_map[c] = 'volume'

            df = df.rename(columns=col_map)
            if any(c not in df.columns for c in ['date', 'open', 'close', 'high', 'low', 'volume']):
                return None

            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')[['open', 'high', 'low', 'close', 'volume']]
            cutoff = datetime.now() - timedelta(days=days)
            df = df[df.index >= cutoff]

            return df if not df.empty else None

        except Exception as e:
            print(f"[akshare 分时] 失败: {e}")
            return None

    def _fetch_intraday_eastmoney(self, interval: str, days: int) -> Optional[pd.DataFrame]:
        """东方财富分时 K线"""
        try:
            period_map = {'1m': '1', '5m': '5', '15m': '15', '30m': '30', '60m': '60'}
            klt = period_map.get(interval, '5')
            end_dt   = datetime.now()
            start_dt = end_dt - timedelta(days=days + 5)

            url = (
                f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
                f"?secid=1.{self.code}"
                f"&fields1=f1,f2,f3,f4,f5,f6"
                f"&fields2=f51,f52,f53,f54,f55,f56"
                f"&klt={klt}&fqt=1"
                f"&beg={start_dt.strftime('%Y%m%d')}"
                f"&end={end_dt.strftime('%Y%m%d')}"
            )
            resp = requests.get(url, timeout=10,
                                headers={'User-Agent': 'Mozilla/5.0'})
            klines = resp.json().get('data', {}).get('klines', [])
            if not klines:
                return None

            records = []
            for line in klines:
                parts = line.split(',')
                if len(parts) >= 6:
                    records.append({
                        'date':   parts[0],
                        'open':   float(parts[1]),
                        'close':  float(parts[2]),
                        'high':   float(parts[3]),
                        'low':    float(parts[4]),
                        'volume': float(parts[5]),
                    })

            if not records:
                return None

            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')[['open', 'high', 'low', 'close', 'volume']]

            return df if not df.empty else None

        except Exception as e:
            print(f"[东方财富分时] 失败: {e}")
            return None

    # ──────────────────────────────
    # 基本信息
    # ──────────────────────────────
    def get_stock_info(self) -> Dict:
        """获取 ETF 基本信息"""
        base_info = {
            'symbol':         self.symbol,
            'name':           '科创芯片ETF',
            'sector':         '半导体/芯片',
            'industry':       'ETF基金',
            'market_cap':     0,
            'pe_ratio':       0,
            'pb_ratio':       0,
            'dividend_yield': 0,
            'avg_volume':     0,
            '52w_high':       0,
            '52w_low':        0,
            'beta':           0,
        }

        try:
            import akshare as ak
            df = ak.fund_etf_spot_em()
            df.columns = [str(c).strip() for c in df.columns]
            row = df[df['代码'] == self.code]
            if not row.empty:
                r = row.iloc[0]
                name = str(r.get('名称', '') or r.get('基金名称', '') or '科创芯片ETF')
                base_info.update({
                    'name':       name if name else '科创芯片ETF',
                    'market_cap': self._to_float(r, ['总市值', '规模(亿元)', '基金规模'], 0),
                    'avg_volume': self._to_float(r, ['成交量', '手数'], 0),
                })
        except Exception as e:
            print(f"[akshare 基本信息] 失败: {e}")

        # 尝试获取52周高低（从历史数据计算）
        try:
            df_hist = self.get_historical_data(days=252)
            if not df_hist.empty:
                base_info['52w_high'] = float(df_hist['high'].max())
                base_info['52w_low']  = float(df_hist['low'].min())
        except Exception:
            pass

        return base_info

    # ──────────────────────────────
    # 工具方法
    # ──────────────────────────────
    def _to_float(self, row, field_names: list, default: float) -> float:
        """从行数据中尝试多个字段名，返回第一个有效的浮点值"""
        for name in field_names:
            try:
                val = row.get(name)
                if val is not None and val != '' and not (isinstance(val, float) and np.isnan(val)):
                    return float(val)
            except Exception:
                continue
        return default

    def _fallback(self) -> Dict:
        return {
            'symbol':         self.symbol,
            'price':          0.0,
            'prev_close':     0.0,
            'change':         0.0,
            'change_percent': 0.0,
            'volume':         0,
            'amount':         0.0,
            'high':           0.0,
            'low':            0.0,
            'open':           0.0,
            'timestamp':      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error':          '数据获取失败，请检查网络连接或稍后重试',
            'data_source':    'fallback',
        }

    # 保持旧接口兼容
    def get_fallback_data(self) -> Dict:
        return self._fallback()
