#!/usr/bin/env python3
"""
Launch script for Email Drafting Agent
"""
import os
import sys
import subprocess
import platform

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import groq
        import dotenv
        return True
    except ImportError:
        return False

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def check_env_file():
    """Check if .env file exists and has API key"""
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("Please create a .env file with your GROQ_API_KEY")
        print("Example: GROQ_API_KEY=your_api_key_here")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'GROQ_API_KEY' not in content or 'your_groq_api_key_here' in content:
            print("⚠️  Warning: Please set your actual Groq API key in the .env file")
            return False
    return True

def launch_streamlit():
    """Launch the Streamlit application"""
    print("🚀 Starting Email Drafting Agent...")
    print("📧 Open your browser to: http://localhost:8501")
    print("🔧 Press Ctrl+C to stop the application")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "email_drafting_agent.py"])
    except KeyboardInterrupt:
        print("\n👋 Email Drafting Agent stopped.")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

def main():
    """Main launcher function"""
    print("📧 Email Drafting Agent Launcher")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    # Check if requirements are installed
    if not check_requirements():
        print("📦 Installing dependencies...")
        install_requirements()
    
    # Check environment configuration
    env_ok = check_env_file()
    
    if not env_ok:
        print("\n❓ Do you want to continue anyway? (y/n): ", end="")
        if input().lower() != 'y':
            print("Please configure your .env file first.")
            sys.exit(1)
    
    # Launch the application
    launch_streamlit()

if __name__ == "__main__":
    main()
