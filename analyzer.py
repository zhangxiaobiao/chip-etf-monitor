#!/usr/bin/env python3
"""
科创芯片ETF (588200) 数据分析工具
用于离线分析和回测
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher
from signals import SignalGenerator
from utils import DataVisualizer, DataProcessor
from config import STOCK_SYMBOL, STOCK_NAME, CHECK_HISTORY_DAYS

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class StockAnalyzer:
    """股票数据分析器"""
    
    def __init__(self, symbol: str = STOCK_SYMBOL):
        self.symbol = symbol
        self.data_fetcher = DataFetcher(symbol)
        self.signal_generator = SignalGenerator()
        self.visualizer = DataVisualizer()
        self.data_processor = DataProcessor()
        
        print(f"📊 股票分析器初始化完成 - {STOCK_NAME} ({symbol})")
    
    def fetch_data(self, days: int = CHECK_HISTORY_DAYS) -> pd.DataFrame:
        """获取数据"""
        print(f"正在获取 {days} 天的历史数据...")
        
        data = self.data_fetcher.get_historical_data(days=days)
        
        if data.empty:
            print("❌ 数据获取失败")
            return pd.DataFrame()
        
        print(f"✅ 数据获取成功: {len(data)} 条记录")
        print(f"数据时间范围: {data.index[0]} 到 {data.index[-1]}")
        
        return data
    
    def analyze_basic_statistics(self, df: pd.DataFrame):
        """分析基本统计信息"""
        if df.empty:
            print("数据为空，无法分析")
            return
        
        print("\n" + "="*60)
        print("📈 基本统计分析")
        print("="*60)
        
        # 价格统计
        price_stats = df['close'].describe()
        print(f"价格统计:")
        print(f"  最小值: {price_stats['min']:.3f}")
        print(f"  最大值: {price_stats['max']:.3f}")
        print(f"  平均值: {price_stats['mean']:.3f}")
        print(f"  标准差: {price_stats['std']:.3f}")
        print(f"  25%分位数: {price_stats['25%']:.3f}")
        print(f"  50%分位数: {price_stats['50%']:.3f}")
        print(f"  75%分位数: {price_stats['75%']:.3f}")
        
        # 涨跌幅统计
        returns = df['close'].pct_change().dropna()
        if len(returns) > 0:
            print(f"\n涨跌幅统计:")
            print(f"  平均日收益: {returns.mean() * 100:.4f}%")
            print(f"  日收益标准差: {returns.std() * 100:.4f}%")
            print(f"  最大单日涨幅: {returns.max() * 100:.4f}%")
            print(f"  最大单日跌幅: {returns.min() * 100:.4f}%")
            print(f"  正收益天数: {sum(returns > 0)}")
            print(f"  负收益天数: {sum(returns < 0)}")
            
            # 夏普比率（假设无风险利率为0）
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
            print(f"  年化夏普比率: {sharpe_ratio:.4f}")
        
        # 成交量统计
        if 'volume' in df.columns:
            volume_stats = df['volume'].describe()
            print(f"\n成交量统计:")
            print(f"  平均成交量: {volume_stats['mean']:,.0f}")
            print(f"  最大成交量: {volume_stats['max']:,.0f}")
            print(f"  最小成交量: {volume_stats['min']:,.0f}")
    
    def analyze_technical_indicators(self, df: pd.DataFrame):
        """分析技术指标"""
        if df.empty or len(df) < 20:
            print("数据不足，无法分析技术指标")
            return
        
        print("\n" + "="*60)
        print("📊 技术指标分析")
        print("="*60)
        
        # 计算技术指标
        df_with_indicators = self.signal_generator.calculate_indicators(df)
        
        # MACD分析
        if 'macd' in df_with_indicators.columns and 'macd_signal' in df_with_indicators.columns:
            macd_cross_up = ((df_with_indicators['macd'] > df_with_indicators['macd_signal']) & 
                            (df_with_indicators['macd'].shift(1) <= df_with_indicators['macd_signal'].shift(1)))
            macd_cross_down = ((df_with_indicators['macd'] < df_with_indicators['macd_signal']) & 
                              (df_with_indicators['macd'].shift(1) >= df_with_indicators['macd_signal'].shift(1)))
            
            print(f"MACD分析:")
            print(f"  MACD金叉次数: {macd_cross_up.sum()}")
            print(f"  MACD死叉次数: {macd_cross_down.sum()}")
            print(f"  当前MACD值: {df_with_indicators['macd'].iloc[-1]:.4f}")
            print(f"  当前信号线值: {df_with_indicators['macd_signal'].iloc[-1]:.4f}")
            print(f"  当前差值: {df_with_indicators['macd_diff'].iloc[-1]:.4f}")
        
        # RSI分析
        if 'rsi' in df_with_indicators.columns:
            rsi_values = df_with_indicators['rsi'].dropna()
            if len(rsi_values) > 0:
                print(f"\nRSI分析:")
                print(f"  当前RSI值: {rsi_values.iloc[-1]:.2f}")
                print(f"  RSI平均值: {rsi_values.mean():.2f}")
                print(f"  RSI标准差: {rsi_values.std():.2f}")
                print(f"  超买天数(RSI>70): {(rsi_values > 70).sum()}")
                print(f"  超卖天数(RSI<30): {(rsi_values < 30).sum()}")
        
        # 布林带分析
        if all(col in df_with_indicators.columns for col in ['bb_high', 'bb_low', 'bb_mid']):
            current_price = df_with_indicators['close'].iloc[-1]
            bb_high = df_with_indicators['bb_high'].iloc[-1]
            bb_low = df_with_indicators['bb_low'].iloc[-1]
            bb_mid = df_with_indicators['bb_mid'].iloc[-1]
            
            print(f"\n布林带分析:")
            print(f"  当前价格: {current_price:.3f}")
            print(f"  布林带上轨: {bb_high:.3f}")
            print(f"  布林带中轨: {bb_mid:.3f}")
            print(f"  布林带下轨: {bb_low:.3f}")
            print(f"  带宽: {(bb_high - bb_low):.3f}")
            print(f"  相对位置: {((current_price - bb_low) / (bb_high - bb_low) * 100):.1f}%")
            
            # 统计触及布林带的次数
            touch_upper = (df_with_indicators['close'] >= df_with_indicators['bb_high'] * 0.99).sum()
            touch_lower = (df_with_indicators['close'] <= df_with_indicators['bb_low'] * 1.01).sum()
            print(f"  触及上轨次数: {touch_upper}")
            print(f"  触及下轨次数: {touch_lower}")
    
    def analyze_signals(self, df: pd.DataFrame):
        """分析买卖信号"""
        if df.empty or len(df) < 20:
            print("数据不足，无法分析买卖信号")
            return
        
        print("\n" + "="*60)
        print("🚦 买卖信号分析")
        print("="*60)
        
        # 生成历史信号
        signals_history = []
        for i in range(20, len(df)):
            historical_slice = df.iloc[:i]
            current_price = df['close'].iloc[i-1]
            
            signals = self.signal_generator.generate_signals(historical_slice, current_price)
            signals_history.append({
                'date': df.index[i-1],
                'price': current_price,
                'signal': signals['overall_signal'],
                'strength': signals['signal_strength'],
                'recommendation': signals['recommendation']
            })
        
        if not signals_history:
            print("未生成有效信号")
            return
        
        # 转换为DataFrame
        signals_df = pd.DataFrame(signals_history)
        
        # 信号统计
        print(f"信号统计:")
        print(f"  总信号数: {len(signals_df)}")
        print(f"  买入信号: {(signals_df['signal'] == '买入').sum()}")
        print(f"  卖出信号: {(signals_df['signal'] == '卖出').sum()}")
        print(f"  中性信号: {(signals_df['signal'] == '中性').sum()}")
        
        # 信号强度分析
        print(f"\n信号强度分析:")
        print(f"  平均强度: {signals_df['strength'].mean():.1f}")
        print(f"  最大强度: {signals_df['strength'].max():.1f}")
        print(f"  最小强度: {signals_df['strength'].min():.1f}")
        
        # 信号后的表现（简单回测）
        if len(signals_df) > 1:
            print(f"\n信号后表现分析:")
            
            buy_signals = signals_df[signals_df['signal'] == '买入']
            sell_signals = signals_df[signals_df['signal'] == '卖出']
            
            if len(buy_signals) > 0:
                # 买入信号后的平均收益
                buy_returns = []
                for idx, row in buy_signals.iterrows():
                    signal_date = row['date']
                    signal_price = row['price']
                    
                    # 找到信号后的下一个交易日
                    future_dates = signals_df[signals_df['date'] > signal_date]
                    if len(future_dates) > 0:
                        future_price = future_dates.iloc[0]['price']
                        return_pct = (future_price - signal_price) / signal_price * 100
                        buy_returns.append(return_pct)
                
                if buy_returns:
                    print(f"  买入信号后平均收益: {np.mean(buy_returns):.2f}%")
                    print(f"  买入信号后最大收益: {np.max(buy_returns):.2f}%")
                    print(f"  买入信号后最小收益: {np.min(buy_returns):.2f}%")
            
            if len(sell_signals) > 0:
                # 卖出信号后的平均收益
                sell_returns = []
                for idx, row in sell_signals.iterrows():
                    signal_date = row['date']
                    signal_price = row['price']
                    
                    # 找到信号后的下一个交易日
                    future_dates = signals_df[signals_df['date'] > signal_date]
                    if len(future_dates) > 0:
                        future_price = future_dates.iloc[0]['price']
                        return_pct = (future_price - signal_price) / signal_price * 100
                        sell_returns.append(return_pct)
                
                if sell_returns:
                    print(f"  卖出信号后平均收益: {np.mean(sell_returns):.2f}%")
                    print(f"  卖出信号后最大收益: {np.max(sell_returns):.2f}%")
                    print(f"  卖出信号后最小收益: {np.min(sell_returns):.2f}%")
    
    def generate_visualizations(self, df: pd.DataFrame, output_dir: str = "analysis_output"):
        """生成可视化图表"""
        if df.empty:
            print("数据为空，无法生成图表")
            return
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"\n正在生成可视化图表到目录: {output_dir}")
        
        # 计算技术指标
        df_with_indicators = self.signal_generator.calculate_indicators(df)
        
        # 1. 价格走势图
        fig_price = self.visualizer.create_price_chart(df_with_indicators, f"{STOCK_NAME} 价格走势")
        fig_price.write_html(os.path.join(output_dir, "price_chart.html"))
        fig_price.write_image(os.path.join(output_dir, "price_chart.png"), width=1200, height=600)
        
        # 2. 技术分析图
        fig_technical = self.visualizer.create_technical_chart(df_with_indicators)
        fig_technical.write_html(os.path.join(output_dir, "technical_chart.html"))
        
        # 3. 收益分布直方图
        plt.figure(figsize=(10, 6))
        returns = df['close'].pct_change().dropna() * 100
        
        plt.hist(returns, bins=50, edgecolor='black', alpha=0.7)
        plt.title(f'{STOCK_NAME} 日收益分布', fontsize=16)
        plt.xlabel('日收益 (%)', fontsize=12)
        plt.ylabel('频数', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # 添加统计信息
        stats_text = f'平均值: {returns.mean():.2f}%\n标准差: {returns.std():.2f}%\n'
        stats_text += f'偏度: {returns.skew():.2f}\n峰度: {returns.kurtosis():.2f}'
        plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "returns_distribution.png"), dpi=300)
        plt.close()
        
        # 4. 移动平均线图
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['close'], label='收盘价', linewidth=2)
        
        if 'sma_10' in df_with_indicators.columns:
            plt.plot(df_with_indicators.index, df_with_indicators['sma_10'], label='10日均线', linestyle='--')
        if 'sma_20' in df_with_indicators.columns:
            plt.plot(df_with_indicators.index, df_with_indicators['sma_20'], label='20日均线', linestyle='--')
        if 'sma_50' in df_with_indicators.columns:
            plt.plot(df_with_indicators.index, df_with_indicators['sma_50'], label='50日均线', linestyle='--')
        
        plt.title(f'{STOCK_NAME} 移动平均线分析', fontsize=16)
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('价格', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "moving_averages.png"), dpi=300)
        plt.close()
        
        # 5. 相关性热图
        if len(df_with_indicators.columns) > 5:
            numeric_cols = df_with_indicators.select_dtypes(include=[np.number]).columns
            corr_matrix = df_with_indicators[numeric_cols].corr()
            
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                       center=0, square=True, linewidths=0.5)
            plt.title(f'{STOCK_NAME} 技术指标相关性热图', fontsize=16)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), dpi=300)
            plt.close()
        
        print(f"✅ 图表生成完成: {output_dir}")
    
    def generate_report(self, df: pd.DataFrame, output_file: str = "analysis_report.txt"):
        """生成分析报告"""
        if df.empty:
            print("数据为空，无法生成报告")
            return
        
        print(f"\n正在生成分析报告: {output_file}")
        
        report = f"{'='*60}\n"
        report += f"科创芯片ETF (588200) 分析报告\n"
        report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"{'='*60}\n\n"
        
        # 基本统计
        report += "📈 基本统计分析\n"
        report += "-" * 40 + "\n"
        
        price_stats = df['close'].describe()
        report += f"价格统计:\n"
        report += f"  数据点数: {len(df)}\n"
        report += f"  时间范围: {df.index[0]} 到 {df.index[-1]}\n"
        report += f"  最低价: {price_stats['min']:.3f}\n"
        report += f"  最高价: {price_stats['max']:.3f}\n"
        report += f"  平均价: {price_stats['mean']:.3f}\n"
        report += f"  标准差: {price_stats['std']:.3f}\n\n"
        
        # 收益统计
        returns = df['close'].pct_change().dropna()
        if len(returns) > 0:
            report += f"收益统计:\n"
            report += f"  平均日收益: {returns.mean() * 100:.4f}%\n"
            report += f"  日收益标准差: {returns.std() * 100:.4f}%\n"
            report += f"  夏普比率: {returns.mean() / returns.std() * np.sqrt(252):.4f}\n"
            report += f"  正收益天数: {sum(returns > 0)} ({sum(returns > 0)/len(returns)*100:.1f}%)\n"
            report += f"  负收益天数: {sum(returns < 0)} ({sum(returns < 0)/len(returns)*100:.1f}%)\n\n"
        
        # 技术指标
        df_with_indicators = self.signal_generator.calculate_indicators(df)
        if not df_with_indicators.empty:
            report += "📊 技术指标分析\n"
            report += "-" * 40 + "\n"
            
            latest = df_with_indicators.iloc[-1]
            
            if 'rsi' in df_with_indicators.columns and not pd.isna(latest['rsi']):
                report += f"RSI: {latest['rsi']:.2f}\n"
            
            if 'macd' in df_with_indicators.columns and not pd.isna(latest['macd']):
                report += f"MACD: {latest['macd']:.4f}\n"
                report += f"MACD信号线: {latest['macd_signal']:.4f}\n"
                report += f"MACD差值: {latest['macd_diff']:.4f}\n"
            
            if all(col in df_with_indicators.columns for col in ['bb_high', 'bb_low', 'bb_mid']):
                report += f"布林带上轨: {latest['bb_high']:.3f}\n"
                report += f"布林带中轨: {latest['bb_mid']:.3f}\n"
                report += f"布林带下轨: {latest['bb_low']:.3f}\n"
                report += f"布林带宽度: {latest['bb_width']:.2f}%\n\n"
        
        # 买卖信号
        current_price = df['close'].iloc[-1]
        signals = self.signal_generator.generate_signals(df, current_price)
        
        report += "🚦 买卖信号分析\n"
        report += "-" * 40 + "\n"
        report += f"当前价格: {current_price:.3f}\n"
        report += f"总体信号: {signals['overall_signal']}\n"
        report += f"信号强度: {signals['signal_strength']}/100\n"
        report += f"操作建议: {signals['recommendation']}\n"
        report += f"风险等级: {signals['risk_level']}\n\n"
        
        # 具体信号
        signal_list = signals.get('signals', [])
        if signal_list:
            report += "具体技术信号:\n"
            for signal in signal_list:
                report += f"  - {signal['type']}: {signal['description']}\n"
            report += "\n"
        
        # 投资建议
        report += "💡 投资建议\n"
        report += "-" * 40 + "\n"
        
        if signals['overall_signal'] == '买入':
            if signals['signal_strength'] >= 80:
                report += "建议: 强烈买入，信号明确，风险较低\n"
            elif signals['signal_strength'] >= 60:
                report += "建议: 积极买入，信号较强\n"
            else:
                report += "建议: 谨慎买入，信号较弱\n"
        elif signals['overall_signal'] == '卖出':
            if signals['signal_strength'] >= 80:
                report += "建议: 强烈卖出，信号明确\n"
            elif signals['signal_strength'] >= 60:
                report += "建议: 积极卖出，信号较强\n"
            else:
                report += "建议: 谨慎卖出，信号较弱\n"
        else:
            report += "建议: 观望，等待明确信号\n"
        
        report += f"\n风险提示: {signals['risk_level']}风险\n"
        
        # 免责声明
        report += f"\n{'='*60}\n"
        report += "免责声明:\n"
        report += "本报告为技术分析工具生成，仅供参考。\n"
        report += "不构成投资建议，投资者应独立判断并承担风险。\n"
        report += f"{'='*60}\n"
        
        # 保存报告
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 分析报告生成完成: {output_file}")
        
        # 在控制台显示报告摘要
        print("\n报告摘要:")
        print("-" * 40)
        lines = report.split('\n')
        for line in lines[:30]:  # 只显示前30行
            print(line)

def main():
    """主函数"""
    print("📊 科创芯片ETF (588200) 数据分析工具")
    print("="*60)
    
    # 创建分析器
    analyzer = StockAnalyzer()
    
    # 获取数据
    days = int(input("请输入要分析的历史数据天数 (默认30): ") or "30")
    df = analyzer.fetch_data(days=days)
    
    if df.empty:
        print("❌ 无法获取数据，程序退出")
        return
    
    # 显示菜单
    while True:
        print("\n" + "="*60)
        print("数据分析菜单:")
        print("="*60)
        print("1. 基本统计分析")
        print("2. 技术指标分析")
        print("3. 买卖信号分析")
        print("4. 生成可视化图表")
        print("5. 生成完整报告")
        print("6. 执行所有分析")
        print("0. 退出")
        print("="*60)
        
        choice = input("请选择操作 (0-6): ").strip()
        
        if choice == '1':
            analyzer.analyze_basic_statistics(df)
        elif choice == '2':
            analyzer.analyze_technical_indicators(df)
        elif choice == '3':
            analyzer.analyze_signals(df)
        elif choice == '4':
            output_dir = input("请输入输出目录 (默认: analysis_output): ") or "analysis_output"
            analyzer.generate_visualizations(df, output_dir)
        elif choice == '5':
            output_file = input("请输入报告文件名 (默认: analysis_report.txt): ") or "analysis_report.txt"
            analyzer.generate_report(df, output_file)
        elif choice == '6':
            # 执行所有分析
            analyzer.analyze_basic_statistics(df)
            analyzer.analyze_technical_indicators(df)
            analyzer.analyze_signals(df)
            analyzer.generate_visualizations(df)
            analyzer.generate_report(df)
        elif choice == '0':
            print("感谢使用，再见！")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()