"""
图表可视化模块
提供 K 线图、技术指标图表等高级可视化功能
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class ChartVisualizer:
    """图表可视化类"""

    def __init__(self):
        self.fig = None
        self.axes = None

    def plot_candlestick(self, df, stock_code='', figsize=(15, 12), show_volume=True):
        """
        绘制 K 线图（蜡烛图）+ 技术指标

        参数：
            df: DataFrame，包含 OHLCV 数据和技术指标
            stock_code: str，股票代码
            figsize: tuple，图表大小
            show_volume: bool，是否显示成交量
        """
        if df is None or df.empty:
            print(f"无法绘制 {stock_code} 的图表：数据为空")
            return

        # 准备数据
        df = df.copy()
        df['Date'] = df.index

        # 创建子图
        num_subplots = 4 if show_volume else 3
        fig, axes = plt.subplots(num_subplots, 1, figsize=figsize, sharex=True)

        # ========== 子图 1: K 线图 + 移动平均线 ==========
        ax1 = axes[0]

        # 绘制 K 线
        self._draw_candlesticks(ax1, df)

        # 绘制移动平均线
        if 'MA5' in df.columns:
            ax1.plot(df.index, df['MA5'], label='MA5', linewidth=1.5, alpha=0.8, color='#FF6B6B')
        if 'MA10' in df.columns:
            ax1.plot(df.index, df['MA10'], label='MA10', linewidth=1.5, alpha=0.8, color='#4ECDC4')
        if 'MA20' in df.columns:
            ax1.plot(df.index, df['MA20'], label='MA20', linewidth=1.5, alpha=0.8, color='#45B7D1')
        if 'MA60' in df.columns:
            ax1.plot(df.index, df['MA60'], label='MA60', linewidth=1.5, alpha=0.8, color='#FFA07A')

        ax1.set_title(f'{stock_code} 股价趋势图 (K线图)', fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel('股价 (Price)', fontsize=12, fontweight='bold')
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True, alpha=0.3, linestyle='--')

        # ========== 子图 2: 成交量 ==========
        if show_volume:
            ax2 = axes[1]
            self._draw_volume(ax2, df)
            ax2.set_ylabel('成交量 (Volume)', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3, linestyle='--')

        # ========== 子图 3: RSI ==========
        ax3 = axes[2] if show_volume else axes[1]
        if 'RSI' in df.columns:
            ax3.plot(df.index, df['RSI'], label='RSI', color='#9B59B6', linewidth=2)
            ax3.axhline(y=70, color='r', linestyle='--', alpha=0.6, linewidth=1, label='超买区 (70)')
            ax3.axhline(y=30, color='g', linestyle='--', alpha=0.6, linewidth=1, label='超卖区 (30)')
            ax3.axhline(y=50, color='gray', linestyle=':', alpha=0.4, linewidth=1)
            ax3.fill_between(df.index, 70, 100, alpha=0.1, color='red')
            ax3.fill_between(df.index, 0, 30, alpha=0.1, color='green')
            ax3.set_ylabel('RSI', fontsize=12, fontweight='bold')
            ax3.set_ylim(0, 100)
            ax3.legend(loc='upper left', fontsize=9)
            ax3.grid(True, alpha=0.3, linestyle='--')

        # ========== 子图 4: MACD ==========
        ax4 = axes[3] if show_volume else axes[2]
        if 'MACD' in df.columns and 'MACD_signal' in df.columns:
            ax4.plot(df.index, df['MACD'], label='MACD', color='#3498DB', linewidth=2)
            ax4.plot(df.index, df['MACD_signal'], label='Signal', color='#E74C3C', linewidth=2)

            # 绘制 MACD 柱状图
            if 'MACD_histogram' in df.columns:
                colors = ['green' if val >= 0 else 'red' for val in df['MACD_histogram']]
                ax4.bar(df.index, df['MACD_histogram'], label='Histogram', alpha=0.3, color=colors, width=0.8)

            ax4.axhline(y=0, color='gray', linestyle='-', alpha=0.3, linewidth=1)
            ax4.set_ylabel('MACD', fontsize=12, fontweight='bold')
            ax4.legend(loc='upper left', fontsize=9)
            ax4.grid(True, alpha=0.3, linestyle='--')

        # 设置 X 轴日期格式
        ax4.set_xlabel('日期 (Date)', fontsize=12, fontweight='bold')
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax4.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()
        plt.show()

        self.fig = fig
        self.axes = axes

    def _draw_candlesticks(self, ax, df):
        """绘制 K 线（蜡烛图）"""
        width = 0.6
        width2 = 0.05

        for idx in range(len(df)):
            row = df.iloc[idx]
            date = row.name
            open_price = row['Open']
            close_price = row['Close']
            high_price = row['High']
            low_price = row['Low']

            # 判断涨跌
            if close_price >= open_price:
                color = '#FF4444'  # 红色（涨）
                body_color = '#FF4444'
                edge_color = '#CC0000'
            else:
                color = '#00CC00'  # 绿色（跌）
                body_color = '#00CC00'
                edge_color = '#009900'

            # 绘制上下影线
            ax.plot([date, date], [low_price, high_price], color=color, linewidth=1, solid_capstyle='round')

            # 绘制实体
            height = abs(close_price - open_price)
            bottom = min(open_price, close_price)

            rect = Rectangle((mdates.date2num(date) - width / 2, bottom), width, height,
                             facecolor=body_color, edgecolor=edge_color, linewidth=0.8, alpha=0.9)
            ax.add_patch(rect)

    def _draw_volume(self, ax, df):
        """绘制成交量柱状图"""
        # 根据涨跌设置颜色
        colors = []
        for idx in range(len(df)):
            row = df.iloc[idx]
            if row['Close'] >= row['Open']:
                colors.append('#FF4444')  # 红色（涨）
            else:
                colors.append('#00CC00')  # 绿色（跌）

        ax.bar(df.index, df['Volume'], color=colors, alpha=0.6, width=0.8)

    def plot_technical_comparison(self, df, stock_code='', figsize=(15, 8)):
        """
        绘制技术指标对比图

        参数：
            df: DataFrame，包含技术指标数据
            stock_code: str，股票代码
            figsize: tuple，图表大小
        """
        if df is None or df.empty:
            print(f"无法绘制 {stock_code} 的技术对比图：数据为空")
            return

        fig, axes = plt.subplots(2, 2, figsize=figsize)

        # 子图 1: 价格 + 布林通道
        ax1 = axes[0, 0]
        ax1.plot(df.index, df['Close'], label='收盘价', linewidth=2, color='#2C3E50')
        if 'BB_upper' in df.columns:
            ax1.plot(df.index, df['BB_upper'], label='布林上轨', linestyle='--', alpha=0.7, color='#E74C3C')
            ax1.plot(df.index, df['BB_middle'], label='布林中轨', linestyle='--', alpha=0.7, color='#3498DB')
            ax1.plot(df.index, df['BB_lower'], label='布林下轨', linestyle='--', alpha=0.7, color='#2ECC71')
            ax1.fill_between(df.index, df['BB_upper'], df['BB_lower'], alpha=0.1, color='gray')
        ax1.set_title('布林通道 (Bollinger Bands)', fontweight='bold')
        ax1.set_ylabel('价格')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        # 子图 2: KD 指标
        ax2 = axes[0, 1]
        if 'K' in df.columns and 'D' in df.columns:
            ax2.plot(df.index, df['K'], label='K 值', linewidth=2, color='#3498DB')
            ax2.plot(df.index, df['D'], label='D 值', linewidth=2, color='#E74C3C')
            ax2.axhline(y=80, color='r', linestyle='--', alpha=0.5, linewidth=1)
            ax2.axhline(y=20, color='g', linestyle='--', alpha=0.5, linewidth=1)
            ax2.fill_between(df.index, 80, 100, alpha=0.1, color='red')
            ax2.fill_between(df.index, 0, 20, alpha=0.1, color='green')
        ax2.set_title('KD 随机指标 (Stochastic)', fontweight='bold')
        ax2.set_ylabel('KD 值')
        ax2.set_ylim(0, 100)
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)

        # 子图 3: RSI
        ax3 = axes[1, 0]
        if 'RSI' in df.columns:
            ax3.plot(df.index, df['RSI'], label='RSI', linewidth=2, color='#9B59B6')
            ax3.axhline(y=70, color='r', linestyle='--', alpha=0.5, linewidth=1, label='超买')
            ax3.axhline(y=30, color='g', linestyle='--', alpha=0.5, linewidth=1, label='超卖')
            ax3.fill_between(df.index, 70, 100, alpha=0.1, color='red')
            ax3.fill_between(df.index, 0, 30, alpha=0.1, color='green')
        ax3.set_title('RSI 相对强弱指标', fontweight='bold')
        ax3.set_ylabel('RSI')
        ax3.set_ylim(0, 100)
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)

        # 子图 4: MACD
        ax4 = axes[1, 1]
        if 'MACD' in df.columns:
            ax4.plot(df.index, df['MACD'], label='MACD', linewidth=2, color='#3498DB')
            ax4.plot(df.index, df['MACD_signal'], label='Signal', linewidth=2, color='#E74C3C')
            if 'MACD_histogram' in df.columns:
                colors = ['green' if val >= 0 else 'red' for val in df['MACD_histogram']]
                ax4.bar(df.index, df['MACD_histogram'], alpha=0.3, color=colors, width=0.8)
            ax4.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
        ax4.set_title('MACD 指标', fontweight='bold')
        ax4.set_ylabel('MACD')
        ax4.legend(fontsize=8)
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        self.fig = fig
        self.axes = axes

    def save_chart(self, filename, dpi=300):
        """
        保存图表为文件

        参数：
            filename: str，文件名
            dpi: int，分辨率
        """
        if self.fig is not None:
            self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
            print(f"✅ 图表已保存至: {filename}")
        else:
            print("❌ 没有可保存的图表")


# 便捷函数
def plot_candlestick_chart(df, stock_code='', figsize=(15, 12), show_volume=True):
    """
    快速绘制 K 线图

    参数：
        df: DataFrame，股票数据
        stock_code: str，股票代码
        figsize: tuple，图表大小
        show_volume: bool，是否显示成交量
    """
    visualizer = ChartVisualizer()
    visualizer.plot_candlestick(df, stock_code, figsize, show_volume)
    return visualizer


def plot_technical_charts(df, stock_code='', figsize=(15, 8)):
    """
    快速绘制技术指标对比图

    参数：
        df: DataFrame，股票数据
        stock_code: str，股票代码
        figsize: tuple，图表大小
    """
    visualizer = ChartVisualizer()
    visualizer.plot_technical_comparison(df, stock_code, figsize)
    return visualizer
