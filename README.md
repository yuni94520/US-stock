# 台股技術分析工具 Taiwan Stock Technical Analyzer

這是一個可以在 Google Colab 上執行的台股技術分析工具，用於爬取 Yahoo Finance 台股數據，分析技術型態，並根據可調整的投資策略篩選符合條件的股票。

## 功能特色

- 📊 **成交量排名**：自動抓取前一天成交量前 50 名的台股
- 📈 **技術指標分析**：支援多種技術指標（MA、RSI、MACD、KD 等）
- 🎯 **投資策略**：可自訂多種投資策略並篩選符合條件的股票
- 💻 **Colab 友善**：專為 Google Colab 環境優化，無需本地安裝
- 🔄 **即時數據**：從 Yahoo Finance 抓取最新台股數據

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

```python
# 1. 獲取成交量前 50 名股票
top_50_stocks = get_top_volume_stocks(date='2025-12-09')

# 2. 分析技術指標
stock_data = analyze_stock('2330.TW')  # 台積電

# 3. 應用投資策略
matched_stocks = apply_strategy(top_50_stocks, strategy='golden_cross')

# 4. 顯示結果
display_results(matched_stocks)
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

- pandas：數據處理
- yfinance：Yahoo Finance API
- pandas-ta：技術指標計算
- matplotlib：數據視覺化
- requests：網路請求

## 授權

MIT License

## 貢獻

歡迎提交 Issues 和 Pull Requests！

## 免責聲明

本工具僅供教育和研究用途。所有投資決策應基於您自己的研究和風險評估。作者不對任何投資損失負責。
