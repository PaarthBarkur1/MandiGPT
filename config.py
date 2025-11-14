import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Weather API Configuration
    OPENWEATHER_API_KEY = os.getenv(
        "OPENWEATHER_API_KEY", "20ad0e93d90a0cdd3687bd8c87f12c73")

    # Commodity Price API Configuration
    COMMODITY_API_KEY = os.getenv(
        "COMMODITY_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")

    # Application Configuration
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    # Indian Agricultural Data
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
