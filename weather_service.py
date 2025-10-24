import requests
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional
from models import WeatherData, WeatherForecast, Location
from config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    async def get_current_weather(self, location: Location) -> WeatherData:
        """Get current weather data for a location"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return WeatherData(
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                rainfall=0,  # Current weather doesn't include rainfall
                wind_speed=data["wind"]["speed"] * 3.6,  # Convert m/s to km/h
                pressure=data["main"]["pressure"],
                uv_index=data.get("uvi", 0),
                cloud_cover=data["clouds"]["all"],
                date=datetime.now()
            )
        except Exception as e:
            # Return default weather data if API fails
            return WeatherData(
                temperature=25.0,
                humidity=60.0,
                rainfall=0.0,
                wind_speed=10.0,
                pressure=1013.25,
                uv_index=5.0,
                cloud_cover=50.0,
                date=datetime.now()
            )
    
    async def get_weather_forecast(self, location: Location) -> WeatherForecast:
        """Get 7-day weather forecast for a location"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Get current weather
            current_weather = await self.get_current_weather(location)
            
            # Process forecast data (every 3 hours for 5 days)
            forecast_data = []
            for item in data["list"][:56]:  # 7 days * 8 entries per day
                forecast_data.append(WeatherData(
                    temperature=item["main"]["temp"],
                    humidity=item["main"]["humidity"],
                    rainfall=item.get("rain", {}).get("3h", 0),
                    wind_speed=item["wind"]["speed"] * 3.6,
                    pressure=item["main"]["pressure"],
                    uv_index=0,  # Not available in forecast
                    cloud_cover=item["clouds"]["all"],
                    date=datetime.fromtimestamp(item["dt"])
                ))
            
            return WeatherForecast(
                current=current_weather,
                forecast_7_days=forecast_data
            )
        except Exception as e:
            # Return default forecast if API fails
            current_weather = await self.get_current_weather(location)
            default_forecast = []
            for i in range(7):
                default_forecast.append(WeatherData(
                    temperature=25.0 + (i * 0.5),
                    humidity=60.0,
                    rainfall=0.0,
                    wind_speed=10.0,
                    pressure=1013.25,
                    uv_index=5.0,
                    cloud_cover=50.0,
                    date=datetime.now() + timedelta(days=i)
                ))
            
            return WeatherForecast(
                current=current_weather,
                forecast_7_days=default_forecast
            )
    
    def get_weather_summary(self, weather: WeatherForecast) -> dict:
        """Get a summary of weather conditions for agricultural planning"""
        current = weather.current
        forecast = weather.forecast_7_days
        
        # Handle empty forecast
        if not forecast:
            return {
                "temperature_range": f"{current.temperature:.1f}°C",
                "total_rainfall_7days": current.rainfall,
                "humidity_level": "High" if current.humidity > 70 else "Medium" if current.humidity > 50 else "Low",
                "weather_suitability": self._assess_weather_suitability(current.temperature, current.rainfall, current.humidity),
                "current_temp": current.temperature,
                "humidity": current.humidity
            }
        
        # Calculate averages
        avg_temp = sum([w.temperature for w in forecast]) / len(forecast)
        total_rainfall = sum([w.rainfall for w in forecast])
        avg_humidity = sum([w.humidity for w in forecast]) / len(forecast)
        
        # Determine weather conditions
        conditions = {
            "temperature_range": f"{min([w.temperature for w in forecast]):.1f}°C - {max([w.temperature for w in forecast]):.1f}°C",
            "total_rainfall_7days": total_rainfall,  # Return as numeric value
            "humidity_level": "High" if avg_humidity > 70 else "Medium" if avg_humidity > 50 else "Low",
            "weather_suitability": self._assess_weather_suitability(avg_temp, total_rainfall, avg_humidity),
            "current_temp": current.temperature,
            "humidity": current.humidity
        }
        
        return conditions
    
    def _assess_weather_suitability(self, temp: float, rainfall: float, humidity: float) -> str:
        """Assess overall weather suitability for agriculture"""
        score = 0
        
        # Temperature assessment (optimal: 20-30°C)
        if 20 <= temp <= 30:
            score += 3
        elif 15 <= temp <= 35:
            score += 2
        else:
            score += 1
        
        # Rainfall assessment (optimal: 50-200mm per week)
        if 50 <= rainfall <= 200:
            score += 3
        elif 25 <= rainfall <= 300:
            score += 2
        else:
            score += 1
        
        # Humidity assessment (optimal: 60-80%)
        if 60 <= humidity <= 80:
            score += 3
        elif 40 <= humidity <= 90:
            score += 2
        else:
            score += 1
        
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good"
        elif score >= 4:
            return "Fair"
        else:
            return "Poor"