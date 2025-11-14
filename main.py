from fastapi import FastAPI, HTTPException, Request, Query, Path, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import asyncio
import logging
from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field, validator
from models import FarmerQuery, Location, WeatherForecast, CommodityPrice, CropSuggestionResponse
from recommendation_engine import CropRecommendationEngine
from weather_service import WeatherService
from commodity_service import CommodityService
from free_commodity_service import FreeCommodityService
from llm_service import LocalLLMService
from config import Config


# Configure logging
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MandiGPT - AI Crop Recommendation Tool",
    description="AI-powered agricultural advisory tool for Indian farmers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (using dependency injection pattern)


def get_recommendation_engine() -> CropRecommendationEngine:
    return CropRecommendationEngine()


def get_weather_service() -> WeatherService:
    return WeatherService()


def get_commodity_service() -> CommodityService:
    return CommodityService()


def get_free_commodity_service() -> FreeCommodityService:
    return FreeCommodityService()


def get_llm_service() -> LocalLLMService:
    return LocalLLMService()


# Templates
templates = Jinja2Templates(directory="templates")

# Response Models


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class WeatherResponse(BaseModel):
    weather_forecast: WeatherForecast
    weather_summary: dict


class CommodityPricesResponse(BaseModel):
    commodity_prices: List[CommodityPrice]
    market_analysis: Dict[str, Any]  # Advanced analysis with visualizations


class HealthResponse(BaseModel):
    status: str
    service: str
    llm_available: bool
    features: dict
    timestamp: datetime = Field(default_factory=datetime.now)


class LLMStatusResponse(BaseModel):
    llm_available: bool
    available_models: List[str]
    current_model: str
    service_url: str

# Exception Handlers


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later.",
            "timestamp": datetime.now().isoformat()
        }
    )

# Routes


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with farmer input form"""
    try:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "states": Config.INDIAN_STATES,
            "crops": Config.MAJOR_CROPS
        })
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load home page")


@app.post("/api/recommendations", response_model=CropSuggestionResponse)
async def get_crop_recommendations(
    query: FarmerQuery,
    recommendation_engine: CropRecommendationEngine = Depends(
        get_recommendation_engine),
    weather_service: WeatherService = Depends(get_weather_service),
    commodity_service: CommodityService = Depends(get_commodity_service)
):
    """Get AI-powered crop recommendations"""
    try:
        logger.info(
            f"Generating recommendations for location: {query.location.state}, {query.location.district}")

        # Validate location coordinates
        if not (-90 <= query.location.latitude <= 90):
            raise HTTPException(
                status_code=400, detail="Invalid latitude. Must be between -90 and 90.")
        if not (-180 <= query.location.longitude <= 180):
            raise HTTPException(
                status_code=400, detail="Invalid longitude. Must be between -180 and 180.")

        # Get weather data if not provided
        if query.weather is None:
            weather_forecast = await weather_service.get_weather_forecast(query.location)
            query.weather = weather_forecast

        # Get commodity prices if not provided
        if query.commodity_prices is None:
            commodity_prices = await commodity_service.get_commodity_prices(
                query.location, query.preferred_crops
            )
            query.commodity_prices = commodity_prices

        # Generate recommendations
        recommendations = await recommendation_engine.generate_recommendations(query)

        logger.info(
            f"Successfully generated {len(recommendations.recommendations)} recommendations")
        return recommendations

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Value error in recommendations: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(
            f"Error generating recommendations: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to generate recommendations: {str(e)}")


@app.get("/api/weather/{state}/{district}", response_model=WeatherResponse)
async def get_weather_data(
    state: str = Path(..., description="State name", min_length=2),
    district: str = Path(..., description="District name", min_length=2),
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    weather_service: WeatherService = Depends(get_weather_service)
):
    """Get weather data for a specific location"""
    try:
        logger.info(
            f"Fetching weather for {state}, {district} at ({lat}, {lon})")

        location = Location(
            state=state,
            district=district,
            latitude=lat,
            longitude=lon
        )

        weather_forecast = await weather_service.get_weather_forecast(location)
        weather_summary = weather_service.get_weather_summary(weather_forecast)

        return WeatherResponse(
            weather_forecast=weather_forecast,
            weather_summary=weather_summary
        )

    except ValueError as e:
        logger.error(f"Value error in weather data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching weather data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch weather data: {str(e)}")


@app.get("/api/commodity-prices", response_model=CommodityPricesResponse)
async def get_commodity_prices(
    state: str = Query(..., min_length=2, description="State name"),
    district: str = Query(..., min_length=2, description="District name"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    crops: Optional[str] = Query(
        None, description="Comma-separated list of crops"),
    free_commodity_service: FreeCommodityService = Depends(
        get_free_commodity_service)
):
    """Get commodity prices for specified crops"""
    try:
        logger.info(
            f"Fetching commodity prices for {state}, {district}, crops: {crops}")

        # Validate location
        if not state or not district:
            raise HTTPException(
                status_code=400, detail="State and district are required")

        location = Location(
            state=state,
            district=district,
            latitude=lat,
            longitude=lon
        )

        # Handle crops parameter - split if provided and not empty
        crop_list = None
        if crops and crops.strip():
            crop_list = [c.strip() for c in crops.split(",") if c.strip()]
            if not crop_list:  # If all crops were empty strings
                crop_list = None
            logger.info(f"Requested crops: {crop_list}")

        # Ensure service is initialized
        if free_commodity_service is None:
            raise HTTPException(
                status_code=500, detail="Commodity service not initialized")

        prices = await free_commodity_service.get_commodity_prices(location, crop_list)

        # Handle empty prices - return empty with diagnostic info
        if not prices:
            logger.warning(
                f"⚠️ No commodity prices found for {state}, {district}, crops: {crop_list}")
            logger.warning("This could be due to:")
            logger.warning(
                "  1. API not returning data for the requested crops/state")
            logger.warning(
                "  2. Commodity name mismatch between request and API")
            logger.warning("  3. API service unavailable")
            logger.warning(
                "Check server logs for detailed API response information")

            market_analysis = {
                "market_sentiment": "Neutral",
                "average_price": 0,
                "trend_distribution": {
                    "increasing": 0,
                    "decreasing": 0,
                    "stable": 0
                },
                "message": f"No real-time price data available for the requested crops/location. Check logs for details.",
                "data_source": "Real API (no data found)",
                "diagnostic": {
                    "requested_crops": crop_list,
                    "state": state,
                    "district": district
                }
            }
        else:
            market_analysis = free_commodity_service.get_market_analysis(
                prices)

        return CommodityPricesResponse(
            commodity_prices=prices,
            market_analysis=market_analysis
        )

    except ValueError as e:
        logger.error(f"Value error in commodity prices: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(
            f"Error fetching commodity prices: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch commodity prices: {str(e)}")


@app.get("/api/crop-info/{crop_name}")
async def get_crop_information(
    crop_name: str = Path(..., min_length=2, description="Crop name")
):
    """Get detailed information about a specific crop"""
    try:
        logger.info(f"Fetching crop information for: {crop_name}")

        from agricultural_database import IndianAgriculturalDatabase
        agri_db = IndianAgriculturalDatabase()

        crop_info = agri_db.get_crop_info(crop_name)
        if not crop_info:
            raise HTTPException(
                status_code=404, detail=f"Crop '{crop_name}' not found")

        return crop_info

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error fetching crop information: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch crop information: {str(e)}")


@app.get("/api/regional-info/{state}")
async def get_regional_information(
    state: str = Path(..., min_length=2, description="State name")
):
    """Get agricultural information for a specific state"""
    try:
        logger.info(f"Fetching regional information for: {state}")

        from agricultural_database import IndianAgriculturalDatabase
        agri_db = IndianAgriculturalDatabase()

        regional_info = agri_db.get_regional_info(state)
        if not regional_info:
            raise HTTPException(
                status_code=404, detail=f"State '{state}' not found")

        return regional_info

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error fetching regional information: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch regional information: {str(e)}")


@app.get("/api/price-trends/{commodity}")
async def get_price_trends(
    commodity: str = Path(..., min_length=2, description="Commodity name"),
    days: int = Query(30, ge=1, le=365,
                      description="Number of days for trend analysis"),
    free_commodity_service: FreeCommodityService = Depends(
        get_free_commodity_service)
):
    """Get price trends for a specific commodity"""
    try:
        logger.info(f"Fetching price trends for {commodity} over {days} days")

        trends = await free_commodity_service.get_price_trends(commodity, days)

        if "error" in trends:
            raise HTTPException(status_code=404, detail=trends["error"])

        return trends

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching price trends: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to fetch price trends: {str(e)}")


@app.get("/api/llm-status", response_model=LLMStatusResponse)
async def llm_status(llm_service: LocalLLMService = Depends(get_llm_service)):
    """Check LLM service status"""
    try:
        is_available = llm_service.is_ollama_available()
        models = llm_service.get_available_models() if is_available else []

        return LLMStatusResponse(
            llm_available=is_available,
            available_models=models,
            current_model=llm_service.model_name,
            service_url=llm_service.ollama_url
        )
    except Exception as e:
        logger.error(f"Error checking LLM status: {str(e)}", exc_info=True)
        return LLMStatusResponse(
            llm_available=False,
            available_models=[],
            current_model="unknown",
            service_url="unknown"
        )


@app.get("/health", response_model=HealthResponse)
async def health_check(llm_service: LocalLLMService = Depends(get_llm_service)):
    """Health check endpoint"""
    try:
        llm_status_check = llm_service.is_ollama_available()
        return HealthResponse(
            status="healthy",
            service="MandiGPT",
            llm_available=llm_status_check,
            features={
                "local_llm": llm_status_check,
                "free_commodity_prices": True,
                "weather_forecast": True,
                "crop_recommendations": True
            },
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}", exc_info=True)
        return HealthResponse(
            status="degraded",
            service="MandiGPT",
            llm_available=False,
            features={
                "local_llm": False,
                "free_commodity_prices": True,
                "weather_forecast": True,
                "crop_recommendations": True
            },
            timestamp=datetime.now()
        )

if __name__ == "__main__":
    import uvicorn
    # Use string import for reload to work properly
    if Config.DEBUG:
        uvicorn.run(
            "main:app",
            host=Config.HOST,
            port=Config.PORT,
            reload=True,
            log_level="info"
        )
    else:
        uvicorn.run(
            app,
            host=Config.HOST,
            port=Config.PORT,
            reload=False,
            log_level="info"
        )
