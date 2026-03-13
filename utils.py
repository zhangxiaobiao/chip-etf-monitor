import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import json
import hashlib
import time

class DataVisualizer:
    """数据可视化工具"""
    
    @staticmethod
    def create_price_chart(df: pd.DataFrame, title: str = "价格走势") -> go.Figure:
        """创建价格走势图"""
        if df.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # 添加收盘价线
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['close'],
            mode='lines',
            name='收盘价',
            line=dict(color='#2E86AB', width=2),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.1)'
        ))
        
        # 添加移动平均线
        if 'sma_10' in df.columns and not df['sma_10'].isna().all():
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['sma_10'],
                mode='lines',
                name='10日均线',
                line=dict(color='#F18F01', width=1, dash='dot')
            ))
        
        if 'sma_20' in df.columns and not df['sma_20'].isna().all():
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['sma_20'],
                mode='lines',
                name='20日均线',
                line=dict(color='#C73E1D', width=1, dash='dot')
            ))
        
        if 'sma_50' in df.columns and not df['sma_50'].isna().all():
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['sma_50'],
                mode='lines',
                name='50日均线',
                line=dict(color='#6A994E', width=1, dash='dot')
            ))
        
        # 添加布林带
        if all(col in df.columns for col in ['bb_high', 'bb_low', 'bb_mid']):
            # 上轨
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['bb_high'],
                mode='lines',
                name='布林带上轨',
                line=dict(color='rgba(128, 128, 128, 0.3)', width=1),
                showlegend=False
            ))
            
            # 下轨
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['bb_low'],
                mode='lines',
                name='布林带下轨',
                line=dict(color='rgba(128, 128, 128, 0.3)', width=1),
                fill='tonexty',
                fillcolor='rgba(128, 128, 128, 0.1)',
                showlegend=False
            ))
            
            # 中轨
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['bb_mid'],
                mode='lines',
                name='布林带中轨',
                line=dict(color='rgba(128, 128, 128, 0.5)', width=1, dash='dash'),
                showlegend=True
            ))
        
        # 更新布局
        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center'),
            xaxis_title="日期",
            yaxis_title="价格",
            hovermode='x unified',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template="plotly_white",
            height=400,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    @staticmethod
    def create_technical_chart(df: pd.DataFrame) -> go.Figure:
        """创建技术指标图"""
        if df.empty or len(df) < 20:
            return go.Figure()
        
        # 创建子图
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('价格与成交量', 'MACD', 'RSI', '布林带宽度'),
            row_heights=[0.4, 0.2, 0.2, 0.2]
        )
        
        # 1. 价格与成交量
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['close'],
            mode='lines',
            name='收盘价',
            line=dict(color='#2E86AB', width=2)
        ), row=1, col=1)
        
        # 成交量柱状图
        colors = ['green' if df['close'].iloc[i] >= df['close'].iloc[i-1] 
                 else 'red' for i in range(1, len(df))]
        colors.insert(0, 'green')  # 第一个数据点
        
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['volume'],
            name='成交量',
            marker_color=colors,
            opacity=0.5
        ), row=1, col=1)
        
        # 2. MACD
        if 'macd' in df.columns and 'macd_signal' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['macd'],
                mode='lines',
                name='MACD',
                line=dict(color='blue', width=2)
            ), row=2, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['macd_signal'],
                mode='lines',
                name='信号线',
                line=dict(color='red', width=1)
            ), row=2, col=1)
            
            # MACD柱状图
            macd_diff_colors = ['green' if x > 0 else 'red' for x in df['macd_diff']]
            fig.add_trace(go.Bar(
                x=df.index,
                y=df['macd_diff'],
                name='MACD柱',
                marker_color=macd_diff_colors,
                opacity=0.5
            ), row=2, col=1)
        
        # 3. RSI
        if 'rsi' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['rsi'],
                mode='lines',
                name='RSI',
                line=dict(color='purple', width=2)
            ), row=3, col=1)
            
            # 添加超买超卖线
            fig.add_hline(y=70, line_dash="dash", line_color="red", 
                         annotation_text="超买线", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", 
                         annotation_text="超卖线", row=3, col=1)
            fig.add_hline(y=50, line_dash="dot", line_color="gray", 
                         row=3, col=1)
        
        # 4. 布林带宽度
        if 'bb_width' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['bb_width'],
                mode='lines',
                name='布林带宽度',
                line=dict(color='orange', width=2),
                fill='tozeroy',
                fillcolor='rgba(255, 165, 0, 0.1)'
            ), row=4, col=1)
        
        # 更新布局
        fig.update_layout(
            title=dict(text="技术指标分析", x=0.5, xanchor='center'),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            template="plotly_white",
            height=800,
            margin=dict(l=50, r=50, t=100, b=50)
        )
        
        # 更新坐标轴
        fig.update_xaxes(rangeslider_visible=False, row=4, col=1)
        
        return fig
    
    @staticmethod
    def create_signal_gauge(signal_strength: int, signal_type: str) -> go.Figure:
        """创建信号强度仪表盘"""
        # 根据信号类型设置颜色
        if signal_type == '买入':
            colors = ['red', 'yellow', 'green']
            range_val = [0, 100]
        elif signal_type == '卖出':
            colors = ['green', 'yellow', 'red']
            range_val = [0, 100]
        else:  # 中性
            colors = ['gray', 'gray', 'gray']
            range_val = [0, 100]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=signal_strength,
            title={'text': f"{signal_type}信号强度"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': range_val},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 33], 'color': colors[0]},
                    {'range': [33, 66], 'color': colors[1]},
                    {'range': [66, 100], 'color': colors[2]}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': signal_strength
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig

class NotificationManager:
    """通知管理器"""
    
    def __init__(self, telegram_bot_token: str = None, telegram_chat_id: str = None):
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.notification_history = []
    
    def send_telegram_message(self, message: str) -> bool:
        """发送Telegram消息"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            return False
        
        try:
            import requests
            
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                self._log_notification('telegram', message, True)
                return True
            else:
                print(f"Telegram发送失败: {response.status_code}")
                self._log_notification('telegram', message, False)
                return False
                
        except Exception as e:
            print(f"Telegram发送异常: {e}")
            self._log_notification('telegram', message, False)
            return False
    
    def send_alert(self, alert_type: str, data: Dict, threshold: float = None) -> bool:
        """发送警报"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if alert_type == 'price_change':
            message = self._format_price_alert(data, threshold)
        elif alert_type == 'signal':
            message = self._format_signal_alert(data)
        elif alert_type == 'system':
            message = self._format_system_alert(data)
        else:
            message = f"警报: {alert_type}\n数据: {json.dumps(data, ensure_ascii=False, indent=2)}"
        
        # 添加时间戳
        message = f"⏰ {timestamp}\n{message}"
        
        # 发送到Telegram
        telegram_sent = self.send_telegram_message(message)
        
        # 同时在控制台输出
        print(f"\n{'='*50}")
        print(message)
        print(f"{'='*50}\n")
        
        return telegram_sent
    
    def _format_price_alert(self, data: Dict, threshold: float) -> str:
        """格式化价格变动警报"""
        symbol = data.get('symbol', '未知')
        price = data.get('price', 0)
        change_percent = data.get('change_percent', 0)
        
        if change_percent > 0:
            emoji = "📈"
            direction = "上涨"
        else:
            emoji = "📉"
            direction = "下跌"
        
        return f"{emoji} <b>价格变动警报</b>\n\n" \
               f"股票: {symbol}\n" \
               f"价格: {price:.3f}\n" \
               f"涨跌幅: {change_percent:+.2f}%\n" \
               f"状态: {direction}超过{abs(threshold)}%阈值"
    
    def _format_signal_alert(self, data: Dict) -> str:
        """格式化买卖信号警报"""
        signal = data.get('overall_signal', '中性')
        strength = data.get('signal_strength', 0)
        price = data.get('price', 0)
        recommendation = data.get('recommendation', '观望')
        
        if signal == '买入':
            emoji = "🟢"
        elif signal == '卖出':
            emoji = "🔴"
        else:
            emoji = "🟡"
        
        # 收集具体信号
        signals_list = data.get('signals', [])
        signals_text = "\n".join([f"- {s['type']}: {s['description']}" 
                                 for s in signals_list[:3]])  # 只显示前3个
        
        return f"{emoji} <b>买卖信号警报</b>\n\n" \
               f"信号类型: {signal}\n" \
               f"信号强度: {strength}/100\n" \
               f"当前价格: {price:.3f}\n" \
               f"建议操作: {recommendation}\n\n" \
               f"具体信号:\n{signals_text}"
    
    def _format_system_alert(self, data: Dict) -> str:
        """格式化系统警报"""
        alert_type = data.get('type', '系统通知')
        message = data.get('message', '')
        
        return f"🛠 <b>{alert_type}</b>\n\n{message}"
    
    def _log_notification(self, channel: str, message: str, success: bool):
        """记录通知历史"""
        self.notification_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'channel': channel,
            'message': message[:100],  # 只保存前100个字符
            'success': success
        })
        
        # 只保留最近50条记录
        if len(self.notification_history) > 50:
            self.notification_history = self.notification_history[-50:]
    
    def get_notification_stats(self) -> Dict:
        """获取通知统计信息"""
        if not self.notification_history:
            return {
                'total': 0,
                'success': 0,
                'failure': 0,
                'success_rate': 0,
                'last_notification': '无记录'
            }
        
        total = len(self.notification_history)
        success = sum(1 for n in self.notification_history if n['success'])
        failure = total - success
        success_rate = (success / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'success': success,
            'failure': failure,
            'success_rate': round(success_rate, 1),
            'last_notification': self.notification_history[-1]['timestamp']
        }

class DataProcessor:
    """数据处理工具"""
    
    @staticmethod
    def calculate_statistics(df: pd.DataFrame) -> Dict:
        """计算统计指标"""
        if df.empty:
            return {}
        
        stats = {
            'current_price': float(df['close'].iloc[-1]) if len(df) > 0 else 0,
            'price_change': 0,
            'price_change_percent': 0,
            'volume': 0,
            'high': 0,
            'low': 0,
            'volatility': 0,
            'trend': 'unknown'
        }
        
        if len(df) >= 2:
            current = df['close'].iloc[-1]
            previous = df['close'].iloc[-2]
            
            stats['price_change'] = float(current - previous)
            stats['price_change_percent'] = float((current - previous) / previous * 100) if previous != 0 else 0
        
        if len(df) > 0:
            stats['volume'] = int(df['volume'].iloc[-1]) if 'volume' in df.columns else 0
            stats['high'] = float(df['high'].max()) if 'high' in df.columns else 0
            stats['low'] = float(df['low'].min()) if 'low' in df.columns else 0
            
            # 计算波动率
            if 'close' in df.columns and len(df) > 1:
                returns = df['close'].pct_change().dropna()
                if len(returns) > 0:
                    stats['volatility'] = float(returns.std() * np.sqrt(252))  # 年化波动率
        
        # 判断趋势
        if len(df) >= 10:
            recent_prices = df['close'].tail(10).values
            if recent_prices[-1] > recent_prices[0]:
                stats['trend'] = 'up'
            elif recent_prices[-1] < recent_prices[0]:
                stats['trend'] = 'down'
            else:
                stats['trend'] = 'sideways'
        
        return stats
    
    @staticmethod
    def detect_patterns(df: pd.DataFrame) -> List[Dict]:
        """检测价格形态"""
        patterns = []
        
        if df.empty or len(df) < 10:
            return patterns
        
        prices = df['close'].values
        
        # 检测双底形态
        if len(prices) >= 20:
            # 简单检测：最近20个交易日中的最低点
            min_idx = np.argmin(prices[-20:])
            if min_idx < 15:  # 最低点在15天前
                recent_low = prices[-20 + min_idx]
                # 检查是否形成双底
                if abs(prices[-1] - recent_low) / recent_low < 0.05:  # 价格接近前期低点
                    patterns.append({
                        'type': 'double_bottom',
                        'confidence': 60,
                        'description': '可能形成双底形态'
                    })
        
        # 检测突破
        if len(df) >= 20 and 'sma_20' in df.columns:
            current_price = prices[-1]
            sma_20 = df['sma_20'].iloc[-1]
            
            if not pd.isna(sma_20):
                if current_price > sma_20 * 1.02:  # 突破20日均线2%
                    patterns.append({
                        'type': 'breakout_above_ma',
                        'confidence': 70,
                        'description': '价格突破20日均线'
                    })
                elif current_price < sma_20 * 0.98:  # 跌破20日均线2%
                    patterns.append({
                        'type': 'breakdown_below_ma',
                        'confidence': 70,
                        'description': '价格跌破20日均线'
                    })
        
        return patterns
    
    @staticmethod
    def generate_report(data: Dict, signals: Dict) -> str:
        """生成分析报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"📊 科创芯片ETF (588200) 分析报告\n"
        report += f"生成时间: {timestamp}\n"
        report += f"{'='*50}\n\n"
        
        # 当前行情
        report += f"📈 当前行情:\n"
        report += f"- 当前价格: {data.get('price', 0):.3f}\n"
        report += f"- 涨跌幅: {data.get('change_percent', 0):+.2f}%\n"
        report += f"- 成交量: {data.get('volume', 0):,}\n"
        report += f"- 最高价: {data.get('high', 0):.3f}\n"
        report += f"- 最低价: {data.get('low', 0):.3f}\n\n"
        
        # 买卖信号
        report += f"🚦 买卖信号:\n"
        report += f"- 总体信号: {signals.get('overall_signal', '中性')}\n"
        report += f"- 信号强度: {signals.get('signal_strength', 0)}/100\n"
        report += f"- 操作建议: {signals.get('recommendation', '观望')}\n"
        report += f"- 风险等级: {signals.get('risk_level', '中等')}\n\n"
        
        # 具体信号
        signal_list = signals.get('signals', [])
        if signal_list:
            report += f"🔍 具体技术信号:\n"
            for signal in signal_list[:5]:  # 最多显示5个
                report += f"- {signal['type']}: {signal['description']}\n"
            report += "\n"
        
        # 指标状态
        indicators = signals.get('indicators', {})
        if indicators:
            report += f"📊 技术指标状态:\n"
            for key, value in indicators.items():
                if isinstance(value, dict):
                    report += f"- {key}: {value}\n"
        
        return report