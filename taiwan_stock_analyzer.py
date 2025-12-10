"""
台股技術分析工具 - 主程式
Taiwan Stock Technical Analyzer - Main Program

可在 Google Colab 或本地 Jupyter Notebook 執行
"""

import pandas as pd
import numpy as np
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# 設定中文字型（在 Colab 上需要額外配置）
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 嘗試導入策略模組（如果在同目錄下）
try:
    from strategies import TradingStrategies, apply_strategy, apply_custom_strategy, get_strategy_summary
    STRATEGIES_AVAILABLE = True
except ImportError:
    STRATEGIES_AVAILABLE = False
    print("注意：strategies.py 未找到，將使用內建簡化策略")


class TaiwanStockAnalyzer:
    """台股分析器"""

    def __init__(self):
        self.taiwan_stocks = []
        self.stock_data = {}

    def get_taiwan_stock_list(self):
        """
        獲取台股列表
        注意：這是簡化版本，實際應從更可靠的來源獲取
        """
        # 常見的台股代碼（前50大市值公司範例）
        common_stocks = [
            '2330.TW',  # 台積電
            '2317.TW',  # 鴻海
            '2454.TW',  # 聯發科
            '2308.TW',  # 台達電
            '2882.TW',  # 國泰金
            '2881.TW',  # 富邦金
            '2886.TW',  # 兆豐金
            '2891.TW',  # 中信金
            '2412.TW',  # 中華電
            '2303.TW',  # 聯電
            '2002.TW',  # 中鋼
            '1301.TW',  # 台塑
            '1303.TW',  # 南亞
            '2884.TW',  # 玉山金
            '2892.TW',  # 第一金
            '2887.TW',  # 台新金
            '2880.TW',  # 華南金
            '2885.TW',  # 元大金
            '2883.TW',  # 開發金
            '2890.TW',  # 永豐金
            '2207.TW',  # 和泰車
            '2382.TW',  # 廣達
            '2357.TW',  # 華碩
            '2409.TW',  # 友達
            '3008.TW',  # 大立光
            '2327.TW',  # 國巨
            '2379.TW',  # 瑞昱
            '2301.TW',  # 光磊
            '3711.TW',  # 日月光投控
            '2105.TW',  # 正新
            '2912.TW',  # 統一超
            '2395.TW',  # 研華
            '5880.TW',  # 合庫金
            '2324.TW',  # 仁寶
            '2345.TW',  # 智邦
            '2408.TW',  # 南亞科
            '6505.TW',  # 台塑化
            '1216.TW',  # 統一
            '2603.TW',  # 長榮
            '2609.TW',  # 陽明
            '2610.TW',  # 華航
            '3045.TW',  # 台灣大
            '4904.TW',  # 遠傳
            '2356.TW',  # 英業達
            '2377.TW',  # 微星
            '3034.TW',  # 聯詠
            '2474.TW',  # 可成
            '6415.TW',  # 矽力-KY
            '5269.TW',  # 祥碩
            '3231.TW',  # 緯創
        ]
        return common_stocks

    def fetch_stock_data(self, stock_code, period='3mo', interval='1d'):
        """
        抓取單一股票數據

        參數：
            stock_code: str，股票代碼（例如：2330.TW）
            period: str，時間範圍（1mo, 3mo, 6mo, 1y, 2y, 5y, max）
            interval: str，時間間隔（1d, 1wk, 1mo）

        返回：
            DataFrame，股票數據
        """
        try:
            stock = yf.Ticker(stock_code)
            df = stock.history(period=period, interval=interval)

            if df.empty:
                print(f"⚠️  {stock_code} 無數據")
                return None

            # 獲取股票資訊
            info = stock.info
            stock_name = info.get('longName', info.get('shortName', stock_code))

            print(f"✅ {stock_code} ({stock_name}) 數據獲取成功，共 {len(df)} 筆")
            return df

        except Exception as e:
            print(f"❌ {stock_code} 數據獲取失敗: {e}")
            return None

    def calculate_technical_indicators(self, df):
        """
        計算技術指標

        參數：
            df: DataFrame，股票價格數據

        返回：
            DataFrame，包含技術指標的數據
        """
        if df is None or df.empty:
            return None

        # 複製數據避免修改原始數據
        df = df.copy()

        # 移動平均線 (MA)
        df['MA5'] = ta.sma(df['Close'], length=5)
        df['MA10'] = ta.sma(df['Close'], length=10)
        df['MA20'] = ta.sma(df['Close'], length=20)
        df['MA60'] = ta.sma(df['Close'], length=60)

        # RSI 相對強弱指標
        df['RSI'] = ta.rsi(df['Close'], length=14)

        # MACD
        macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
        if macd is not None:
            df['MACD'] = macd['MACD_12_26_9']
            df['MACD_signal'] = macd['MACDs_12_26_9']
            df['MACD_histogram'] = macd['MACDh_12_26_9']

        # KD 隨機指標
        stoch = ta.stoch(df['High'], df['Low'], df['Close'], k=9, d=3, smooth_k=3)
        if stoch is not None:
            df['K'] = stoch['STOCHk_9_3_3']
            df['D'] = stoch['STOCHd_9_3_3']

        # 布林通道
        bbands = ta.bbands(df['Close'], length=20, std=2)
        if bbands is not None:
            df['BB_upper'] = bbands['BBU_20_2.0']
            df['BB_middle'] = bbands['BBM_20_2.0']
            df['BB_lower'] = bbands['BBL_20_2.0']

        return df

    def get_stock_info(self, stock_code):
        """獲取股票基本資訊"""
        try:
            stock = yf.Ticker(stock_code)
            info = stock.info

            return {
                'code': stock_code,
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'industry': info.get('industry', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 'N/A'),
            }
        except:
            return {'code': stock_code, 'name': 'N/A'}

    def get_top_volume_stocks(self, stock_list=None, top_n=50):
        """
        獲取成交量前 N 名的股票

        參數：
            stock_list: list，股票代碼列表，若為 None 則使用預設列表
            top_n: int，取前幾名

        返回：
            list，排序後的股票代碼列表
        """
        if stock_list is None:
            stock_list = self.get_taiwan_stock_list()

        print(f"📊 正在獲取 {len(stock_list)} 支股票的成交量數據...\n")

        volume_data = []

        for i, stock_code in enumerate(stock_list, 1):
            try:
                stock = yf.Ticker(stock_code)
                hist = stock.history(period='2d')  # 獲取最近2天數據

                if not hist.empty:
                    latest_volume = hist['Volume'].iloc[-1]
                    info = stock.info
                    stock_name = info.get('longName', info.get('shortName', stock_code))

                    volume_data.append({
                        'code': stock_code,
                        'name': stock_name,
                        'volume': latest_volume,
                    })

                    print(f"  [{i}/{len(stock_list)}] {stock_code} ({stock_name}): {latest_volume:,.0f}")

                # 避免請求過快
                if i % 10 == 0:
                    time.sleep(1)

            except Exception as e:
                print(f"  [{i}/{len(stock_list)}] {stock_code} 獲取失敗: {e}")

        # 按成交量排序
        volume_df = pd.DataFrame(volume_data)
        volume_df = volume_df.sort_values('volume', ascending=False).head(top_n)

        print(f"\n✅ 成交量前 {top_n} 名股票獲取完成！\n")

        return volume_df

    def analyze_stocks(self, stock_list, period='3mo'):
        """
        批量分析股票並計算技術指標

        參數：
            stock_list: list 或 DataFrame，股票代碼列表或包含 'code' 欄位的 DataFrame
            period: str，歷史數據時間範圍

        返回：
            dict，{股票代碼: 包含技術指標的 DataFrame}
        """
        if isinstance(stock_list, pd.DataFrame):
            stock_codes = stock_list['code'].tolist()
        else:
            stock_codes = stock_list

        print(f"🔍 開始分析 {len(stock_codes)} 支股票...\n")

        results = {}

        for i, stock_code in enumerate(stock_codes, 1):
            print(f"[{i}/{len(stock_codes)}] 分析 {stock_code}...")

            # 獲取數據
            df = self.fetch_stock_data(stock_code, period=period)

            if df is not None:
                # 計算技術指標
                df_with_indicators = self.calculate_technical_indicators(df)
                results[stock_code] = df_with_indicators

            # 避免請求過快
            if i % 5 == 0:
                time.sleep(1)

        print(f"\n✅ 分析完成！成功分析 {len(results)} 支股票\n")

        return results

    def display_analysis_summary(self, stock_data_dict, stock_info_df=None):
        """
        顯示分析摘要

        參數：
            stock_data_dict: dict，{股票代碼: DataFrame}
            stock_info_df: DataFrame，股票資訊表
        """
        summary = []

        for stock_code, df in stock_data_dict.items():
            if df is None or df.empty:
                continue

            latest = df.iloc[-1]

            # 從 stock_info_df 獲取股票名稱
            stock_name = stock_code
            if stock_info_df is not None:
                match = stock_info_df[stock_info_df['code'] == stock_code]
                if not match.empty:
                    stock_name = f"{match.iloc[0]['name']} ({stock_code})"

            summary.append({
                '股票': stock_name,
                '收盤價': f"{latest['Close']:.2f}",
                'MA5': f"{latest['MA5']:.2f}" if pd.notna(latest.get('MA5')) else 'N/A',
                'MA20': f"{latest['MA20']:.2f}" if pd.notna(latest.get('MA20')) else 'N/A',
                'RSI': f"{latest['RSI']:.2f}" if pd.notna(latest.get('RSI')) else 'N/A',
                'K': f"{latest['K']:.2f}" if pd.notna(latest.get('K')) else 'N/A',
                'D': f"{latest['D']:.2f}" if pd.notna(latest.get('D')) else 'N/A',
                '成交量': f"{latest['Volume']:,.0f}",
            })

        summary_df = pd.DataFrame(summary)
        print("📈 技術指標摘要\n")
        print(summary_df.to_string(index=False))
        print()

        return summary_df

    def plot_stock_chart(self, stock_code, df, figsize=(14, 10)):
        """
        繪製股票技術分析圖表

        參數：
            stock_code: str，股票代碼
            df: DataFrame，包含技術指標的數據
            figsize: tuple，圖表大小
        """
        if df is None or df.empty:
            print(f"無法繪製 {stock_code} 的圖表：數據為空")
            return

        fig, axes = plt.subplots(4, 1, figsize=figsize, sharex=True)

        # 子圖 1: 價格與移動平均線
        axes[0].plot(df.index, df['Close'], label='收盤價', linewidth=2)
        axes[0].plot(df.index, df['MA5'], label='MA5', alpha=0.7)
        axes[0].plot(df.index, df['MA20'], label='MA20', alpha=0.7)
        axes[0].plot(df.index, df['MA60'], label='MA60', alpha=0.7)
        axes[0].set_ylabel('價格')
        axes[0].set_title(f'{stock_code} 技術分析圖表')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # 子圖 2: 成交量
        axes[1].bar(df.index, df['Volume'], alpha=0.5)
        axes[1].set_ylabel('成交量')
        axes[1].grid(True, alpha=0.3)

        # 子圖 3: RSI
        if 'RSI' in df.columns:
            axes[2].plot(df.index, df['RSI'], label='RSI', color='purple')
            axes[2].axhline(y=70, color='r', linestyle='--', alpha=0.5, label='超買')
            axes[2].axhline(y=30, color='g', linestyle='--', alpha=0.5, label='超賣')
            axes[2].set_ylabel('RSI')
            axes[2].legend()
            axes[2].grid(True, alpha=0.3)

        # 子圖 4: MACD
        if 'MACD' in df.columns:
            axes[3].plot(df.index, df['MACD'], label='MACD', color='blue')
            axes[3].plot(df.index, df['MACD_signal'], label='Signal', color='red')
            axes[3].bar(df.index, df['MACD_histogram'], label='Histogram', alpha=0.3)
            axes[3].set_ylabel('MACD')
            axes[3].legend()
            axes[3].grid(True, alpha=0.3)

        plt.xlabel('日期')
        plt.tight_layout()
        plt.show()


# ==================== 簡化版策略（當 strategies.py 不可用時） ====================

def simple_golden_cross(df):
    """簡化版黃金交叉"""
    if len(df) < 2:
        return False
    current = df.iloc[-1]
    previous = df.iloc[-2]
    return (current['MA5'] > current['MA20'] and previous['MA5'] <= previous['MA20'])


def simple_rsi_oversold(df):
    """簡化版 RSI 超賣"""
    if len(df) < 1:
        return False
    return df.iloc[-1]['RSI'] < 30


def apply_simple_strategy(stock_data_dict, strategy='golden_cross'):
    """應用簡化版策略"""
    strategies = {
        'golden_cross': simple_golden_cross,
        'rsi_oversold': simple_rsi_oversold,
    }

    if strategy not in strategies:
        print(f"策略 '{strategy}' 不存在")
        return []

    strategy_func = strategies[strategy]
    matched = []

    for stock_code, df in stock_data_dict.items():
        if df is not None and not df.empty:
            try:
                if strategy_func(df):
                    matched.append(stock_code)
            except:
                pass

    return matched


# ==================== 主程式範例 ====================

def main():
    """主程式"""

    print("=" * 60)
    print("台股技術分析工具 Taiwan Stock Technical Analyzer")
    print("=" * 60)
    print()

    # 初始化分析器
    analyzer = TaiwanStockAnalyzer()

    # 步驟 1: 獲取成交量前 50 名股票
    print("📊 步驟 1: 獲取成交量前 50 名股票\n")
    top_50 = analyzer.get_top_volume_stocks(top_n=50)

    print("\n成交量前 50 名股票：")
    print(top_50.to_string(index=False))
    print("\n" + "=" * 60 + "\n")

    # 步驟 2: 分析這些股票的技術指標
    print("🔍 步驟 2: 分析技術指標\n")
    stock_data = analyzer.analyze_stocks(top_50, period='3mo')

    # 步驟 3: 顯示技術指標摘要
    print("\n" + "=" * 60 + "\n")
    summary = analyzer.display_analysis_summary(stock_data, top_50)

    # 步驟 4: 應用投資策略
    print("=" * 60)
    print("🎯 步驟 3: 應用投資策略\n")

    if STRATEGIES_AVAILABLE:
        # 使用完整策略模組
        strategies = TradingStrategies()
        print("可用策略：")
        for strategy_name in strategies.list_strategies():
            print(f"  - {strategy_name}")
        print()

        # 應用黃金交叉策略
        matched = apply_strategy(stock_data, 'golden_cross')
        print(f"符合「黃金交叉」策略的股票 ({len(matched)} 支)：")
        for stock_code in matched:
            stock_name = top_50[top_50['code'] == stock_code]['name'].values[0]
            print(f"  ✅ {stock_code} ({stock_name})")
    else:
        # 使用簡化版策略
        print("使用簡化版策略...\n")
        matched = apply_simple_strategy(stock_data, 'golden_cross')
        print(f"符合「黃金交叉」策略的股票 ({len(matched)} 支)：")
        for stock_code in matched:
            stock_name = top_50[top_50['code'] == stock_code]['name'].values[0]
            print(f"  ✅ {stock_code} ({stock_name})")

    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
