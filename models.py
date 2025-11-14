from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Season(str, Enum):
    KHARIF = "Kharif"
    RABI = "Rabi"
    ZAID = "Zaid"

class SoilType(str, Enum):
    ALLUVIAL = "Alluvial"
    BLACK = "Black"
    RED = "Red"
    LATERITE = "Laterite"
    MOUNTAIN = "Mountain"
    DESERT = "Desert"

class Location(BaseModel):
    state: str
    district: str
    latitude: float
    longitude: float
    soil_type: Optional[SoilType] = None

class WeatherData(BaseModel):
    temperature: float  # in Celsius
    humidity: float    # percentage
    rainfall: float    # in mm
    wind_speed: float  # in km/h
    pressure: float    # in hPa
    uv_index: float
    cloud_cover: float # percentage
    date: datetime

class WeatherForecast(BaseModel):
    current: WeatherData
    forecast_7_days: List[WeatherData]

class CommodityPrice(BaseModel):
    commodity_name: str
    current_price: float  # per quintal
    price_trend: str     # "increasing", "decreasing", "stable"
    market_location: str
    date: datetime

class CropRecommendation(BaseModel):
    crop_name: str
    confidence_score: float  # 0.0 to 1.0
    expected_yield: float   # quintals per hectare
    market_price: float     # per quintal
    estimated_profit: float # per hectare
    planting_season: Season
    planting_time: str
    harvesting_time: str
    water_requirement: str  # "Low", "Medium", "High"
    fertilizer_requirement: str
    pest_risk: str         # "Low", "Medium", "High"
    market_demand: str     # "Low", "Medium", "High"
    reasons: List[str]     # Why this crop is recommended

class AgriculturalAdvice(BaseModel):
    advice_type: str       # "Planting", "Harvesting", "Pest Control", "Irrigation", "Fertilization"
    title: str
    description: str
    confidence_score: float
    urgency: str          # "Low", "Medium", "High"
    implementation_time: str
    cost_estimate: Optional[float]

class FarmerQuery(BaseModel):
    location: Location
    weather: Optional[WeatherForecast] = None
    commodity_prices: Optional[List[CommodityPrice]] = None
    budget: Optional[float] = None
    land_size: Optional[float] = None  # in hectares
    preferred_crops: Optional[List[str]] = None
    risk_tolerance: str = "Medium"  # "Low", "Medium", "High"

class CropSuggestionResponse(BaseModel):
    recommendations: List[CropRecommendation]
    advice: List[AgriculturalAdvice]
    market_analysis: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    generated_at: datetime
    location_summary: Dict[str, Any]
    ai_recommendations: Optional[str] = None  # AI-generated recommendations