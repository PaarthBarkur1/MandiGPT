#!/usr/bin/env python3
"""
Diagnose the data.gov.in API response structure
"""

import requests
import json

api_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

params = {
    'api-key': api_key,
    'format': 'json',
    'limit': 2
}

print("Making request...")
response = requests.get(url, params=params, timeout=15)

print(f"Status Code: {response.status_code}")
print(f"\nResponse Keys: {list(response.json().keys())}")

data = response.json()

print(f"\n--- Response Structure ---")
print(f"Keys: {list(data.keys())}")

# Check for success flag
if 'success' in data:
    print(f"\nsuccess key: {data['success']}")
else:
    print(f"\nNo 'success' key found")

# Check for records
if 'records' in data:
    print(f"\nRecords found: {len(data['records'])}")
    if len(data['records']) > 0:
        print("\nFirst record structure:")
        print(json.dumps(data['records'][0], indent=2))
else:
    print(f"\nNo 'records' key found")

# Show all top-level keys and their types
print("\n--- Top Level Keys and Types ---")
for key, value in data.items():
    if key != 'records':
        print(f"{key}: {type(value).__name__} = {str(value)[:100]}")
    else:
        print(f"{key}: {type(value).__name__} (array with {len(value)} items)")
