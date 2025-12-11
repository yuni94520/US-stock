# 進階使用指南 Advanced User Guide

本指南將詳細介紹如何使用新增的進階功能。

## 📋 目錄

1. [完整分析報告生成](#1-完整分析報告生成)
2. [K 線圖繪製](#2-k-線圖繪製)
3. [新聞情緒分析](#3-新聞情緒分析)
4. [AI 綜合分析](#4-ai-綜合分析)
5. [批量處理](#5-批量處理)
6. [報告導出](#6-報告導出)

---

## 1. 完整分析報告生成

### 🚀 一鍵生成完整報告

最簡單的使用方式：只需一行代碼即可生成包含所有功能的完整報告。

```python
from comprehensive_report import quick_report

# 生成 NVDA 的完整報告
generator = quick_report(
    stock_code='NVDA',
    period='3mo',
    num_news=20,
    show_charts=True,
    export_excel=True
)
```

### 📊 報告包含內容

執行後會自動生成：

1. ✅ **股價趨勢圖**：專業 K 線圖 + 技術指標
2. ✅ **新聞情緒分析**：最新新聞的情緒統計
3. ✅ **AI 分析報告**：綜合分析和投資建議
4. ✅ **Excel 報告**：完整數據導出

### 🔑 啟用 Gemini AI（推薦）

如果你有 Google Gemini API Key，可以啟用 AI 深度分析：

```python
GEMINI_API_KEY = "your-api-key-here"

generator = quick_report(
    stock_code='2330.TW',
    gemini_api_key=GEMINI_API_KEY,
    use_gemini=True,  # 啟用 AI 分析
    period='6mo',
    num_news=30,
    show_charts=True,
    export_excel=True
)
```

**AI 分析的優勢：**
- 更精準的新聞情緒識別
- 自動生成詳細的分析摘要
- 智能風險評估
- 個性化投資建議

---

## 2. K 線圖繪製

### 📈 繪製專業 K 線圖

```python
from chart_visualizer import plot_candlestick_chart
from taiwan_stock_analyzer import TaiwanStockAnalyzer

# 1. 獲取數據
analyzer = TaiwanStockAnalyzer()
df = analyzer.fetch_stock_data('NVDA', period='6mo')
df = analyzer.calculate_technical_indicators(df)

# 2. 繪製 K 線圖
plot_candlestick_chart(df, stock_code='NVDA', show_volume=True)
```

### 🎨 圖表功能

K 線圖包含：
- **蠟燭圖**：顯示每日開盤、收盤、最高、最低價
  - 紅色：上漲
  - 綠色：下跌
- **移動平均線**：MA5、MA10、MA20、MA60
- **成交量**：顏色對應漲跌
- **RSI 指標**：超買超賣區域標示
- **MACD 指標**：含柱狀圖

### 📊 技術指標對比圖

```python
from chart_visualizer import plot_technical_charts

# 繪製技術指標對比圖（2x2 布局）
plot_technical_charts(df, stock_code='NVDA')
```

包含四個子圖：
1. 布林通道 (Bollinger Bands)
2. KD 隨機指標
3. RSI 相對強弱指標
4. MACD 指標

---

## 3. 新聞情緒分析

### 📰 快速情緒分析

```python
from sentiment_analyzer import quick_sentiment_analysis

# 分析 NVDA 的新聞情緒
analyzer, summary = quick_sentiment_analysis(
    stock_symbol='NVDA',
    num_articles=20,
    use_gemini=False  # 改為 True 以使用 AI
)
```

### 📊 情緒統計輸出

自動顯示：

```
📊 新聞情緒分析摘要 (Sentiment News Summary)
======================================================================

📰 分析新聞總數: 20 篇
📅 分析時間: 2025-12-11 12:30:45

🎯 整體市場情緒: 稍微看漲 (Somewhat Bullish)
📈 平均情緒分數: 0.425 (範圍: -1 到 1)
🎲 平均置信度: 75.0%

📊 情緒分布統計:
----------------------------------------------------------------------
  Somewhat-Bullish     | ██████████████████████████████  60.0% (12 篇)
  Neutral              | ████████████████████            40.0% (8 篇)
======================================================================
```

### 🎯 進階使用

#### 3.1 僅獲取新聞（不分析）

```python
from sentiment_analyzer import SentimentAnalyzer

analyzer = SentimentAnalyzer()
news = analyzer.fetch_stock_news('TSLA', num_articles=30)

# 查看新聞標題
for item in news[:5]:
    print(f"{item['title']} ({item['publisher']})")
```

#### 3.2 自訂情緒分析

```python
# 分析特定新聞
sentiment_results = analyzer.analyze_news_sentiment(news)

# 查看詳細結果
print(sentiment_results[['title', 'sentiment', 'score', 'confidence']])
```

#### 3.3 繪製情緒圖表

```python
# 獲取摘要
summary = analyzer.get_sentiment_summary()

# 繪製餅圖和柱狀圖
analyzer.plot_sentiment_distribution(summary)
```

---

## 4. AI 綜合分析

### 🤖 生成 AI 分析報告

```python
from ai_analyzer import quick_ai_analysis
from taiwan_stock_analyzer import TaiwanStockAnalyzer

# 1. 獲取股票數據
analyzer = TaiwanStockAnalyzer()
df = analyzer.fetch_stock_data('2330.TW', period='3mo')
df = analyzer.calculate_technical_indicators(df)

# 2. 可選：獲取情緒分析
from sentiment_analyzer import SentimentAnalyzer
sentiment_analyzer = SentimentAnalyzer()
news = sentiment_analyzer.fetch_stock_news('2330.TW', num_articles=20)
sentiment_results = sentiment_analyzer.analyze_news_sentiment(news)
sentiment_summary = sentiment_analyzer.get_sentiment_summary()

# 3. 生成 AI 分析報告
analysis = quick_ai_analysis(
    stock_code='2330.TW',
    df=df,
    sentiment_summary=sentiment_summary,
    use_gemini=False  # 改為 True 使用 Gemini AI
)
```

### 📋 AI 報告內容

#### 4.1 分析摘要
- 股價趨勢描述（過去 30 天）
- 技術指標關鍵發現
- 媒體情緒觀察
- 綜合評估

#### 4.2 短期分析 (1-4週)
- 技術指標信號判斷
- 預測價格區間
- 短期操作建議
- 媒體情緒影響評估

#### 4.3 中長期分析 (1-6個月)
- 增長潛力評估
- 關鍵因素分析
- 潛在風險提示
- 長期投資建議

### 💡 範例輸出

```
🤖 AI 分析報告 (AI Analysis Report)
================================================================================

📊 股票代碼: 2330.TW
📅 分析時間: 2025-12-11 12:45:30

================================================================================

📋 **分析摘要 (Analysis Summary)**

**📈 股價趨勢分析**

2330.TW 在過去 30 天內呈現 **上漲 (Uptrend)** 態勢，股價從 $580.00 上漲至
$620.00，漲跌幅為 6.90%。

期間最高價為 $625.00，最低價為 $575.00，平均價格為 $600.50。

**🔍 技術信號分析**

技術指標顯示 **看漲 (Bullish)** 信號，其中 4 個看漲信號，1 個看跌信號。

  ✅ MA5 > MA20: 短期趨勢向上
  ✅ RSI = 62.5: 強勢區域
  ✅ MACD 柱狀圖 > 0: 多頭趨勢
  ✅ KD 黃金交叉 (K=75.2, D=68.3): 買入信號

================================================================================

🔮 **短期分析 (1-4週)**

  預計短期價格區間: $610.00 - $640.00
  📰 媒體情緒偏向看漲，支持短期上漲

💡 建議: 短期看漲，可考慮逢低買入

================================================================================

🎯 **中長期分析 (1-6個月)**

📈 增長潛力: 增長潛力強勁，長期看好

關鍵要點:
  ✅ 股價處於上升趨勢，基本面向好
  🔑 關鍵因素: 關注行業政策變化、競爭格局、公司基本面

💡 建議: 適合長期持有，可分批建倉

================================================================================

⚠️  **免責聲明**: 本分析僅供參考，不構成投資建議。投資有風險，決策需謹慎。
================================================================================
```

---

## 5. 批量處理

### 📦 批量生成報告

適合同時分析多支股票：

```python
from comprehensive_report import batch_report

# 定義股票列表
stock_list = [
    'NVDA',      # NVIDIA
    'TSLA',      # Tesla
    'AAPL',      # Apple
    '2330.TW',   # 台積電
    '2454.TW',   # 聯發科
]

# 批量生成報告
reports = batch_report(
    stock_codes=stock_list,
    period='3mo',
    num_news=10,  # 每支股票分析 10 篇新聞
    use_gemini=False,
    show_charts=False  # 批量處理建議關閉圖表
)

# 每支股票會自動生成 Excel 報告
```

### 🎯 批量處理特點

- ✅ 自動處理錯誤（某支股票失敗不影響其他）
- ✅ 每支股票生成獨立的 Excel 報告
- ✅ 自動延遲避免 API 限流
- ✅ 顯示處理進度

---

## 6. 報告導出

### 📁 導出 Excel 報告

```python
from comprehensive_report import ComprehensiveReportGenerator

# 生成報告
generator = ComprehensiveReportGenerator()
report = generator.generate_full_report(
    stock_code='NVDA',
    period='3mo',
    num_news=20,
    show_charts=True
)

# 導出 Excel
filename = generator.export_report_to_excel()
# 輸出: NVDA_report_20251211_123045.xlsx
```

### 📊 Excel 報告內容

報告包含多個工作表 (Sheet)：

1. **基本信息**
   - 股票代碼
   - 生成時間
   - 分析周期

2. **股票數據**
   - 完整的 OHLCV 數據
   - 所有技術指標

3. **情緒分析**
   - 每篇新聞的標題、情緒、分數
   - 發布時間、來源

4. **價格趨勢**
   - 起始/結束價格
   - 漲跌幅
   - 最高/最低價
   - 趨勢判斷

5. **技術信號**
   - 整體信號
   - 看漲/看跌信號統計

### 🖼️ 保存圖表

```python
# 保存所有圖表為 PNG
saved_files = generator.save_charts(prefix='NVDA')
# 輸出: ['NVDA_chart.png']
```

---

## 🎓 實戰範例

### 範例 1：完整分析台積電

```python
from comprehensive_report import quick_report

# 生成台積電完整分析
report = quick_report(
    stock_code='2330.TW',
    period='6mo',  # 6個月數據
    num_news=30,   # 分析30篇新聞
    show_charts=True,
    export_excel=True
)

print("✅ 報告生成完成！")
print(f"📊 分析了 {len(report['stock_data'])} 個交易日")
if report['sentiment_summary']:
    print(f"📰 分析了 {report['sentiment_summary']['total_articles']} 篇新聞")
```

### 範例 2：比較多支股票

```python
from comprehensive_report import ComprehensiveReportGenerator

stocks = ['2330.TW', '2454.TW', '2317.TW']  # 台積電、聯發科、鴻海
results = {}

for stock in stocks:
    generator = ComprehensiveReportGenerator()
    report = generator.generate_full_report(
        stock_code=stock,
        period='3mo',
        num_news=15,
        show_charts=False
    )

    # 提取關鍵指標
    if report:
        results[stock] = {
            'trend': report['ai_analysis']['price_trend']['trend'],
            'price_change_pct': report['ai_analysis']['price_trend']['price_change_pct'],
            'overall_signal': report['ai_analysis']['technical_signals']['overall_signal'],
        }

        # 導出報告
        generator.export_report_to_excel()

# 比較結果
import pandas as pd
comparison = pd.DataFrame(results).T
print("\n📊 股票比較：")
print(comparison)
```

### 範例 3：定時監控（每日分析）

```python
import schedule
import time

def daily_analysis():
    """每日定時分析"""
    from comprehensive_report import quick_report
    from datetime import datetime

    print(f"\n{'='*60}")
    print(f"📅 每日分析 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 分析關注的股票
    watchlist = ['2330.TW', 'NVDA', 'TSLA']

    for stock in watchlist:
        print(f"\n分析 {stock}...")
        quick_report(
            stock_code=stock,
            period='1mo',
            num_news=10,
            show_charts=False,
            export_excel=True
        )

    print("\n✅ 今日分析完成！")

# 設定每天早上 9:00 執行
schedule.every().day.at("09:00").do(daily_analysis)

# 運行調度器
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## ⚠️ 常見問題

### Q1: 為什麼有些股票無法獲取新聞？
**A:** 某些股票（特別是小型股）可能沒有足夠的新聞報導。系統會自動跳過情緒分析，繼續完成技術分析部分。

### Q2: Gemini API 有使用限制嗎？
**A:** 是的，免費版有請求頻率限制（通常每分鐘 60 次）。批量處理時建議：
- 減少 `num_news` 數量
- 設置 `use_gemini=False` 使用簡化版分析
- 在請求之間增加延遲

### Q3: 如何提高情緒分析準確度？
**A:**
1. 使用 Gemini API（`use_gemini=True`）
2. 增加分析的新聞數量
3. 關注近期新聞（最近 7 天效果最好）

### Q4: Excel 報告可以自訂格式嗎？
**A:** 可以修改 `comprehensive_report.py` 中的 `export_report_to_excel()` 方法來自訂工作表、格式和內容。

### Q5: 可以分析加密貨幣嗎？
**A:** 可以！只需使用加密貨幣的代碼，例如：
```python
quick_report(stock_code='BTC-USD', period='1mo')
```

---

## 📚 下一步

- 查看 [README.md](README.md) 了解基本功能
- 查看 [QUICK_START.md](QUICK_START.md) 快速上手
- 嘗試在 Jupyter Notebook 中運行範例
- 探索自訂策略和參數調整

## 🤝 需要幫助？

如有問題，請：
1. 查看項目文檔
2. 提交 GitHub Issue
3. 參考代碼中的註釋和 docstring

祝您投資順利！📈
