#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
科创芯片ETF (588200) - 简化监控系统
Python 2.7兼容版本
"""

import urllib2
import json
import time
from datetime import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class SimpleStockMonitor:
    """简化股票监控器"""
    
    def __init__(self):
        self.symbol = "588200.SS"
        self.name = u"科创芯片ETF"
        self.last_price = 0
        self.last_change = 0
        
    def get_stock_data(self):
        """获取股票数据"""
        try:
            # 使用公开API获取数据
            url = "https://qt.gtimg.cn/q=" + self.symbol
            
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            response = urllib2.urlopen(req, timeout=10)
            data = response.read().decode('gbk')
            
            # 解析数据 (格式: v_sz002415="51~中兴通讯~ZXTX~27.38~27.20~27.35~10250~10250~0~27.38~27.39~...")
            if data:
                parts = data.split('~')
                if len(parts) >= 5:
                    stock_name = parts[1]
                    current_price = float(parts[3])
                    prev_close = float(parts[4])
                    change = current_price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close != 0 else 0
                    
                    return {
                        'success': True,
                        'symbol': self.symbol,
                        'name': stock_name,
                        'price': round(current_price, 3),
                        'prev_close': round(prev_close, 3),
                        'change': round(change, 3),
                        'change_percent': round(change_percent, 2),
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    }
        
        except Exception as e:
            print(u"API获取失败: {}".format(str(e)))
        
        # 返回模拟数据
        return {
            'success': False,
            'symbol': self.symbol,
            'name': self.name,
            'price': 1.234,
            'prev_close': 1.200,
            'change': 0.034,
            'change_percent': 2.83,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'note': u"模拟数据"
        }
    
    def analyze_signal(self, data):
        """分析买卖信号"""
        price = data['price']
        change_percent = data['change_percent']
        
        signals = []
        
        # 简单信号规则
        if change_percent > 3.0:
            signals.append({
                'type': u'大涨信号',
                'action': u'注意',
                'desc': u'涨幅超过3%，可能过热'
            })
        elif change_percent > 1.0:
            signals.append({
                'type': u'上涨信号',
                'action': u'关注',
                'desc': u'温和上涨'
            })
        elif change_percent < -3.0:
            signals.append({
                'type': u'大跌信号',
                'action': u'机会',
                'desc': u'跌幅较大，可能有买入机会'
            })
        elif change_percent < -1.0:
            signals.append({
                'type': u'下跌信号',
                'action': u'观察',
                'desc': u'温和下跌'
            })
        else:
            signals.append({
                'type': u'盘整信号',
                'action': u'观望',
                'desc': u'价格波动较小'
            })
        
        # 总体建议
        if change_percent > 2.0:
            overall = u'偏多'
            advice = u'可考虑持有'
        elif change_percent < -2.0:
            overall = u'偏空'
            advice = u'谨慎操作'
        else:
            overall = u'中性'
            advice = u'观望为主'
        
        return {
            'overall': overall,
            'advice': advice,
            'signals': signals
        }
    
    def display_dashboard(self, data, analysis):
        """显示仪表盘"""
        # 清屏
        print("\n" * 50)
        
        # 显示标题
        print(u"=" * 60)
        print(u"📈 科创芯片ETF (588200) 实时监控系统")
        print(u"=" * 60)
        
        # 显示行情
        print(u"\n📊 实时行情:")
        print(u"  股票: {}".format(data['name']))
        print(u"  代码: {}".format(data['symbol']))
        print(u"  时间: {}".format(data['timestamp']))
        
        if data['success']:
            print(u"  数据: ✅ 实时数据")
        else:
            print(u"  数据: ⚠️  模拟数据")
        
        # 显示价格
        price_color = u'▲' if data['change'] >= 0 else u'▼'
        color_code = u'32' if data['change'] >= 0 else u'31'  # 绿色/红色
        
        print(u"\n💰 价格信息:")
        print(u"  当前价: {:.3f}".format(data['price']))
        print(u"  昨收价: {:.3f}".format(data['prev_close']))
        print(u"  涨跌幅: {}{:+.3f} ({:+.2f}%)".format(
            price_color, data['change'], data['change_percent']))
        
        # 显示分析
        print(u"\n🚦 技术分析:")
        print(u"  总体判断: {}".format(analysis['overall']))
        print(u"  操作建议: {}".format(analysis['advice']))
        
        print(u"\n🔔 具体信号:")
        for signal in analysis['signals']:
            print(u"  • {} [{}] {}".format(
                signal['type'], signal['action'], signal['desc']))
        
        print(u"\n" + "=" * 60)
        print(u"🔄 自动刷新: 每30秒更新一次")
        print(u"⏹️  按 Ctrl+C 停止")
        print(u"=" * 60)
    
    def run(self):
        """运行监控"""
        print(u"正在启动科创芯片ETF监控系统...")
        print(u"系统初始化...")
        
        try:
            while True:
                # 获取数据
                data = self.get_stock_data()
                
                # 分析信号
                analysis = self.analyze_signal(data)
                
                # 显示仪表盘
                self.display_dashboard(data, analysis)
                
                # 更新历史价格
                self.last_price = data['price']
                self.last_change = data['change_percent']
                
                # 等待30秒
                time.sleep(30)
                
        except KeyboardInterrupt:
            print(u"\n\n监控系统已停止")
            print(u"感谢使用！")
        except Exception as e:
            print(u"\n系统错误: {}".format(str(e)))

def main():
    """主函数"""
    monitor = SimpleStockMonitor()
    monitor.run()

if __name__ == "__main__":
    main()