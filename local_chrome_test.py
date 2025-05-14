import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_chrome_locally():
    print("Testing Chrome and ChromeDriver setup locally...")
    
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        
        # Initialize WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
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
    result = test_chrome_locally()
    sys.exit(0 if result else 1) 