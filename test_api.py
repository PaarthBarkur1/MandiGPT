#!/usr/bin/env python3
"""
Test API endpoints for MandiGPT
"""

import requests
import json
from datetime import datetime

def test_crop_recommendations():
    """Test crop recommendations API"""
    print("Testing crop recommendations API...")
    
    # Create proper farmer query with all required fields
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
            "forecast_7_days": [
                {
                    "temperature": 28.5,
                    "humidity": 65.0,
                    "rainfall": 15.0,
                    "wind_speed": 10.0,
                    "pressure": 1013.25,
                    "uv_index": 6.0,
                    "cloud_cover": 30.0,
                    "date": datetime.now().isoformat()
                }
            ]
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
            "http://localhost:8000/api/recommendations",
            json=farmer_query,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS: Crop recommendations generated!")
            print(f"Number of recommendations: {len(data.get('recommendations', []))}")
            print(f"Number of advice items: {len(data.get('advice', []))}")
            print(f"Market analysis available: {bool(data.get('market_analysis'))}")
            print(f"AI recommendations available: {bool(data.get('ai_recommendations'))}")
            
            # Show first recommendation
            if data.get('recommendations'):
                first_rec = data['recommendations'][0]
                print(f"\nFirst recommendation: {first_rec.get('crop_name')}")
                print(f"Confidence: {first_rec.get('confidence_score', 0):.2f}")
                print(f"Expected yield: {first_rec.get('expected_yield', 0):.1f} quintals")
                print(f"Market price: ₹{first_rec.get('market_price', 0)}/quintal")
            
            return True
        else:
            print(f"ERROR: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Main test function"""
    print("MandiGPT API Test")
    print("=" * 30)
    
    success = test_crop_recommendations()
    
    if success:
        print("\nAPI test completed successfully!")
    else:
        print("\nAPI test failed.")

if __name__ == "__main__":
    main()
