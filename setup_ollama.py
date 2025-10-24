#!/usr/bin/env python3
"""
Setup script for Ollama local LLM integration
This script helps install and configure Ollama for MandiGPT
"""

import subprocess
import sys
import platform
import requests
import json
import time

class OllamaSetup:
    def __init__(self):
        self.system = platform.system()
        self.ollama_url = "http://localhost:11434"
        
    def check_ollama_installed(self):
        """Check if Ollama is already installed"""
        try:
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def install_ollama(self):
        """Install Ollama based on the operating system"""
        print("Installing Ollama...")
        
        if self.system == "Windows":
            self._install_ollama_windows()
        elif self.system == "Darwin":  # macOS
            self._install_ollama_macos()
        elif self.system == "Linux":
            self._install_ollama_linux()
        else:
            print(f"Unsupported operating system: {self.system}")
            return False
        
        return True
    
    def _install_ollama_windows(self):
        """Install Ollama on Windows"""
        print("Installing Ollama on Windows...")
        print("Please download and install Ollama from: https://ollama.ai/download")
        print("After installation, restart your terminal and run this script again.")
        
        # Try to open the download page
        import webbrowser
        webbrowser.open("https://ollama.ai/download")
    
    def _install_ollama_macos(self):
        """Install Ollama on macOS"""
        print("Installing Ollama on macOS...")
        try:
            # Try using Homebrew
            subprocess.run(["brew", "install", "ollama"], check=True)
            print("Ollama installed successfully via Homebrew")
        except subprocess.CalledProcessError:
            print("Homebrew not found. Please install Ollama manually from: https://ollama.ai/download")
        except FileNotFoundError:
            print("Please install Ollama manually from: https://ollama.ai/download")
    
    def _install_ollama_linux(self):
        """Install Ollama on Linux"""
        print("Installing Ollama on Linux...")
        try:
            # Download and install Ollama
            subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh"
            ], check=True, stdout=subprocess.PIPE)
            
            # Execute the install script
            subprocess.run([
                "bash", "-c", "curl -fsSL https://ollama.ai/install.sh | sh"
            ], check=True)
            
            print("Ollama installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Ollama: {e}")
            print("Please install Ollama manually from: https://ollama.ai/download")
    
    def start_ollama_service(self):
        """Start the Ollama service"""
        print("Starting Ollama service...")
        try:
            if self.system == "Windows":
                subprocess.Popen(["ollama", "serve"], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(["ollama", "serve"])
            
            # Wait for service to start
            time.sleep(3)
            
            # Check if service is running
            if self.check_ollama_running():
                print("Ollama service started successfully")
                return True
            else:
                print("Failed to start Ollama service")
                return False
                
        except Exception as e:
            print(f"Error starting Ollama service: {e}")
            return False
    
    def check_ollama_running(self):
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def download_recommended_model(self):
        """Download a recommended model for agricultural recommendations"""
        print("Downloading recommended model (llama3.2)...")
        print("This may take several minutes depending on your internet connection...")
        
        try:
            # Download llama3.2 model (good balance of performance and size)
            process = subprocess.Popen(
                ["ollama", "pull", "llama3.2"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Show progress
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            if process.returncode == 0:
                print("Model downloaded successfully!")
                return True
            else:
                print("Failed to download model")
                return False
                
        except Exception as e:
            print(f"Error downloading model: {e}")
            return False
    
    def test_ollama_integration(self):
        """Test Ollama integration with a simple query"""
        print("Testing Ollama integration...")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3.2",
                    "prompt": "Hello, can you help with agricultural advice?",
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Ollama integration test successful!")
                print(f"Response: {result.get('response', 'No response')[:100]}...")
                return True
            else:
                print(f"❌ Ollama integration test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Ollama integration test failed: {e}")
            return False
    
    def setup_complete(self):
        """Complete setup process"""
        print("\n🎉 Ollama setup complete!")
        print("\nNext steps:")
        print("1. Run 'python run.py' to start MandiGPT")
        print("2. The application will now use local LLM for recommendations")
        print("3. If Ollama is not available, the app will use fallback recommendations")
        print("\nNote: Ollama service must be running for AI features to work.")
        print("To start Ollama service manually, run: ollama serve")

def main():
    """Main setup function"""
    print("🤖 MandiGPT Ollama Setup")
    print("=" * 40)
    
    setup = OllamaSetup()
    
    # Check if Ollama is already installed
    if setup.check_ollama_installed():
        print("✅ Ollama is already installed")
    else:
        print("❌ Ollama not found")
        if not setup.install_ollama():
            print("Please install Ollama manually and run this script again.")
            return
    
    # Start Ollama service
    if not setup.check_ollama_running():
        if not setup.start_ollama_service():
            print("Failed to start Ollama service. Please start it manually.")
            return
    else:
        print("✅ Ollama service is already running")
    
    # Download recommended model
    if not setup.download_recommended_model():
        print("Failed to download model. You can download it manually later.")
    
    # Test integration
    setup.test_ollama_integration()
    
    # Complete setup
    setup.setup_complete()

if __name__ == "__main__":
    main()
