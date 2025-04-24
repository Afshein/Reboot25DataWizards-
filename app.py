#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    """
    Main entry point to run the Streamlit application.
    This script launches the Streamlit server with the pruct_mobile2.py app.
    """
    print("Starting LBG Personalized Products Application...")
    
    # Check if Streamlit is installed
    try:
        import streamlit
        print(f"Streamlit version {streamlit.__version__} found.")
    except ImportError:
        print("Streamlit not found. Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully.")
    
    # Check if the target file exists
    target_file = os.path.join("pages", "pruct_mobile.py")
    if not os.path.exists(target_file):
        # Copy our enhanced file to the target location
        source_file = os.path.join("pages", "pruct_mobile.py")
        if os.path.exists(source_file):
            print(f"Target file {target_file} not found. Creating it from {source_file}...")
            with open(source_file, 'r') as src:
                content = src.read()
            with open(target_file, 'w') as dst:
                dst.write(content)
            print(f"Created {target_file} successfully.")
        else:
            print(f"Error: Neither {target_file} nor {source_file} exists.")
            return 1
    
    # Run the Streamlit application
    print("Launching Streamlit application...")
    cmd = [sys.executable, "-m", "streamlit", "run", target_file]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"Error running Streamlit application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())