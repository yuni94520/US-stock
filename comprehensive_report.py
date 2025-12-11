"""
综合报告生成器
整合所有分析模块，生成完整的股票分析报告
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 导入各个分析模块
try:
    from taiwan_stock_analyzer import TaiwanStockAnalyzer
    from chart_visualizer import ChartVisualizer, plot_candlestick_chart
    from sentiment_analyzer import SentimentAnalyzer
    from ai_analyzer import AIAnalyzer
except ImportError as e:
    print(f"⚠️  导入模块失败: {e}")


class ComprehensiveReportGenerator:
    """综合报告生成器"""

    def __init__(self, gemini_api_key=None):
        """
        初始化综合报告生成器

        参数：
            gemini_api_key: str, Google Gemini API Key（可选）
        """
        self.gemini_api_key = gemini_api_key
        self.stock_analyzer = TaiwanStockAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer(gemini_api_key)
        self.ai_analyzer = AIAnalyzer(gemini_api_key)
        self.chart_visualizer = ChartVisualizer()

        self.report_data = {}

    def generate_full_report(self, stock_code, period='3mo', num_news=20,
                            use_gemini=False, show_charts=True):
        """
        生成完整的分析报告

        参数：
            stock_code: str, 股票代码（例如：NVDA, 2330.TW）
            period: str, 数据时间范围（1mo, 3mo, 6mo, 1y）
            num_news: int, 分析新闻数量
            use_gemini: bool, 是否使用 Gemini AI
            show_charts: bool, 是否显示图表

        返回：
            dict, 完整报告数据
        """
        print("\n" + "=" * 80)
        print(f"🚀 开始生成 {stock_code} 的综合分析报告")
        print("=" * 80 + "\n")

        # ==================== 步骤 1: 获取股票数据 ====================
        print("📊 步骤 1/4: 获取股票数据...\n")
        df = self.stock_analyzer.fetch_stock_data(stock_code, period=period)

        if df is None or df.empty:
            print(f"❌ 无法获取 {stock_code} 的数据，报告生成失败")
            return None

        # 计算技术指标
        df = self.stock_analyzer.calculate_technical_indicators(df)

        # ==================== 步骤 2: 新闻情绪分析 ====================
        print("\n" + "=" * 80)
        print("📰 步骤 2/4: 新闻情绪分析...\n")

        # 获取新闻
        news = self.sentiment_analyzer.fetch_stock_news(stock_code, num_news)

        sentiment_summary = None
        if news:
            # 分析情绪
            sentiment_results = self.sentiment_analyzer.analyze_news_sentiment(
                news, use_gemini=use_gemini, api_key=self.gemini_api_key
            )

            # 获取情绪摘要
            sentiment_summary = self.sentiment_analyzer.get_sentiment_summary(sentiment_results)

            # 显示情绪摘要
            self.sentiment_analyzer.display_sentiment_summary(sentiment_summary)

            # 绘制情绪分布图
            if show_charts:
                self.sentiment_analyzer.plot_sentiment_distribution(sentiment_summary)
        else:
            print("⚠️  未获取到新闻数据，跳过情绪分析")

        # ==================== 步骤 3: AI 综合分析 ====================
        print("\n" + "=" * 80)
        print("🤖 步骤 3/4: AI 综合分析...\n")

        analysis = self.ai_analyzer.generate_analysis_summary(
            stock_code, df, sentiment_summary, use_gemini=use_gemini
        )

        # 显示分析报告
        self.ai_analyzer.display_analysis_report(analysis)

        # ==================== 步骤 4: 绘制图表 ====================
        if show_charts:
            print("\n" + "=" * 80)
            print("📈 步骤 4/4: 绘制技术分析图表...\n")

            # 绘制 K 线图
            print("绘制 K 线图...")
            self.chart_visualizer.plot_candlestick(df, stock_code, show_volume=True)

            # 绘制技术指标对比图
            print("\n绘制技术指标对比图...")
            self.chart_visualizer.plot_technical_comparison(df, stock_code)

        # ==================== 整理报告数据 ====================
        self.report_data = {
            'stock_code': stock_code,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'period': period,
            'stock_data': df,
            'sentiment_summary': sentiment_summary,
            'sentiment_results': self.sentiment_analyzer.sentiment_results if news else None,
            'ai_analysis': analysis,
        }

        print("\n" + "=" * 80)
        print("✅ 综合分析报告生成完成！")
        print("=" * 80 + "\n")

        return self.report_data

    def export_report_to_excel(self, filename=None):
        """
        导出报告到 Excel 文件

        参数：
            filename: str, 文件名（如果为 None，自动生成）

        返回：
            str, 导出的文件名
        """
        if not self.report_data:
            print("❌ 没有可导出的报告数据")
            return None

        if filename is None:
            stock_code = self.report_data['stock_code'].replace('.', '_')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{stock_code}_report_{timestamp}.xlsx"

        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # 1. 基本信息
                info_data = {
                    '股票代码': [self.report_data['stock_code']],
                    '生成时间': [self.report_data['generated_at']],
                    '分析周期': [self.report_data['period']],
                }
                pd.DataFrame(info_data).to_excel(writer, sheet_name='基本信息', index=False)

                # 2. 股票数据
                if 'stock_data' in self.report_data:
                    df = self.report_data['stock_data']
                    df.to_excel(writer, sheet_name='股票数据')

                # 3. 情绪分析结果
                if self.report_data.get('sentiment_results') is not None:
                    sentiment_df = self.report_data['sentiment_results']
                    if isinstance(sentiment_df, pd.DataFrame):
                        sentiment_df.to_excel(writer, sheet_name='情绪分析', index=False)

                # 4. AI 分析摘要
                if 'ai_analysis' in self.report_data:
                    analysis = self.report_data['ai_analysis']

                    # 价格趋势
                    price_trend_df = pd.DataFrame([analysis['price_trend']])
                    price_trend_df.to_excel(writer, sheet_name='价格趋势', index=False)

                    # 技术信号
                    tech_signals = {
                        '整体信号': [analysis['technical_signals']['overall_signal']],
                        '看涨信号数': [analysis['technical_signals']['bullish_count']],
                        '看跌信号数': [analysis['technical_signals']['bearish_count']],
                    }
                    pd.DataFrame(tech_signals).to_excel(writer, sheet_name='技术信号', index=False)

            print(f"✅ 报告已导出至: {filename}")
            return filename

        except Exception as e:
            print(f"❌ 导出报告失败: {e}")
            return None

    def save_charts(self, prefix=None):
        """
        保存图表为图片文件

        参数：
            prefix: str, 文件名前缀（如果为 None，使用股票代码）

        返回：
            list, 保存的文件名列表
        """
        if not self.report_data:
            print("❌ 没有可保存的图表")
            return []

        if prefix is None:
            prefix = self.report_data['stock_code'].replace('.', '_')

        saved_files = []

        try:
            # 保存当前图表（如果存在）
            if self.chart_visualizer.fig is not None:
                filename = f"{prefix}_chart.png"
                self.chart_visualizer.save_chart(filename, dpi=300)
                saved_files.append(filename)

            return saved_files

        except Exception as e:
            print(f"❌ 保存图表失败: {e}")
            return saved_files


# ==================== 便捷函数 ====================

def quick_report(stock_code, gemini_api_key=None, period='3mo', num_news=20,
                use_gemini=False, show_charts=True, export_excel=False):
    """
    快速生成完整报告

    参数：
        stock_code: str, 股票代码
        gemini_api_key: str, Gemini API Key（可选）
        period: str, 数据时间范围
        num_news: int, 分析新闻数量
        use_gemini: bool, 是否使用 Gemini AI
        show_charts: bool, 是否显示图表
        export_excel: bool, 是否导出 Excel

    返回：
        ComprehensiveReportGenerator 实例
    """
    generator = ComprehensiveReportGenerator(gemini_api_key)

    # 生成报告
    report = generator.generate_full_report(
        stock_code=stock_code,
        period=period,
        num_news=num_news,
        use_gemini=use_gemini,
        show_charts=show_charts
    )

    # 导出 Excel（如果需要）
    if export_excel and report:
        generator.export_report_to_excel()

    return generator


def batch_report(stock_codes, gemini_api_key=None, period='3mo',
                num_news=10, use_gemini=False, show_charts=False):
    """
    批量生成多支股票的报告

    参数：
        stock_codes: list, 股票代码列表
        gemini_api_key: str, Gemini API Key
        period: str, 数据时间范围
        num_news: int, 每支股票分析的新闻数量
        use_gemini: bool, 是否使用 Gemini AI
        show_charts: bool, 是否显示图表

    返回：
        dict, {股票代码: 报告数据}
    """
    print("\n" + "=" * 80)
    print(f"🚀 批量生成 {len(stock_codes)} 支股票的分析报告")
    print("=" * 80 + "\n")

    all_reports = {}

    for i, stock_code in enumerate(stock_codes, 1):
        print(f"\n{'#' * 80}")
        print(f"# [{i}/{len(stock_codes)}] 正在处理: {stock_code}")
        print(f"{'#' * 80}\n")

        generator = ComprehensiveReportGenerator(gemini_api_key)

        report = generator.generate_full_report(
            stock_code=stock_code,
            period=period,
            num_news=num_news,
            use_gemini=use_gemini,
            show_charts=show_charts
        )

        if report:
            all_reports[stock_code] = report

            # 导出 Excel
            generator.export_report_to_excel()

        # 避免请求过快
        import time
        time.sleep(2)

    print("\n" + "=" * 80)
    print(f"✅ 批量报告生成完成！成功生成 {len(all_reports)} 份报告")
    print("=" * 80 + "\n")

    return all_reports


# ==================== 示例使用 ====================

if __name__ == "__main__":
    # 示例 1: 快速生成单一股票报告
    print("示例 1: 生成 NVDA 的综合分析报告\n")

    # 如果有 Gemini API Key，可以启用 AI 分析
    # GEMINI_API_KEY = "your-api-key-here"
    GEMINI_API_KEY = None

    generator = quick_report(
        stock_code='NVDA',
        gemini_api_key=GEMINI_API_KEY,
        period='3mo',
        num_news=20,
        use_gemini=False,  # 设为 True 以使用 Gemini AI
        show_charts=True,
        export_excel=True
    )

    # 示例 2: 批量生成多支股票报告（取消注释以运行）
    # stock_list = ['2330.TW', '2454.TW', '2317.TW']
    # batch_report(stock_list, gemini_api_key=GEMINI_API_KEY, show_charts=False)
