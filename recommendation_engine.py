import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from models import (
    FarmerQuery, CropRecommendation, AgriculturalAdvice, 
    CropSuggestionResponse, Location, Season
)
from agricultural_database import IndianAgriculturalDatabase
from weather_service import WeatherService
from commodity_service import CommodityService
from llm_service import LocalLLMService
from free_commodity_service import FreeCommodityService

class CropRecommendationEngine:
    """AI-powered crop recommendation engine for Indian farmers"""
    
    def __init__(self):
        self.agri_db = IndianAgriculturalDatabase()
        self.weather_service = WeatherService()
        self.commodity_service = CommodityService()
        self.free_commodity_service = FreeCommodityService()
        self.llm_service = LocalLLMService()
    
    async def generate_recommendations(self, query: FarmerQuery) -> CropSuggestionResponse:
        """Generate comprehensive crop recommendations and agricultural advice"""
        
        # Get weather summary
        weather_summary = self.weather_service.get_weather_summary(query.weather)
        
        # Get commodity prices using free service
        commodity_prices = await self.free_commodity_service.get_commodity_prices(
            query.location, query.preferred_crops
        )
        
        # Generate AI-powered recommendations using local LLM
        ai_recommendations = await self._generate_ai_recommendations(
            query, weather_summary, commodity_prices
        )
        
        # Generate traditional crop recommendations as backup
        traditional_recommendations = await self._generate_crop_recommendations(
            query, weather_summary, commodity_prices
        )
        
        # Generate agricultural advice
        advice = await self._generate_agricultural_advice(
            query, weather_summary, traditional_recommendations
        )
        
        # Perform market analysis using free service
        market_analysis = self.free_commodity_service.get_market_analysis(commodity_prices)
        
        # Perform risk assessment
        risk_assessment = self._assess_risks(query, weather_summary, commodity_prices)
        
        # Create location summary
        location_summary = self._create_location_summary(query.location)
        
        return CropSuggestionResponse(
            recommendations=traditional_recommendations,
            advice=advice,
            market_analysis=market_analysis,
            risk_assessment=risk_assessment,
            generated_at=datetime.now(),
            location_summary=location_summary,
            ai_recommendations=ai_recommendations  # Add AI recommendations
        )
    
    async def _generate_crop_recommendations(
        self, 
        query: FarmerQuery, 
        weather_summary: Dict, 
        commodity_prices: List
    ) -> List[CropRecommendation]:
        """Generate crop recommendations with confidence scores"""
        
        recommendations = []
        current_season = self._determine_current_season()
        
        # Get all available crops
        all_crops = list(self.agri_db.crop_data.keys())
        if query.preferred_crops:
            all_crops = [crop for crop in all_crops if crop in query.preferred_crops]
        
        for crop in all_crops:
            # Calculate suitability score
            suitability_score = self.agri_db.get_crop_suitability(
                crop, query.location.state, weather_summary
            )
            
            # Get crop information
            crop_info = self.agri_db.get_crop_info(crop)
            
            # Calculate market score
            market_score = self._calculate_market_score(crop, commodity_prices)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                suitability_score, market_score, crop_info, query
            )
            
            # Only recommend crops with confidence > 0.3
            if confidence_score > 0.3:
                # Get current market price
                market_price = self._get_market_price(crop, commodity_prices)
                
                # Calculate expected yield and profit
                expected_yield = crop_info["yield_per_hectare"]
                if query.land_size:
                    expected_yield *= query.land_size
                
                estimated_profit = (market_price * expected_yield * crop_info["profit_margin"])
                
                # Determine planting and harvesting times
                planting_time, harvesting_time = self._get_planting_schedule(
                    crop, current_season
                )
                
                # Generate reasons for recommendation
                reasons = self._generate_recommendation_reasons(
                    crop, suitability_score, market_score, weather_summary
                )
                
                recommendation = CropRecommendation(
                    crop_name=crop,
                    confidence_score=confidence_score,
                    expected_yield=expected_yield,
                    market_price=market_price,
                    estimated_profit=estimated_profit,
                    planting_season=current_season,
                    planting_time=planting_time,
                    harvesting_time=harvesting_time,
                    water_requirement=crop_info["water_requirement"],
                    fertilizer_requirement=crop_info["fertilizer_requirement"],
                    pest_risk=crop_info["pest_risk"],
                    market_demand=crop_info["market_demand"],
                    reasons=reasons
                )
                
                recommendations.append(recommendation)
        
        # Sort by confidence score and return top 5
        recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
        return recommendations[:5]
    
    async def _generate_ai_recommendations(
        self, 
        query: FarmerQuery, 
        weather_summary: Dict, 
        commodity_prices: List
    ) -> str:
        """Generate AI-powered recommendations using local LLM"""
        
        # Prepare data for LLM
        farmer_data = {
            "location": {
                "state": query.location.state,
                "district": query.location.district,
                "soil_type": query.location.soil_type
            },
            "land_size": query.land_size,
            "budget": query.budget,
            "risk_tolerance": query.risk_tolerance,
            "preferred_crops": query.preferred_crops
        }
        
        # Convert commodity prices to dict format
        price_data = []
        for price in commodity_prices:
            price_data.append({
                "commodity_name": price.commodity_name,
                "current_price": price.current_price,
                "price_trend": price.price_trend,
                "market_location": price.market_location
            })
        
        # Generate AI recommendations
        ai_recommendations = await self.llm_service.generate_crop_recommendations(
            farmer_data, weather_summary, price_data
        )
        
        return ai_recommendations
    
    async def _generate_agricultural_advice(
        self, 
        query: FarmerQuery, 
        weather_summary: Dict, 
        recommendations: List[CropRecommendation]
    ) -> List[AgriculturalAdvice]:
        """Generate agricultural advice based on current conditions"""
        
        advice = []
        
        # Weather-based advice
        if weather_summary["weather_suitability"] == "Poor":
            advice.append(AgriculturalAdvice(
                advice_type="Weather",
                title="Adverse Weather Conditions",
                description="Current weather conditions are not optimal for most crops. Consider greenhouse farming or delay planting until conditions improve.",
                confidence_score=0.9,
                urgency="High",
                implementation_time="Immediate",
                cost_estimate=5000
            ))
        
        # Irrigation advice
        rainfall = weather_summary.get("total_rainfall_7days", 0)
        if isinstance(rainfall, str):
            # Extract numeric value from string if needed
            rainfall = float(rainfall.replace("mm", "").strip())
        if rainfall < 50:
            advice.append(AgriculturalAdvice(
                advice_type="Irrigation",
                title="Irrigation Required",
                description="Low rainfall detected. Ensure adequate irrigation for your crops. Consider drip irrigation for water efficiency.",
                confidence_score=0.8,
                urgency="Medium",
                implementation_time="1-2 days",
                cost_estimate=2000
            ))
        
        # Pest control advice
        if any(rec.pest_risk == "High" for rec in recommendations):
            advice.append(AgriculturalAdvice(
                advice_type="Pest Control",
                title="High Pest Risk Detected",
                description="Some recommended crops have high pest risk. Implement integrated pest management and regular monitoring.",
                confidence_score=0.7,
                urgency="Medium",
                implementation_time="1 week",
                cost_estimate=3000
            ))
        
        # Market advice
        if recommendations:
            best_crop = max(recommendations, key=lambda x: x.confidence_score)
            advice.append(AgriculturalAdvice(
                advice_type="Market",
                title=f"Best Crop: {best_crop.crop_name}",
                description=f"Based on current market conditions and weather, {best_crop.crop_name} shows the highest potential with {best_crop.confidence_score:.1%} confidence.",
                confidence_score=best_crop.confidence_score,
                urgency="Low",
                implementation_time="1-2 weeks",
                cost_estimate=best_crop.estimated_profit * 0.3
            ))
        
        return advice
    
    def _calculate_confidence_score(
        self, 
        suitability_score: float, 
        market_score: float, 
        crop_info: Dict, 
        query: FarmerQuery
    ) -> float:
        """Calculate overall confidence score for a crop recommendation"""
        
        # Base confidence from suitability and market
        base_confidence = (suitability_score * 0.6) + (market_score * 0.4)
        
        # Adjust for risk tolerance
        if query.risk_tolerance == "Low":
            # Prefer stable, low-risk crops
            if crop_info["pest_risk"] == "Low" and crop_info["market_demand"] == "High":
                base_confidence += 0.1
        elif query.risk_tolerance == "High":
            # Prefer high-profit crops
            if crop_info["profit_margin"] > 0.3:
                base_confidence += 0.1
        
        # Adjust for budget constraints
        if query.budget:
            estimated_cost = crop_info["yield_per_hectare"] * 1000  # Rough cost estimate
            if estimated_cost > query.budget:
                base_confidence *= 0.5
        
        return min(base_confidence, 1.0)
    
    def _calculate_market_score(self, crop: str, commodity_prices: List) -> float:
        """Calculate market score based on commodity prices"""
        for price in commodity_prices:
            if price.commodity_name == crop:
                if price.price_trend == "increasing":
                    return 0.9
                elif price.price_trend == "stable":
                    return 0.7
                else:  # decreasing
                    return 0.4
        
        # Default score if no price data
        return 0.5
    
    def _get_market_price(self, crop: str, commodity_prices: List) -> float:
        """Get current market price for a crop"""
        for price in commodity_prices:
            if price.commodity_name == crop:
                return price.current_price
        
        # Default price if not found
        return 2000
    
    def _determine_current_season(self) -> Season:
        """Determine current agricultural season"""
        current_month = datetime.now().month
        
        if current_month in [6, 7, 8, 9, 10]:
            return Season.KHARIF
        elif current_month in [10, 11, 12, 1, 2, 3]:
            return Season.RABI
        else:
            return Season.ZAID
    
    def _get_planting_schedule(self, crop: str, season: Season) -> Tuple[str, str]:
        """Get planting and harvesting schedule for a crop"""
        crop_info = self.agri_db.get_crop_info(crop)
        
        if season == Season.KHARIF:
            return "June-July", "October-November"
        elif season == Season.RABI:
            return "October-November", "March-April"
        else:  # Zaid
            return "March-April", "May-June"
    
    def _generate_recommendation_reasons(
        self, 
        crop: str, 
        suitability_score: float, 
        market_score: float, 
        weather_summary: Dict
    ) -> List[str]:
        """Generate reasons for crop recommendation"""
        reasons = []
        
        if suitability_score > 0.8:
            reasons.append("Excellent suitability for current weather conditions")
        elif suitability_score > 0.6:
            reasons.append("Good suitability for current weather conditions")
        
        if market_score > 0.8:
            reasons.append("Strong market demand and favorable price trends")
        elif market_score > 0.6:
            reasons.append("Stable market conditions")
        
        crop_info = self.agri_db.get_crop_info(crop)
        if crop_info["market_demand"] == "High":
            reasons.append("High market demand ensures good selling opportunities")
        
        if crop_info["profit_margin"] > 0.3:
            reasons.append("High profit potential")
        
        if weather_summary["weather_suitability"] == "Excellent":
            reasons.append("Optimal weather conditions for this crop")
        
        return reasons
    
    def _assess_risks(
        self, 
        query: FarmerQuery, 
        weather_summary: Dict, 
        commodity_prices: List
    ) -> Dict:
        """Assess various risks for agricultural planning"""
        
        risks = {
            "weather_risk": "Low",
            "market_risk": "Low",
            "pest_risk": "Low",
            "financial_risk": "Low",
            "overall_risk": "Low"
        }
        
        # Weather risk assessment
        if weather_summary["weather_suitability"] in ["Poor", "Fair"]:
            risks["weather_risk"] = "High"
        elif weather_summary["weather_suitability"] == "Good":
            risks["weather_risk"] = "Medium"
        
        # Market risk assessment
        market_analysis = self.commodity_service.get_market_analysis(commodity_prices)
        if market_analysis.get("market_sentiment") == "Bearish":
            risks["market_risk"] = "High"
        elif market_analysis.get("market_sentiment") == "Neutral":
            risks["market_risk"] = "Medium"
        
        # Financial risk assessment
        if query.budget and query.land_size:
            estimated_cost = query.land_size * 50000  # Rough estimate
            if estimated_cost > query.budget * 1.5:
                risks["financial_risk"] = "High"
            elif estimated_cost > query.budget:
                risks["financial_risk"] = "Medium"
        
        # Overall risk assessment
        high_risks = sum(1 for risk in risks.values() if risk == "High")
        if high_risks >= 2:
            risks["overall_risk"] = "High"
        elif high_risks >= 1:
            risks["overall_risk"] = "Medium"
        
        return risks
    
    def _create_location_summary(self, location: Location) -> Dict:
        """Create summary of location-specific information"""
        regional_info = self.agri_db.get_regional_info(location.state)
        
        return {
            "state": location.state,
            "district": location.district,
            "soil_type": location.soil_type or regional_info.get("soil_type", "Unknown"),
            "climate": regional_info.get("climate", "Unknown"),
            "irrigation_coverage": regional_info.get("irrigation_coverage", 0),
            "average_rainfall": regional_info.get("average_rainfall", 0),
            "major_crops": regional_info.get("major_crops", [])
        }