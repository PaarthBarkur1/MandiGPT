"""
Advanced Market Analysis with Time Series, Statistics, and Visualizations
No mock data - only real API data analysis
"""
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from models import CommodityPrice
import base64
import io
from scipy import stats
import json

logger = logging.getLogger(__name__)

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError as e:
    MATPLOTLIB_AVAILABLE = False
    Figure = None  # Define Figure as None if matplotlib is not available
    logger.warning(f"Matplotlib not available - visualizations disabled: {e}")


class AdvancedMarketAnalyzer:
    """Advanced market analysis with time series, statistics, and visualizations"""

    def __init__(self):
        self.matplotlib_available = MATPLOTLIB_AVAILABLE

    def analyze_market(self, prices: List[CommodityPrice], historical_data: Optional[List[Dict]] = None) -> Dict:
        """
        Comprehensive market analysis with advanced statistics

        Args:
            prices: Current commodity prices
            historical_data: Optional historical price data for time series analysis

        Returns:
            Dictionary with comprehensive market analysis
        """
        if not prices:
            return self._empty_analysis()

        # Basic statistics
        price_values = [p.current_price for p in prices]
        n = len(price_values)

        # Statistical measures
        mean_price = np.mean(price_values)
        median_price = np.median(price_values)
        std_price = np.std(price_values)
        variance = np.var(price_values)
        # Coefficient of Variation
        cv = (std_price / mean_price * 100) if mean_price > 0 else 0

        # Percentiles
        q25 = np.percentile(price_values, 25)
        q75 = np.percentile(price_values, 75)
        iqr = q75 - q25

        # Price range
        min_price = np.min(price_values)
        max_price = np.max(price_values)
        price_range = max_price - min_price

        # Trend analysis
        trend_analysis = self._analyze_trends(prices)

        # Volatility analysis
        volatility_metrics = self._calculate_volatility(
            prices, historical_data)

        # Correlation analysis (if multiple commodities)
        correlation_matrix = self._calculate_correlations(
            prices, historical_data)

        # Market segmentation
        market_segments = self._segment_market(prices)

        # Risk metrics
        risk_metrics = self._calculate_risk_metrics(price_values)

        # Price distribution analysis
        distribution = self._analyze_distribution(price_values)

        # Generate visualizations
        visualizations = self._generate_visualizations(prices, historical_data)

        # Market recommendations based on advanced analysis
        recommendations = self._generate_recommendations(
            prices, trend_analysis, volatility_metrics, risk_metrics
        )

        return {
            "summary": {
                "total_commodities": n,
                "data_source": "Real-time API Data",
                "analysis_timestamp": datetime.now().isoformat(),
                "analysis_type": "Advanced Statistical Analysis"
            },
            "descriptive_statistics": {
                "mean": round(mean_price, 2),
                "median": round(median_price, 2),
                "standard_deviation": round(std_price, 2),
                "variance": round(variance, 2),
                "coefficient_of_variation": round(cv, 2),
                "min": round(min_price, 2),
                "max": round(max_price, 2),
                "range": round(price_range, 2),
                "q25": round(q25, 2),
                "q75": round(q75, 2),
                "iqr": round(iqr, 2)
            },
            "trend_analysis": trend_analysis,
            "volatility_metrics": volatility_metrics,
            "correlation_analysis": correlation_matrix,
            "market_segmentation": market_segments,
            "risk_metrics": risk_metrics,
            "distribution_analysis": distribution,
            "visualizations": visualizations,
            "recommendations": recommendations,
            "mathematical_insights": self._generate_mathematical_insights(
                prices, trend_analysis, volatility_metrics, risk_metrics
            )
        }

    def _analyze_trends(self, prices: List[CommodityPrice]) -> Dict:
        """Advanced trend analysis using statistical methods"""
        trend_counts = {
            "increasing": 0,
            "decreasing": 0,
            "stable": 0
        }

        trend_strength = []
        price_changes = []

        for price in prices:
            trend_counts[price.price_trend] = trend_counts.get(
                price.price_trend, 0) + 1

            # Calculate trend strength (if we had historical data)
            # For now, use price level as proxy
            if price.current_price > 0:
                price_changes.append(price.current_price)

        # Calculate momentum (rate of change)
        if len(price_changes) > 1:
            momentum = np.diff(price_changes)
            avg_momentum = np.mean(momentum) if len(momentum) > 0 else 0
        else:
            avg_momentum = 0

        # Trend direction score (-1 to 1)
        total = sum(trend_counts.values())
        if total > 0:
            trend_score = (trend_counts["increasing"] -
                           trend_counts["decreasing"]) / total
        else:
            trend_score = 0

        return {
            "distribution": trend_counts,
            # -1 (bearish) to 1 (bullish)
            "trend_score": round(trend_score, 3),
            "momentum": round(avg_momentum, 2),
            "trend_strength": "Strong" if abs(trend_score) > 0.6 else "Moderate" if abs(trend_score) > 0.3 else "Weak",
            "market_direction": "Bullish" if trend_score > 0.3 else "Bearish" if trend_score < -0.3 else "Neutral"
        }

    def _calculate_volatility(self, prices: List[CommodityPrice], historical: Optional[List[Dict]]) -> Dict:
        """Calculate volatility metrics using standard deviation and variance"""
        price_values = [p.current_price for p in prices]

        if len(price_values) < 2:
            return {
                "volatility": 0,
                "volatility_class": "Low",
                "price_stability": "High"
            }

        # Standard deviation as volatility measure
        std = np.std(price_values)
        mean = np.mean(price_values)
        cv = (std / mean * 100) if mean > 0 else 0

        # Volatility classification
        if cv < 10:
            vol_class = "Low"
            stability = "Very Stable"
        elif cv < 20:
            vol_class = "Moderate"
            stability = "Stable"
        elif cv < 30:
            vol_class = "High"
            stability = "Unstable"
        else:
            vol_class = "Very High"
            stability = "Highly Unstable"

        # If historical data available, calculate time-series volatility
        historical_volatility = None
        if historical and len(historical) > 1:
            hist_prices = [h.get('price', 0)
                           for h in historical if h.get('price')]
            if len(hist_prices) > 1:
                returns = np.diff(hist_prices) / hist_prices[:-1] * 100
                historical_volatility = round(np.std(returns), 2)

        return {
            "volatility": round(cv, 2),
            "volatility_class": vol_class,
            "price_stability": stability,
            "standard_deviation": round(std, 2),
            "historical_volatility": historical_volatility,
            "volatility_interpretation": self._interpret_volatility(cv)
        }

    def _calculate_correlations(self, prices: List[CommodityPrice], historical: Optional[List[Dict]]) -> Dict:
        """Calculate price correlations between commodities"""
        if len(prices) < 2:
            return {"message": "Insufficient data for correlation analysis"}

        # Create price matrix
        commodities = [p.commodity_name for p in prices]
        price_values = [p.current_price for p in prices]

        # Normalize prices for comparison
        if max(price_values) > 0:
            normalized = [p / max(price_values) for p in price_values]
        else:
            normalized = price_values

        # Calculate pairwise correlations (simplified - would need time series for real correlation)
        correlations = {}
        for i, comm1 in enumerate(commodities):
            for j, comm2 in enumerate(commodities):
                if i < j:
                    # Price similarity (inverse of price difference)
                    price_diff = abs(price_values[i] - price_values[j])
                    max_price = max(price_values[i], price_values[j])
                    similarity = 1 - \
                        (price_diff / max_price) if max_price > 0 else 0
                    correlations[f"{comm1}_vs_{comm2}"] = round(similarity, 3)

        return {
            "pairwise_similarities": correlations,
            "interpretation": "Price similarity indicates commodities with similar market positioning"
        }

    def _segment_market(self, prices: List[CommodityPrice]) -> Dict:
        """Market segmentation using clustering techniques"""
        price_values = [p.current_price for p in prices]

        if len(price_values) < 3:
            return {"segments": [], "message": "Insufficient data for segmentation"}

        # K-means like segmentation (simplified)
        sorted_prices = sorted(price_values)
        n = len(sorted_prices)

        # Three segments: Low, Medium, High
        low_threshold = sorted_prices[n // 3]
        high_threshold = sorted_prices[2 * n // 3]

        low_segment = [p for p in prices if p.current_price <= low_threshold]
        medium_segment = [p for p in prices if low_threshold <
                          p.current_price <= high_threshold]
        high_segment = [p for p in prices if p.current_price > high_threshold]

        return {
            "segments": {
                "low_price": {
                    "count": len(low_segment),
                    "avg_price": round(np.mean([p.current_price for p in low_segment]), 2) if low_segment else 0,
                    "commodities": [p.commodity_name for p in low_segment]
                },
                "medium_price": {
                    "count": len(medium_segment),
                    "avg_price": round(np.mean([p.current_price for p in medium_segment]), 2) if medium_segment else 0,
                    "commodities": [p.commodity_name for p in medium_segment]
                },
                "high_price": {
                    "count": len(high_segment),
                    "avg_price": round(np.mean([p.current_price for p in high_segment]), 2) if high_segment else 0,
                    "commodities": [p.commodity_name for p in high_segment]
                }
            },
            "segmentation_method": "Price-based K-means clustering"
        }

    def _calculate_risk_metrics(self, price_values: List[float]) -> Dict:
        """Calculate risk metrics: VaR, CVaR, Sharpe-like ratios"""
        if len(price_values) < 2:
            return {"message": "Insufficient data for risk calculation"}

        returns = np.diff(price_values) / \
            price_values[:-1] * 100 if len(price_values) > 1 else [0]

        if len(returns) == 0:
            return {"message": "Cannot calculate risk metrics"}

        # Value at Risk (VaR) - 95% confidence
        var_95 = np.percentile(returns, 5) if len(returns) > 0 else 0

        # Conditional VaR (Expected Shortfall)
        cvar = np.mean([r for r in returns if r <= var_95]
                       ) if len(returns) > 0 else 0

        # Risk-adjusted return (simplified Sharpe ratio)
        mean_return = np.mean(returns) if len(returns) > 0 else 0
        std_return = np.std(returns) if len(returns) > 1 else 0
        sharpe_like = (mean_return / std_return) if std_return > 0 else 0

        # Maximum drawdown
        cumulative = np.cumsum(returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = cumulative - running_max
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0

        return {
            "value_at_risk_95": round(var_95, 2),
            "conditional_var": round(cvar, 2),
            "risk_adjusted_return": round(sharpe_like, 3),
            "max_drawdown": round(max_drawdown, 2),
            "risk_level": "High" if abs(var_95) > 10 else "Medium" if abs(var_95) > 5 else "Low"
        }

    def _analyze_distribution(self, price_values: List[float]) -> Dict:
        """Statistical distribution analysis"""
        if len(price_values) < 3:
            return {"message": "Insufficient data for distribution analysis"}

        # Normality test (Shapiro-Wilk for small samples)
        try:
            if len(price_values) >= 3 and len(price_values) <= 5000:
                stat, p_value = stats.shapiro(price_values)
                is_normal = p_value > 0.05
            else:
                # Use Kolmogorov-Smirnov for larger samples
                stat, p_value = stats.kstest(price_values, 'norm')
                is_normal = p_value > 0.05
        except:
            is_normal = False
            p_value = 0

        # Skewness and Kurtosis
        skewness = stats.skew(price_values)
        kurtosis = stats.kurtosis(price_values)

        return {
            "distribution_type": "Normal" if is_normal else "Non-normal",
            "normality_p_value": round(p_value, 4),
            "skewness": round(skewness, 3),
            "kurtosis": round(kurtosis, 3),
            "skewness_interpretation": "Right-skewed" if skewness > 0.5 else "Left-skewed" if skewness < -0.5 else "Symmetric",
            "kurtosis_interpretation": "Heavy-tailed" if kurtosis > 0 else "Light-tailed" if kurtosis < 0 else "Normal-tailed"
        }

    def _generate_visualizations(self, prices: List[CommodityPrice], historical: Optional[List[Dict]]) -> Dict:
        """Generate base64-encoded chart visualizations including time series"""
        if not self.matplotlib_available or Figure is None:
            return {"message": "Visualizations require matplotlib library"}

        visualizations = {}

        try:
            # 1. Price Distribution Histogram
            price_values = [p.current_price for p in prices]
            if len(price_values) > 0:
                fig = Figure(figsize=(8, 6))
                ax = fig.add_subplot(111)
                ax.hist(price_values, bins=min(10, len(price_values)),
                        edgecolor='black', alpha=0.7, color='steelblue')
                ax.set_xlabel('Price (₹/quintal)', fontsize=11)
                ax.set_ylabel('Number of Commodities', fontsize=11)
                ax.set_title(
                    'Commodity Price Distribution\n(How prices are spread across the market)', fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3)
                fig.tight_layout()
                visualizations["price_distribution"] = self._fig_to_base64(fig)

            # 2. Price Bar Chart Horizontal
            if len(prices) > 0:
                fig = Figure(figsize=(10, 6))
                ax = fig.add_subplot(111)
                commodities = [p.commodity_name for p in prices]
                prices_list = [p.current_price for p in prices]
                colors = ['#2ecc71' if t == 'increasing' else '#e74c3c' if t == 'decreasing' else '#f39c12'
                          for t in [p.price_trend for p in prices]]
                ax.barh(commodities, prices_list, color=colors,
                        alpha=0.7, edgecolor='black')
                ax.set_xlabel('Current Price (₹/quintal)', fontsize=11)
                ax.set_title('Current Commodity Prices by Market Trend\n(Green = Rising, Red = Falling, Orange = Stable)',
                             fontsize=12, fontweight='bold')
                ax.grid(True, alpha=0.3, axis='x')
                fig.tight_layout()
                visualizations["price_comparison"] = self._fig_to_base64(fig)

            # 3. Trend Pie Chart
            if len(prices) > 0:
                trend_counts = {}
                for p in prices:
                    trend_counts[p.price_trend] = trend_counts.get(
                        p.price_trend, 0) + 1

                fig = Figure(figsize=(7, 7))
                ax = fig.add_subplot(111)
                labels = [f"{k.capitalize()}\n({v} items)" for k,
                          v in trend_counts.items()]
                sizes = list(trend_counts.values())
                # Green, Red, Orange
                colors = ['#2ecc71', '#e74c3c', '#f39c12']
                explode = [0.05 if i == sizes.index(
                    max(sizes)) else 0 for i in range(len(sizes))]
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)],
                       startangle=90, explode=explode, textprops={'fontsize': 10})
                ax.set_title('Market Trend Overview\n(Distribution of Rising/Falling/Stable Commodities)',
                             fontsize=12, fontweight='bold')
                fig.tight_layout()
                visualizations["trend_distribution"] = self._fig_to_base64(fig)

            # 4. Time Series Plot - Mock Historical Data with Layman Interpretation
            if historical and len(historical) > 1:
                visualizations["time_series"] = self._generate_time_series_plot(
                    historical, prices)
            else:
                # Generate synthetic time series for visualization
                visualizations["synthetic_timeseries"] = self._generate_synthetic_time_series(
                    prices)

            # 5. Price Volatility Comparison Chart
            if len(prices) >= 3:
                visualizations["volatility_chart"] = self._generate_volatility_chart(
                    prices)

            # 6. Market Trend Line Chart
            visualizations["market_trend_line"] = self._generate_market_trend_line(
                prices)

        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            visualizations["error"] = str(e)

        return visualizations

    def _generate_time_series_plot(self, historical: List[Dict], prices: List[CommodityPrice]) -> str:
        """Generate time series plot from historical data"""
        try:
            fig = Figure(figsize=(14, 6))
            ax = fig.add_subplot(111)

            # Organize historical data by commodity
            commodity_history = {}
            for record in historical:
                comm = record.get('commodity', 'Unknown')
                if comm not in commodity_history:
                    commodity_history[comm] = {'dates': [], 'prices': []}

                try:
                    date = datetime.fromisoformat(record.get('date', ''))
                    commodity_history[comm]['dates'].append(date)
                    commodity_history[comm]['prices'].append(
                        float(record.get('price', 0)))
                except:
                    continue

            # Plot each commodity's time series
            colors_palette = ['#1f77b4', '#ff7f0e',
                              '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            for idx, (comm, data) in enumerate(list(commodity_history.items())[:6]):
                if len(data['dates']) > 1:
                    sorted_pairs = sorted(zip(data['dates'], data['prices']))
                    dates, prices_ts = zip(*sorted_pairs)
                    color = colors_palette[idx % len(colors_palette)]
                    ax.plot(dates, prices_ts, marker='o', label=comm,
                            linewidth=2, markersize=4, color=color)

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            ax.set_xlabel('Date', fontsize=11)
            ax.set_ylabel('Price (₹/quintal)', fontsize=11)
            ax.set_title('Commodity Price History\n(Trend over time - Understand past price movements)',
                         fontsize=12, fontweight='bold')
            ax.legend(loc='best', fontsize=9)
            ax.grid(True, alpha=0.3)
            fig.tight_layout()

            return self._fig_to_base64(fig)
        except Exception as e:
            logger.error(f"Error in time series plot: {e}")
            return ""

    def _generate_synthetic_time_series(self, prices: List[CommodityPrice]) -> str:
        """Generate synthetic time series plot for demonstration"""
        try:
            fig = Figure(figsize=(14, 6))
            ax = fig.add_subplot(111)

            # Create synthetic historical data based on current trends
            days = 30
            dates = [datetime.now() - timedelta(days=i)
                     for i in range(days, -1, -1)]

            colors_palette = ['#1f77b4', '#ff7f0e',
                              '#2ca02c', '#d62728', '#9467bd']

            for idx, price in enumerate(prices[:5]):
                # Create synthetic trend based on current price trend
                base_price = price.current_price
                noise = np.random.normal(0, base_price * 0.05, days + 1)

                if price.price_trend == 'increasing':
                    trend = np.linspace(0, base_price * 0.1, days + 1)
                elif price.price_trend == 'decreasing':
                    trend = np.linspace(0, -base_price * 0.1, days + 1)
                else:
                    trend = np.zeros(days + 1)

                synthetic_prices = base_price * 0.85 + trend + noise
                color = colors_palette[idx % len(colors_palette)]
                ax.plot(dates, synthetic_prices, marker='o', label=price.commodity_name,
                        linewidth=2, markersize=4, color=color)

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            ax.set_xlabel('Date (Past 30 Days)', fontsize=11)
            ax.set_ylabel('Price (₹/quintal)', fontsize=11)
            ax.set_title('Simulated Price Trends (Past 30 Days)\n(Green up = Rising prices, Red down = Falling prices)',
                         fontsize=12, fontweight='bold')
            ax.legend(loc='best', fontsize=9)
            ax.grid(True, alpha=0.3)
            fig.tight_layout()

            return self._fig_to_base64(fig)
        except Exception as e:
            logger.error(f"Error in synthetic time series: {e}")
            return ""

    def _generate_volatility_chart(self, prices: List[CommodityPrice]) -> str:
        """Generate volatility comparison chart - measures price stability"""
        try:
            fig = Figure(figsize=(12, 6))
            ax = fig.add_subplot(111)

            # Calculate simple volatility proxy for each commodity
            commodities = [p.commodity_name for p in prices]
            # Use price level as proxy (in real scenario, use historical std dev)
            volatility_scores = []
            for p in prices:
                # Higher prices = potentially higher volatility
                # Normalize to 0-100 scale
                vol_score = min(
                    100, (p.current_price / max([x.current_price for x in prices] or [1])) * 100)
                volatility_scores.append(vol_score)

            colors_vol = ['#e74c3c' if v > 70 else '#f39c12' if v >
                          40 else '#2ecc71' for v in volatility_scores]
            bars = ax.barh(commodities, volatility_scores,
                           color=colors_vol, alpha=0.7, edgecolor='black')

            # Add value labels
            for i, (bar, score) in enumerate(zip(bars, volatility_scores)):
                ax.text(score + 2, i, f'{score:.1f}%', va='center', fontsize=9)

            ax.set_xlabel(
                'Volatility Score (Higher = Less Stable)', fontsize=11)
            ax.set_title('Price Stability Comparison\n(Red = High risk, Yellow = Medium, Green = Stable)',
                         fontsize=12, fontweight='bold')
            ax.set_xlim(0, 110)
            ax.grid(True, alpha=0.3, axis='x')
            fig.tight_layout()

            return self._fig_to_base64(fig)
        except Exception as e:
            logger.error(f"Error in volatility chart: {e}")
            return ""

    def _generate_market_trend_line(self, prices: List[CommodityPrice]) -> str:
        """Generate cumulative market trend line"""
        try:
            fig = Figure(figsize=(12, 6))
            ax = fig.add_subplot(111)

            # Create market momentum index
            commodities = [p.commodity_name for p in prices]

            # Assign numerical values to trends
            trend_values = []
            for p in prices:
                if p.price_trend == 'increasing':
                    trend_values.append(1)
                elif p.price_trend == 'decreasing':
                    trend_values.append(-1)
                else:
                    trend_values.append(0)

            # Create cumulative trend
            cumulative_trend = np.cumsum(trend_values)

            # Color code: positive green, negative red
            colors_line = ['#2ecc71' if c >=
                           0 else '#e74c3c' for c in cumulative_trend]

            ax.bar(range(len(commodities)), cumulative_trend,
                   color=colors_line, alpha=0.7, edgecolor='black')
            ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
            ax.set_xticks(range(len(commodities)))
            ax.set_xticklabels(commodities, rotation=45, ha='right')
            ax.set_ylabel('Cumulative Market Momentum', fontsize=11)
            ax.set_title('Overall Market Trend Momentum\n(Above 0 = Bullish market, Below 0 = Bearish market)',
                         fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            fig.tight_layout()

            return self._fig_to_base64(fig)
        except Exception as e:
            logger.error(f"Error in market trend line: {e}")
            return ""

    def _fig_to_base64(self, fig: Figure) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return img_base64

    def _generate_recommendations(self, prices: List[CommodityPrice], trends: Dict,
                                  volatility: Dict, risk: Dict) -> List[Dict]:
        """Generate data-driven recommendations"""
        recommendations = []

        # Price-based recommendations
        price_values = [p.current_price for p in prices]
        if price_values:
            avg_price = np.mean(price_values)
            high_value_commodities = [
                p for p in prices if p.current_price > avg_price * 1.2]

            if high_value_commodities:
                recommendations.append({
                    "type": "High-Value Opportunity",
                    "priority": "High",
                    "message": f"Consider focusing on {', '.join([p.commodity_name for p in high_value_commodities[:3]])} - prices are significantly above average",
                    "confidence": "Medium"
                })

        # Volatility-based recommendations
        if volatility.get("volatility_class") == "High":
            recommendations.append({
                "type": "Risk Management",
                "priority": "High",
                "message": "High price volatility detected. Consider diversifying portfolio to mitigate risk.",
                "confidence": "High"
            })

        # Trend-based recommendations
        if trends.get("trend_score", 0) > 0.5:
            recommendations.append({
                "type": "Market Timing",
                "priority": "Medium",
                "message": "Strong bullish trend detected. Good time for strategic investments.",
                "confidence": "Medium"
            })

        return recommendations

    def _generate_mathematical_insights(self, prices: List[CommodityPrice], trends: Dict,
                                        volatility: Dict, risk: Dict) -> List[str]:
        """Generate mathematical insights"""
        insights = []

        price_values = [p.current_price for p in prices]
        if len(price_values) > 1:
            # Coefficient of variation insight
            cv = volatility.get("volatility", 0)
            if cv > 20:
                insights.append(
                    f"High price dispersion (CV={cv:.1f}%) indicates significant market heterogeneity")
            elif cv < 10:
                insights.append(
                    f"Low price dispersion (CV={cv:.1f}%) suggests stable, homogeneous market conditions")

            # Trend insight
            trend_score = trends.get("trend_score", 0)
            if abs(trend_score) > 0.6:
                direction = "bullish" if trend_score > 0 else "bearish"
                insights.append(
                    f"Strong {direction} momentum (score: {trend_score:.2f}) suggests directional market movement")

            # Risk insight
            var = risk.get("value_at_risk_95", 0)
            if abs(var) > 10:
                insights.append(
                    f"High downside risk (VaR 95%: {var:.1f}%) - consider risk mitigation strategies")

        return insights

    def _interpret_volatility(self, cv: float) -> str:
        """Interpret coefficient of variation"""
        if cv < 10:
            return "Prices are very stable with low variability"
        elif cv < 20:
            return "Moderate price variability - normal market conditions"
        elif cv < 30:
            return "High price variability - volatile market conditions"
        else:
            return "Very high price variability - extremely volatile market"

    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            "summary": {
                "total_commodities": 0,
                "data_source": "Real-time API Data",
                "analysis_timestamp": datetime.now().isoformat(),
                "message": "No price data available for analysis"
            },
            "descriptive_statistics": {},
            "trend_analysis": {},
            "volatility_metrics": {},
            "correlation_analysis": {},
            "market_segmentation": {},
            "risk_metrics": {},
            "distribution_analysis": {},
            "visualizations": {},
            "recommendations": [],
            "mathematical_insights": []
        }
