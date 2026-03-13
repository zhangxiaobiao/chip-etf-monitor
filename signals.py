import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import ta
from datetime import datetime
from config import (
    RSI_OVERBOUGHT, RSI_OVERSOLD, MACD_FAST, MACD_SLOW, MACD_SIGNAL,
    BBANDS_PERIOD, BBANDS_STD
)

class SignalGenerator:
    """买卖信号生成器"""
    
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
        df['macd'] = ta.trend.macd(df['close'], window_slow=MACD_SLOW, window_fast=MACD_FAST)
        df['macd_signal'] = ta.trend.macd_signal(df['close'], window_slow=MACD_SLOW, window_fast=MACD_FAST, window_sign=MACD_SIGNAL)
        df['macd_diff'] = ta.trend.macd_diff(df['close'], window_slow=MACD_SLOW, window_fast=MACD_FAST, window_sign=MACD_SIGNAL)
        
        # RSI
        df['rsi'] = ta.momentum.rsi(df['close'], window=14)
        
        # 布林带
        bollinger = ta.volatility.BollingerBands(df['close'], window=BBANDS_PERIOD, window_dev=BBANDS_STD)
        df['bb_high'] = bollinger.bollinger_hband()
        df['bb_low'] = bollinger.bollinger_lband()
        df['bb_mid'] = bollinger.bollinger_mavg()
        df['bb_width'] = (df['bb_high'] - df['bb_low']) / df['bb_mid'] * 100
        
        # 成交量指标
        df['volume_sma'] = ta.trend.sma_indicator(df['volume'], window=20)
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        # ATR (平均真实波动范围)
        df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)
        
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
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'price': current_price,
                'overall_signal': '中性',
                'signal_strength': 0,
                'signals': [],
                'indicators': {},
                'recommendation': '观望',
                'risk_level': '中等'
            }
            
            # 收集指标值
            indicators = {}
            
            # MACD信号
            if not pd.isna(latest['macd']) and not pd.isna(latest['macd_signal']):
                macd_signal = self._get_macd_signal(latest, prev)
                if macd_signal['signal'] != '中性':
                    signals['signals'].append(macd_signal)
                indicators['macd'] = {
                    'value': round(latest['macd'], 3),
                    'signal': latest['macd_signal'],
                    'diff': round(latest['macd_diff'], 3)
                }
            
            # RSI信号
            if not pd.isna(latest['rsi']):
                rsi_signal = self._get_rsi_signal(latest['rsi'])
                if rsi_signal['signal'] != '中性':
                    signals['signals'].append(rsi_signal)
                indicators['rsi'] = {
                    'value': round(latest['rsi'], 2),
                    'overbought': RSI_OVERBOUGHT,
                    'oversold': RSI_OVERSOLD
                }
            
            # 布林带信号
            if not pd.isna(latest['bb_high']) and not pd.isna(latest['bb_low']):
                bb_signal = self._get_bollinger_signal(current_price, latest['bb_high'], latest['bb_low'], latest['bb_mid'])
                if bb_signal['signal'] != '中性':
                    signals['signals'].append(bb_signal)
                indicators['bollinger'] = {
                    'upper': round(latest['bb_high'], 3),
                    'middle': round(latest['bb_mid'], 3),
                    'lower': round(latest['bb_low'], 3),
                    'width': round(latest['bb_width'], 2)
                }
            
            # 移动平均线信号
            if all(not pd.isna(latest[f'sma_{period}']) for period in [10, 20, 50]):
                ma_signal = self._get_ma_signal(current_price, latest['sma_10'], latest['sma_20'], latest['sma_50'])
                if ma_signal['signal'] != '中性':
                    signals['signals'].append(ma_signal)
                indicators['moving_averages'] = {
                    'sma_10': round(latest['sma_10'], 3),
                    'sma_20': round(latest['sma_20'], 3),
                    'sma_50': round(latest['sma_50'], 3)
                }
            
            # 成交量信号
            if not pd.isna(latest['volume_ratio']):
                volume_signal = self._get_volume_signal(latest['volume_ratio'])
                if volume_signal['signal'] != '中性':
                    signals['signals'].append(volume_signal)
                indicators['volume'] = {
                    'ratio': round(latest['volume_ratio'], 2),
                    'volume': int(latest['volume'])
                }
            
            # 计算总体信号
            overall_signal = self._calculate_overall_signal(signals['signals'])
            signals['overall_signal'] = overall_signal['signal']
            signals['signal_strength'] = overall_signal['strength']
            signals['indicators'] = indicators
            
            # 生成投资建议
            recommendation = self._generate_recommendation(signals)
            signals['recommendation'] = recommendation['action']
            signals['risk_level'] = recommendation['risk']
            
            # 保存信号历史
            self.signals_history.append({
                'timestamp': signals['timestamp'],
                'price': signals['price'],
                'signal': signals['overall_signal'],
                'strength': signals['signal_strength']
            })
            
            # 只保留最近100条记录
            if len(self.signals_history) > 100:
                self.signals_history = self.signals_history[-100:]
            
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
            # MACD向上
            elif latest['macd'] > 0 and latest['macd_diff'] > 0:
                signal['signal'] = '买入'
                signal['confidence'] = 60
                signal['description'] = 'MACD在零轴上方，趋势向上'
            # MACD向下
            elif latest['macd'] < 0 and latest['macd_diff'] < 0:
                signal['signal'] = '卖出'
                signal['confidence'] = 60
                signal['description'] = 'MACD在零轴下方，趋势向下'
            
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
        
        if rsi_value <= RSI_OVERSOLD:
            signal['signal'] = '买入'
            signal['confidence'] = 80
            signal['description'] = f'RSI超卖 ({rsi_value:.1f} < {RSI_OVERSOLD})，可能反弹'
        elif rsi_value >= RSI_OVERBOUGHT:
            signal['signal'] = '卖出'
            signal['confidence'] = 80
            signal['description'] = f'RSI超买 ({rsi_value:.1f} > {RSI_OVERBOUGHT})，可能回调'
        elif rsi_value < 45:
            signal['signal'] = '买入'
            signal['confidence'] = 60
            signal['description'] = 'RSI偏弱，可能有上涨机会'
        elif rsi_value > 55:
            signal['signal'] = '卖出'
            signal['confidence'] = 60
            signal['description'] = 'RSI偏强，可能有下跌风险'
        
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
        
        if position <= 10:  # 价格接近下轨
            signal['signal'] = '买入'
            signal['confidence'] = 75
            signal['description'] = f'价格接近布林带下轨({position:.1f}%)，可能反弹'
        elif position >= 90:  # 价格接近上轨
            signal['signal'] = '卖出'
            signal['confidence'] = 75
            signal['description'] = f'价格接近布林带上轨({position:.1f}%)，可能回调'
        elif price > bb_mid:
            signal['signal'] = '买入'
            signal['confidence'] = 60
            signal['description'] = '价格在布林带中轨上方，趋势向上'
        elif price < bb_mid:
            signal['signal'] = '卖出'
            signal['confidence'] = 60
            signal['description'] = '价格在布林带中轨下方，趋势向下'
        
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
        if sma_10 > sma_20 > sma_50:  # 多头排列
            signal['signal'] = '买入'
            signal['confidence'] = 70
            signal['description'] = '均线多头排列，趋势向上'
        elif sma_10 < sma_20 < sma_50:  # 空头排列
            signal['signal'] = '卖出'
            signal['confidence'] = 70
            signal['description'] = '均线空头排列，趋势向下'
        elif price > sma_10 > sma_20:  # 价格在所有均线上方
            signal['signal'] = '买入'
            signal['confidence'] = 65
            signal['description'] = '价格在所有均线上方，强势'
        elif price < sma_10 < sma_20:  # 价格在所有均线下方
            signal['signal'] = '卖出'
            signal['confidence'] = 65
            signal['description'] = '价格在所有均线下方，弱势'
        
        return signal
    
    def _get_volume_signal(self, volume_ratio: float) -> Dict:
        """生成成交量信号"""
        signal = {
            'type': '成交量',
            'signal': '中性',
            'confidence': 0,
            'description': ''
        }
        
        if pd.isna(volume_ratio):
            return signal
        
        if volume_ratio > 1.5:  # 成交量放大
            signal['signal'] = '买入'
            signal['confidence'] = 65
            signal['description'] = f'成交量放大{volume_ratio:.1f}倍，关注突破'
        elif volume_ratio < 0.7:  # 成交量萎缩
            signal['signal'] = '卖出'
            signal['confidence'] = 55
            signal['description'] = f'成交量萎缩{volume_ratio:.1f}倍，动能不足'
        
        return signal
    
    def _calculate_overall_signal(self, signals: List[Dict]) -> Dict:
        """计算总体信号"""
        if not signals:
            return {'signal': '中性', 'strength': 0}
        
        # 计算信号强度
        buy_signals = [s for s in signals if s['signal'] == '买入']
        sell_signals = [s for s in signals if s['signal'] == '卖出']
        
        buy_score = sum(s.get('confidence', 0) for s in buy_signals)
        sell_score = sum(s.get('confidence', 0) for s in sell_signals)
        
        total_score = buy_score + sell_score
        if total_score == 0:
            return {'signal': '中性', 'strength': 0}
        
        # 计算信号强度（-100到100）
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
        
        recommendations = {
            '买入': [
                {'threshold': 80, 'action': '强烈买入', 'risk': '低'},
                {'threshold': 60, 'action': '建议买入', 'risk': '中低'},
                {'threshold': 40, 'action': '考虑买入', 'risk': '中等'},
                {'threshold': 20, 'action': '轻仓买入', 'risk': '中高'}
            ],
            '卖出': [
                {'threshold': 80, 'action': '强烈卖出', 'risk': '低'},
                {'threshold': 60, 'action': '建议卖出', 'risk': '中低'},
                {'threshold': 40, 'action': '考虑卖出', 'risk': '中等'},
                {'threshold': 20, 'action': '减仓卖出', 'risk': '中高'}
            ],
            '中性': [
                {'threshold': 0, 'action': '观望', 'risk': '中等'}
            ]
        }
        
        if overall_signal in recommendations:
            for rec in recommendations[overall_signal]:
                if signal_strength >= rec['threshold']:
                    return {'action': rec['action'], 'risk': rec['risk']}
        
        return {'action': '观望', 'risk': '中等'}
    
    def get_empty_signals(self, current_price: float) -> Dict:
        """获取空的信号数据"""
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'price': current_price,
            'overall_signal': '中性',
            'signal_strength': 0,
            'signals': [],
            'indicators': {},
            'recommendation': '数据不足，请等待',
            'risk_level': '高'
        }
    
    def get_signals_summary(self) -> Dict:
        """获取信号摘要"""
        if not self.signals_history:
            return {
                'total_signals': 0,
                'buy_signals': 0,
                'sell_signals': 0,
                'neutral_signals': 0,
                'latest_signal': '无历史信号',
                'signal_accuracy': 0  # 需要实际交易数据才能计算准确率
            }
        
        latest = self.signals_history[-1]
        buy_count = sum(1 for s in self.signals_history if s['signal'] == '买入')
        sell_count = sum(1 for s in self.signals_history if s['signal'] == '卖出')
        neutral_count = sum(1 for s in self.signals_history if s['signal'] == '中性')
        
        return {
            'total_signals': len(self.signals_history),
            'buy_signals': buy_count,
            'sell_signals': sell_count,
            'neutral_signals': neutral_count,
            'latest_signal': f"{latest['signal']} (强度: {latest['strength']})",
            'signal_accuracy': 0  # 占位符
        }