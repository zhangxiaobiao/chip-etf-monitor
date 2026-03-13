import pandas as pd
import ta
from typing import Dict, List

class SignalGenerator:
    """买卖信号生成器 - 核心模块"""
    
    def __init__(self):
        self.signals_history = []
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        if df.empty or len(df) < 20:
            return df
        
        df = df.copy()
        
        # 移动平均线
        df['sma_10'] = ta.trend.sma_indicator(df['close'], window=10)
        df['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
        df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
        
        # MACD
        df['macd'] = ta.trend.macd(df['close'], window_slow=26, window_fast=12)
        df['macd_signal'] = ta.trend.macd_signal(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd_diff'] = ta.trend.macd_diff(df['close'], window_slow=26, window_fast=12, window_sign=9)
        
        # RSI
        df['rsi'] = ta.momentum.rsi(df['close'], window=14)
        
        # 布林带
        bollinger = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2.0)
        df['bb_high'] = bollinger.bollinger_hband()
        df['bb_low'] = bollinger.bollinger_lband()
        df['bb_mid'] = bollinger.bollinger_mavg()
        
        return df
    
    def generate_signals(self, df: pd.DataFrame, current_price: float) -> Dict:
        """生成买卖信号"""
        if df.empty or len(df) < 20:
            return self.get_empty_signals(current_price)
        
        try:
            df_with_indicators = self.calculate_indicators(df)
            latest = df_with_indicators.iloc[-1]
            prev = df_with_indicators.iloc[-2] if len(df_with_indicators) > 1 else latest
            
            signals = {
                'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'price': current_price,
                'overall_signal': '中性',
                'signal_strength': 0,
                'signals': [],
                'indicators': {},
                'recommendation': '观望',
                'risk_level': '中等'
            }
            
            # MACD信号
            if not pd.isna(latest['macd']) and not pd.isna(latest['macd_signal']):
                macd_signal = self._get_macd_signal(latest, prev)
                if macd_signal['signal'] != '中性':
                    signals['signals'].append(macd_signal)
            
            # RSI信号
            if not pd.isna(latest['rsi']):
                rsi_signal = self._get_rsi_signal(latest['rsi'])
                if rsi_signal['signal'] != '中性':
                    signals['signals'].append(rsi_signal)
            
            # 布林带信号
            if not pd.isna(latest['bb_high']) and not pd.isna(latest['bb_low']):
                bb_signal = self._get_bollinger_signal(current_price, latest['bb_high'], latest['bb_low'], latest['bb_mid'])
                if bb_signal['signal'] != '中性':
                    signals['signals'].append(bb_signal)
            
            # 移动平均线信号
            if all(not pd.isna(latest[f'sma_{period}']) for period in [10, 20, 50]):
                ma_signal = self._get_ma_signal(current_price, latest['sma_10'], latest['sma_20'], latest['sma_50'])
                if ma_signal['signal'] != '中性':
                    signals['signals'].append(ma_signal)
            
            # 计算总体信号
            overall_signal = self._calculate_overall_signal(signals['signals'])
            signals['overall_signal'] = overall_signal['signal']
            signals['signal_strength'] = overall_signal['strength']
            
            # 生成投资建议
            recommendation = self._generate_recommendation(signals)
            signals['recommendation'] = recommendation['action']
            signals['risk_level'] = recommendation['risk']
            
            return signals
            
        except Exception as e:
            print(f"生成信号时出错: {e}")
            return self.get_empty_signals(current_price)
    
    def _get_macd_signal(self, latest: pd.Series, prev: pd.Series) -> Dict:
        """生成MACD信号"""
        signal = {
            'type': 'MACD',
            'signal': '中性',
            'confidence': 0,
            'description': ''
        }
        
        try:
            # MACD金叉
            if latest['macd'] > latest['macd_signal'] and prev['macd'] <= prev['macd_signal']:
                signal['signal'] = '买入'
                signal['confidence'] = 70
                signal['description'] = 'MACD金叉，短期可能上涨'
            # MACD死叉
            elif latest['macd'] < latest['macd_signal'] and prev['macd'] >= prev['macd_signal']:
                signal['signal'] = '卖出'
                signal['confidence'] = 70
                signal['description'] = 'MACD死叉，短期可能下跌'
            
        except Exception as e:
            print(f"计算MACD信号时出错: {e}")
        
        return signal
    
    def _get_rsi_signal(self, rsi_value: float) -> Dict:
        """生成RSI信号"""
        signal = {
            'type': 'RSI',
            'signal': '中性',
            'confidence': 0,
            'description': ''
        }
        
        if pd.isna(rsi_value):
            return signal
        
        if rsi_value <= 30:
            signal['signal'] = '买入'
            signal['confidence'] = 80
            signal['description'] = f'RSI超卖 ({rsi_value:.1f} < 30)，可能反弹'
        elif rsi_value >= 70:
            signal['signal'] = '卖出'
            signal['confidence'] = 80
            signal['description'] = f'RSI超买 ({rsi_value:.1f} > 70)，可能回调'
        
        return signal
    
    def _get_bollinger_signal(self, price: float, bb_high: float, bb_low: float, bb_mid: float) -> Dict:
        """生成布林带信号"""
        signal = {
            'type': '布林带',
            'signal': '中性',
            'confidence': 0,
            'description': ''
        }
        
        if pd.isna(bb_high) or pd.isna(bb_low) or pd.isna(bb_mid):
            return signal
        
        # 计算价格相对于布林带的位置
        position = (price - bb_low) / (bb_high - bb_low) * 100 if bb_high != bb_low else 50
        
        if position <= 10:
            signal['signal'] = '买入'
            signal['confidence'] = 75
            signal['description'] = f'价格接近布林带下轨，可能反弹'
        elif position >= 90:
            signal['signal'] = '卖出'
            signal['confidence'] = 75
            signal['description'] = f'价格接近布林带上轨，可能回调'
        
        return signal
    
    def _get_ma_signal(self, price: float, sma_10: float, sma_20: float, sma_50: float) -> Dict:
        """生成移动平均线信号"""
        signal = {
            'type': '移动平均线',
            'signal': '中性',
            'confidence': 0,
            'description': ''
        }
        
        if any(pd.isna(x) for x in [sma_10, sma_20, sma_50]):
            return signal
        
        # 均线排列判断
        if sma_10 > sma_20 > sma_50:
            signal['signal'] = '买入'
            signal['confidence'] = 70
            signal['description'] = '均线多头排列，趋势向上'
        elif sma_10 < sma_20 < sma_50:
            signal['signal'] = '卖出'
            signal['confidence'] = 70
            signal['description'] = '均线空头排列，趋势向下'
        
        return signal
    
    def _calculate_overall_signal(self, signals: List[Dict]) -> Dict:
        """计算总体信号"""
        if not signals:
            return {'signal': '中性', 'strength': 0}
        
        buy_signals = [s for s in signals if s['signal'] == '买入']
        sell_signals = [s for s in signals if s['signal'] == '卖出']
        
        buy_score = sum(s.get('confidence', 0) for s in buy_signals)
        sell_score = sum(s.get('confidence', 0) for s in sell_signals)
        
        total_score = buy_score + sell_score
        if total_score == 0:
            return {'signal': '中性', 'strength': 0}
        
        signal_strength = ((buy_score - sell_score) / total_score) * 100
        
        if signal_strength > 20:
            return {'signal': '买入', 'strength': int(signal_strength)}
        elif signal_strength < -20:
            return {'signal': '卖出', 'strength': int(abs(signal_strength))}
        else:
            return {'signal': '中性', 'strength': int(abs(signal_strength))}
    
    def _generate_recommendation(self, signals: Dict) -> Dict:
        """生成投资建议"""
        overall_signal = signals['overall_signal']
        signal_strength = signals['signal_strength']
        
        if overall_signal == '买入':
            if signal_strength >= 80:
                return {'action': '强烈买入', 'risk': '低'}
            elif signal_strength >= 60:
                return {'action': '建议买入', 'risk': '中低'}
            elif signal_strength >= 40:
                return {'action': '考虑买入', 'risk': '中等'}
            else:
                return {'action': '轻仓买入', 'risk': '中高'}
        elif overall_signal == '卖出':
            if signal_strength >= 80:
                return {'action': '强烈卖出', 'risk': '低'}
            elif signal_strength >= 60:
                return {'action': '建议卖出', 'risk': '中低'}
            elif signal_strength >= 40:
                return {'action': '考虑卖出', 'risk': '中等'}
            else:
                return {'action': '减仓卖出', 'risk': '中高'}
        else:
            return {'action': '观望', 'risk': '中等'}
    
    def get_empty_signals(self, current_price: float) -> Dict:
        """获取空的信号数据"""
        return {
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'price': current_price,
            'overall_signal': '中性',
            'signal_strength': 0,
            'signals': [],
            'indicators': {},
            'recommendation': '数据不足，请等待',
            'risk_level': '高'
        }