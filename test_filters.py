#!/usr/bin/env python3
"""Test the API filtering"""

import requests

api_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

# Test 1: Filter by commodity
print("Test 1: Filter by Cotton")
params = {
    'api-key': api_key,
    'format': 'json',
    'limit': 10,
    'filters[commodity_name]': 'Cotton',
    'filters[state]': 'Gujarat'
}
r = requests.get(url, params=params)
print(f"Status: {r.json().get('status')}")
print(f"Records: {len(r.json().get('records', []))}")
if r.json().get('records'):
    print(f"First record: {r.json()['records'][0]}")

# Test 2: Try without filters
print("\n\nTest 2: Get first cotton record from all data")
r = requests.get(url, params={'api-key': api_key,
                 'format': 'json', 'limit': 1000})
records = r.json().get('records', [])
cotton_records = [x for x in records if x.get('commodity') == 'Cotton']
print(f"Cotton records found: {len(cotton_records)}")
if cotton_records:
    print(f"First cotton: {cotton_records[0]}")

# Test 3: Check available states
print("\n\nTest 3: Available states")
states = set(x.get('state') for x in records[:100])
print(f"States: {sorted(list(states))}")
