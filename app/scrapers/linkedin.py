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
import undetected_chromedriver as uc
from app import db
from app.models import Job

class LinkedInScraper:
    def __init__(self):
        self.setup_driver()
        
    def setup_driver(self):
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
            print("Starting ChromeDriver...")
            
            # Use ChromeDriver from the path specified in environment variable
            chrome_driver_path = os.environ.get('CHROME_DRIVER', '/usr/local/bin/chromedriver')
            service = Service(executable_path=chrome_driver_path)
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set up wait
            self.wait = WebDriverWait(self.driver, 15)  # Increase wait time for Docker
            
            print("ChromeDriver setup successful")
            
        except Exception as e:
            print(f"Error setting up ChromeDriver: {str(e)}")
            raise

    def login(self):
        try:
            print("Navigating to LinkedIn login page...")
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(5)  # Additional sleep for Docker
            
            # Enter email
            print("Entering email...")
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            email_input.send_keys(os.getenv('LINKEDIN_EMAIL'))
            
            # Enter password
            print("Entering password...")
            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(os.getenv('LINKEDIN_PASSWORD'))
            
            # Click login button
            print("Clicking login button...")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(8)  # Increased wait for login in Docker
            print("Login successful")
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def search_jobs(self, keywords="Laravel developer", location="Remote", check_visa_sponsorship=False):
        try:
            # Add visa keywords if needed
            if check_visa_sponsorship:
                keywords = f"{keywords} visa sponsorship"
                
            # Navigate to LinkedIn Jobs
            print(f"Searching for jobs with keywords: {keywords}, location: {location}")
            self.driver.get(f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}")
            time.sleep(5)

            # Scroll to load more jobs
            self._scroll_jobs_list()

            # Get all job cards
            print("Extracting job cards...")
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
            print(f"Found {len(job_cards)} job cards")
            
            for index, job_card in enumerate(job_cards):
                try:
                    print(f"Processing job card {index + 1}/{len(job_cards)}")
                    job_data = self._extract_job_data(job_card, check_visa_sponsorship)
                    if job_data and self._is_relevant_job(job_data):
                        self._save_job(job_data)
                        print(f"Saved job: {job_data['title']} at {job_data['company']}")
                    else:
                        print("Job not relevant or extraction failed, skipping")
                except Exception as e:
                    print(f"Error processing job card {index + 1}: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error in search_jobs: {str(e)}")

    def _scroll_jobs_list(self):
        print("Scrolling to load more jobs...")
        for i in range(5):  # Scroll 5 times to load more jobs
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"Scroll {i+1}/5 completed")
            time.sleep(3)  # Increased time for Docker

    def _extract_job_data(self, job_card, check_visa_sponsorship=False):
        try:
            title = job_card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text.strip()
            company = job_card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle").text.strip()
            location = job_card.find_element(By.CSS_SELECTOR, ".job-search-card__location").text.strip()
            job_link = job_card.find_element(By.CSS_SELECTOR, "a.base-card__full-link").get_attribute('href')
            
            print(f"Found job: {title} at {company}")
            
            # Click on the job to load details
            print("Clicking job to load details...")
            job_card.click()
            time.sleep(3)  # Increased wait for Docker
            
            # Get job description
            print("Extracting job description...")
            description = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".show-more-less-html__markup")
            )).text.strip()

            is_remote = any(keyword.lower() in description.lower() or keyword.lower() in location.lower() 
                          for keyword in ['remote', 'work from home', 'wfh'])
                          
            has_visa_sponsorship = self._check_visa_sponsorship(description, title, company) if check_visa_sponsorship else False

            return {
                'title': title,
                'company': company,
                'location': location,
                'link': job_link,
                'description': description,
                'is_remote': is_remote,
                'has_visa_sponsorship': has_visa_sponsorship,
                'posted_date': datetime.now(),
                'salary_range': self._extract_salary(description),
                'experience_level': self._extract_experience(description)
            }

        except Exception as e:
            print(f"Error extracting job data: {str(e)}")
            return None

    def _is_relevant_job(self, job_data):
        keywords = ['laravel', 'php', 'web development', 'backend', 'full stack']
        is_relevant = any(keyword in job_data['description'].lower() for keyword in keywords)
        if is_relevant:
            print(f"Job is relevant: {job_data['title']}")
        return is_relevant
        
    def _check_visa_sponsorship(self, description, title, company):
        # Keywords that indicate visa sponsorship
        visa_keywords = [
            'visa sponsorship', 
            'sponsor visa',
            'work permit',
            'can sponsor',
            'will sponsor',
            'sponsorship available',
            'sponsor international',
            'relocation assistance',
            'visa support',
            'nomad visa',
            'digital nomad',
            'global mobility',
            'international candidates',
            'work authorization'
        ]
        
        # Check for visa sponsorship in description
        description_lower = description.lower()
        
        # Check for negatives first
        negative_phrases = [
            'no visa sponsorship',
            'cannot sponsor',
            'not sponsor',
            'unable to sponsor',
            'no sponsorship',
            'no relocation'
        ]
        
        for phrase in negative_phrases:
            if phrase in description_lower:
                print(f"Found negative visa phrase: '{phrase}'")
                return False
                
        # Then check for positives
        for keyword in visa_keywords:
            if keyword in description_lower:
                print(f"Found visa sponsorship indicator: '{keyword}'")
                return True
                
        print("No visa sponsorship indicators found")
        return False

    def _extract_salary(self, description):
        # Basic salary extraction - can be improved
        if '$' in description:
            return description[description.find('$'):description.find('$')+30].split()[0]
        return ''

    def _extract_experience(self, description):
        experience_keywords = ['years of experience', 'year experience', 'years experience']
        for keyword in experience_keywords:
            if keyword in description.lower():
                # Extract the sentence containing the experience requirement
                start = max(0, description.lower().find(keyword) - 50)
                end = min(len(description), description.lower().find(keyword) + 50)
                return description[start:end].strip()
        return ''
    
    def _save_job(self, job_data):
        # Check if job already exists
        existing_job = Job.query.filter_by(job_link=job_data['link']).first()
        if existing_job:
            print(f"Job already exists: {job_data['title']}")
            return
        
        # Create new job
        new_job = Job(
            job_title=job_data['title'],
            company_name=job_data['company'],
            location=job_data['location'],
            job_link=job_data['link'],
            is_remote=job_data['is_remote'],
            has_visa_sponsorship=job_data['has_visa_sponsorship'],
            description=job_data['description'],
            posted_date=job_data['posted_date'],
            salary_range=job_data.get('salary_range', ''),
            experience_level=job_data.get('experience_level', '')
        )
        
        try:
            db.session.add(new_job)
            db.session.commit()
            print(f"Job saved to database: {job_data['title']}")
            return new_job.id
        except Exception as e:
            db.session.rollback()
            print(f"Error saving job to database: {str(e)}")
            return None

    def close(self):
        if hasattr(self, 'driver'):
            print("Closing ChromeDriver...")
            self.driver.quit() 