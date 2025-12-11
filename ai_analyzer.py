"""
AI 分析总结模块
结合技术分析和情绪分析，生成综合性的投资分析报告
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class AIAnalyzer:
    """AI 综合分析器"""

    def __init__(self, gemini_api_key=None):
        """
        初始化 AI 分析器

        参数：
            gemini_api_key: str, Google Gemini API Key
        """
        self.gemini_api_key = gemini_api_key
        self.analysis_result = {}

    def analyze_price_trend(self, df, period_days=30):
        """
        分析股价趋势

        参数：
            df: DataFrame, 股票数据
            period_days: int, 分析周期（天数）

        返回：
            dict, 趋势分析结果
        """
        if df is None or df.empty:
            return {}

        # 获取指定周期的数据
        df_period = df.tail(period_days) if len(df) > period_days else df

        start_price = df_period['Close'].iloc[0]
        end_price = df_period['Close'].iloc[-1]
        price_change = end_price - start_price
        price_change_pct = (price_change / start_price) * 100

        highest_price = df_period['High'].max()
        lowest_price = df_period['Low'].min()
        avg_price = df_period['Close'].mean()
        volatility = df_period['Close'].std()

        # 判断趋势
        if price_change_pct > 10:
            trend = '强劲上涨 (Strong Uptrend)'
            trend_en = 'Strong Uptrend'
        elif price_change_pct > 3:
            trend = '上涨 (Uptrend)'
            trend_en = 'Uptrend'
        elif price_change_pct > -3:
            trend = '盘整 (Sideways)'
            trend_en = 'Sideways'
        elif price_change_pct > -10:
            trend = '下跌 (Downtrend)'
            trend_en = 'Downtrend'
        else:
            trend = '大幅下跌 (Strong Downtrend)'
            trend_en = 'Strong Downtrend'

        return {
            'period_days': period_days,
            'start_price': round(start_price, 2),
            'end_price': round(end_price, 2),
            'price_change': round(price_change, 2),
            'price_change_pct': round(price_change_pct, 2),
            'highest_price': round(highest_price, 2),
            'lowest_price': round(lowest_price, 2),
            'avg_price': round(avg_price, 2),
            'volatility': round(volatility, 2),
            'trend': trend,
            'trend_en': trend_en,
        }

    def analyze_technical_signals(self, df):
        """
        分析技术信号

        参数：
            df: DataFrame, 包含技术指标的股票数据

        返回：
            dict, 技术信号分析
        """
        if df is None or df.empty:
            return {}

        latest = df.iloc[-1]
        signals = []
        bullish_count = 0
        bearish_count = 0

        # 1. 移动平均线信号
        if 'MA5' in df.columns and 'MA20' in df.columns:
            if latest['MA5'] > latest['MA20']:
                signals.append('✅ MA5 > MA20: 短期趋势向上')
                bullish_count += 1
            else:
                signals.append('❌ MA5 < MA20: 短期趋势向下')
                bearish_count += 1

        # 2. RSI 信号
        if 'RSI' in df.columns:
            rsi = latest['RSI']
            if rsi > 70:
                signals.append(f'⚠️  RSI = {rsi:.1f}: 超买区域，可能回调')
                bearish_count += 1
            elif rsi < 30:
                signals.append(f'✅ RSI = {rsi:.1f}: 超卖区域，可能反弹')
                bullish_count += 1
            elif 40 <= rsi <= 60:
                signals.append(f'➡️  RSI = {rsi:.1f}: 中性区域')
            elif rsi > 60:
                signals.append(f'✅ RSI = {rsi:.1f}: 强势区域')
                bullish_count += 1
            else:
                signals.append(f'❌ RSI = {rsi:.1f}: 弱势区域')
                bearish_count += 1

        # 3. MACD 信号
        if 'MACD_histogram' in df.columns:
            macd_hist = latest['MACD_histogram']
            if macd_hist > 0:
                signals.append('✅ MACD 柱状图 > 0: 多头趋势')
                bullish_count += 1
            else:
                signals.append('❌ MACD 柱状图 < 0: 空头趋势')
                bearish_count += 1

        # 4. KD 信号
        if 'K' in df.columns and 'D' in df.columns:
            k_value = latest['K']
            d_value = latest['D']
            if k_value > d_value and k_value < 80:
                signals.append(f'✅ KD 黄金交叉 (K={k_value:.1f}, D={d_value:.1f}): 买入信号')
                bullish_count += 1
            elif k_value < d_value and k_value > 20:
                signals.append(f'❌ KD 死亡交叉 (K={k_value:.1f}, D={d_value:.1f}): 卖出信号')
                bearish_count += 1

        # 5. 布林通道信号
        if 'BB_upper' in df.columns and 'BB_lower' in df.columns:
            close_price = latest['Close']
            bb_upper = latest['BB_upper']
            bb_lower = latest['BB_lower']

            if close_price > bb_upper:
                signals.append('⚠️  股价突破布林上轨: 可能超买')
                bearish_count += 1
            elif close_price < bb_lower:
                signals.append('✅ 股价跌破布林下轨: 可能超卖')
                bullish_count += 1

        # 综合判断
        total_signals = bullish_count + bearish_count
        if total_signals > 0:
            bullish_ratio = bullish_count / total_signals
            if bullish_ratio > 0.6:
                overall_signal = '看涨 (Bullish)'
            elif bullish_ratio > 0.4:
                overall_signal = '中性 (Neutral)'
            else:
                overall_signal = '看跌 (Bearish)'
        else:
            overall_signal = '中性 (Neutral)'

        return {
            'signals': signals,
            'bullish_count': bullish_count,
            'bearish_count': bearish_count,
            'overall_signal': overall_signal,
        }

    def generate_analysis_summary(self, stock_code, df, sentiment_summary=None, use_gemini=False):
        """
        生成分析摘要

        参数：
            stock_code: str, 股票代码
            df: DataFrame, 股票数据
            sentiment_summary: dict, 情绪分析摘要
            use_gemini: bool, 是否使用 Gemini AI 生成摘要

        返回：
            dict, 分析摘要
        """
        # 1. 价格趋势分析
        price_trend = self.analyze_price_trend(df, period_days=30)

        # 2. 技术信号分析
        technical_signals = self.analyze_technical_signals(df)

        # 3. 结合情绪分析
        if sentiment_summary:
            overall_sentiment = sentiment_summary.get('overall_sentiment', '中性')
            avg_sentiment_score = sentiment_summary.get('average_score', 0)
        else:
            overall_sentiment = '无情绪数据'
            avg_sentiment_score = 0

        # 4. 生成摘要文本
        if use_gemini and self.gemini_api_key:
            summary_text = self._generate_ai_summary(stock_code, price_trend, technical_signals, sentiment_summary)
        else:
            summary_text = self._generate_simple_summary(stock_code, price_trend, technical_signals, sentiment_summary)

        # 5. 短期和中长期分析
        short_term = self._analyze_short_term(price_trend, technical_signals, sentiment_summary)
        mid_long_term = self._analyze_mid_long_term(price_trend, technical_signals, sentiment_summary)

        analysis = {
            'stock_code': stock_code,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'price_trend': price_trend,
            'technical_signals': technical_signals,
            'sentiment_summary': sentiment_summary,
            'summary_text': summary_text,
            'short_term_analysis': short_term,
            'mid_long_term_analysis': mid_long_term,
        }

        self.analysis_result = analysis
        return analysis

    def _generate_simple_summary(self, stock_code, price_trend, technical_signals, sentiment_summary):
        """生成简化版摘要"""
        summary_parts = []

        # 价格趋势部分
        summary_parts.append(f"**📈 股价趋势分析**\n")
        summary_parts.append(
            f"{stock_code} 在过去 {price_trend['period_days']} 天内呈现 **{price_trend['trend']}** 态势，"
            f"股价从 ${price_trend['start_price']:.2f} {'上涨' if price_trend['price_change'] > 0 else '下跌'}至 "
            f"${price_trend['end_price']:.2f}，涨跌幅为 {price_trend['price_change_pct']:.2f}%。"
        )

        summary_parts.append(f"\n期间最高价为 ${price_trend['highest_price']:.2f}，"
                            f"最低价为 ${price_trend['lowest_price']:.2f}，"
                            f"平均价格为 ${price_trend['avg_price']:.2f}。")

        # 技术信号部分
        summary_parts.append(f"\n\n**🔍 技术信号分析**\n")
        summary_parts.append(f"技术指标显示 **{technical_signals['overall_signal']}** 信号，")
        summary_parts.append(f"其中 {technical_signals['bullish_count']} 个看涨信号，")
        summary_parts.append(f"{technical_signals['bearish_count']} 个看跌信号。\n")

        for signal in technical_signals['signals']:
            summary_parts.append(f"  {signal}\n")

        # 情绪分析部分
        if sentiment_summary:
            summary_parts.append(f"\n**📰 媒体情绪观察**\n")
            summary_parts.append(f"根据 {sentiment_summary['total_articles']} 篇相关新闻分析，")
            summary_parts.append(f"整体市场情绪为 **{sentiment_summary['overall_sentiment']}**，")
            summary_parts.append(f"平均情绪分数为 {sentiment_summary['average_score']:.3f}。\n")

            # 列出主要情绪分布
            summary_parts.append("\n情绪分布：\n")
            for sentiment, data in sorted(sentiment_summary['sentiment_distribution'].items(),
                                         key=lambda x: x[1]['percentage'], reverse=True):
                summary_parts.append(f"  • {sentiment}: {data['percentage']:.1f}%\n")

        return ''.join(summary_parts)

    def _generate_ai_summary(self, stock_code, price_trend, technical_signals, sentiment_summary):
        """使用 Gemini AI 生成摘要"""
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-pro')

            # 准备数据摘要
            data_summary = f"""
股票代码: {stock_code}
分析周期: {price_trend['period_days']} 天

价格数据:
- 起始价格: ${price_trend['start_price']}
- 结束价格: ${price_trend['end_price']}
- 涨跌幅: {price_trend['price_change_pct']}%
- 趋势: {price_trend['trend']}

技术信号:
- 整体信号: {technical_signals['overall_signal']}
- 看涨信号数: {technical_signals['bullish_count']}
- 看跌信号数: {technical_signals['bearish_count']}
"""

            if sentiment_summary:
                data_summary += f"""
情绪分析:
- 总新闻数: {sentiment_summary['total_articles']}
- 整体情绪: {sentiment_summary['overall_sentiment']}
- 平均分数: {sentiment_summary['average_score']}
"""

            prompt = f"""
请基于以下股票分析数据，生成一份专业的分析摘要。

{data_summary}

请以清晰、专业的语言撰写摘要，包含以下内容：
1. 股价趋势总结
2. 技术指标关键发现
3. 媒体情绪观察（如果有）
4. 综合评估

格式要求：使用 Markdown 格式，分段清晰，要点突出。
"""

            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            print(f"⚠️  Gemini AI 生成摘要失败: {e}，使用简化版本")
            return self._generate_simple_summary(stock_code, price_trend, technical_signals, sentiment_summary)

    def _analyze_short_term(self, price_trend, technical_signals, sentiment_summary):
        """短期分析（1-4周）"""
        analysis = {
            'title': '短期分析 (1-4周)',
            'key_points': [],
            'price_range': '',
            'recommendation': '',
        }

        # 基于技术信号判断
        if technical_signals['overall_signal'] == '看涨 (Bullish)':
            analysis['recommendation'] = '短期看涨，可考虑逢低买入'
            analysis['key_points'].append('✅ 技术指标显示短期向上趋势')
        elif technical_signals['overall_signal'] == '看跌 (Bearish)':
            analysis['recommendation'] = '短期看跌，建议观望或减仓'
            analysis['key_points'].append('❌ 技术指标显示短期向下趋势')
        else:
            analysis['recommendation'] = '短期中性，等待明确信号'
            analysis['key_points'].append('➡️  技术指标中性，方向不明')

        # 预测价格区间
        current_price = price_trend['end_price']
        volatility = price_trend['volatility']

        if technical_signals['overall_signal'] == '看涨 (Bullish)':
            lower_bound = current_price - volatility
            upper_bound = current_price + volatility * 2
        elif technical_signals['overall_signal'] == '看跌 (Bearish)':
            lower_bound = current_price - volatility * 2
            upper_bound = current_price + volatility
        else:
            lower_bound = current_price - volatility * 1.5
            upper_bound = current_price + volatility * 1.5

        analysis['price_range'] = f"预计短期价格区间: ${lower_bound:.2f} - ${upper_bound:.2f}"
        analysis['key_points'].append(analysis['price_range'])

        # 结合情绪分析
        if sentiment_summary:
            if '看涨' in sentiment_summary.get('overall_sentiment', ''):
                analysis['key_points'].append('📰 媒体情绪偏向看涨，支持短期上涨')
            elif '看跌' in sentiment_summary.get('overall_sentiment', ''):
                analysis['key_points'].append('📰 媒体情绪偏向看跌，可能施压股价')

        return analysis

    def _analyze_mid_long_term(self, price_trend, technical_signals, sentiment_summary):
        """中长期分析（1-6个月）"""
        analysis = {
            'title': '中长期分析 (1-6个月)',
            'key_points': [],
            'growth_potential': '',
            'risks': [],
            'recommendation': '',
        }

        # 基于趋势判断
        trend_en = price_trend.get('trend_en', '')

        if 'Uptrend' in trend_en:
            analysis['growth_potential'] = '增长潜力强劲，长期看好'
            analysis['recommendation'] = '适合长期持有，可分批建仓'
            analysis['key_points'].append('✅ 股价处于上升趋势，基本面向好')
        elif 'Downtrend' in trend_en:
            analysis['growth_potential'] = '面临下行压力，需谨慎'
            analysis['recommendation'] = '暂不建议长期配置，等待趋势反转'
            analysis['key_points'].append('❌ 股价处于下降趋势，可能继续调整')
        else:
            analysis['growth_potential'] = '盘整阶段，等待突破'
            analysis['recommendation'] = '可小仓位关注，等待明确方向'
            analysis['key_points'].append('➡️  股价处于盘整，需要突破确认')

        # 风险提示
        if price_trend['volatility'] > price_trend['avg_price'] * 0.05:
            analysis['risks'].append('⚠️  波动率较高，注意风险控制')

        if technical_signals.get('bearish_count', 0) > 2:
            analysis['risks'].append('⚠️  多个技术指标显示看跌信号')

        if sentiment_summary and '看跌' in sentiment_summary.get('overall_sentiment', ''):
            analysis['risks'].append('⚠️  媒体情绪偏向负面，需关注市场情绪变化')

        # 关键因素
        analysis['key_points'].append('🔑 关键因素: 关注行业政策变化、竞争格局、公司基本面')

        return analysis

    def display_analysis_report(self, analysis=None):
        """
        显示分析报告

        参数：
            analysis: dict, 分析结果（如果为 None，使用 self.analysis_result）
        """
        if analysis is None:
            analysis = self.analysis_result

        if not analysis:
            print("⚠️  没有可显示的分析报告")
            return

        print("\n" + "=" * 80)
        print("🤖 AI 分析报告 (AI Analysis Report)")
        print("=" * 80)
        print(f"\n📊 股票代码: {analysis['stock_code']}")
        print(f"📅 分析时间: {analysis['analysis_date']}")
        print("\n" + "=" * 80)

        # 1. 分析摘要
        print("\n📋 **分析摘要 (Analysis Summary)**\n")
        print(analysis['summary_text'])

        # 2. 短期分析
        print("\n" + "=" * 80)
        short_term = analysis['short_term_analysis']
        print(f"\n🔮 **{short_term['title']}**\n")
        for point in short_term['key_points']:
            print(f"  {point}")
        print(f"\n💡 建议: {short_term['recommendation']}")

        # 3. 中长期分析
        print("\n" + "=" * 80)
        mid_long = analysis['mid_long_term_analysis']
        print(f"\n🎯 **{mid_long['title']}**\n")
        print(f"📈 增长潜力: {mid_long['growth_potential']}\n")

        print("关键要点:")
        for point in mid_long['key_points']:
            print(f"  {point}")

        if mid_long['risks']:
            print("\n潜在风险:")
            for risk in mid_long['risks']:
                print(f"  {risk}")

        print(f"\n💡 建议: {mid_long['recommendation']}")

        print("\n" + "=" * 80)
        print("\n⚠️  **免责声明**: 本分析仅供参考，不构成投资建议。投资有风险，决策需谨慎。")
        print("=" * 80 + "\n")


# 便捷函数
def quick_ai_analysis(stock_code, df, sentiment_summary=None, use_gemini=False, api_key=None):
    """
    快速生成 AI 分析报告

    参数：
        stock_code: str, 股票代码
        df: DataFrame, 股票数据
        sentiment_summary: dict, 情绪分析摘要
        use_gemini: bool, 是否使用 Gemini AI
        api_key: str, Gemini API Key

    返回：
        dict, 分析报告
    """
    analyzer = AIAnalyzer(gemini_api_key=api_key)
    analysis = analyzer.generate_analysis_summary(stock_code, df, sentiment_summary, use_gemini)
    analyzer.display_analysis_report(analysis)
    return analysis
