#!/usr/bin/env python3
"""
Test script for MandiGPT
Run this to test the basic functionality
"""

import asyncio
import sys
from datetime import datetime
from models import FarmerQuery, Location, WeatherData, WeatherForecast
from recommendation_engine import CropRecommendationEngine

async def test_basic_functionality():
    """Test basic functionality of MandiGPT"""
    print("🧪 Testing MandiGPT Basic Functionality")
    print("=" * 50)
    
    try:
        # Initialize recommendation engine
        engine = CropRecommendationEngine()
        print("✅ Recommendation engine initialized")
        
        # Create test location (Punjab, India)
        location = Location(
            state="Punjab",
            district="Ludhiana",
            latitude=30.9010,
            longitude=75.8573
        )
        print("✅ Test location created")
        
        # Create mock weather data
        current_weather = WeatherData(
            temperature=25.0,
            humidity=65.0,
            rainfall=0.0,
            wind_speed=12.0,
            pressure=1013.25,
            uv_index=6.0,
            cloud_cover=30.0,
            date=datetime.now()
        )
        
        forecast_weather = [
            WeatherData(
                temperature=26.0 + i,
                humidity=60.0 + i,
                rainfall=0.0,
                wind_speed=10.0 + i,
                pressure=1013.25,
                uv_index=5.0,
                cloud_cover=40.0,
                date=datetime.now()
            ) for i in range(7)
        ]
        
        weather_forecast = WeatherForecast(
            current=current_weather,
            forecast_7_days=forecast_weather
        )
        print("✅ Mock weather data created")
        
        # Create test farmer query
        query = FarmerQuery(
            location=location,
            weather=weather_forecast,
            commodity_prices=[],
            land_size=2.0,
            budget=50000,
            preferred_crops=["Wheat", "Rice"],
            risk_tolerance="Medium"
        )
        print("✅ Test farmer query created")
        
        # Test agricultural database
        from agricultural_database import IndianAgriculturalDatabase
        agri_db = IndianAgriculturalDatabase()
        
        # Test crop suitability
        wheat_suitability = agri_db.get_crop_suitability(
            "Wheat", "Punjab", {"temperature": 25, "rainfall": 200, "humidity": 65}
        )
        print(f"✅ Wheat suitability score: {wheat_suitability:.2f}")
        
        # Test regional info
        punjab_info = agri_db.get_regional_info("Punjab")
        print(f"✅ Punjab info: {punjab_info.get('climate', 'Unknown')} climate")
        
        # Test weather service
        from weather_service import WeatherService
        weather_service = WeatherService()
        weather_summary = weather_service.get_weather_summary(weather_forecast)
        print(f"✅ Weather summary: {weather_summary['weather_suitability']}")
        
        # Test commodity service
        from commodity_service import CommodityService
        commodity_service = CommodityService()
        prices = await commodity_service.get_commodity_prices(location, ["Wheat", "Rice"])
        print(f"✅ Commodity prices: {len(prices)} crops")
        
        print("\n🎉 All basic tests passed!")
        print("MandiGPT is ready to use!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_recommendation_engine():
    """Test the recommendation engine with a full query"""
    print("\n🔬 Testing Recommendation Engine")
    print("=" * 50)
    
    try:
        # Create a more complete test query
        location = Location(
            state="Punjab",
            district="Ludhiana", 
            latitude=30.9010,
            longitude=75.8573
        )
        
        # Mock weather data
        current_weather = WeatherData(
            temperature=22.0,
            humidity=70.0,
            rainfall=5.0,
            wind_speed=8.0,
            pressure=1013.25,
            uv_index=4.0,
            cloud_cover=60.0,
            date=datetime.now()
        )
        
        forecast_weather = [
            WeatherData(
                temperature=20.0 + i,
                humidity=65.0 + i,
                rainfall=2.0 + i,
                wind_speed=10.0,
                pressure=1013.25,
                uv_index=5.0,
                cloud_cover=50.0,
                date=datetime.now()
            ) for i in range(7)
        ]
        
        weather_forecast = WeatherForecast(
            current=current_weather,
            forecast_7_days=forecast_weather
        )
        
        # Mock commodity prices
        from models import CommodityPrice
        commodity_prices = [
            CommodityPrice(
                commodity_name="Wheat",
                current_price=2200,
                price_trend="stable",
                market_location="Punjab",
                date=datetime.now()
            ),
            CommodityPrice(
                commodity_name="Rice",
                current_price=2500,
                price_trend="increasing",
                market_location="Punjab",
                date=datetime.now()
            )
        ]
        
        query = FarmerQuery(
            location=location,
            weather=weather_forecast,
            commodity_prices=commodity_prices,
            land_size=2.0,
            budget=100000,
            preferred_crops=["Wheat", "Rice", "Maize"],
            risk_tolerance="Medium"
        )
        
        # Test recommendation engine
        engine = CropRecommendationEngine()
        recommendations = await engine.generate_recommendations(query)
        
        print(f"✅ Generated {len(recommendations.recommendations)} crop recommendations")
        print(f"✅ Generated {len(recommendations.advice)} pieces of advice")
        print(f"✅ Market analysis: {recommendations.market_analysis.get('market_sentiment', 'Unknown')}")
        print(f"✅ Risk assessment: {recommendations.risk_assessment.get('overall_risk', 'Unknown')}")
        
        # Display top recommendation
        if recommendations.recommendations:
            top_rec = recommendations.recommendations[0]
            print(f"\n🏆 Top Recommendation: {top_rec.crop_name}")
            print(f"   Confidence: {top_rec.confidence_score:.1%}")
            print(f"   Expected Profit: ₹{top_rec.estimated_profit:,.0f}")
            print(f"   Market Price: ₹{top_rec.market_price:,.0f}/quintal")
        
        print("\n🎉 Recommendation engine test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Recommendation engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🌾 MandiGPT Test Suite")
    print("=" * 50)
    
    # Run basic functionality tests
    basic_test = await test_basic_functionality()
    
    if basic_test:
        # Run recommendation engine tests
        engine_test = await test_recommendation_engine()
        
        if engine_test:
            print("\n🎉 All tests passed! MandiGPT is working correctly.")
            print("You can now run the application with: python run.py")
        else:
            print("\n❌ Some tests failed. Please check the error messages above.")
            sys.exit(1)
    else:
        print("\n❌ Basic functionality tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
