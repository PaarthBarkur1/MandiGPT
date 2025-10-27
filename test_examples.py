#!/usr/bin/env python3
"""
Test examples for MandiGPT API
This script demonstrates how to test the application endpoints
"""

import requests
import json
import asyncio
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check Response:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_llm_status():
    """Test the LLM status endpoint"""
    print("\n🤖 Testing LLM Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/llm-status")
        if response.status_code == 200:
            data = response.json()
            print("✅ LLM Status Response:")
            print(json.dumps(data, indent=2))
            return data.get("llm_available", False)
        else:
            print(f"❌ LLM status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_weather_data():
    """Test weather data endpoint"""
    print("\n🌤️ Testing Weather Data...")
    try:
        # Test with Delhi coordinates
        response = requests.get(f"{BASE_URL}/api/weather/Delhi/Central Delhi?lat=28.6139&lon=77.2090")
        if response.status_code == 200:
            data = response.json()
            print("✅ Weather Data Response:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Weather data failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_commodity_prices():
    """Test commodity prices endpoint"""
    print("\n💰 Testing Commodity Prices...")
    try:
        # Test with commodities that are available in the API
        response = requests.get(f"{BASE_URL}/api/commodity-prices?state=Maharashtra&district=Pune&lat=18.5204&lon=73.8567&crops=Gold,Silver,Cotton")
        if response.status_code == 200:
            data = response.json()
            print("✅ Commodity Prices Response:")
            print(json.dumps(data, indent=2))
            
            # Validate response structure
            if "commodity_prices" in data and isinstance(data["commodity_prices"], list):
                for price_data in data["commodity_prices"]:
                    if not all(key in price_data for key in ['commodity_name', 'current_price', 'market_location']):
                        print("❌ Missing required fields in response")
                        return False
                return True
            else:
                print("❌ Missing or invalid commodity_prices in response")
                return False
        else:
            print(f"❌ Commodity prices failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_crop_recommendations():
    """Test crop recommendations endpoint"""
    print("\n🌾 Testing Crop Recommendations...")
    
    # Sample farmer query
    farmer_query = {
        "location": {
            "state": "Maharashtra",
            "district": "Pune",
            "latitude": 18.5204,
            "longitude": 73.8567,
            "soil_type": "Black"
        },
        "land_size": 2.5,
        "budget": 50000,
        "risk_tolerance": "Medium",
        "preferred_crops": ["Cotton"],  # Only using Cotton as it's an agricultural commodity
        "weather": {
            "current": {
                "temperature": 25.0,
                "humidity": 60.0,
                "rainfall": 0.0,
                "wind_speed": 10.0,
                "pressure": 1013.25,
                "uv_index": 5.0,
                "cloud_cover": 50.0,
                "date": "2025-10-28T00:00:00"
            },
            "forecast_7_days": [
                {
                    "temperature": 25.0,
                    "humidity": 60.0,
                    "rainfall": 0.0,
                    "wind_speed": 10.0,
                    "pressure": 1013.25,
                    "uv_index": 5.0,
                    "cloud_cover": 50.0,
                    "date": "2025-10-28T00:00:00"
                }
            ]
        },
        "commodity_prices": [
            {
                "commodity_name": "Cotton",
                "current_price": 7032.81,
                "price_trend": "stable",
                "market_location": "Mumbai",
                "date": "2025-10-28T00:00:00"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json=farmer_query,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Crop Recommendations Response:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Crop recommendations failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_price_trends():
    """Test price trends endpoint"""
    print("\n📈 Testing Price Trends...")
    try:
        # Test with a commodity available in the API
        response = requests.get(f"{BASE_URL}/api/price-trends/Cotton?days=30")
        if response.status_code == 200:
            data = response.json()
            print("✅ Price Trends Response:")
            print(json.dumps(data, indent=2))
            
            # Validate response structure
            required_fields = ['commodity', 'trend', 'price_history', 'current_price']
            if all(field in data for field in required_fields):
                if isinstance(data['price_history'], list) and len(data['price_history']) > 0:
                    return True
                else:
                    print("❌ Price history data is missing or empty")
                    return False
            else:
                print("❌ Missing required fields in response")
                return False
        else:
            print(f"❌ Price trends failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 MandiGPT API Testing Suite")
    print("=" * 50)
    
    # Test all endpoints
    tests = [
        test_health_check,
        test_llm_status,
        test_weather_data,
        test_commodity_prices,
        test_crop_recommendations,
        test_price_trends
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
