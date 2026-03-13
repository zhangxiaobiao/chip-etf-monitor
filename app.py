import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import time
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import DataFetcher
from signals import SignalGenerator
from utils import DataVisualizer, NotificationManager, DataProcessor
from config import get_config_summary, STOCK_SYMBOL, STOCK_NAME, ENABLE_TELEGRAM

# 设置页面配置
st.set_page_config(
    page_title="科创芯片ETF实时监控系统",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化组件
@st.cache_resource
def init_components():
    """初始化组件（缓存）"""
    return {
        'data_fetcher': DataFetcher(),
        'signal_generator': SignalGenerator(),
        'visualizer': DataVisualizer(),
        'data_processor': DataProcessor(),
        'notification_manager': NotificationManager()
    }

# 获取配置
config = get_config_summary()

# 应用标题
st.title("📈 科创芯片ETF (588200) 实时监控系统")
st.markdown("---")

# 初始化组件
components = init_components()
data_fetcher = components['data_fetcher']
signal_generator = components['signal_generator']
visualizer = components['visualizer']
data_processor = components['data_processor']

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 系统配置")
    
    # 监控控制
    st.subheader("监控控制")
    auto_refresh = st.checkbox("自动刷新", value=True)
    refresh_interval = st.slider("刷新间隔（秒）", 10, 300, 60, 10)
    
    # 数据显示
    st.subheader("数据显示")
    show_technical = st.checkbox("显示技术指标", value=True)
    show_volume = st.checkbox("显示成交量", value=True)
    history_days = st.slider("历史数据天数", 5, 365, 30, 5)
    
    # 警报设置
    st.subheader("警报设置")
    alert_threshold = st.slider("价格变动警报阈值 (%)", 1.0, 10.0, 2.0, 0.5)
    enable_alerts = st.checkbox("启用警报", value=True)
    
    # 系统信息
    st.markdown("---")
    st.subheader("📊 系统信息")
    st.write(f"**监控股票:** {STOCK_NAME}")
    st.write(f"**股票代码:** {STOCK_SYMBOL}")
    st.write(f"**技术指标:** MACD, RSI, 布林带")
    st.write(f"**数据源:** AKShare / 东方财富")
    
    if auto_refresh:
        st.write(f"**下次刷新:** {refresh_interval}秒后")
    
    # 手动刷新按钮
    if st.button("🔄 手动刷新数据", use_container_width=True):
        st.rerun()

# 主内容区域
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # 获取实时数据
    with st.spinner("正在获取实时数据..."):
        realtime_data = data_fetcher.get_realtime_data()
        historical_data = data_fetcher.get_historical_data(days=history_days)
    
    # 显示实时行情
    st.subheader("📊 实时行情")
    
    # 创建指标卡片
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        price_color = "green" if realtime_data.get('change', 0) >= 0 else "red"
        st.metric(
            label="当前价格",
            value=f"{realtime_data.get('price', 0):.3f}",
            delta=f"{realtime_data.get('change_percent', 0):+.2f}%",
            delta_color=price_color
        )
    
    with metric_col2:
        st.metric(
            label="今日开盘",
            value=f"{realtime_data.get('open', 0):.3f}"
        )
    
    with metric_col3:
        st.metric(
            label="今日最高",
            value=f"{realtime_data.get('high', 0):.3f}"
        )
    
    with metric_col4:
        st.metric(
            label="今日最低",
            value=f"{realtime_data.get('low', 0):.3f}"
        )
    
    # 显示成交量
    st.metric(
        label="成交量",
        value=f"{realtime_data.get('volume', 0):,}"
    )
    
    # 更新时间
    st.caption(f"更新时间: {realtime_data.get('timestamp', '未知')}")

with col2:
    # 获取股票基本信息
    with st.spinner("获取股票信息..."):
        stock_info = data_fetcher.get_stock_info()
    
    st.subheader("ℹ️ 股票信息")
    
    if stock_info:
        info_data = {
            "名称": stock_info.get('name', STOCK_NAME),
            "行业": stock_info.get('industry', '未知'),
            "板块": stock_info.get('sector', '未知'),
            "市值": f"{stock_info.get('market_cap', 0):,.0f}",
            "市盈率": f"{stock_info.get('pe_ratio', 0):.2f}",
            "市净率": f"{stock_info.get('pb_ratio', 0):.2f}",
            "股息率": f"{stock_info.get('dividend_yield', 0):.2%}",
            "52周最高": f"{stock_info.get('52w_high', 0):.2f}",
            "52周最低": f"{stock_info.get('52w_low', 0):.2f}",
            "Beta系数": f"{stock_info.get('beta', 0):.2f}"
        }
        
        for key, value in info_data.items():
            st.write(f"**{key}:** {value}")
    else:
        st.info("股票信息获取失败，请检查网络连接")

with col3:
    # 系统状态
    st.subheader("🚦 系统状态")
    
    # 数据源状态
    data_source_status = "✅ 正常" if realtime_data.get('price', 0) > 0 else "❌ 异常"
    st.write(f"**数据源:** {data_source_status}")
    
    # 历史数据状态
    hist_data_status = "✅ 正常" if not historical_data.empty else "⚠️ 数据不足"
    st.write(f"**历史数据:** {hist_data_status}")
    
    # 警报状态
    alert_status = "✅ 启用" if enable_alerts else "⏸️ 禁用"
    st.write(f"**警报系统:** {alert_status}")
    
    # Telegram状态
    telegram_status = "✅ 已配置" if ENABLE_TELEGRAM else "⏸️ 未配置"
    st.write(f"**Telegram通知:** {telegram_status}")
    
    # 刷新状态
    if auto_refresh:
        refresh_status = f"⏰ {refresh_interval}秒"
    else:
        refresh_status = "手动"
    st.write(f"**刷新模式:** {refresh_status}")

# 买卖信号区域
st.markdown("---")
st.subheader("🚦 买卖信号分析")

# 初始化 signals 为 None，避免后续区域引用时未定义
signals = None

# 数据异常提示
if realtime_data.get('error'):
    st.warning(f"⚠️ 实时数据提示：{realtime_data.get('error')}")

if realtime_data.get('data_source'):
    st.caption(f"数据来源: {realtime_data.get('data_source')}")

if not historical_data.empty and realtime_data.get('price', 0) > 0:
    # 生成买卖信号
    with st.spinner("正在分析技术指标..."):
        try:
            signals = signal_generator.generate_signals(
                historical_data, 
                realtime_data.get('price', 0)
            )
        except Exception as e:
            st.error(f"信号生成出错: {e}")
            signals = signal_generator.get_empty_signals(realtime_data.get('price', 0))
    
    if signals:
        # 显示信号卡片
        signal_col1, signal_col2, signal_col3, signal_col4 = st.columns(4)
        
        with signal_col1:
            signal_color = "normal" if signals.get('overall_signal') == '中性' else \
                          ("off" if signals.get('overall_signal') == '卖出' else "normal")
            st.metric(
                label="总体信号",
                value=signals.get('overall_signal', '中性'),
                delta=f"强度: {signals.get('signal_strength', 0)}",
            )
        
        with signal_col2:
            st.metric(
                label="操作建议",
                value=signals.get('recommendation', '观望')
            )
        
        with signal_col3:
            st.metric(
                label="风险等级",
                value=signals.get('risk_level', '中等')
            )
        
        with signal_col4:
            signal_stats = signal_generator.get_signals_summary()
            st.metric(
                label="历史信号",
                value=f"{signal_stats.get('total_signals', 0)}"
            )
        
        # 显示信号仪表盘
        try:
            fig_gauge = visualizer.create_signal_gauge(
                signals.get('signal_strength', 0),
                signals.get('overall_signal', '中性')
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        except Exception as e:
            st.info(f"仪表盘渲染失败: {e}")
        
        # 显示具体信号
        st.subheader("🔍 具体技术信号")
        
        signal_list = signals.get('signals', [])
        if signal_list:
            for sig in signal_list:
                with st.expander(f"{sig['type']}: {sig['signal']}信号", expanded=False):
                    st.write(f"**置信度:** {sig['confidence']}%")
                    st.write(f"**说明:** {sig['description']}")
        else:
            st.info("暂无具体技术信号（数据量不足或市场处于中性区间）")
        
        # 技术指标状态
        st.subheader("📊 技术指标状态")
        
        indicators = signals.get('indicators', {})
        if indicators:
            for indicator_name, indicator_data in indicators.items():
                with st.expander(f"{indicator_name}", expanded=False):
                    if isinstance(indicator_data, dict):
                        for key, value in indicator_data.items():
                            st.write(f"**{key}:** {value}")
                    else:
                        st.write(indicator_data)
        else:
            st.info("技术指标数据不足（需要至少20个交易日数据）")
        
        # 警报检查
        if enable_alerts:
            price_change = abs(realtime_data.get('change_percent', 0))
            if price_change >= alert_threshold:
                st.warning(f"⚠️ 价格变动超过阈值: {price_change:.2f}% ≥ {alert_threshold}%")
                
                if ENABLE_TELEGRAM:
                    notification_manager = NotificationManager()
                    alert_sent = notification_manager.send_alert(
                        'price_change', 
                        realtime_data, 
                        alert_threshold
                    )
                    if alert_sent:
                        st.success("警报已发送到Telegram")
else:
    if historical_data.empty:
        st.error("❌ 历史数据获取失败，无法生成买卖信号")
        st.info("💡 可能原因：\n1. 网络连接问题\n2. akshare 版本过旧（运行 `pip install akshare --upgrade`）\n3. 交易时间外数据可能延迟")
    elif realtime_data.get('price', 0) <= 0:
        st.warning("⚠️ 实时价格获取失败，无法生成买卖信号")
        st.info("💡 请检查网络连接或稍后重试")

# 图表区域
st.markdown("---")
st.subheader("📈 价格走势图")

if not historical_data.empty:
    # 选择图表类型
    chart_type = st.radio(
        "选择图表类型:",
        ["价格走势", "技术分析"],
        horizontal=True
    )
    
    if chart_type == "价格走势":
        # 价格走势图
        fig_price = visualizer.create_price_chart(
            historical_data, 
            f"{STOCK_NAME} 价格走势 ({history_days}天)"
        )
        st.plotly_chart(fig_price, use_container_width=True)
        
        # 显示统计数据
        st.subheader("📊 统计指标")
        
        stats = data_processor.calculate_statistics(historical_data)
        if stats:
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            
            with stats_col1:
                st.metric("当前价格", f"{stats.get('current_price', 0):.3f}")
                st.metric("价格变动", f"{stats.get('price_change', 0):+.3f}")
            
            with stats_col2:
                st.metric("涨跌幅", f"{stats.get('price_change_percent', 0):+.2f}%")
                st.metric("波动率", f"{stats.get('volatility', 0):.2%}")
            
            with stats_col3:
                trend_emoji = {
                    'up': '📈', 
                    'down': '📉', 
                    'sideways': '➡️',
                    'unknown': '❓'
                }
                trend = stats.get('trend', 'unknown')
                st.metric("趋势", f"{trend_emoji.get(trend, '❓')} {trend}")
                st.metric("成交量", f"{stats.get('volume', 0):,}")
        
    else:
        # 技术分析图
        if show_technical:
            # 添加技术指标
            df_with_indicators = signal_generator.calculate_indicators(historical_data)
            
            fig_technical = visualizer.create_technical_chart(df_with_indicators)
            st.plotly_chart(fig_technical, use_container_width=True)
            
            # 检测价格形态
            patterns = data_processor.detect_patterns(df_with_indicators)
            if patterns:
                st.subheader("🔍 检测到的价格形态")
                for pattern in patterns:
                    st.info(f"**{pattern['type']}**: {pattern['description']} (置信度: {pattern['confidence']}%)")
else:
    st.warning("历史数据为空，无法显示图表")

# 报告生成区域
st.markdown("---")
st.subheader("📄 分析报告")

if not historical_data.empty and realtime_data.get('price', 0) > 0 and signals is not None:
    # 生成报告
    try:
        report = data_processor.generate_report(realtime_data, signals)
    except Exception as e:
        report = f"报告生成出错: {e}"
    
    # 显示报告
    with st.expander("查看完整分析报告", expanded=False):
        st.text(report)
    
    # 下载报告
    report_filename = f"科创芯片ETF分析报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    st.download_button(
        label="📥 下载分析报告",
        data=report,
        file_name=report_filename,
        mime="text/plain",
        use_container_width=True
    )
else:
    st.info("数据不足，无法生成分析报告（请等待数据加载完成）")

# 底部信息
st.markdown("---")
st.caption("💡 提示: 本系统为辅助决策工具，不构成投资建议。金融市场有风险，投资需谨慎。")
st.caption(f"🔄 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 自动刷新逻辑
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()