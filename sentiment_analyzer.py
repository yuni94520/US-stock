"""
新闻情绪分析模块
使用 AI 分析股票相关新闻的市场情绪
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
from collections import Counter
import time
import warnings
warnings.filterwarnings('ignore')


class SentimentAnalyzer:
    """新闻情绪分析器"""

    def __init__(self, gemini_api_key=None):
        """
        初始化情绪分析器

        参数：
            gemini_api_key: str, Google Gemini API Key（用于 AI 情绪分析）
        """
        self.gemini_api_key = gemini_api_key
        self.news_data = []
        self.sentiment_results = {}

    def fetch_stock_news(self, stock_symbol, num_articles=20):
        """
        获取股票相关新闻

        参数：
            stock_symbol: str, 股票代码（例如：NVDA, 2330.TW）
            num_articles: int, 获取新闻数量

        返回：
            list, 新闻列表
        """
        print(f"📰 正在获取 {stock_symbol} 的新闻...")

        # 使用 yfinance 获取新闻
        try:
            import yfinance as yf
            stock = yf.Ticker(stock_symbol)
            news = stock.news

            if not news:
                print("⚠️  无法获取新闻数据")
                return []

            # 整理新闻数据
            news_list = []
            for item in news[:num_articles]:
                news_item = {
                    'title': item.get('title', ''),
                    'publisher': item.get('publisher', ''),
                    'link': item.get('link', ''),
                    'published_date': datetime.fromtimestamp(item.get('providerPublishTime', 0)),
                    'type': item.get('type', 'article'),
                }
                news_list.append(news_item)

            self.news_data = news_list
            print(f"✅ 成功获取 {len(news_list)} 篇新闻")
            return news_list

        except Exception as e:
            print(f"❌ 获取新闻失败: {e}")
            return []

    def analyze_sentiment_with_gemini(self, text, api_key=None):
        """
        使用 Google Gemini API 分析文本情绪

        参数：
            text: str, 要分析的文本
            api_key: str, Gemini API Key

        返回：
            dict, 情绪分析结果
        """
        if api_key is None:
            api_key = self.gemini_api_key

        if not api_key:
            # 如果没有 API Key，使用简化版情绪分析
            return self._simple_sentiment_analysis(text)

        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')

            prompt = f"""
请分析以下股票新闻标题的市场情绪。

新闻标题: {text}

请以 JSON 格式返回分析结果，包含以下字段：
1. sentiment: 情绪分类（Bullish / Somewhat-Bullish / Neutral / Somewhat-Bearish / Bearish）
2. score: 情绪分数（-1 到 1 之间，-1 为极度看跌，1 为极度看涨）
3. confidence: 置信度（0 到 1 之间）
4. reason: 简短的判断理由

格式：
{{
  "sentiment": "Bullish",
  "score": 0.8,
  "confidence": 0.9,
  "reason": "新闻提到公司业绩强劲增长"
}}
"""

            response = model.generate_content(prompt)
            result_text = response.text.strip()

            # 尝试解析 JSON
            import json
            # 移除可能的 markdown 代码块标记
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            result = json.loads(result_text)
            return result

        except Exception as e:
            print(f"⚠️  Gemini API 分析失败: {e}，使用简化版分析")
            return self._simple_sentiment_analysis(text)

    def _simple_sentiment_analysis(self, text):
        """
        简化版情绪分析（基于关键词）

        参数：
            text: str, 要分析的文本

        返回：
            dict, 情绪分析结果
        """
        text_lower = text.lower()

        # 定义关键词
        bullish_keywords = [
            'surge', 'soar', 'rally', 'gain', 'rise', 'jump', 'climb', 'growth', 'profit',
            'beat', 'exceed', 'strong', 'bullish', 'positive', 'upgrade', 'buy', 'outperform',
            '上涨', '增长', '看涨', '利好', '突破', '创新高', '强劲', '超预期'
        ]

        bearish_keywords = [
            'plunge', 'fall', 'drop', 'decline', 'loss', 'weak', 'bearish', 'negative',
            'downgrade', 'sell', 'underperform', 'concern', 'risk', 'warning',
            '下跌', '下降', '看跌', '利空', '风险', '警告', '疲软', '亏损'
        ]

        neutral_keywords = [
            'stable', 'hold', 'maintain', 'unchanged', 'flat',
            '稳定', '持平', '维持', '不变'
        ]

        # 计算情绪分数
        bullish_count = sum(1 for keyword in bullish_keywords if keyword in text_lower)
        bearish_count = sum(1 for keyword in bearish_keywords if keyword in text_lower)
        neutral_count = sum(1 for keyword in neutral_keywords if keyword in text_lower)

        total_count = bullish_count + bearish_count + neutral_count

        if total_count == 0:
            return {
                'sentiment': 'Neutral',
                'score': 0.0,
                'confidence': 0.5,
                'reason': '未检测到明显情绪关键词'
            }

        # 计算分数
        score = (bullish_count - bearish_count) / max(total_count, 1)

        # 确定情绪类别
        if score > 0.5:
            sentiment = 'Bullish'
        elif score > 0.2:
            sentiment = 'Somewhat-Bullish'
        elif score > -0.2:
            sentiment = 'Neutral'
        elif score > -0.5:
            sentiment = 'Somewhat-Bearish'
        else:
            sentiment = 'Bearish'

        confidence = min(abs(score) + 0.3, 1.0)

        return {
            'sentiment': sentiment,
            'score': score,
            'confidence': confidence,
            'reason': f'检测到 {bullish_count} 个看涨关键词, {bearish_count} 个看跌关键词'
        }

    def analyze_news_sentiment(self, news_list=None, use_gemini=False, api_key=None):
        """
        批量分析新闻情绪

        参数：
            news_list: list, 新闻列表（如果为 None，使用 self.news_data）
            use_gemini: bool, 是否使用 Gemini API
            api_key: str, Gemini API Key

        返回：
            DataFrame, 情绪分析结果
        """
        if news_list is None:
            news_list = self.news_data

        if not news_list:
            print("⚠️  没有可分析的新闻")
            return pd.DataFrame()

        print(f"\n🤖 开始分析 {len(news_list)} 篇新闻的情绪...")

        results = []

        for i, news in enumerate(news_list, 1):
            title = news.get('title', '')
            print(f"  [{i}/{len(news_list)}] 分析: {title[:50]}...")

            # 分析情绪
            if use_gemini and api_key:
                sentiment_result = self.analyze_sentiment_with_gemini(title, api_key)
                time.sleep(1)  # 避免 API 限流
            else:
                sentiment_result = self._simple_sentiment_analysis(title)

            results.append({
                'title': title,
                'publisher': news.get('publisher', ''),
                'published_date': news.get('published_date', ''),
                'sentiment': sentiment_result.get('sentiment', 'Neutral'),
                'score': sentiment_result.get('score', 0.0),
                'confidence': sentiment_result.get('confidence', 0.5),
                'reason': sentiment_result.get('reason', ''),
            })

        results_df = pd.DataFrame(results)
        self.sentiment_results = results_df

        print(f"✅ 情绪分析完成！\n")

        return results_df

    def get_sentiment_summary(self, results_df=None):
        """
        获取情绪统计摘要

        参数：
            results_df: DataFrame, 情绪分析结果（如果为 None，使用 self.sentiment_results）

        返回：
            dict, 情绪摘要统计
        """
        if results_df is None:
            if isinstance(self.sentiment_results, pd.DataFrame):
                results_df = self.sentiment_results
            else:
                print("⚠️  没有可用的情绪分析结果")
                return {}

        if results_df.empty:
            return {}

        # 统计情绪分布
        sentiment_counts = results_df['sentiment'].value_counts()
        total_count = len(results_df)

        # 计算比例
        sentiment_distribution = {}
        for sentiment, count in sentiment_counts.items():
            sentiment_distribution[sentiment] = {
                'count': count,
                'percentage': round(count / total_count * 100, 1)
            }

        # 计算平均分数
        avg_score = results_df['score'].mean()
        avg_confidence = results_df['confidence'].mean()

        # 整体情绪判断
        if avg_score > 0.3:
            overall_sentiment = '看涨 (Bullish)'
        elif avg_score > 0.1:
            overall_sentiment = '稍微看涨 (Somewhat Bullish)'
        elif avg_score > -0.1:
            overall_sentiment = '中性 (Neutral)'
        elif avg_score > -0.3:
            overall_sentiment = '稍微看跌 (Somewhat Bearish)'
        else:
            overall_sentiment = '看跌 (Bearish)'

        summary = {
            'total_articles': total_count,
            'sentiment_distribution': sentiment_distribution,
            'average_score': round(avg_score, 3),
            'average_confidence': round(avg_confidence, 3),
            'overall_sentiment': overall_sentiment,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        return summary

    def display_sentiment_summary(self, summary=None):
        """
        显示情绪摘要

        参数：
            summary: dict, 情绪摘要（如果为 None，自动生成）
        """
        if summary is None:
            summary = self.get_sentiment_summary()

        if not summary:
            print("⚠️  没有可显示的情绪摘要")
            return

        print("\n" + "=" * 70)
        print("📊 新闻情绪分析摘要 (Sentiment News Summary)")
        print("=" * 70)
        print(f"\n📰 分析新闻总数: {summary['total_articles']} 篇")
        print(f"📅 分析时间: {summary['analysis_date']}")
        print(f"\n🎯 整体市场情绪: {summary['overall_sentiment']}")
        print(f"📈 平均情绪分数: {summary['average_score']:.3f} (范围: -1 到 1)")
        print(f"🎲 平均置信度: {summary['average_confidence']:.1%}")

        print("\n📊 情绪分布统计:")
        print("-" * 70)

        for sentiment, data in sorted(summary['sentiment_distribution'].items(),
                                       key=lambda x: x[1]['count'], reverse=True):
            count = data['count']
            percentage = data['percentage']
            bar = '█' * int(percentage / 2)
            print(f"  {sentiment:20} | {bar:50} {percentage:5.1f}% ({count} 篇)")

        print("=" * 70 + "\n")

    def plot_sentiment_distribution(self, summary=None, figsize=(12, 6)):
        """
        绘制情绪分布图表

        参数：
            summary: dict, 情绪摘要
            figsize: tuple, 图表大小
        """
        import matplotlib.pyplot as plt

        if summary is None:
            summary = self.get_sentiment_summary()

        if not summary:
            print("⚠️  没有可绘制的情绪数据")
            return

        # 准备数据
        sentiments = []
        percentages = []
        colors_map = {
            'Bullish': '#2ECC71',
            'Somewhat-Bullish': '#82E0AA',
            'Neutral': '#95A5A6',
            'Somewhat-Bearish': '#F1948A',
            'Bearish': '#E74C3C'
        }

        for sentiment, data in sorted(summary['sentiment_distribution'].items(),
                                       key=lambda x: x[1]['percentage'], reverse=True):
            sentiments.append(sentiment)
            percentages.append(data['percentage'])

        colors = [colors_map.get(s, '#95A5A6') for s in sentiments]

        # 创建图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # 饼图
        ax1.pie(percentages, labels=sentiments, autopct='%1.1f%%',
                colors=colors, startangle=90, textprops={'fontsize': 10})
        ax1.set_title('新闻情绪分布 (Sentiment Distribution)', fontweight='bold', fontsize=14)

        # 柱状图
        bars = ax2.bar(sentiments, percentages, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
        ax2.set_title('情绪统计 (Sentiment Statistics)', fontweight='bold', fontsize=14)
        ax2.set_ylabel('百分比 (%)', fontweight='bold')
        ax2.set_xlabel('情绪类别', fontweight='bold')
        ax2.grid(axis='y', alpha=0.3, linestyle='--')

        # 在柱状图上显示数值
        for bar, pct in zip(bars, percentages):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')

        plt.xticks(rotation=15, ha='right')
        plt.tight_layout()
        plt.show()


# 便捷函数
def quick_sentiment_analysis(stock_symbol, num_articles=20, use_gemini=False, api_key=None):
    """
    快速进行情绪分析

    参数：
        stock_symbol: str, 股票代码
        num_articles: int, 分析新闻数量
        use_gemini: bool, 是否使用 Gemini API
        api_key: str, Gemini API Key

    返回：
        tuple, (SentimentAnalyzer实例, 情绪摘要)
    """
    analyzer = SentimentAnalyzer(gemini_api_key=api_key)

    # 获取新闻
    news = analyzer.fetch_stock_news(stock_symbol, num_articles)

    if not news:
        return analyzer, {}

    # 分析情绪
    results = analyzer.analyze_news_sentiment(news, use_gemini, api_key)

    # 获取摘要
    summary = analyzer.get_sentiment_summary(results)

    # 显示摘要
    analyzer.display_sentiment_summary(summary)

    # 绘制图表
    analyzer.plot_sentiment_distribution(summary)

    return analyzer, summary
