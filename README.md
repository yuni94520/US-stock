# 台股技術分析工具 Taiwan Stock Technical Analyzer

這是一個功能完整的股票技術分析工具，可在 Google Colab 上執行。支援台股、美股等多個市場，提供技術分析、新聞情緒分析和 AI 綜合報告。

## 🆕 最新功能

### ✨ 完整的 AI 驅動分析報告

只需輸入股票代碼（如 NVDA、2330.TW），即可自動生成包含以下內容的完整分析報告：

1. **📈 股價趨勢圖 (K 線圖)**
   - 專業的蜡烛圖（K 線圖）顯示開盤、收盤、最高、最低價
   - 多條移動平均線（MA5、MA10、MA20、MA60）
   - 成交量柱狀圖
   - 技術指標圖表（RSI、MACD、KD、布林通道）

2. **📰 情緒新聞摘要**
   - 自動抓取最新相關新聞（支援 Yahoo Finance）
   - AI 驅動的情緒分析（支援 Google Gemini API）
   - 情緒統計總覽：
     - 股東情緒分佈（看漲、稍樂觀、中性等）
     - 文章情緒分佈
     - 新聞總數、平均情緒分數
   - 視覺化情緒分佈圖表

3. **🤖 AI 分析結果**
   - **分析總結**：描述股價趨勢、關鍵發現、媒體情緒觀察
   - **技術信號分析**：綜合判斷多個技術指標的買賣信號
   - **潛在風險提示**：指出市場可能面臨的挑戰

4. **🎯 綜合分析（短期與中長期）**
   - **短期分析（1-4週）**：預測近期股價區間、提供操作建議
   - **中長期分析（1-6個月）**：評估長期增長潛力、關鍵因素分析
   - **投資建議**：基於多維度分析的具體建議

5. **📊 報告導出**
   - 導出完整的 Excel 報告（包含所有數據和分析結果）
   - 保存高清圖表（PNG 格式）
   - 支援批量生成多支股票報告

## 功能特色

- 📊 **成交量排名**：自動抓取前一天成交量前 50 名的台股
- 📈 **技術指標分析**：支援多種技術指標（MA、RSI、MACD、KD、布林通道）
- 📰 **新聞情緒分析**：AI 分析市場新聞，評估投資者情緒
- 🤖 **AI 綜合分析**：結合技術面和情緒面，生成投資建議
- 📉 **專業圖表**：K 線圖、技術指標圖、情緒分佈圖
- 🎯 **投資策略**：8+ 種內建策略，支援自訂策略
- 💻 **Colab 友善**：專為 Google Colab 環境優化，無需本地安裝
- 🔄 **即時數據**：從 Yahoo Finance 抓取最新股票數據
- 📁 **報告導出**：自動生成 Excel 報告和圖表文件

## 快速開始

### 在 Google Colab 中使用

1. 打開 Google Colab：https://colab.research.google.com/
2. 上傳 `taiwan_stock_analyzer.ipynb` 檔案
3. 執行第一個 cell 安裝依賴套件
4. 依序執行其他 cells 開始分析

### 本地使用

```bash
# 安裝依賴
pip install -r requirements.txt

# 執行 Jupyter Notebook
jupyter notebook taiwan_stock_analyzer.ipynb
```

## 支援的技術指標

- **移動平均線（MA）**：5日、10日、20日、60日均線
- **相對強弱指標（RSI）**：衡量超買超賣
- **KD 指標**：隨機指標
- **MACD**：指數平滑移動平均線
- **布林通道（Bollinger Bands）**：波動率指標
- **成交量分析**：量價關係

## 內建投資策略

1. **黃金交叉策略**：短期均線向上突破長期均線
2. **RSI 超賣策略**：RSI < 30，潛在反彈機會
3. **量增價漲策略**：成交量放大且股價上漲
4. **突破策略**：突破布林通道上緣
5. **KD 黃金交叉**：K 線向上突破 D 線

## 使用範例

### 範例 1：快速生成完整分析報告

```python
from comprehensive_report import quick_report

# 生成 NVDA 的完整分析報告（包含 K 線圖、情緒分析、AI 分析）
generator = quick_report(
    stock_code='NVDA',
    period='3mo',           # 分析 3 個月數據
    num_news=20,            # 分析 20 篇新聞
    show_charts=True,       # 顯示圖表
    export_excel=True       # 導出 Excel 報告
)

# 如果有 Google Gemini API Key，可以啟用 AI 分析
generator = quick_report(
    stock_code='2330.TW',
    gemini_api_key='your-api-key-here',
    use_gemini=True,        # 使用 Gemini AI 進行深度分析
    show_charts=True
)
```

### 範例 2：傳統技術分析（台股）

```python
from taiwan_stock_analyzer import TaiwanStockAnalyzer
from strategies import apply_strategy

# 1. 初始化分析器
analyzer = TaiwanStockAnalyzer()

# 2. 獲取成交量前 50 名股票
top_50 = analyzer.get_top_volume_stocks(top_n=50)

# 3. 分析技術指標
stock_data = analyzer.analyze_stocks(top_50, period='3mo')

# 4. 應用黃金交叉策略
matched = apply_strategy(stock_data, 'golden_cross')
print(f"符合黃金交叉策略的股票: {matched}")

# 5. 繪製台積電的技術圖表
analyzer.plot_stock_chart('2330.TW', stock_data['2330.TW'])
```

### 範例 3：繪製專業 K 線圖

```python
from chart_visualizer import plot_candlestick_chart
from taiwan_stock_analyzer import TaiwanStockAnalyzer

# 獲取股票數據
analyzer = TaiwanStockAnalyzer()
df = analyzer.fetch_stock_data('NVDA', period='6mo')
df = analyzer.calculate_technical_indicators(df)

# 繪製 K 線圖
plot_candlestick_chart(df, stock_code='NVDA', show_volume=True)
```

### 範例 4：新聞情緒分析

```python
from sentiment_analyzer import quick_sentiment_analysis

# 快速分析 NVDA 的新聞情緒
analyzer, summary = quick_sentiment_analysis(
    stock_symbol='NVDA',
    num_articles=20,
    use_gemini=False  # 設為 True 使用 Gemini AI
)

# 結果會自動顯示：
# - 情緒分布統計
# - 平均情緒分數
# - 情緒分布圖表（餅圖和柱狀圖）
```

### 範例 5：批量生成多支股票報告

```python
from comprehensive_report import batch_report

# 批量分析多支股票
stock_list = ['NVDA', 'TSLA', 'AAPL', '2330.TW', '2454.TW']

reports = batch_report(
    stock_codes=stock_list,
    period='3mo',
    num_news=10,
    show_charts=False  # 批量處理時建議關閉圖表顯示
)

# 每支股票會自動生成 Excel 報告
```

## 自訂策略

您可以輕鬆自訂投資策略：

```python
def my_custom_strategy(df):
    """
    自訂策略範例：RSI < 40 且 MA5 > MA20
    """
    condition = (df['RSI'] < 40) & (df['MA5'] > df['MA20'])
    return condition

# 應用自訂策略
results = apply_custom_strategy(top_50_stocks, my_custom_strategy)
```

## 注意事項

- 台股代碼需加上 `.TW` 後綴（例如：2330.TW）
- Yahoo Finance API 有請求限制，建議加入延遲
- 技術分析僅供參考，投資有風險，請謹慎評估
- 建議使用至少 3 個月的歷史數據進行分析

## 依賴套件

- **pandas**：數據處理
- **yfinance**：Yahoo Finance API
- **pandas-ta**：技術指標計算
- **matplotlib**：數據視覺化和圖表繪製
- **seaborn**：進階視覺化
- **requests**：網路請求
- **google-generativeai**：Google Gemini AI API（可選，用於 AI 分析）
- **openpyxl**：Excel 報告導出
- **beautifulsoup4 & lxml**：網頁解析

## 模組說明

本專案包含以下核心模組：

| 模組文件 | 功能說明 |
|---------|---------|
| `taiwan_stock_analyzer.py` | 台股分析器主程式，提供基礎技術分析功能 |
| `strategies.py` | 投資策略模組，包含 8+ 種內建策略 |
| `chart_visualizer.py` | 圖表可視化模組，繪製 K 線圖和技術指標圖 |
| `sentiment_analyzer.py` | 新聞情緒分析模組，支援 AI 情緒識別 |
| `ai_analyzer.py` | AI 綜合分析模組，生成投資建議和風險評估 |
| `comprehensive_report.py` | 綜合報告生成器，整合所有功能 |
| `taiwan_stock_analyzer.ipynb` | Jupyter Notebook 版本，適合 Colab 使用 |

## 獲取 Google Gemini API Key（可選）

如果想使用 AI 驅動的情緒分析和智能報告，需要 Google Gemini API Key：

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入 Google 帳號
3. 點擊「Create API Key」
4. 複製 API Key
5. 在程式中設定：

```python
GEMINI_API_KEY = "your-api-key-here"
generator = quick_report(stock_code='NVDA', gemini_api_key=GEMINI_API_KEY, use_gemini=True)
```

**注意**：即使不使用 Gemini API，本工具仍可正常運行，會使用基於關鍵詞的簡化版情緒分析。

## 授權

MIT License

## 貢獻

歡迎提交 Issues 和 Pull Requests！

## 免責聲明

本工具僅供教育和研究用途。所有投資決策應基於您自己的研究和風險評估。作者不對任何投資損失負責。
