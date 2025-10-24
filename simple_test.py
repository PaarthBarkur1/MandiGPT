#!/usr/bin/env python3
"""
Simple test for MandiGPT API
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_basic_endpoints():
    """Test basic endpoints"""
    print("Testing basic endpoints...")
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            print("Response:", response.json())
    except Exception as e:
        print(f"Health check error: {e}")
    
    # Test commodity prices
    try:
        response = requests.get(f"{BASE_URL}/api/commodity-prices?state=Maharashtra&district=Pune&lat=18.5204&lon=73.8567&crops=Rice,Wheat,Maize")
        print(f"Commodity Prices: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Sample prices:")
            for price in data['commodity_prices'][:2]:
                print(f"  {price['commodity_name']}: ₹{price['current_price']} ({price['price_trend']})")
    except Exception as e:
        print(f"Commodity prices error: {e}")
    
    # Test weather data
    try:
        response = requests.get(f"{BASE_URL}/api/weather/Maharashtra/Pune?lat=18.5204&lon=73.8567")
        print(f"Weather Data: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Weather summary available")
    except Exception as e:
        print(f"Weather data error: {e}")

def test_crop_recommendations():
    """Test crop recommendations with proper data structure"""
    print("\nTesting crop recommendations...")
    
    # Create a proper farmer query with all required fields
    farmer_query = {
        "location": {
            "state": "Maharashtra",
            "district": "Pune",
            "latitude": 18.5204,
            "longitude": 73.8567,
            "soil_type": "Black"
        },
        "weather": {
            "current": {
                "temperature": 28.5,
                "humidity": 65.0,
                "rainfall": 15.0,
                "wind_speed": 10.0,
                "pressure": 1013.25,
                "uv_index": 6.0,
                "cloud_cover": 30.0,
                "date": datetime.now().isoformat()
            },
            "forecast_7_days": []
        },
        "commodity_prices": [
            {
                "commodity_name": "Rice",
                "current_price": 2500.0,
                "price_trend": "increasing",
                "market_location": "Mumbai",
                "date": datetime.now().isoformat()
            },
            {
                "commodity_name": "Wheat",
                "current_price": 2200.0,
                "price_trend": "stable",
                "market_location": "Mumbai",
                "date": datetime.now().isoformat()
            }
        ],
        "budget": 50000,
        "land_size": 2.5,
        "risk_tolerance": "Medium",
        "preferred_crops": ["Rice", "Wheat", "Maize"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json=farmer_query,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Recommendations: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Recommendations generated successfully!")
            print(f"Number of recommendations: {len(data.get('recommendations', []))}")
            print(f"Number of advice items: {len(data.get('advice', []))}")
            print(f"Market analysis available: {bool(data.get('market_analysis'))}")
            print(f"AI recommendations available: {bool(data.get('ai_recommendations'))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Recommendations error: {e}")

if __name__ == "__main__":
    test_basic_endpoints()
    test_crop_recommendations()
