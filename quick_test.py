#!/usr/bin/env python3
"""
Quick test for MandiGPT without Unicode issues
"""

import asyncio
from models import FarmerQuery, Location, WeatherForecast, WeatherData
from recommendation_engine import CropRecommendationEngine
from datetime import datetime

async def test_recommendation_engine():
    """Test the recommendation engine"""
    print("Testing recommendation engine...")
    
    try:
        # Create test data
        location = Location(
            state="Maharashtra",
            district="Pune", 
            latitude=18.5204,
            longitude=73.8567,
            soil_type="Black"
        )
        
        # Create mock weather data
        current_weather = WeatherData(
            temperature=28.5,
            humidity=65.0,
            rainfall=15.0,
            wind_speed=10.0,
            pressure=1013.25,
            uv_index=6.0,
            cloud_cover=30.0,
            date=datetime.now()
        )
        
        weather_forecast = WeatherForecast(
            current=current_weather,
            forecast_7_days=[current_weather]  # Use current as forecast
        )
        
        # Create farmer query
        query = FarmerQuery(
            location=location,
            weather=weather_forecast,
            commodity_prices=[],  # Empty for now
            budget=50000,
            land_size=2.5,
            risk_tolerance="Medium",
            preferred_crops=["Rice", "Wheat", "Maize"]
        )
        
        # Test recommendation engine
        engine = CropRecommendationEngine()
        recommendations = await engine.generate_recommendations(query)
        
        print("SUCCESS: Recommendation engine working!")
        print(f"Number of recommendations: {len(recommendations.recommendations)}")
        print(f"Number of advice items: {len(recommendations.advice)}")
        print(f"Market analysis available: {bool(recommendations.market_analysis)}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("MandiGPT Quick Test")
    print("=" * 30)
    
    success = await test_recommendation_engine()
    
    if success:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")

if __name__ == "__main__":
    asyncio.run(main())
