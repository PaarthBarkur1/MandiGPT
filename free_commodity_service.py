import httpx
import asyncio
import json
import logging
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from models import CommodityPrice, Location
from config import Config

logger = logging.getLogger(__name__)


class FreeCommodityService:
    """Free commodity price service using public APIs and web scraping"""

    def __init__(self):
        # Indian commodity price sources (free APIs)
        self.price_sources = {
            "agmarknet": "https://agmarknet.gov.in/api/price/commodity/",
            "mandi": "https://api.agmarknet.gov.in/api/price/commodity/",
            "krishijagran": "https://www.krishijagran.com/api/commodity-prices",
            "datagov": "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        }

        # Data.gov.in API Key
        self.datagov_api_key = Config.COMMODITY_API_KEY or "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

        # Crop name mapping from frontend to backend names (for normalization only)
        self.crop_name_mapping = {
            "Chillies": "Red Chilli",
            "Chilli": "Red Chilli",
            "Red Chilli": "Red Chilli",
            "Rice": "Rice",
            "Wheat": "Wheat",
            "Maize": "Maize",
            "Cotton": "Cotton",
            "Sugarcane": "Sugarcane",
            "Tomato": "Tomato",
            "Onion": "Onion",
            "Potato": "Potato",
            "Groundnut": "Groundnut",
            "Turmeric": "Turmeric",
            "Cabbage": "Cabbage",
            "Cauliflower": "Cauliflower",
            "Carrot": "Carrot",
            "Cucumber": "Cucumber",
        }

    def _normalize_crop_name(self, crop_name: str) -> str:
        """Normalize crop name for API matching"""
        crop_name = crop_name.strip()
        # Check direct mapping first
        if crop_name in self.crop_name_mapping:
            return self.crop_name_mapping[crop_name]
        # Return normalized version (capitalize first letter)
        return crop_name.title() if crop_name else crop_name

    async def get_commodity_prices(self, location: Location, commodities: List[str] = None) -> List[CommodityPrice]:
        """Get commodity prices from free sources - NO MOCK DATA"""

        prices = []

        try:
            # If no commodities specified, use common Indian crops
            if commodities is None or not commodities:
                logger.info(
                    "No commodities specified, fetching prices for common Indian crops")
                commodities = ["Rice", "Wheat", "Maize",
                               "Potato", "Onion", "Tomato"]

            # Normalize commodity names
            valid_commodities = []
            seen_commodities = set()

            for c in commodities:
                if c and c.strip():
                    normalized = self._normalize_crop_name(c)
                    if normalized not in seen_commodities:
                        valid_commodities.append(normalized)
                        seen_commodities.add(normalized)

            if not valid_commodities:
                logger.warning("No valid commodities after normalization")
                return []

            logger.info(
                f"Fetching real prices for commodities: {valid_commodities} in {location.state}, {location.district}")

            for commodity in valid_commodities:
                try:
                    logger.info(
                        f"Attempting to fetch price for {commodity}...")
                    real_price = await self._fetch_real_price(commodity, location)
                    if real_price:
                        logger.info(
                            f"✅ Successfully fetched price for {commodity}: ₹{real_price.current_price}/quintal")
                        prices.append(real_price)
                    else:
                        logger.warning(
                            f"❌ No price data found for {commodity} in {location.state}")
                except Exception as e:
                    logger.error(
                        f"Error fetching price for {commodity}: {e}", exc_info=True)
                    # Continue to next commodity - NO MOCK FALLBACK

            logger.info(
                f"Total prices fetched: {len(prices)} out of {len(valid_commodities)} requested")
            return prices

        except Exception as e:
            logger.error(
                f"Critical error in get_commodity_prices: {e}", exc_info=True)
            return []

    async def _fetch_real_price(self, commodity: str, location: Location) -> Optional[CommodityPrice]:
        """Try to fetch real commodity prices from free sources"""

        try:
            # Try data.gov.in API first (most reliable)
            datagov_price = await self._fetch_datagov_price(commodity, location)
            if datagov_price:
                return datagov_price

            # Try Agmarknet API (Government of India)
            agmarknet_price = await self._fetch_agmarknet_price(commodity, location)
            if agmarknet_price:
                return agmarknet_price

            # Try other free sources
            other_price = await self._fetch_other_sources(commodity, location)
            if other_price:
                return other_price

        except Exception as e:
            logger.error(f"Error fetching real price for {commodity}: {e}")

        return None

    async def _fetch_agmarknet_price(self, commodity: str, location: Location) -> Optional[CommodityPrice]:
        """Fetch price from Agmarknet (Government API) - with diagnostics"""

        try:
            # Agmarknet commodity codes mapping
            commodity_codes = {
                "Rice": "1101",
                "Wheat": "1102",
                "Maize": "1103",
                "Sugarcane": "1104",
                "Cotton": "1105",
                "Soybean": "1106",
                "Groundnut": "1107",
                "Potato": "1108",
                "Onion": "1109",
                "Tomato": "1110"
            }

            commodity_code = commodity_codes.get(commodity)
            if not commodity_code:
                logger.debug(f"Agmarknet: No commodity code for {commodity}")
                return None

            logger.debug(
                f"Trying Agmarknet API for {commodity} (code: {commodity_code})")
            url = f"https://agmarknet.gov.in/api/price/commodity/{commodity_code}"

            async with httpx.AsyncClient(timeout=10.0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}) as client:
                response = await client.get(url)

                if response.status_code == 200:
                    # Check if response is JSON or HTML
                    content_type = response.headers.get(
                        'content-type', '').lower()
                    if 'application/json' not in content_type:
                        logger.debug(
                            f"Agmarknet returned HTML instead of JSON (status 200 but content-type: {content_type})")
                        logger.debug(
                            f"Response preview: {response.text[:200]}")
                        return None

                    try:
                        data = response.json()
                    except Exception as e:
                        logger.debug(
                            f"Agmarknet response is not valid JSON: {e}")
                        logger.debug(
                            f"Response preview: {response.text[:200]}")
                        return None

                    logger.debug(
                        f"Agmarknet response structure: {list(data.keys())}")
                    prices = data.get('price', [])

                    if prices:
                        logger.info(
                            f"Agmarknet: Found {len(prices)} price records for {commodity}")
                        latest_price = prices[0]
                        price_val = latest_price.get('price', 0)

                        try:
                            price = float(str(price_val).replace(',', ''))
                            if price > 0:
                                return CommodityPrice(
                                    commodity_name=commodity,
                                    current_price=price,
                                    price_trend="stable",
                                    market_location=latest_price.get(
                                        'market', location.state),
                                    date=datetime.now()
                                )
                        except (ValueError, TypeError) as e:
                            logger.warning(
                                f"Agmarknet: Invalid price value for {commodity}: {price_val}")
                    else:
                        logger.debug(
                            f"Agmarknet: No price data in response for {commodity}")
                else:
                    logger.warning(
                        f"Agmarknet API returned status {response.status_code} for {commodity}")

        except httpx.HTTPStatusError as e:
            logger.warning(
                f"Agmarknet API HTTP error for {commodity}: {e.response.status_code}")
        except httpx.RequestError as e:
            logger.warning(f"Agmarknet API request error for {commodity}: {e}")
        except Exception as e:
            logger.error(
                f"Agmarknet API error for {commodity}: {e}", exc_info=True)

        return None

    async def _fetch_datagov_price(self, commodity: str, location: Location) -> Optional[CommodityPrice]:
        """Fetch price from data.gov.in API - with detailed diagnostics"""

        try:
            url = self.price_sources["datagov"]

            # Try to fetch multiple pages for better coverage
            all_records = []
            max_pages = 3  # Fetch up to 3 pages (3000 records)

            async with httpx.AsyncClient(timeout=15.0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}) as client:
                for page in range(max_pages):
                    params = {
                        'api-key': self.datagov_api_key,
                        'format': 'json',
                        'limit': 1000,  # Max per request
                        'offset': page * 1000
                    }

                    logger.debug(
                        f"Fetching page {page + 1} from data.gov.in: commodity={commodity}, state={location.state}")
                    try:
                        response = await client.get(url, params=params)
                        response.raise_for_status()

                        data = response.json()

                        if data.get('status') == 'ok' and data.get('records'):
                            page_records = data['records']
                            all_records.extend(page_records)
                            logger.debug(
                                f"Page {page + 1}: Got {len(page_records)} records")

                            # If we got fewer than limit, we've reached the end
                            if len(page_records) < 1000:
                                break
                        else:
                            break
                    except (httpx.HTTPStatusError, httpx.RequestError) as e:
                        logger.debug(
                            f"data.gov.in API error on page {page + 1}: {e}")
                        break
                    except Exception as e:
                        logger.debug(
                            f"Unexpected error fetching data.gov.in page {page + 1}: {e}")
                        break

            records = all_records
            logger.info(
                f"Total records fetched from data.gov.in: {len(records)}")

            if records:
                # More flexible matching with better commodity name handling
                matching_records = []
                commodity_lower = commodity.lower()
                state_lower = location.state.lower()

                # Create commodity search terms (e.g., "Rice" -> ["rice", "paddy"])
                commodity_search_terms = [commodity_lower]
                commodity_variations = {
                    "rice": ["paddy", "rice", "basmati"],
                    "wheat": ["wheat", "gehun"],
                    "maize": ["maize", "corn", "makka"],
                    "potato": ["potato", "aloo"],
                    "onion": ["onion", "pyaz"],
                    "tomato": ["tomato", "tamatar"],
                    "chilli": ["chilli", "chili", "chillies", "mirch"],
                    "cotton": ["cotton", "kapas"],
                    "sugarcane": ["sugarcane", "ganna"],
                }

                # Add variations if available
                for key, variations in commodity_variations.items():
                    if key in commodity_lower:
                        commodity_search_terms.extend(variations)
                        break

                logger.debug(
                    f"Searching for commodity '{commodity}' using terms: {commodity_search_terms}")

                # First try: match commodity and state
                for r in records:
                    record_commodity = r.get('commodity', '').strip().lower()
                    record_state = r.get('state', '').strip().lower()

                    # Check if any search term matches
                    commodity_match = any(term in record_commodity or record_commodity in term
                                          for term in commodity_search_terms)
                    state_match = state_lower in record_state or record_state in state_lower

                    if commodity_match and state_match:
                        matching_records.append(r)

                logger.info(
                    f"Found {len(matching_records)} matching records for {commodity} in {location.state}")

                # If no matches with state, try just commodity match
                if not matching_records:
                    logger.debug(
                        f"No state-specific matches, trying commodity-only match...")
                    for r in records:
                        record_commodity = r.get(
                            'commodity', '').strip().lower()
                        commodity_match = any(term in record_commodity or record_commodity in term
                                              for term in commodity_search_terms)
                        if commodity_match:
                            matching_records.append(r)
                            if len(matching_records) >= 10:  # Get more records
                                break

                    if matching_records:
                        logger.info(
                            f"Found {len(matching_records)} records for {commodity} (any state)")

                # If still no matches, log available commodities for debugging
                if not matching_records:
                    available_commodities = sorted(set(r.get('commodity', '').strip()
                                                       for r in records if r.get('commodity')))[:20]
                    available_states = sorted(set(r.get('state', '').strip()
                                                  for r in records if r.get('state')))[:20]
                    logger.warning(
                        f"No matches found for '{commodity}' in '{location.state}'")
                    logger.warning(
                        f"Available commodities (sample): {available_commodities}")
                    logger.warning(
                        f"Available states (sample): {available_states}")

                if matching_records:
                    # Get the first record (most recent)
                    latest_record = matching_records[0]

                    # Extract price - try multiple fields
                    price = None
                    for price_field in ['modal_price', 'max_price', 'min_price', 'price']:
                        price_val = latest_record.get(price_field)
                        if price_val:
                            try:
                                price_str = str(
                                    price_val).strip().replace(',', '')
                                if price_str.replace('.', '', 1).replace('-', '', 1).isdigit():
                                    price = float(price_str)
                                    break
                            except (ValueError, AttributeError):
                                continue

                    if price and price > 0:
                        return CommodityPrice(
                            commodity_name=latest_record.get(
                                'commodity', commodity),
                            current_price=price,
                            price_trend="stable",
                            market_location=latest_record.get(
                                'market') or latest_record.get('district') or location.state,
                            date=datetime.now()
                        )
                    else:
                        logger.warning(
                            f"Price extraction failed for {commodity}. Record: {latest_record}")
            else:
                logger.warning(f"No records returned from data.gov.in API")

        except httpx.HTTPStatusError as e:
            logger.error(
                f"data.gov.in API HTTP error for {commodity}: {e.response.status_code} - {e.response.text[:200]}")
        except httpx.RequestError as e:
            logger.error(f"data.gov.in API request error for {commodity}: {e}")
        except (KeyError, ValueError, TypeError) as e:
            logger.error(
                f"Error parsing data.gov.in response for {commodity}: {e}", exc_info=True)

        return None

    async def _fetch_other_sources(self, commodity: str, location: Location) -> Optional[CommodityPrice]:
        """Fetch from other free sources"""

        try:
            # This would implement other free sources like:
            # - Web scraping from government websites
            # - RSS feeds from agricultural departments
            # - Public APIs from state agricultural boards

            # For now, return None to use mock data
            return None

        except Exception as e:
            logger.error(f"Other sources error for {commodity}: {e}")

        return None

    def _find_closest_market(self, location: Location, markets: List[str] = None) -> str:
        """Find the closest market to the given location"""

        state_market_mapping = {
            "Delhi": "Delhi",
            "Haryana": "Delhi",
            "Punjab": "Punjab",
            "UP": "UP",
            "Uttar Pradesh": "UP",
            "Maharashtra": "Mumbai",
            "Gujarat": "Gujarat",
            "Karnataka": "Karnataka",
            "Tamil Nadu": "Chennai",
            "West Bengal": "Kolkata",
            "Bihar": "Bihar",
            "Rajasthan": "Rajasthan",
            "Madhya Pradesh": "Madhya Pradesh",
            "Andhra Pradesh": "Andhra Pradesh",
            "Telangana": "Telangana",
            "Kerala": "Kerala",
            "Odisha": "Odisha",
            "Assam": "Assam"
        }

        return state_market_mapping.get(location.state, markets[0] if markets else location.state)

    async def get_price_trends(self, commodity: str, days: int = 30, location: Optional[Location] = None) -> Dict:
        """Get price trends for a commodity using real API data - NO MOCK DATA"""

        try:
            # Fetch historical data from API
            historical_data = await self._fetch_historical_prices(commodity, location, days)

            if not historical_data:
                return {
                    "commodity": commodity,
                    "error": "No historical price data available from API",
                    "source": "Real API (no data)"
                }

            # Calculate trend from real data
            prices = [h.get('price', 0)
                      for h in historical_data if h.get('price')]
            if len(prices) < 2:
                return {
                    "commodity": commodity,
                    "error": "Insufficient historical data for trend analysis",
                    "source": "Real API"
                }

            # Calculate trend using linear regression
            x = np.arange(len(prices))
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                x, prices)

            # Determine trend direction
            if slope > 0.1:
                trend = "increasing"
            elif slope < -0.1:
                trend = "decreasing"
            else:
                trend = "stable"

            return {
                "commodity": commodity,
                "trend": trend,
                "price_history": historical_data,
                "current_price": prices[-1] if prices else 0,
                "price_change": prices[-1] - prices[0] if len(prices) > 1 else 0,
                "trend_strength": round(abs(slope), 2),
                "correlation": round(r_value, 3),
                "source": "Real-time API Data"
            }
        except Exception as e:
            logger.error(f"Error fetching price trends for {commodity}: {e}")
            return {
                "commodity": commodity,
                "error": f"Failed to fetch trends: {str(e)}",
                "source": "Real API"
            }

    async def _fetch_historical_prices(self, commodity: str, location: Optional[Location], days: int) -> List[Dict]:
        """Fetch historical price data from API"""
        # This would fetch multiple days of data from the API
        # For now, return empty - would need API support for historical queries
        # In production, you'd query the API with date ranges
        return []

    def get_market_analysis(self, prices: List[CommodityPrice], historical_data: Optional[List[Dict]] = None) -> Dict:
        """Advanced market analysis using statistical methods - NO MOCK DATA"""
        try:
            from advanced_market_analysis import AdvancedMarketAnalyzer

            analyzer = AdvancedMarketAnalyzer()
            return analyzer.analyze_market(prices, historical_data)
        except ImportError as e:
            logger.error(f"Failed to import AdvancedMarketAnalyzer: {e}")
            # Return basic analysis if advanced analyzer fails
            return {
                "summary": {
                    "total_commodities": len(prices),
                    "data_source": "Basic Analysis",
                    "analysis_timestamp": datetime.now().isoformat(),
                    "error": "Advanced visualization not available"
                },
                "descriptive_statistics": {},
                "trend_analysis": {},
                "volatility_metrics": {},
                "visualizations": {}
            }
        except Exception as e:
            logger.error(f"Error in market analysis: {e}", exc_info=True)
            # Return basic analysis if advanced analyzer fails
            return {
                "summary": {
                    "total_commodities": len(prices),
                    "data_source": "Basic Analysis",
                    "analysis_timestamp": datetime.now().isoformat(),
                    "error": str(e)
                },
                "descriptive_statistics": {},
                "trend_analysis": {},
                "volatility_metrics": {},
                "visualizations": {}
            }
