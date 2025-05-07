import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
import undetected_chromedriver as uc
from database import init_database, save_job

class LinkedInJobScraper:
    def __init__(self):
        self.setup_driver();
    def setup_dirver(self):
        chrome_options = us.chromeOptions();
        chrome_options.add_argument('--headless');
        chrome_options.add_argument('--no-sandbox');
        chrome_options.add_argument('--disable-dev-shm-usage');

        self.driver = uc.Chrome(options=chrome_options);
        self.wait = WebDriverWait(self.driver, 10);