# MandiGPT - AI Crop Recommendation Tool for Indian Farmers

## 🌾 Overview

MandiGPT is an advanced AI-powered agricultural advisory tool specifically designed for Indian farmers. It provides personalized crop recommendations using **local LLM integration** and **free commodity price APIs**. The tool helps farmers minimize losses and maximize profits through data-driven insights powered by artificial intelligence.

## ✨ Key Features

### 🤖 **AI-Powered Recommendations**
- **Local LLM Integration**: Uses Ollama for AI-powered crop recommendations
- **Intelligent Analysis**: Advanced algorithms analyze weather, market, and soil conditions
- **Natural Language Processing**: AI generates human-readable agricultural advice

### 💰 **Free Commodity Price Integration**
- **Real-time Prices**: Live commodity prices from Agmarknet (Government API)
- **Market Analysis**: Comprehensive market sentiment and trend analysis
- **Price Trends**: Historical price data and future predictions
- **Regional Pricing**: Location-specific market prices across India

### 🌤️ **Weather Intelligence**
- **Current Conditions**: Real-time weather data integration
- **7-Day Forecast**: Extended weather predictions for planning
- **Agricultural Suitability**: Weather-based crop suitability analysis

### 📊 **Comprehensive Recommendations**
- **Confidence Scoring**: AI confidence levels for each recommendation (0-100%)
- **Risk Assessment**: Multi-factor risk analysis (weather, market, financial)
- **Profit Estimation**: Expected yield and profit calculations
- **Planting Schedules**: Optimal planting and harvesting times

### 🗺️ **Location-Specific Intelligence**
- **Indian States Coverage**: All 28 Indian states supported
- **District-Level Analysis**: Granular location-based recommendations
- **Soil Type Integration**: Soil-specific crop suitability
- **Regional Crop Database**: Comprehensive Indian agricultural database

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.13 recommended)
- **Ollama** (for local LLM features - optional)
- **Internet connection** (for real-time data)

### Installation

#### 1. **Clone and Setup**
```bash
git clone <repository-url>
cd mandigpt

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. **Environment Configuration**
```bash
# Create .env file (optional - app works without it)
OPENWEATHER_API_KEY=your_openweather_api_key_here
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

#### 3. **Ollama Setup (Optional - for AI features)**

**Windows:**
```bash
# Download Ollama from: https://ollama.ai/download
# Install Ollama, then run:
ollama serve

# In another terminal:
ollama pull llama3.2
```

**Linux/Mac:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Download recommended model
ollama pull llama3.2
```

**Automated Setup:**
```bash
# Run the automated setup script
python setup_ollama.py
```

#### 4. **Run the Application**
```bash
# Start the application
python run.py

# Or run directly
python main.py
```

## 🌐 Usage

### **Web Interface**
1. Open your browser and go to: `http://localhost:8000`
2. Fill in farmer details:
   - Location (State, District)
   - Land size (hectares)
   - Budget (₹)
   - Risk tolerance
   - Preferred crops
3. Get AI-powered recommendations instantly!

### **API Endpoints**

#### **Health Check**
```bash
curl http://localhost:8000/health
```

#### **LLM Status**
```bash
curl http://localhost:8000/api/llm-status
```

#### **Commodity Prices**
```bash
curl "http://localhost:8000/api/commodity-prices?state=Maharashtra&district=Pune&lat=18.5204&lon=73.8567&crops=Rice,Wheat,Maize"
```

#### **Weather Data**
```bash
curl "http://localhost:8000/api/weather/Maharashtra/Pune?lat=18.5204&lon=73.8567"
```

#### **Crop Recommendations**
```bash
curl -X POST "http://localhost:8000/api/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "location": {
      "state": "Maharashtra",
      "district": "Pune",
      "latitude": 18.5204,
      "longitude": 73.8567,
      "soil_type": "Black"
    },
    "budget": 50000,
    "land_size": 2.5,
    "risk_tolerance": "Medium",
    "preferred_crops": ["Rice", "Wheat", "Maize"]
  }'
```

## 🧪 Testing

### **Run Test Suite**
```bash
# Basic functionality test
python quick_test.py

# Comprehensive API test
python simple_final_test.py

# Original test suite (may have Unicode issues on Windows)
python test_mandigpt.py
```

### **Expected Test Results**
```
MandiGPT Comprehensive Test
==================================================
1. Testing Health Check...     PASS
2. Testing LLM Status...       PASS  
3. Testing Commodity Prices... PASS
4. Testing Weather Data...     PASS
5. Testing Crop Recommendations... PASS
6. Testing Price Trends...     PASS
==================================================

All core features are working!
MandiGPT is ready for use!
```

## 📊 API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with:
- **Swagger UI**: Interactive API testing
- **Request/Response Examples**: Complete API examples
- **Schema Definitions**: Data model documentation

## 🔧 Configuration

### **Environment Variables**
```bash
# Optional - app works without these
OPENWEATHER_API_KEY=your_key_here    # For real weather data
DEBUG=True                            # Development mode
HOST=0.0.0.0                         # Server host
PORT=8000                            # Server port
```

### **LLM Configuration**
- **Default Model**: `llama3.2`
- **Service URL**: `http://localhost:11434`
- **Fallback**: Rule-based recommendations when LLM unavailable

### **Commodity Price Sources**
- **Primary**: Agmarknet (Government of India API)
- **Fallback**: Realistic mock data with 12+ major Indian crops
- **Coverage**: Rice, Wheat, Maize, Sugarcane, Cotton, Soybean, etc.

## 🏗️ Architecture

### **Core Components**

```
MandiGPT/
├── main.py                    # FastAPI application
├── run.py                     # Application launcher
├── models.py                  # Data models
├── config.py                  # Configuration
├── recommendation_engine.py    # AI recommendation engine
├── llm_service.py            # Local LLM integration
├── free_commodity_service.py  # Free commodity price API
├── weather_service.py         # Weather data service
├── commodity_service.py       # Legacy commodity service
├── agricultural_database.py   # Indian agricultural database
├── templates/
│   └── index.html            # Web interface
├── requirements.txt           # Dependencies
├── setup_ollama.py           # Ollama setup script
└── test_*.py                 # Test scripts
```

### **Data Flow**
1. **Farmer Input** → Location, budget, preferences
2. **Weather Service** → Current and forecasted conditions
3. **Commodity Service** → Real-time market prices
4. **LLM Service** → AI-powered analysis
5. **Recommendation Engine** → Combined intelligence
6. **Response** → Personalized recommendations

## 🎯 Features in Detail

### **AI-Powered Recommendations**
- **Local LLM**: Uses Ollama for privacy and offline capability
- **Intelligent Analysis**: Considers multiple factors simultaneously
- **Natural Language**: Human-readable agricultural advice
- **Confidence Scoring**: AI confidence levels for each recommendation

### **Free Commodity Prices**
- **Government API**: Agmarknet integration for official prices
- **Real-time Data**: Live market prices across India
- **Market Analysis**: Bullish/bearish sentiment analysis
- **Price Trends**: Historical and predictive pricing

### **Weather Intelligence**
- **Current Conditions**: Real-time weather data
- **Agricultural Suitability**: Weather-based crop recommendations
- **Risk Assessment**: Weather-related risk evaluation
- **Forecasting**: 7-day weather predictions

### **Comprehensive Analysis**
- **Multi-factor Scoring**: Weather, market, soil, and financial factors
- **Risk Assessment**: Weather, market, pest, and financial risks
- **Profit Estimation**: Expected yield and profit calculations
- **Implementation Guidance**: Step-by-step farming advice

## 🚨 Troubleshooting

### **Common Issues**

#### **Pandas Installation Issues (Python 3.13)**
```bash
# Solution: Use compatible versions
pip install --only-binary=all -r requirements.txt
```

#### **Ollama Not Found**
```bash
# Windows: Download from https://ollama.ai/download
# Linux/Mac: curl -fsSL https://ollama.ai/install.sh | sh
# Then: ollama serve
```

#### **Unicode Display Issues (Windows)**
```bash
# Use simple test scripts without Unicode characters
python simple_final_test.py
```

#### **API Connection Issues**
- Check if application is running on `http://localhost:8000`
- Verify virtual environment is activated
- Ensure all dependencies are installed

### **Fallback Systems**
- **No LLM**: Uses rule-based recommendations
- **No Weather API**: Uses realistic mock weather data
- **No Commodity API**: Uses comprehensive mock price data
- **No Internet**: Works with cached/mock data

## 📈 Performance

### **Response Times**
- **Health Check**: < 100ms
- **Commodity Prices**: < 500ms
- **Weather Data**: < 1s
- **Crop Recommendations**: < 3s (with LLM), < 1s (without LLM)

### **Resource Usage**
- **Memory**: ~200MB base, +500MB with Ollama
- **CPU**: Minimal without LLM, moderate with LLM
- **Storage**: ~100MB application, +2GB with Ollama models

## 🔒 Security & Privacy

### **Local Processing**
- **No External AI**: All AI processing happens locally
- **Data Privacy**: No farmer data sent to external services
- **Offline Capability**: Works without internet (with cached data)

### **API Security**
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Graceful error handling and fallbacks
- **Rate Limiting**: Built-in request rate limiting

## 🤝 Contributing

### **Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd mandigpt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt

# Run tests
python simple_final_test.py
```

### **Adding New Features**
1. **New Crop Data**: Update `agricultural_database.py`
2. **New API Endpoints**: Add to `main.py`
3. **New Services**: Create service files following existing patterns
4. **Testing**: Add tests to test suite

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Agmarknet**: For providing free commodity price APIs
- **Ollama**: For local LLM capabilities
- **FastAPI**: For the excellent web framework
- **Indian Agricultural Research**: For crop and regional data

## 📞 Support

### **Getting Help**
1. **Check Documentation**: Visit `http://localhost:8000/docs`
2. **Run Tests**: Use provided test scripts
3. **Check Logs**: Application logs in console
4. **Health Check**: Visit `http://localhost:8000/health`

### **Common Commands**
```bash
# Start application
python run.py

# Test functionality
python simple_final_test.py

# Check LLM status
curl http://localhost:8000/api/llm-status

# Setup Ollama (if needed)
python setup_ollama.py
```

---

**MandiGPT** - Empowering Indian farmers with AI-driven agricultural intelligence! 🌾🤖