#!/usr/bin/env python3
"""
MandiGPT - AI Crop Recommendation Tool
Startup script for the application
"""

import os
import sys
from pathlib import Path

# Fix Unicode encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import requests
        import pydantic
        import pandas
        import numpy
        import sklearn
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_environment():
    """Check environment variables"""
    required_vars = ['OPENWEATHER_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("The application will use mock data for missing services.")
        return False
    else:
        print("✅ Environment variables are set")
        return True

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directory structure created")

def main():
    """Main startup function"""
    print("🌾 MandiGPT - AI Crop Recommendation Tool")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    check_environment()
    
    # Create directories
    create_directories()
    
    print("\n🚀 Starting MandiGPT server...")
    print("📱 Web interface will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the application
    try:
        from main import app
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n👋 MandiGPT server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
