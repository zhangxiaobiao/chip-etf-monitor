#!/usr/bin/env python3
"""
科创芯片ETF (588200) 后台监控服务
实时监控股票行情并发送警报
"""

import time
import schedule
import logging
from datetime import datetime, timedelta
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher
from signals import SignalGenerator
from utils import NotificationManager, DataProcessor
from config import (
    STOCK_SYMBOL, STOCK_NAME, MONITORING_INTERVAL, 
    ALERT_THRESHOLD, CHECK_HISTORY_DAYS,
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ENABLE_TELEGRAM
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StockMonitor:
    """股票监控器"""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.signal_generator = SignalGenerator()
        self.data_processor = DataProcessor()
        
        # 初始化通知管理器
        if ENABLE_TELEGRAM:
            self.notification_manager = NotificationManager(
                telegram_bot_token=TELEGRAM_BOT_TOKEN,
                telegram_chat_id=TELEGRAM_CHAT_ID
            )
            logger.info("Telegram通知已启用")
        else:
            self.notification_manager = NotificationManager()
            logger.info("Telegram通知未配置，仅输出到控制台")
        
        # 监控状态
        self.monitoring_start_time = datetime.now()
        self.total_checks = 0
        self.alerts_sent = 0
        self.last_price = 0
        self.last_change_percent = 0
        
        # 价格历史记录（用于计算趋势）
        self.price_history = []
        self.max_history_size = 100
        
        logger.info(f"股票监控器初始化完成 - 监控对象: {STOCK_NAME} ({STOCK_SYMBOL})")
    
    def check_stock(self):
        """检查股票状态"""
        try:
            self.total_checks += 1
            current_time = datetime.now()
            
            logger.info(f"开始第 {self.total_checks} 次检查 ({current_time.strftime('%Y-%m-%d %H:%M:%S')})")
            
            # 获取实时数据
            realtime_data = self.data_fetcher.get_realtime_data()
            
            if realtime_data.get('error'):
                logger.error(f"获取数据失败: {realtime_data.get('error')}")
                return
            
            # 获取历史数据
            historical_data = self.data_fetcher.get_historical_data(days=CHECK_HISTORY_DAYS)
            
            # 记录价格历史
            current_price = realtime_data.get('price', 0)
            self.price_history.append({
                'timestamp': current_time,
                'price': current_price
            })
            
            # 限制历史记录大小
            if len(self.price_history) > self.max_history_size:
                self.price_history = self.price_history[-self.max_history_size:]
            
            # 生成买卖信号
            if not historical_data.empty and current_price > 0:
                signals = self.signal_generator.generate_signals(
                    historical_data, 
                    current_price
                )
                
                # 检查价格变动警报
                self._check_price_alert(realtime_data)
                
                # 检查买卖信号警报
                self._check_signal_alert(signals, realtime_data)
                
                # 更新上次价格
                self.last_price = current_price
                self.last_change_percent = realtime_data.get('change_percent', 0)
                
                # 记录检查结果
                self._log_check_result(realtime_data, signals)
            else:
                logger.warning("历史数据为空或当前价格为0，跳过信号生成")
            
            logger.info(f"第 {self.total_checks} 次检查完成")
            
        except Exception as e:
            logger.error(f"检查股票时发生错误: {e}", exc_info=True)
    
    def _check_price_alert(self, realtime_data: dict):
        """检查价格变动警报"""
        try:
            change_percent = abs(realtime_data.get('change_percent', 0))
            
            if change_percent >= ALERT_THRESHOLD:
                alert_data = {
                    'symbol': STOCK_SYMBOL,
                    'price': realtime_data.get('price', 0),
                    'change_percent': realtime_data.get('change_percent', 0),
                    'volume': realtime_data.get('volume', 0),
                    'timestamp': realtime_data.get('timestamp', '')
                }
                
                # 发送警报
                self.notification_manager.send_alert(
                    'price_change',
                    alert_data,
                    ALERT_THRESHOLD
                )
                
                self.alerts_sent += 1
                logger.warning(f"价格变动警报: 涨跌幅 {change_percent:.2f}% 超过阈值 {ALERT_THRESHOLD}%")
                
        except Exception as e:
            logger.error(f"检查价格警报时发生错误: {e}")
    
    def _check_signal_alert(self, signals: dict, realtime_data: dict):
        """检查买卖信号警报"""
        try:
            overall_signal = signals.get('overall_signal', '中性')
            signal_strength = signals.get('signal_strength', 0)
            
            # 只对强信号发送警报
            if signal_strength >= 60 and overall_signal != '中性':
                signal_data = {
                    'overall_signal': overall_signal,
                    'signal_strength': signal_strength,
                    'price': realtime_data.get('price', 0),
                    'recommendation': signals.get('recommendation', '观望'),
                    'signals': signals.get('signals', [])
                }
                
                # 发送警报
                self.notification_manager.send_alert('signal', signal_data)
                
                self.alerts_sent += 1
                logger.warning(f"买卖信号警报: {overall_signal}信号 (强度: {signal_strength})")
                
        except Exception as e:
            logger.error(f"检查信号警报时发生错误: {e}")
    
    def _log_check_result(self, realtime_data: dict, signals: dict):
        """记录检查结果"""
        try:
            log_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'price': realtime_data.get('price', 0),
                'change_percent': realtime_data.get('change_percent', 0),
                'volume': realtime_data.get('volume', 0),
                'signal': signals.get('overall_signal', '中性'),
                'signal_strength': signals.get('signal_strength', 0),
                'recommendation': signals.get('recommendation', '观望')
            }
            
            # 记录到日志文件
            logger.info(
                f"检查结果 - 价格: {log_data['price']:.3f} "
                f"({log_data['change_percent']:+.2f}%) | "
                f"信号: {log_data['signal']} ({log_data['signal_strength']}) | "
                f"建议: {log_data['recommendation']}"
            )
            
        except Exception as e:
            logger.error(f"记录检查结果时发生错误: {e}")
    
    def get_monitor_stats(self) -> dict:
        """获取监控统计信息"""
        uptime = datetime.now() - self.monitoring_start_time
        
        # 计算价格趋势
        trend = "未知"
        if len(self.price_history) >= 2:
            first_price = self.price_history[0]['price']
            last_price = self.price_history[-1]['price']
            
            if last_price > first_price * 1.02:  # 上涨2%
                trend = "上涨"
            elif last_price < first_price * 0.98:  # 下跌2%
                trend = "下跌"
            else:
                trend = "震荡"
        
        # 获取信号统计
        signal_stats = self.signal_generator.get_signals_summary()
        
        # 获取通知统计
        notification_stats = self.notification_manager.get_notification_stats()
        
        return {
            'uptime': str(uptime).split('.')[0],  # 去掉微秒部分
            'total_checks': self.total_checks,
            'alerts_sent': self.alerts_sent,
            'current_price': self.last_price,
            'current_change_percent': self.last_change_percent,
            'price_trend': trend,
            'signal_stats': signal_stats,
            'notification_stats': notification_stats,
            'monitoring_start': self.monitoring_start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def print_stats(self):
        """打印监控统计信息"""
        stats = self.get_monitor_stats()
        
        print("\n" + "="*60)
        print("📊 监控系统统计信息")
        print("="*60)
        print(f"运行时间: {stats['uptime']}")
        print(f"开始时间: {stats['monitoring_start']}")
        print(f"最后检查: {stats['last_check']}")
        print(f"总检查次数: {stats['total_checks']}")
        print(f"发送警报数: {stats['alerts_sent']}")
        print(f"当前价格: {stats['current_price']:.3f} ({stats['current_change_percent']:+.2f}%)")
        print(f"价格趋势: {stats['price_trend']}")
        print("\n📈 信号统计:")
        print(f"  总信号数: {stats['signal_stats']['total_signals']}")
        print(f"  买入信号: {stats['signal_stats']['buy_signals']}")
        print(f"  卖出信号: {stats['signal_stats']['sell_signals']}")
        print(f"  中性信号: {stats['signal_stats']['neutral_signals']}")
        print(f"  最新信号: {stats['signal_stats']['latest_signal']}")
        print("\n📨 通知统计:")
        print(f"  总通知数: {stats['notification_stats']['total']}")
        print(f"  成功数: {stats['notification_stats']['success']}")
        print(f"  失败数: {stats['notification_stats']['failure']}")
        print(f"  成功率: {stats['notification_stats']['success_rate']}%")
        print(f"  最后通知: {stats['notification_stats']['last_notification']}")
        print("="*60 + "\n")
    
    def run_continuously(self):
        """持续运行监控"""
        logger.info(f"开始持续监控，检查间隔: {MONITORING_INTERVAL}秒")
        
        # 发送启动通知
        if ENABLE_TELEGRAM:
            startup_message = f"🚀 科创芯片ETF监控系统已启动\n\n" \
                            f"📈 监控对象: {STOCK_NAME} ({STOCK_SYMBOL})\n" \
                            f"⏰ 检查间隔: {MONITORING_INTERVAL}秒\n" \
                            f"📊 价格警报阈值: {ALERT_THRESHOLD}%\n" \
                            f"🕐 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            self.notification_manager.send_telegram_message(startup_message)
        
        # 立即执行一次检查
        self.check_stock()
        
        # 设置定时任务
        schedule.every(MONITORING_INTERVAL).seconds.do(self.check_stock)
        
        # 每10分钟打印一次统计信息
        schedule.every(10).minutes.do(self.print_stats)
        
        logger.info("监控系统已启动，按Ctrl+C停止")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("收到停止信号，正在关闭监控系统...")
            
            # 发送关闭通知
            if ENABLE_TELEGRAM:
                shutdown_message = f"🛑 科创芯片ETF监控系统已关闭\n\n" \
                                 f"⏱️ 运行时间: {self.get_monitor_stats()['uptime']}\n" \
                                 f"📊 总检查次数: {self.total_checks}\n" \
                                 f"🚨 发送警报数: {self.alerts_sent}\n" \
                                 f"🕐 关闭时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                self.notification_manager.send_telegram_message(shutdown_message)
            
            logger.info("监控系统已关闭")
            sys.exit(0)
            
        except Exception as e:
            logger.error(f"监控系统运行时发生错误: {e}", exc_info=True)
            sys.exit(1)

def main():
    """主函数"""
    print("🚀 科创芯片ETF (588200) 实时监控系统")
    print("="*50)
    print(f"监控对象: {STOCK_NAME} ({STOCK_SYMBOL})")
    print(f"检查间隔: {MONITORING_INTERVAL}秒")
    print(f"价格警报阈值: {ALERT_THRESHOLD}%")
    print(f"历史数据天数: {CHECK_HISTORY_DAYS}天")
    print("="*50)
    
    # 创建监控器
    monitor = StockMonitor()
    
    # 运行监控
    monitor.run_continuously()

if __name__ == "__main__":
    main()