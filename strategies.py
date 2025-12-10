"""
台股投資策略模組
提供多種技術分析策略，用於篩選符合條件的股票
"""

import pandas as pd
import numpy as np


class TradingStrategies:
    """交易策略類別"""

    def __init__(self):
        self.strategies = {
            'golden_cross': self.golden_cross,
            'death_cross': self.death_cross,
            'rsi_oversold': self.rsi_oversold,
            'rsi_overbought': self.rsi_overbought,
            'volume_surge': self.volume_surge,
            'macd_bullish': self.macd_bullish,
            'kd_golden_cross': self.kd_golden_cross,
            'bollinger_breakout': self.bollinger_breakout,
            'combined_bullish': self.combined_bullish,
        }

    def golden_cross(self, df):
        """
        黃金交叉策略：短期均線向上突破長期均線
        條件：MA5 > MA20 且前一天 MA5 <= MA20
        """
        if len(df) < 2:
            return False

        current = df.iloc[-1]
        previous = df.iloc[-2]

        return (current['MA5'] > current['MA20'] and
                previous['MA5'] <= previous['MA20'])

    def death_cross(self, df):
        """
        死亡交叉策略：短期均線向下跌破長期均線
        條件：MA5 < MA20 且前一天 MA5 >= MA20
        """
        if len(df) < 2:
            return False

        current = df.iloc[-1]
        previous = df.iloc[-2]

        return (current['MA5'] < current['MA20'] and
                previous['MA5'] >= previous['MA20'])

    def rsi_oversold(self, df):
        """
        RSI 超賣策略：潛在反彈機會
        條件：RSI < 30
        """
        if len(df) < 1:
            return False

        current = df.iloc[-1]
        return current['RSI'] < 30

    def rsi_overbought(self, df):
        """
        RSI 超買策略：潛在回調風險
        條件：RSI > 70
        """
        if len(df) < 1:
            return False

        current = df.iloc[-1]
        return current['RSI'] > 70

    def volume_surge(self, df):
        """
        量增價漲策略：成交量放大且股價上漲
        條件：成交量 > 20日平均成交量的1.5倍 且 收盤價 > 前一日收盤價
        """
        if len(df) < 21:
            return False

        current = df.iloc[-1]
        previous = df.iloc[-2]
        avg_volume = df['Volume'].iloc[-20:].mean()

        return (current['Volume'] > avg_volume * 1.5 and
                current['Close'] > previous['Close'])

    def macd_bullish(self, df):
        """
        MACD 多頭策略：MACD 柱狀圖由負轉正
        條件：MACD Histogram > 0 且前一天 < 0
        """
        if len(df) < 2:
            return False

        current = df.iloc[-1]
        previous = df.iloc[-2]

        return (current['MACD_histogram'] > 0 and
                previous['MACD_histogram'] <= 0)

    def kd_golden_cross(self, df):
        """
        KD 黃金交叉策略：K 線向上突破 D 線
        條件：K > D 且前一天 K <= D
        """
        if len(df) < 2:
            return False

        current = df.iloc[-1]
        previous = df.iloc[-2]

        return (current['K'] > current['D'] and
                previous['K'] <= previous['D'])

    def bollinger_breakout(self, df):
        """
        布林通道突破策略：突破上軌
        條件：收盤價 > 布林通道上軌
        """
        if len(df) < 1:
            return False

        current = df.iloc[-1]
        return current['Close'] > current['BB_upper']

    def combined_bullish(self, df):
        """
        綜合多頭策略：多個多頭指標同時滿足
        條件：
        1. MA5 > MA20
        2. RSI 介於 40-70（強勢但未超買）
        3. MACD Histogram > 0
        4. 成交量 > 20日平均
        """
        if len(df) < 20:
            return False

        current = df.iloc[-1]
        avg_volume = df['Volume'].iloc[-20:].mean()

        return (current['MA5'] > current['MA20'] and
                40 < current['RSI'] < 70 and
                current['MACD_histogram'] > 0 and
                current['Volume'] > avg_volume)

    def get_strategy(self, strategy_name):
        """獲取指定策略"""
        return self.strategies.get(strategy_name)

    def list_strategies(self):
        """列出所有可用策略"""
        return list(self.strategies.keys())

    def describe_strategy(self, strategy_name):
        """獲取策略說明"""
        strategy_func = self.strategies.get(strategy_name)
        if strategy_func:
            return strategy_func.__doc__
        return "策略不存在"


def apply_strategy(stock_data_dict, strategy_name='golden_cross'):
    """
    對多支股票應用指定策略

    參數：
        stock_data_dict: dict，格式為 {股票代碼: DataFrame}
        strategy_name: str，策略名稱

    返回：
        list，符合策略的股票代碼列表
    """
    strategies = TradingStrategies()
    strategy_func = strategies.get_strategy(strategy_name)

    if not strategy_func:
        print(f"策略 '{strategy_name}' 不存在")
        return []

    matched_stocks = []

    for stock_code, df in stock_data_dict.items():
        if df is not None and not df.empty:
            try:
                if strategy_func(df):
                    matched_stocks.append(stock_code)
            except Exception as e:
                print(f"分析 {stock_code} 時發生錯誤: {e}")

    return matched_stocks


def apply_custom_strategy(stock_data_dict, custom_func):
    """
    應用自訂策略函數

    參數：
        stock_data_dict: dict，格式為 {股票代碼: DataFrame}
        custom_func: function，自訂策略函數，接受 DataFrame 返回 bool

    返回：
        list，符合策略的股票代碼列表
    """
    matched_stocks = []

    for stock_code, df in stock_data_dict.items():
        if df is not None and not df.empty:
            try:
                if custom_func(df):
                    matched_stocks.append(stock_code)
            except Exception as e:
                print(f"分析 {stock_code} 時發生錯誤: {e}")

    return matched_stocks


def get_strategy_summary():
    """獲取所有策略的摘要資訊"""
    strategies = TradingStrategies()
    summary = []

    for strategy_name in strategies.list_strategies():
        doc = strategies.describe_strategy(strategy_name)
        summary.append({
            'strategy_name': strategy_name,
            'description': doc.strip() if doc else "無說明"
        })

    return pd.DataFrame(summary)


# 範例自訂策略函數
def example_custom_strategy(df):
    """
    範例自訂策略：RSI < 40 且 MA5 > MA20
    """
    if len(df) < 1:
        return False

    current = df.iloc[-1]
    return current['RSI'] < 40 and current['MA5'] > current['MA20']
