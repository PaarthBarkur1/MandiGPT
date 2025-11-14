#!/usr/bin/env python3
"""
MandiGPT - Data.gov.in Commodity API Usage Examples
This file demonstrates how to use the integrated API in your application
"""

import asyncio
from datetime import datetime
from models import Location
from free_commodity_service import FreeCommodityService

# ============================================================================
# EXAMPLE 1: Basic Commodity Price Fetching
# ============================================================================


async def example_basic_prices():
    """Example 1: Fetch commodity prices for a location"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Commodity Price Fetching")
    print("="*70)

    # Initialize service
    service = FreeCommodityService()

    # Define location
    location = Location(
        state="Maharashtra",
        district="Pune",
        latitude=18.5204,
        longitude=73.8567,
        soil_type="Black"
    )

    # Fetch prices (automatically tries data.gov.in first)
    commodities = ["Rice", "Wheat", "Cotton"]
    prices = await service.get_commodity_prices(location, commodities)

    print(f"\nCommodity prices for {location.state}, {location.district}:")
    print("-" * 70)

    for price in prices:
        print(f"\n🌾 {price.commodity_name}")
        print(f"   Current Price: ₹{price.current_price}/quintal")
        print(f"   Market: {price.market_location}")
        print(f"   Trend: {price.price_trend} 📈" if price.price_trend == "increasing"
              else f"   Trend: {price.price_trend} 📉" if price.price_trend == "decreasing"
              else f"   Trend: {price.price_trend} ➡️")
        print(f"   Last Updated: {price.date}")


# ============================================================================
# EXAMPLE 2: Specific Commodity Analysis
# ============================================================================

async def example_commodity_analysis():
    """Example 2: Analyze a specific commodity"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Specific Commodity Analysis")
    print("="*70)

    service = FreeCommodityService()

    # Get price trends for a commodity
    commodity = "Rice"
    print(f"\nAnalyzing {commodity} prices over 30 days...")
    print("-" * 70)

    trends = await service.get_price_trends(commodity, days=30)

    if trends.get('error'):
        print(f"❌ Error: {trends['error']}")
    else:
        print(f"Commodity: {trends['commodity']}")
        print(f"Market Trend: {trends['trend']} 📊")
        print(f"Current Price: ₹{trends['current_price']}/quintal")
        print(f"Price Change (30 days): ₹{trends['price_change']:.2f}")
        print(f"\nRecent Price History:")

        # Show last 7 days
        for record in trends['price_history'][-7:]:
            print(f"  {record['date']}: ₹{record['price']:.2f}")


# ============================================================================
# EXAMPLE 3: Market Analysis
# ============================================================================

async def example_market_analysis():
    """Example 3: Analyze overall market conditions"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Market Analysis")
    print("="*70)

    service = FreeCommodityService()

    location = Location(
        state="Punjab",
        district="Amritsar",
        latitude=31.6340,
        longitude=74.8723,
        soil_type="Alluvial"
    )

    # Fetch multiple commodities
    commodities = ["Wheat", "Rice", "Sugarcane", "Cotton", "Maize"]
    prices = await service.get_commodity_prices(location, commodities)

    # Get market analysis
    analysis = service.get_market_analysis(prices)

    print(f"\nMarket Analysis for {location.state}")
    print("-" * 70)

    if 'error' not in analysis:
        print(f"\n📊 Market Sentiment: {analysis['market_sentiment']}")
        print(f"Average Price: ₹{analysis['average_price']}/quintal")

        print(f"\n📈 Trend Distribution:")
        print(
            f"   Increasing: {analysis['trend_distribution']['increasing']} commodities")
        print(
            f"   Decreasing: {analysis['trend_distribution']['decreasing']} commodities")
        print(
            f"   Stable: {analysis['trend_distribution']['stable']} commodities")

        print(f"\n🏆 Best Performing:")
        best = analysis['best_performing']
        print(
            f"   {best['commodity']}: ₹{best['price']}/unit ({best['trend']})")

        print(f"\n📉 Worst Performing:")
        worst = analysis['worst_performing']
        print(
            f"   {worst['commodity']}: ₹{worst['price']}/unit ({worst['trend']})")

        print(f"\n💡 Recommendation:")
        print(f"   {analysis['market_recommendation']}")


# ============================================================================
# EXAMPLE 4: Multi-Location Comparison
# ============================================================================

async def example_location_comparison():
    """Example 4: Compare prices across different states"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Multi-Location Price Comparison")
    print("="*70)

    service = FreeCommodityService()

    # Define multiple locations
    locations = [
        Location(state="Maharashtra", district="Pune",
                 latitude=18.5204, longitude=73.8567, soil_type="Black"),
        Location(state="Punjab", district="Amritsar", latitude=31.6340,
                 longitude=74.8723, soil_type="Alluvial"),
        Location(state="Karnataka", district="Bangalore",
                 latitude=12.9716, longitude=77.5946, soil_type="Red"),
    ]

    commodity = "Rice"

    print(f"\n🌾 {commodity} Price Comparison Across States")
    print("-" * 70)
    print(f"{'State':<20} {'District':<20} {'Price (₹/qt)':<15} {'Trend':<10}")
    print("-" * 70)

    for location in locations:
        prices = await service.get_commodity_prices(location, [commodity])

        if prices:
            price = prices[0]
            trend_emoji = "📈" if price.price_trend == "increasing" else "📉" if price.price_trend == "decreasing" else "➡️"
            print(f"{location.state:<20} {location.district:<20} ₹{price.current_price:<13.2f} {price.price_trend} {trend_emoji}")


# ============================================================================
# EXAMPLE 5: Farmer Decision Making
# ============================================================================

async def example_farmer_decision():
    """Example 5: Help a farmer decide which crop to plant"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Farmer Decision Support")
    print("="*70)

    service = FreeCommodityService()

    # Farmer's details
    farmer_location = Location(
        state="Maharashtra",
        district="Pune",
        latitude=18.5204,
        longitude=73.8567,
        soil_type="Black"
    )

    farmer_budget = 100000  # ₹ 100,000
    farmer_land = 2.5  # hectares

    # Candidate crops for Maharashtra
    candidate_crops = ["Rice", "Wheat", "Sugarcane", "Cotton", "Soybean"]

    print(f"\nFarmer's Profile:")
    print(f"  Location: {farmer_location.state}, {farmer_location.district}")
    print(f"  Budget: ₹{farmer_budget:,}")
    print(f"  Land Size: {farmer_land} hectares")
    print(f"  Soil Type: {farmer_location.soil_type}")

    print(f"\nAnalyzing crops: {', '.join(candidate_crops)}")
    print("-" * 70)

    prices = await service.get_commodity_prices(farmer_location, candidate_crops)

    # Calculate profit potential (simplified)
    crop_analysis = []

    for price in prices:
        # Simplified: assume 20 quintals/hectare and 30% profit margin for rising trend
        expected_yield = 20 * farmer_land  # quintals
        revenue = expected_yield * price.current_price

        # Adjust profit based on trend
        if price.price_trend == "increasing":
            profit_margin = 0.35
        elif price.price_trend == "stable":
            profit_margin = 0.25
        else:
            profit_margin = 0.15

        profit = revenue * profit_margin

        crop_analysis.append({
            'crop': price.commodity_name,
            'price': price.current_price,
            'trend': price.price_trend,
            'revenue': revenue,
            'profit': profit,
            'roi': (profit / farmer_budget * 100) if farmer_budget > 0 else 0
        })

    # Sort by profit
    crop_analysis.sort(key=lambda x: x['profit'], reverse=True)

    print(f"\n📊 Profit Analysis (for {farmer_land} hectares):")
    print(f"{'Rank':<5} {'Crop':<15} {'Price (₹)':<12} {'Trend':<10} {'Est. Profit (₹)':<18} {'ROI %':<8}")
    print("-" * 70)

    for i, crop in enumerate(crop_analysis, 1):
        trend_emoji = "📈" if crop['trend'] == "increasing" else "📉" if crop['trend'] == "decreasing" else "➡️"
        print(
            f"{i:<5} {crop['crop']:<15} ₹{crop['price']:<11.0f} {crop['trend']:<9} ₹{crop['profit']:<16.0f} {crop['roi']:<7.1f}%  {trend_emoji}")

    print(f"\n💡 Recommendation:")
    best_crop = crop_analysis[0]
    print(
        f"   Plant {best_crop['crop']} - Expected Profit: ₹{best_crop['profit']:.0f} ({best_crop['roi']:.1f}% ROI)")
    print(
        f"   Current Market Price: ₹{best_crop['price']:.0f}/quintal ({best_crop['trend']} trend)")


# ============================================================================
# EXAMPLE 6: Error Handling and Fallbacks
# ============================================================================

async def example_error_handling():
    """Example 6: Demonstrate error handling and fallback mechanisms"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Error Handling & Fallback Mechanisms")
    print("="*70)

    service = FreeCommodityService()

    location = Location(
        state="Telangana",
        district="Hyderabad",
        latitude=17.3850,
        longitude=78.4867,
        soil_type="Laterite"
    )

    # Try to fetch price for a commodity
    commodity = "Turmeric"

    print(f"\nFetching price for {commodity} in {location.state}...")
    print("-" * 70)

    print(f"Attempting fallback chain:")
    print(f"  1️⃣ Trying data.gov.in API...")
    print(f"  2️⃣ If failed → Trying Agmarknet API...")
    print(f"  3️⃣ If failed → Using realistic mock prices...")

    prices = await service.get_commodity_prices(location, [commodity])

    if prices:
        price = prices[0]
        print(f"\n✅ Successfully fetched price!")
        print(f"   Commodity: {price.commodity_name}")
        print(f"   Price: ₹{price.current_price}/quintal")
        print(f"   Market: {price.market_location}")
        print(f"   Source: data.gov.in API (or fallback)")
    else:
        print(f"\n⚠️ Could not fetch price for {commodity}")
        print(f"   Application continues to work with fallback data")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Run all examples"""
    print("\n" + "🌾"*35)
    print("MandiGPT - Data.gov.in API Usage Examples")
    print("🌾"*35)

    try:
        # Run each example
        await example_basic_prices()
        await example_commodity_analysis()
        await example_market_analysis()
        await example_location_comparison()
        await example_farmer_decision()
        await example_error_handling()

        print("\n" + "="*70)
        print("✨ All examples completed successfully!")
        print("="*70)
        print("\n💡 Next Steps:")
        print("  1. Run: python test_datagov_api.py  (to test API connectivity)")
        print("  2. Check: DATAGOV_API_GUIDE.md     (for complete documentation)")
        print("  3. Deploy: MandiGPT is ready with real commodity prices!")
        print()

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
