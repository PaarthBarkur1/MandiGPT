#!/usr/bin/env python3
"""Test commodity prices for Himachal Pradesh"""
import asyncio
import logging
from free_commodity_service import FreeCommodityService
from models import Location

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

async def test():
    service = FreeCommodityService()
    loc = Location(
        state='Himachal Pradesh',
        district='Solan',
        latitude=31.1048,
        longitude=77.1734
    )
    
    print("=" * 60)
    print("Testing commodity prices for Himachal Pradesh, Solan")
    print("=" * 60)
    print(f"\nLocation: {loc.state}, {loc.district}")
    print(f"Testing with NO crops (should use defaults)...")
    
    prices = await service.get_commodity_prices(loc, None)
    print(f"\n✅ Got {len(prices)} prices")
    
    if prices:
        print("\nPrices found:")
        for p in prices:
            print(f"  - {p.commodity_name}: ₹{p.current_price}/quintal at {p.market_location}")
    else:
        print("\n❌ No prices found")
    
    print("\n" + "=" * 60)
    print("Testing with specific crops...")
    prices2 = await service.get_commodity_prices(loc, ["Potato", "Tomato", "Apple"])
    print(f"\n✅ Got {len(prices2)} prices")
    
    if prices2:
        print("\nPrices found:")
        for p in prices2:
            print(f"  - {p.commodity_name}: ₹{p.current_price}/quintal at {p.market_location}")
    else:
        print("\n❌ No prices found")

if __name__ == "__main__":
    asyncio.run(test())

