"""
Entry point for the Self-Tuning Data Structure project.
Run this to start the Streamlit UI.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("🚀 Starting Self-Tuning Data Structure Visualizer...")
    print("📊 This will open in your browser\n")
    
    subprocess.run([
        sys.executable, 
        "-m", 
        "streamlit", 
        "run", 
        "src/ui/app.py"
    ])