from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from typing import List, Optional
from models import FarmerQuery, Location, WeatherForecast, CommodityPrice
from recommendation_engine import CropRecommendationEngine
from weather_service import WeatherService
from commodity_service import CommodityService
from free_commodity_service import FreeCommodityService
from llm_service import LocalLLMService
from config import Config

app = FastAPI(
    title="MandiGPT - AI Crop Recommendation Tool",
    description="AI-powered agricultural advisory tool for Indian farmers",
    version="1.0.0"
)

# Initialize services
recommendation_engine = CropRecommendationEngine()
weather_service = WeatherService()
commodity_service = CommodityService()
free_commodity_service = FreeCommodityService()
llm_service = LocalLLMService()

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with farmer input form"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "states": Config.INDIAN_STATES,
        "crops": Config.MAJOR_CROPS
    })

@app.post("/api/recommendations")
async def get_crop_recommendations(query: FarmerQuery):
    """Get AI-powered crop recommendations"""
    try:
        # Get weather data
        weather_forecast = await weather_service.get_weather_forecast(query.location)
        query.weather = weather_forecast
        
        # Get commodity prices
        commodity_prices = await commodity_service.get_commodity_prices(
            query.location, query.preferred_crops
        )
        query.commodity_prices = commodity_prices
        
        # Generate recommendations
        recommendations = await recommendation_engine.generate_recommendations(query)
        
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather/{state}/{district}")
async def get_weather_data(state: str, district: str, lat: float, lon: float):
    """Get weather data for a specific location"""
    try:
        location = Location(
            state=state,
            district=district,
            latitude=lat,
            longitude=lon
        )
        
        weather_forecast = await weather_service.get_weather_forecast(location)
        weather_summary = weather_service.get_weather_summary(weather_forecast)
        
        return {
            "weather_forecast": weather_forecast,
            "weather_summary": weather_summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/commodity-prices")
async def get_commodity_prices(state: str, district: str, lat: float, lon: float, crops: Optional[str] = None):
    """Get commodity prices for specified crops"""
    try:
        location = Location(
            state=state,
            district=district,
            latitude=lat,
            longitude=lon
        )
        
        crop_list = crops.split(",") if crops else None
        prices = await free_commodity_service.get_commodity_prices(location, crop_list)
        market_analysis = free_commodity_service.get_market_analysis(prices)
        
        return {
            "commodity_prices": prices,
            "market_analysis": market_analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/crop-info/{crop_name}")
async def get_crop_information(crop_name: str):
    """Get detailed information about a specific crop"""
    try:
        from agricultural_database import IndianAgriculturalDatabase
        agri_db = IndianAgriculturalDatabase()
        
        crop_info = agri_db.get_crop_info(crop_name)
        if not crop_info:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        return crop_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regional-info/{state}")
async def get_regional_information(state: str):
    """Get agricultural information for a specific state"""
    try:
        from agricultural_database import IndianAgriculturalDatabase
        agri_db = IndianAgriculturalDatabase()
        
        regional_info = agri_db.get_regional_info(state)
        if not regional_info:
            raise HTTPException(status_code=404, detail="State not found")
        
        return regional_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/price-trends/{commodity}")
async def get_price_trends(commodity: str, days: int = 30):
    """Get price trends for a specific commodity"""
    try:
        trends = await free_commodity_service.get_price_trends(commodity, days)
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/llm-status")
async def llm_status():
    """Check LLM service status"""
    try:
        is_available = llm_service.is_ollama_available()
        models = llm_service.get_available_models() if is_available else []
        
        return {
            "llm_available": is_available,
            "available_models": models,
            "current_model": llm_service.model_name,
            "service_url": llm_service.ollama_url
        }
    except Exception as e:
        return {"llm_available": False, "error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    llm_status_check = llm_service.is_ollama_available()
    return {
        "status": "healthy", 
        "service": "MandiGPT",
        "llm_available": llm_status_check,
        "features": {
            "local_llm": llm_status_check,
            "free_commodity_prices": True,
            "weather_forecast": True,
            "crop_recommendations": True
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT, reload=Config.DEBUG)
