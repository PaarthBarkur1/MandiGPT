"""
Example configuration for MandiGPT
Copy this file to config.py and update with your API keys
"""

# Weather API Configuration
OPENWEATHER_API_KEY = "your_openweather_api_key_here"

# Commodity Price API Configuration (Optional)
COMMODITY_API_KEY = "your_commodity_api_key_here"

# Application Configuration
DEBUG = True
HOST = "0.0.0.0"
PORT = 8000

# Indian States for dropdown
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya",
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal"
]

# Major Indian Crops
MAJOR_CROPS = [
    "Rice", "Wheat", "Maize", "Sugarcane", "Cotton", "Jute", "Tea", "Coffee",
    "Soybean", "Groundnut", "Sunflower", "Mustard", "Chickpea", "Pigeon Pea",
    "Black Gram", "Green Gram", "Lentil", "Potato", "Onion", "Tomato",
    "Brinjal", "Cabbage", "Cauliflower", "Okra", "Cucumber", "Bottle Gourd",
    "Bitter Gourd", "Ridge Gourd", "Spinach", "Coriander", "Mint", "Basil"
]
