#!/usr/bin/env python3
"""
Test the real commodity API to diagnose issues
"""
import asyncio
import httpx
import json
from models import Location

async def test_datagov_api():
    """Test data.gov.in API directly"""
    api_key = "579b464db66ec23bdd000001468e9fd39c6f44e777a85ad2b2e7bc54"
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        print("=" * 60)
        print("Testing data.gov.in API")
        print("=" * 60)
        
        params = {
            'api-key': api_key,
            'format': 'json',
            'limit': 100
        }
        
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            print(f"\n✅ API Response Status: {data.get('status')}")
            print(f"📊 Total Records: {data.get('count', 'Unknown')}")
            print(f"📋 Records Returned: {len(data.get('records', []))}")
            
            if data.get('records'):
                records = data['records']
                
                # Show sample records
                print(f"\n📝 Sample Records (first 3):")
                for i, record in enumerate(records[:3]):
                    print(f"\n  Record {i+1}:")
                    print(f"    Commodity: {record.get('commodity')}")
                    print(f"    State: {record.get('state')}")
                    print(f"    District: {record.get('district')}")
                    print(f"    Market: {record.get('market')}")
                    print(f"    Modal Price: {record.get('modal_price')}")
                    print(f"    Min Price: {record.get('min_price')}")
                    print(f"    Max Price: {record.get('max_price')}")
                
                # Test filtering for Haryana
                print(f"\n🔍 Testing Filter for Haryana:")
                haryana_records = [r for r in records if 'haryana' in r.get('state', '').lower()]
                print(f"   Found {len(haryana_records)} records for Haryana")
                
                if haryana_records:
                    print(f"\n   Sample Haryana Records:")
                    for i, record in enumerate(haryana_records[:3]):
                        print(f"     {i+1}. {record.get('commodity')} - {record.get('market')} - ₹{record.get('modal_price')}/quintal")
                
                # Test filtering for Rice
                print(f"\n🔍 Testing Filter for Rice:")
                rice_records = [r for r in records if 'rice' in r.get('commodity', '').lower()]
                print(f"   Found {len(rice_records)} records for Rice")
                
                if rice_records:
                    print(f"\n   Sample Rice Records:")
                    for i, record in enumerate(rice_records[:3]):
                        print(f"     {i+1}. {record.get('commodity')} - {record.get('state')} - {record.get('market')} - ₹{record.get('modal_price')}/quintal")
                
                # Test combined filter: Rice in Haryana
                print(f"\n🔍 Testing Filter: Rice in Haryana:")
                rice_haryana = [
                    r for r in records 
                    if 'rice' in r.get('commodity', '').lower() 
                    and 'haryana' in r.get('state', '').lower()
                ]
                print(f"   Found {len(rice_haryana)} records for Rice in Haryana")
                
                if rice_haryana:
                    print(f"\n   Rice in Haryana Records:")
                    for i, record in enumerate(rice_haryana[:5]):
                        print(f"     {i+1}. {record.get('commodity')} - {record.get('market')} - ₹{record.get('modal_price')}/quintal")
                else:
                    print(f"   ⚠️ No Rice found in Haryana in this sample")
                
                # Show unique commodities and states
                commodities = set(r.get('commodity', '').strip() for r in records if r.get('commodity'))
                states = set(r.get('state', '').strip() for r in records if r.get('state'))
                
                print(f"\n📦 Available Commodities (sample): {sorted(list(commodities))[:15]}")
                print(f"🗺️  Available States (sample): {sorted(list(states))[:15]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_datagov_api())

