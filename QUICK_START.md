# 快速入門指南 Quick Start Guide

## 🚀 在 Google Colab 上使用（推薦）

### 方法 1：上傳 Notebook

1. 前往 [Google Colab](https://colab.research.google.com/)
2. 點擊 `檔案` → `上傳筆記本`
3. 上傳 `taiwan_stock_analyzer.ipynb`
4. 依序執行每個 Cell

### 方法 2：從 GitHub 直接開啟

1. 將此專案推送到 GitHub
2. 在 Colab 中，點擊 `檔案` → `開啟筆記本` → `GitHub`
3. 輸入倉庫網址並選擇 `taiwan_stock_analyzer.ipynb`

## 💻 本地使用

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 執行 Python 腳本

```bash
python taiwan_stock_analyzer.py
```

### 或在 Jupyter Notebook 中使用

```bash
jupyter notebook taiwan_stock_analyzer.ipynb
```

## 📋 基本使用範例

### 1. 獲取成交量前 50 名股票

```python
from taiwan_stock_analyzer import TaiwanStockAnalyzer

# 初始化分析器
analyzer = TaiwanStockAnalyzer()

# 獲取成交量前 50 名
top_50 = analyzer.get_top_volume_stocks(top_n=50)
print(top_50)
```

### 2. 分析技術指標

```python
# 分析這些股票
stock_data = analyzer.analyze_stocks(top_50, period='3mo')

# 顯示摘要
summary = analyzer.display_analysis_summary(stock_data, top_50)
```

### 3. 應用投資策略

```python
from strategies import apply_strategy

# 應用黃金交叉策略
matched = apply_strategy(stock_data, 'golden_cross')
print(f"符合黃金交叉策略的股票: {matched}")
```

### 4. 繪製技術圖表

```python
# 繪製台積電的技術圖表
analyzer.plot_stock_chart('2330.TW', stock_data['2330.TW'])
```

## 🎯 可用的投資策略

| 策略名稱 | 說明 | 適用情況 |
|---------|------|---------|
| `golden_cross` | 黃金交叉（MA5 > MA20） | 多頭趨勢啟動 |
| `death_cross` | 死亡交叉（MA5 < MA20） | 空頭趨勢啟動 |
| `rsi_oversold` | RSI 超賣（< 30） | 潛在反彈機會 |
| `rsi_overbought` | RSI 超買（> 70） | 潛在回調風險 |
| `volume_surge` | 量增價漲 | 強勢突破 |
| `kd_golden_cross` | KD 黃金交叉 | 短期轉強 |
| `macd_bullish` | MACD 多頭 | 趨勢反轉向上 |
| `combined_bullish` | 綜合多頭策略 | 多重確認的買入信號 |

## 🔧 自訂策略範例

```python
def my_strategy(df):
    """
    自訂策略：尋找從超賣區反彈的股票
    條件：
    - RSI 從低於 30 回升到 30-50 區間
    - MA5 > MA20
    - 成交量放大
    """
    if len(df) < 20:
        return False

    current = df.iloc[-1]
    avg_volume = df['Volume'].iloc[-20:].mean()

    return (
        30 < current['RSI'] < 50 and
        current['MA5'] > current['MA20'] and
        current['Volume'] > avg_volume
    )

# 應用自訂策略
from strategies import apply_custom_strategy
matched = apply_custom_strategy(stock_data, my_strategy)
```

## 📊 分析單一股票

```python
# 快速分析台積電
df = analyzer.fetch_stock_data('2330.TW', period='6mo')
df = analyzer.calculate_technical_indicators(df)

# 查看最新數據
print(df.tail())

# 繪製圖表
analyzer.plot_stock_chart('2330.TW', df)
```

## ⚙️ 進階設定

### 修改時間範圍

```python
# 可用選項：1mo, 3mo, 6mo, 1y, 2y, 5y, max
stock_data = analyzer.analyze_stocks(top_50, period='1y')
```

### 修改技術指標參數

在 `calculate_technical_indicators()` 方法中修改參數：

```python
# 例如：將 RSI 週期從 14 改為 9
df['RSI'] = ta.rsi(df['Close'], length=9)
```

### 批量繪製圖表

```python
# 為前 10 支股票繪製圖表
for stock_code in list(stock_data.keys())[:10]:
    analyzer.plot_stock_chart(stock_code, stock_data[stock_code])
```

## 💡 使用技巧

1. **避免被封鎖**：程式中已加入延遲，但如果分析大量股票，建議增加延遲時間
2. **數據品質**：某些股票可能數據不完整，程式會自動跳過
3. **策略組合**：可以組合多個策略來提高準確率
4. **回測**：使用歷史數據測試策略有效性

## ⚠️ 常見問題

### Q: 為什麼有些股票無法獲取數據？
A: 可能是股票代碼錯誤、股票已下市，或 Yahoo Finance 暫時無法提供數據。

### Q: 如何加快分析速度？
A: 減少分析的股票數量，或縮短時間範圍（例如從 3mo 改為 1mo）。

### Q: 可以分析美股嗎？
A: 可以！只需將股票代碼從 `.TW` 改為對應的美股代碼（例如：`AAPL`、`TSLA`）。

### Q: 技術指標計算有誤怎麼辦？
A: 確保有足夠的歷史數據（建議至少 3 個月），某些指標需要較長的計算週期。

## 📚 延伸資源

- [Yahoo Finance](https://finance.yahoo.com/)
- [yfinance 文件](https://pypi.org/project/yfinance/)
- [pandas-ta 指標列表](https://github.com/twopirllc/pandas-ta)
- [技術分析教學](https://www.investopedia.com/technical-analysis-4689657)

## 🤝 貢獻

歡迎提交 Issues 和 Pull Requests！

## ⚖️ 免責聲明

本工具僅供教育和研究用途。技術分析結果僅供參考，不構成投資建議。投資有風險，請謹慎評估並自行承擔投資決策的責任。
