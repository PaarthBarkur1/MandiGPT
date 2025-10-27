import requests
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from models import CommodityPrice, Location
from config import Config

class CommodityService:
    def __init__(self):
        self.api_key = "2f32c13d3d0c45dab283c0e19f333a7c"
        self.base_url = "https://api.apifreaks.com/v1.0/commodity/rates/latest"
        self.commodity_mapping = {
            "Gold": "XAU",
            "Crude Oil": "WTIOIL",
            "Silver": "XAG",
            "Natural Gas": "NGAS",
            "Copper": "COPPER",
            "Cotton": "COTTON"
        }
        self.default_markets = {
            "Gold": ["Mumbai", "Delhi"],
            "Crude Oil": ["Mumbai"],
            "Silver": ["Mumbai", "Delhi"],
            "Natural Gas": ["Mumbai"],
            "Copper": ["Mumbai"],
            "Cotton": ["Gujarat", "Maharashtra"]
        }
    
    async def get_commodity_prices(self, location: Location, commodities: Optional[List[str]] = None) -> List[CommodityPrice]:
        """Get current commodity prices for specified commodities"""
        if commodities is None:
            commodities = list(self.commodity_mapping.keys())
        
        # Filter commodities to only include those we have mappings for
        valid_commodities = [c for c in commodities if c in self.commodity_mapping]
        if not valid_commodities:
            return []

        # Create the symbols parameter for the API
        symbols = [self.commodity_mapping[c] for c in valid_commodities]
        
        try:
            params = {
                'apikey': self.api_key,
                'updates': '1m',
                'symbols': ','.join(symbols)
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                return []
            
            prices = []
            for commodity in valid_commodities:
                symbol = self.commodity_mapping[commodity]
                if symbol in data['rates']:
                    # Find the closest market to the location
                    closest_market = self._find_closest_market(location, self.default_markets[commodity])
                    
                    # Determine price trend (this would need historical data for accuracy)
                    price_trend = "stable"  # Default trend
                    
                    prices.append(CommodityPrice(
                        commodity_name=commodity,
                        current_price=data['rates'][symbol],
                        price_trend=price_trend,
                        market_location=closest_market,
                        date=datetime.fromtimestamp(data['timestamp'])
                    ))
            
            return prices
            
        except (requests.RequestException, KeyError, ValueError) as e:
            print(f"Error fetching commodity prices: {str(e)}")
            return []
    
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
        if commodity not in self.commodity_mapping:
            return {"error": "Commodity not found"}
        
        try:
            # Get current price
            params = {
                'apikey': self.api_key,
                'updates': '1m',
                'symbols': self.commodity_mapping[commodity]
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                return {"error": "Failed to fetch price data"}
            
            symbol = self.commodity_mapping[commodity]
            current_price = data['rates'][symbol]
            
            # Since historical data is not available in the free tier,
            # we'll determine trend based on current price
            # In a production environment, you would want to use historical data API
            trend = "stable"  # Default to stable since we can't determine trend
            
            prices = [{
                "date": datetime.fromtimestamp(data['timestamp']).strftime("%Y-%m-%d"),
                "price": current_price
            }]
            
            return {
                "commodity": commodity,
                "trend": trend,
                "price_history": prices,
                "current_price": current_price,
                "price_change": 0,  # Since we only have current price
                "unit": data['metaData'][symbol]['unit'],
                "quote_currency": data['metaData'][symbol]['quote']
            }
            
        except (requests.RequestException, KeyError, ValueError) as e:
            return {"error": f"Failed to fetch price trends: {str(e)}"}
    
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