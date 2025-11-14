#!/usr/bin/env python3
"""
Test script for data.gov.in Commodity Price API integration
This demonstrates how to fetch commodity prices from the government API
"""

import requests
import json
from config import Config


class DataGovAPITester:
    """Test data.gov.in API integration"""

    def __init__(self):
        self.api_key = Config.COMMODITY_API_KEY or "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
        self.base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })

    def test_basic_query(self):
        """Test basic API query without filters"""
        print("\n" + "="*60)
        print("TEST 1: Basic Query (No Filters)")
        print("="*60)

        try:
            params = {
                'api-key': self.api_key,
                'format': 'json',
                'limit': 5
            }

            response = self.session.get(
                self.base_url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            # Check for records (no 'success' key in this API)
            if data.get('records') and len(data['records']) > 0:
                total = data.get('total', 'Unknown')
                print(f"✅ SUCCESS: {total} records available")
                print(f"\nFirst record structure:")
                record = data['records'][0]
                print(json.dumps(record, indent=2))
                return True
            elif data.get('status') == 'ok':
                print(f"✅ API OK but no records returned")
                print(f"Total available: {data.get('total', 'Unknown')}")
                return True
            else:
                print(
                    f"❌ API returned error. Status: {data.get('status', 'Unknown')}")
                print(f"Message: {data.get('message', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False

    def test_commodity_filter(self, commodity="Tomato", state="Gujarat"):
        """Test filtering by commodity and state"""
        print("\n" + "="*60)
        print(f"TEST 2: Filter by Commodity '{commodity}' and State '{state}'")
        print("="*60)

        try:
            # Fetch records (API filters don't work well, so we'll filter locally)
            params = {
                'api-key': self.api_key,
                'format': 'json',
                'limit': 1000  # Get more records to find matches
            }

            response = self.session.get(
                self.base_url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            if data.get('status') == 'ok' and data.get('records'):
                records = data['records']
                # Filter locally
                filtered = [r for r in records if r.get(
                    'commodity') == commodity and r.get('state') == state]

                if filtered:
                    print(
                        f"✅ SUCCESS: Found {len(filtered)} records for {commodity} in {state}")
                    print(f"\nSample records:")
                    for i, record in enumerate(filtered[:3]):
                        print(f"\nRecord {i+1}:")
                        for key in ['commodity', 'state', 'market', 'modal_price', 'min_price', 'max_price', 'arrival_date']:
                            if key in record:
                                print(f"  {key}: {record[key]}")
                    return True
                else:
                    print(f"⚠️  No records found for {commodity} in {state}")
                    # Show available
                    commodities = set(r.get('commodity') for r in records)
                    states_available = set(r.get('state') for r in records)
                    print(
                        f"Available commodities: {sorted(list(commodities))}")
                    print(
                        f"Available states: {sorted(list(states_available))}")
                    return False
            else:
                print(f"⚠️  No records found or API error")
                if data.get('message'):
                    print(f"Message: {data.get('message')}")
                return False

        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False

    def test_market_filter(self, market="Jambusar"):
        """Test filtering by market"""
        print("\n" + "="*60)
        print(f"TEST 3: Filter by Market '{market}'")
        print("="*60)

        try:
            # Fetch all records and filter locally
            params = {
                'api-key': self.api_key,
                'format': 'json',
                'limit': 1000
            }

            response = self.session.get(
                self.base_url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            if data.get('status') == 'ok' and data.get('records'):
                records = data['records']
                # Filter locally
                filtered = [r for r in records if r.get('market') == market]

                if filtered:
                    print(
                        f"✅ SUCCESS: Found {len(filtered)} records from market '{market}'")

                    # Extract unique commodities
                    commodities = set()
                    prices = []
                    for record in filtered:
                        commodities.add(record.get('commodity', 'Unknown'))
                        price = record.get(
                            'modal_price') or record.get('max_price')
                        if price:
                            prices.append({
                                'commodity': record.get('commodity'),
                                'price': price,
                                'market': record.get('market')
                            })

                    print(
                        f"\nAvailable commodities in {market}: {', '.join(sorted(commodities))}")
                    print(f"\nPrice samples:")
                    for p in prices[:5]:
                        print(f"  {p['commodity']}: ₹{p['price']}/unit")

                    return True
                else:
                    print(f"⚠️  No records found for market '{market}'")
                    # Show available markets
                    markets_available = set(r.get('market') for r in records)
                    print(
                        f"Available markets: {sorted(list(markets_available))}")
                    return False
            else:
                print(f"⚠️  No records found or API error")
                return False

        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False

    def test_curl_command(self):
        """Show the equivalent curl command for manual testing"""
        print("\n" + "="*60)
        print("CURL COMMAND REFERENCE")
        print("="*60)

        curl_command = f"""curl -X 'GET' \\
  '{self.base_url}?api-key={self.api_key}&format=json&limit=10&filters[commodity_name]=Rice&filters[state]=Maharashtra' \\
  -H 'accept: application/json'"""

        print("\nGeneral format:")
        print("""curl -X 'GET' \\
  'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=YOUR_API_KEY&format=json' \\
  -H 'accept: application/json'""")

        print("\n\nWith filters (commodity and state):")
        print(curl_command)

        print("\n\nCommon filter parameters:")
        print(
            "  - filters[commodity_name]: Name of the commodity (e.g., Rice, Wheat, Cotton)")
        print(
            "  - filters[state]: State name (e.g., Maharashtra, Punjab, Karnataka)")
        print(
            "  - filters[market]: Market name (e.g., Delhi, Mumbai, Chennai)")
        print("  - filters[date]: Date in YYYY-MM-DD format")
        print("  - limit: Number of records to fetch (default: 100)")
        print("  - format: json or xml")

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "🔍 "*20)
        print("DATA.GOV.IN COMMODITY API - INTEGRATION TEST")
        print("🔍 "*20)

        results = {}

        # Test 1: Basic query
        results['basic_query'] = self.test_basic_query()

        # Test 2: Commodity and state filter
        results['commodity_filter'] = self.test_commodity_filter(
            "Rice", "Maharashtra")

        # Test 3: Market filter (using an available market)
        results['market_filter'] = self.test_market_filter("Mangaon")

        # Show curl commands
        self.test_curl_command()

        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name}: {status}")

        all_passed = all(results.values())
        print(
            f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '⚠️  SOME TESTS FAILED'}")

        return all_passed


def main():
    """Main test function"""
    tester = DataGovAPITester()

    print("\n📊 Testing data.gov.in Commodity Price API Integration")
    print("📊 API Key: " + ("*" * (len(tester.api_key) - 4)) +
          tester.api_key[-4:])

    success = tester.run_all_tests()

    if success:
        print("\n✨ Integration is working correctly!")
        print("✨ You can now use real commodity prices in MandiGPT!")
    else:
        print("\n⚠️  Some tests failed. Check the data.gov.in API key and connectivity.")


if __name__ == "__main__":
    main()
