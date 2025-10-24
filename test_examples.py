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
        response = requests.get(f"{BASE_URL}/api/commodity-prices?state=Maharashtra&district=Pune&lat=18.5204&lon=73.8567&crops=Rice,Wheat,Maize")
        if response.status_code == 200:
            data = response.json()
            print("✅ Commodity Prices Response:")
            print(json.dumps(data, indent=2))
            return True
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
        "preferred_crops": ["Rice", "Wheat", "Maize", "Sugarcane"]
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
        response = requests.get(f"{BASE_URL}/api/price-trends/Rice?days=30")
        if response.status_code == 200:
            data = response.json()
            print("✅ Price Trends Response:")
            print(json.dumps(data, indent=2))
            return True
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
