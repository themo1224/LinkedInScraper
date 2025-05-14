"""
Simple script to test if Chrome and ChromeDriver are properly installed and configured.
"""
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_chrome_driver():
    print("Testing Chrome and ChromeDriver setup...")
    
    try:
        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Use ChromeDriver from the path specified in environment variable or default location
        chrome_driver_path = os.environ.get('CHROME_DRIVER', '/usr/local/bin/chromedriver')
        service = Service(executable_path=chrome_driver_path)
        
        print(f"Using ChromeDriver at: {chrome_driver_path}")
        
        # Initialize WebDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Navigate to a simple page
        driver.get("https://www.google.com")
        
        # Print page title as verification
        print(f"Successfully loaded page with title: {driver.title}")
        
        # Get Chrome and ChromeDriver versions
        chrome_info = driver.capabilities['browserVersion']
        driver_info = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        
        print(f"Chrome version: {chrome_info}")
        print(f"ChromeDriver version: {driver_info}")
        
        # Close the driver
        driver.quit()
        
        print("Chrome and ChromeDriver test completed successfully.")
        return True
        
    except Exception as e:
        print(f"Error testing Chrome/ChromeDriver: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    result = test_chrome_driver()
    sys.exit(0 if result else 1) 