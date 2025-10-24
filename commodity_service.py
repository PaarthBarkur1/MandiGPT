import requests
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from models import CommodityPrice, Location
from config import Config

class CommodityService:
    def __init__(self):
        self.api_key = Config.COMMODITY_API_KEY
        # Using a mock service for commodity prices since real APIs require subscription
        self.mock_prices = self._initialize_mock_prices()
        
    def _initialize_mock_prices(self) -> Dict[str, Dict]:
        """Initialize mock commodity prices for Indian markets"""
        return {
            "Rice": {
                "current_price": 2500,
                "trend": "increasing",
                "markets": ["Delhi", "Mumbai", "Kolkata", "Chennai"]
            },
            "Wheat": {
                "current_price": 2200,
                "trend": "stable",
                "markets": ["Delhi", "Punjab", "Haryana", "UP"]
            },
            "Maize": {
                "current_price": 1800,
                "trend": "increasing",
                "markets": ["Karnataka", "Andhra Pradesh", "Maharashtra"]
            },
            "Sugarcane": {
                "current_price": 3200,
                "trend": "stable",
                "markets": ["UP", "Maharashtra", "Karnataka", "Tamil Nadu"]
            },
            "Cotton": {
                "current_price": 6500,
                "trend": "decreasing",
                "markets": ["Gujarat", "Maharashtra", "Punjab", "Haryana"]
            },
            "Soybean": {
                "current_price": 4200,
                "trend": "increasing",
                "markets": ["Madhya Pradesh", "Maharashtra", "Rajasthan"]
            },
            "Groundnut": {
                "current_price": 5500,
                "trend": "stable",
                "markets": ["Gujarat", "Rajasthan", "Tamil Nadu"]
            },
            "Potato": {
                "current_price": 1200,
                "trend": "increasing",
                "markets": ["UP", "West Bengal", "Punjab", "Bihar"]
            },
            "Onion": {
                "current_price": 1800,
                "trend": "decreasing",
                "markets": ["Maharashtra", "Karnataka", "Gujarat"]
            },
            "Tomato": {
                "current_price": 2500,
                "trend": "increasing",
                "markets": ["Karnataka", "Andhra Pradesh", "Maharashtra"]
            }
        }
    
    async def get_commodity_prices(self, location: Location, commodities: List[str] = None) -> List[CommodityPrice]:
        """Get current commodity prices for specified crops"""
        if commodities is None:
            commodities = list(self.mock_prices.keys())
        
        prices = []
        for commodity in commodities:
            if commodity in self.mock_prices:
                price_data = self.mock_prices[commodity]
                
                # Find the closest market to the location
                closest_market = self._find_closest_market(location, price_data["markets"])
                
                prices.append(CommodityPrice(
                    commodity_name=commodity,
                    current_price=price_data["current_price"],
                    price_trend=price_data["trend"],
                    market_location=closest_market,
                    date=datetime.now()
                ))
        
        return prices
    
    def _find_closest_market(self, location: Location, markets: List[str]) -> str:
        """Find the closest market to the given location"""
        # This is a simplified version - in reality, you'd use coordinates
        state_market_mapping = {
            "Delhi": "Delhi",
            "Haryana": "Delhi",
            "Punjab": "Punjab",
            "UP": "UP",
            "Uttar Pradesh": "UP",
            "Maharashtra": "Mumbai",
            "Gujarat": "Gujarat",
            "Karnataka": "Karnataka",
            "Tamil Nadu": "Chennai",
            "West Bengal": "Kolkata",
            "Bihar": "Bihar",
            "Rajasthan": "Rajasthan",
            "Madhya Pradesh": "Madhya Pradesh",
            "Andhra Pradesh": "Andhra Pradesh"
        }
        
        return state_market_mapping.get(location.state, markets[0])
    
    async def get_price_trends(self, commodity: str, days: int = 30) -> Dict:
        """Get price trends for a commodity over specified days"""
        if commodity not in self.mock_prices:
            return {"error": "Commodity not found"}
        
        # Generate mock trend data
        base_price = self.mock_prices[commodity]["current_price"]
        trend = self.mock_prices[commodity]["trend"]
        
        prices = []
        for i in range(days):
            if trend == "increasing":
                price = base_price + (i * 10)
            elif trend == "decreasing":
                price = base_price - (i * 5)
            else:  # stable
                price = base_price + (i * 2 if i % 2 == 0 else -i * 1)
            
            prices.append({
                "date": (datetime.now() - timedelta(days=days-i)).strftime("%Y-%m-%d"),
                "price": max(price, 500)  # Minimum price floor
            })
        
        return {
            "commodity": commodity,
            "trend": trend,
            "price_history": prices,
            "current_price": base_price,
            "price_change": prices[-1]["price"] - prices[0]["price"]
        }
    
    def get_market_analysis(self, prices: List[CommodityPrice]) -> Dict:
        """Analyze market conditions based on commodity prices"""
        if not prices:
            return {"error": "No price data available"}
        
        # Calculate market indicators
        total_commodities = len(prices)
        increasing_trends = sum(1 for p in prices if p.price_trend == "increasing")
        decreasing_trends = sum(1 for p in prices if p.price_trend == "decreasing")
        stable_trends = sum(1 for p in prices if p.price_trend == "stable")
        
        # Calculate average price
        avg_price = sum(p.current_price for p in prices) / len(prices)
        
        # Find best and worst performing commodities
        best_commodity = max(prices, key=lambda x: x.current_price)
        worst_commodity = min(prices, key=lambda x: x.current_price)
        
        return {
            "market_sentiment": self._calculate_market_sentiment(increasing_trends, decreasing_trends, stable_trends),
            "average_price": round(avg_price, 2),
            "trend_distribution": {
                "increasing": increasing_trends,
                "decreasing": decreasing_trends,
                "stable": stable_trends
            },
            "best_performing": {
                "commodity": best_commodity.commodity_name,
                "price": best_commodity.current_price,
                "trend": best_commodity.price_trend
            },
            "worst_performing": {
                "commodity": worst_commodity.commodity_name,
                "price": worst_commodity.current_price,
                "trend": worst_commodity.price_trend
            },
            "market_recommendation": self._get_market_recommendation(increasing_trends, decreasing_trends, total_commodities)
        }
    
    def _calculate_market_sentiment(self, increasing: int, decreasing: int, stable: int) -> str:
        """Calculate overall market sentiment"""
        total = increasing + decreasing + stable
        if total == 0:
            return "Neutral"
        
        increasing_pct = (increasing / total) * 100
        decreasing_pct = (decreasing / total) * 100
        
        if increasing_pct > 60:
            return "Bullish"
        elif decreasing_pct > 60:
            return "Bearish"
        else:
            return "Neutral"
    
    def _get_market_recommendation(self, increasing: int, decreasing: int, total: int) -> str:
        """Get market recommendation based on trends"""
        if total == 0:
            return "No data available"
        
        if increasing > total * 0.6:
            return "Market is showing strong upward trends - good time for planting high-value crops"
        elif decreasing > total * 0.6:
            return "Market is declining - consider diversifying or focusing on staple crops"
        else:
            return "Market is stable - focus on crops with consistent demand"