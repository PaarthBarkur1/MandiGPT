#!/usr/bin/env python3
"""
Generate complete list of states, districts, and markets for webpage dropdowns
This creates the actual data structure your webpage needs
"""

import requests
from collections import defaultdict
import json

api_key = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

print("🔍 Fetching all API data for dropdown options...")

# Fetch ALL records (not limited)
all_records = []
offset = 0

try:
    # First request to get total count
    r = requests.get(url, params={
        'api-key': api_key,
        'format': 'json',
        'limit': 1
    })
    data = r.json()
    total_records = data.get('count', 0)
    print(f"📊 Total records in API: {total_records}\n")

    # Now fetch all in batches
    print("📥 Downloading all records (this will take a moment)...")
    for offset in range(0, min(total_records, 10000), 1000):
        print(f"  Fetching records {offset} to {offset + 1000}...")
        r = requests.get(url, params={
            'api-key': api_key,
            'format': 'json',
            'limit': 1000,
            'offset': offset
        })
        records = r.json().get('records', [])
        all_records.extend(records)
        if not records:
            break

    print(f"✅ Downloaded {len(all_records)} total records\n")

    # Organize data
    states = defaultdict(set)
    districts = defaultdict(set)
    markets = defaultdict(set)
    commodities = set()
    varieties = defaultdict(set)
    grades = set()

    print("🔍 Processing data structure...")
    for record in all_records:
        state = record.get('state', '').strip()
        district = record.get('district', '').strip()
        market = record.get('market', '').strip()
        commodity = record.get('commodity', '').strip()
        variety = record.get('variety', '').strip()
        grade = record.get('grade', '').strip()

        if state:
            states[state].add(state)
            if district:
                districts[state].add(district)
            if market:
                markets[state].add(market)

        if commodity:
            commodities.add(commodity)
            if variety:
                varieties[commodity].add(variety)

        if grade:
            grades.add(grade)

    # Create structured output
    dropdown_data = {
        "states": sorted(list(states.keys())),
        "districts_by_state": {state: sorted(list(districts[state])) for state in states},
        "markets_by_state": {state: sorted(list(markets[state])) for state in states},
        "all_commodities": sorted(list(commodities)),
        "varieties_by_commodity": {comm: sorted(list(varieties[comm])) for comm in commodities},
        "all_grades": sorted(list(grades))
    }

    # Print formatted output for webpage
    print("\n" + "=" * 100)
    print("📱 WEBPAGE DROPDOWN DATA")
    print("=" * 100)

    print(f"\n✅ STATES ({len(dropdown_data['states'])} total)")
    print("=" * 100)
    for i, state in enumerate(dropdown_data['states'], 1):
        num_districts = len(dropdown_data['districts_by_state'].get(state, []))
        num_markets = len(dropdown_data['markets_by_state'].get(state, []))
        print(
            f"{i:2}. {state:<30} | {num_districts:2} districts | {num_markets:3} markets")

    print(f"\n✅ COMMODITIES ({len(dropdown_data['all_commodities'])} total)")
    print("=" * 100)
    for i, comm in enumerate(dropdown_data['all_commodities'], 1):
        num_varieties = len(
            dropdown_data['varieties_by_commodity'].get(comm, []))
        print(f"{i:3}. {comm:<40} | {num_varieties} varieties")

    print(f"\n✅ GRADES ({len(dropdown_data['all_grades'])} total)")
    print("=" * 100)
    for i, grade in enumerate(dropdown_data['all_grades'], 1):
        print(f"{i}. {grade}")

    # Save as JSON for webpage use
    print("\n\n" + "=" * 100)
    print("💾 SAVING DROPDOWN DATA AS JSON")
    print("=" * 100)

    with open('dropdown_data.json', 'w') as f:
        json.dump(dropdown_data, f, indent=2)

    print("✅ Saved to: dropdown_data.json")

    # Print HTML dropdown examples
    print("\n\n" + "=" * 100)
    print("🌐 HTML DROPDOWN EXAMPLES FOR WEBPAGE")
    print("=" * 100)

    print("\n<!-- STATE DROPDOWN -->\n")
    print('<select id="state" name="state" onchange="updateDistricts(this.value)">')
    print('  <option value="">Select State...</option>')
    for state in dropdown_data['states'][:5]:  # Show first 5 as example
        print(f'  <option value="{state}">{state}</option>')
    print('  <!-- ... more states ... -->')
    print('</select>')

    print("\n<!-- COMMODITY DROPDOWN (SEARCHABLE) -->\n")
    print('<select id="commodity" name="commodity">')
    print('  <option value="">Select Commodity...</option>')
    for comm in dropdown_data['all_commodities'][:10]:  # Show first 10 as example
        print(f'  <option value="{comm}">{comm}</option>')
    print('  <!-- ... more commodities ... -->')
    print('</select>')

    print("\n<!-- GRADE DROPDOWN -->\n")
    print('<select id="grade" name="grade">')
    print('  <option value="">Select Grade...</option>')
    for grade in dropdown_data['all_grades']:
        print(f'  <option value="{grade}">{grade}</option>')
    print('</select>')

    # Create summary data file
    print("\n\n" + "=" * 100)
    print("📊 CREATING SUMMARY FILE FOR FRONTEND DEVELOPERS")
    print("=" * 100)

    summary = f"""
# Webpage Dropdown Options Summary

## STATES (Dropdown 1)
Total: {len(dropdown_data['states'])} states
Options: {', '.join(dropdown_data['states'][:5])} + {len(dropdown_data['states']) - 5} more

## DISTRICTS (Dropdown 2 - Dynamic based on State)
Total: {sum(len(v) for v in dropdown_data['districts_by_state'].values())} unique districts
Example (Maharashtra): {', '.join(dropdown_data['districts_by_state'].get(dropdown_data['states'][0], [])[:3])} ...

## MARKETS (Dropdown 3 - Dynamic based on District)
Total: {sum(len(v) for v in dropdown_data['markets_by_state'].values())} unique markets
Example (Gujarat): {', '.join(dropdown_data['markets_by_state'].get(dropdown_data['states'][-1], [])[:3])} ...

## COMMODITIES (Dropdown 4 - Searchable)
Total: {len(dropdown_data['all_commodities'])} commodities
Options: {', '.join(dropdown_data['all_commodities'][:10])} + {len(dropdown_data['all_commodities']) - 10} more

## VARIETIES (Dropdown 5 - Dynamic based on Commodity)
Total: {sum(len(v) for v in dropdown_data['varieties_by_commodity'].values())} unique varieties
Examples:
"""

    for comm in list(dropdown_data['all_commodities'])[:5]:
        vars_list = dropdown_data['varieties_by_commodity'].get(comm, [])
        if vars_list:
            summary += f"\n  - {comm}: {', '.join(vars_list[:3])}"

    summary += f"""

## GRADES (Dropdown 6)
Total: {len(dropdown_data['all_grades'])} grades
Options: {', '.join(dropdown_data['all_grades'])}

## SOIL TYPES (Static - From your database)
- Black Soil (Best for: Cotton, Sugarcane, Chickpea)
- Red Soil (Best for: Groundnut, Millets, Pulses)
- Loamy Soil (Best for: Rice, Vegetables, Wheat)
- Clayey Soil (Best for: Rice, Wheat, Cotton)
- Sandy Soil (Best for: Groundnut, Watermelon, Sugarcane)
- Alluvial Soil (Best for: Rice, Wheat, Sugar Cane)

## SEASONS (Static - Calendar based)
- Kharif (Jun-Oct): Rice, Cotton, Groundnut, Sugarcane
- Rabi (Oct-Mar): Wheat, Gram, Mustard, Linseed
- Summer (Mar-Jun): Vegetables, Watermelon, Melons

## IMPLEMENTATION CHECKLIST FOR DEVELOPERS

- [ ] Create State dropdown (static list, {len(dropdown_data['states'])} options)
- [ ] Create District dropdown (dynamic, loaded from dropdown_data.json)
- [ ] Create Market dropdown (dynamic, loaded from dropdown_data.json)
- [ ] Create Commodity dropdown (dynamic, searchable)
- [ ] Create Variety dropdown (dynamic, based on selected commodity)
- [ ] Create Grade dropdown (static, {len(dropdown_data['all_grades'])} options)
- [ ] Create Soil Type dropdown (static, 6 options)
- [ ] Create Season dropdown (static, 3 options)
- [ ] Connect to API for price fetching
- [ ] Implement recommendation engine logic
- [ ] Add price comparison display
- [ ] Add market trend visualization
"""

    with open('DROPDOWN_OPTIONS_SUMMARY.md', 'w') as f:
        f.write(summary)

    print("✅ Saved to: DROPDOWN_OPTIONS_SUMMARY.md")

    print("\n\n" + "=" * 100)
    print("✨ COMPLETE - Data ready for frontend implementation")
    print("=" * 100)

except Exception as e:
    print(f"❌ Error: {e}")
