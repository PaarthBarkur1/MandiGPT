import requests
import json
from typing import Dict, List, Optional
from config import Config

class LocalLLMService:
    """Service for interacting with local LLM via Ollama"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model_name = "llama3.2"  # You can change this to any model you have installed
        
    def is_ollama_available(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except:
            return []
    
    async def generate_crop_recommendations(
        self, 
        farmer_query: Dict, 
        weather_data: Dict, 
        commodity_prices: List[Dict]
    ) -> str:
        """Generate crop recommendations using local LLM"""
        
        if not self.is_ollama_available():
            return self._fallback_recommendation(farmer_query, weather_data, commodity_prices)
        
        prompt = self._create_agricultural_prompt(farmer_query, weather_data, commodity_prices)
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Unable to generate recommendations")
            else:
                return self._fallback_recommendation(farmer_query, weather_data, commodity_prices)
                
        except Exception as e:
            print(f"LLM service error: {e}")
            return self._fallback_recommendation(farmer_query, weather_data, commodity_prices)
    
    def _create_agricultural_prompt(self, farmer_query: Dict, weather_data: Dict, commodity_prices: List[Dict]) -> str:
        """Create a detailed prompt for agricultural recommendations"""
        
        prompt = f"""
You are an expert agricultural advisor for Indian farmers. Based on the following information, provide detailed crop recommendations and farming advice.

FARMER INFORMATION:
- Location: {farmer_query.get('location', {}).get('state', 'Unknown')}, {farmer_query.get('location', {}).get('district', 'Unknown')}
- Land Size: {farmer_query.get('land_size', 'Not specified')} hectares
- Budget: ₹{farmer_query.get('budget', 'Not specified')}
- Risk Tolerance: {farmer_query.get('risk_tolerance', 'Medium')}
- Preferred Crops: {', '.join(farmer_query.get('preferred_crops', []))}
- Soil Type: {farmer_query.get('location', {}).get('soil_type', 'Not specified')}

WEATHER CONDITIONS:
- Current Temperature: {weather_data.get('current_temp', 'N/A')}°C
- Humidity: {weather_data.get('humidity', 'N/A')}%
- Rainfall (7 days): {weather_data.get('total_rainfall_7days', 'N/A')}mm
- Weather Suitability: {weather_data.get('weather_suitability', 'N/A')}

COMMODITY PRICES:
"""
        
        for price in commodity_prices:
            prompt += f"- {price.get('commodity_name', 'Unknown')}: ₹{price.get('current_price', 0)}/quintal (Trend: {price.get('price_trend', 'stable')})\n"
        
        prompt += """
Please provide:
1. Top 3 crop recommendations with reasons
2. Expected yield and profit estimates
3. Planting schedule and timing
4. Required inputs (seeds, fertilizers, irrigation)
5. Risk factors and mitigation strategies
6. Market outlook and selling advice

Format your response in a clear, actionable manner suitable for farmers.
"""
        
        return prompt
    
    def _fallback_recommendation(self, farmer_query: Dict, weather_data: Dict, commodity_prices: List[Dict]) -> str:
        """Fallback recommendation when LLM is not available"""
        
        location = farmer_query.get('location', {})
        state = location.get('state', 'Unknown')
        
        recommendations = f"""
AGRICULTURAL RECOMMENDATIONS FOR {state.upper()}

Based on your location and current conditions, here are my recommendations:

WEATHER-BASED ADVICE:
- Current weather conditions appear {weather_data.get('weather_suitability', 'moderate')}
- Rainfall: {weather_data.get('total_rainfall_7days', 0)}mm in the last 7 days
- Temperature: {weather_data.get('current_temp', 'N/A')}°C

TOP CROP RECOMMENDATIONS:
"""
        
        # Simple rule-based recommendations
        if weather_data.get('weather_suitability') == 'Excellent':
            recommendations += """
1. RICE - High yield potential with current weather
2. WHEAT - Good market price and stable demand
3. MAIZE - Increasing prices, good profit margin
"""
        else:
            recommendations += """
1. WHEAT - Drought resistant, stable market
2. SUGARCANE - High value crop, good for your region
3. COTTON - Good market demand, suitable for your area
"""
        
        recommendations += f"""
MARKET ANALYSIS:
- Monitor commodity prices regularly
- Best time to sell: Post-harvest season
- Consider contract farming for better prices

BUDGET CONSIDERATIONS:
- Estimated cost: ₹{farmer_query.get('budget', 50000)} for {farmer_query.get('land_size', 1)} hectare
- Focus on high-value crops within your budget
- Consider government schemes for financial support

RISK MANAGEMENT:
- Diversify crops to reduce risk
- Monitor weather forecasts regularly
- Maintain proper irrigation facilities
- Follow integrated pest management practices

Note: This is a basic recommendation. For detailed analysis, please ensure the AI system is properly configured.
"""
        
        return recommendations
    
    async def generate_agricultural_advice(self, context: Dict) -> str:
        """Generate specific agricultural advice based on context"""
        
        if not self.is_ollama_available():
            return "Please ensure Ollama is running for AI-powered agricultural advice."
        
        prompt = f"""
You are an agricultural expert. Provide specific farming advice for:

Context: {context.get('situation', 'General farming advice')}
Location: {context.get('location', 'India')}
Season: {context.get('season', 'Current')}

Provide practical, actionable advice for Indian farmers.
"""
        
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Unable to generate advice")
            else:
                return "Unable to generate advice at this time."
                
        except Exception as e:
            print(f"LLM advice error: {e}")
            return "Unable to generate advice at this time."
