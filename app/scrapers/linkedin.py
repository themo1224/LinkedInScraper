import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
from sqlalchemy.orm import Session
from app import db
from app.models import Job, Company, SearchQuery

class LinkedInScraper:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.base_url = "https://www.linkedin.com"
        self.driver = self._setup_driver()
        self.is_logged_in = False

    def _setup_driver(self):
        """Set up the Chrome driver with appropriate options for Docker container"""
        try:
            # Options for running Chrome in Docker
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Additional options for stability in Docker
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-infobars')
            
            # For debugging
            print("Starting Chrome WebDriver...")
            
            # Initialize Chrome WebDriver with installed ChromeDriver
            service = Service('/usr/local/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set up wait
            self.wait = WebDriverWait(driver, 15)  # Increase wait time for Docker
            
            print("Chrome WebDriver setup successful")
            return driver
            
        except Exception as e:
            print(f"Error setting up Chrome WebDriver: {str(e)}")
            raise

    def login(self, email: str, password: str):
        """Login to LinkedIn"""
        try:
            self.driver.get(f"{self.base_url}/login")
            
            # Wait for email field and enter credentials
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(email)
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            
            # Click login button
            self.driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
            
            # Wait for successful login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".global-nav"))
            )
            
            self.is_logged_in = True
            print("Successfully logged in to LinkedIn")
            
        except TimeoutException:
            print("Failed to login: Timeout waiting for elements")
            raise
        except Exception as e:
            print(f"Failed to login: {str(e)}")
            raise

    def search_jobs(self, keyword: str, location: str = None, page_limit: int = 10):
        """Search for jobs and store results in database"""
        if not self.is_logged_in:
            raise Exception("Must be logged in to search jobs")

        try:
            # Construct search URL
            search_url = f"{self.base_url}/jobs/search/?keywords={keyword}"
            if location:
                search_url += f"&location={location}"
            
            self.driver.get(search_url)
            time.sleep(2)  # Wait for page to load
            
            # Create search query record
            search_query = SearchQuery(
                keyword=keyword,
                location=location,
                date_searched=datetime.utcnow()
            )
            self.db.add(search_query)
            
            jobs_found = 0
            for page in range(page_limit):
                # Extract job listings from current page
                job_cards = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, ".job-card-container")
                    )
                )
                
                for card in job_cards:
                    try:
                        # Extract job details
                        job_data = self._extract_job_data(card)
                        
                        # Store in database
                        if job_data:
                            job = Job(**job_data)
                            self.db.add(job)
                            jobs_found += 1
                    
                    except Exception as e:
                        print(f"Error processing job card: {str(e)}")
                        continue
                
                # Try to go to next page
                try:
                    next_button = self.driver.find_element(
                        By.CSS_SELECTOR, "[aria-label='Next']"
                    )
                    if "disabled" in next_button.get_attribute("class"):
                        break
                    next_button.click()
                    time.sleep(2)
                except NoSuchElementException:
                    break
            
            # Update search query with results count
            search_query.results_count = jobs_found
            self.db.commit()
            
            print(f"Found {jobs_found} jobs for '{keyword}' in {location if location else 'any location'}")
            
        except Exception as e:
            self.db.rollback()
            print(f"Error during job search: {str(e)}")
            raise

    def _extract_job_data(self, card) -> dict:
        """Extract job data from a job card element"""
        try:
            # Click on card to load details
            card.click()
            time.sleep(1)
            
            # Extract basic info
            title = card.find_element(By.CSS_SELECTOR, "h3").text
            company = card.find_element(By.CSS_SELECTOR, "[data-job-hook='company-name']").text
            location = card.find_element(By.CSS_SELECTOR, "[data-job-hook='location']").text
            
            # Get job URL
            job_link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            job_id = job_link.split("currentJobId=")[1].split("&")[0]
            
            # Try to get additional details from expanded view
            try:
                description = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "description"))
                ).text
            except TimeoutException:
                description = None
            
            # Check if remote
            is_remote = "remote" in location.lower() or "remote" in title.lower()
            
            return {
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "job_url": job_link,
                "description": description,
                "is_remote": is_remote,
                "posted_date": datetime.utcnow()  # Actual posting date needs parsing
            }
            
        except Exception as e:
            print(f"Error extracting job data: {str(e)}")
            return None

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit() 