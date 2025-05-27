import os
from sqlalchemy.orm import Session
from app.database import init_db
from app.scrapers.linkedin import LinkedInScraper

def main():
    # Initialize database
    engine, SessionLocal = init_db()
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Initialize scraper
        scraper = LinkedInScraper(db)
        
        # Login to LinkedIn
        email = os.getenv('LINKEDIN_EMAIL')
        password = os.getenv('LINKEDIN_PASSWORD')
        
        if not email or not password:
            raise ValueError("LinkedIn credentials not found in environment variables")
        
        scraper.login(email, password)
        
        # Search for jobs
        keywords = ["Python Developer", "Data Engineer", "Backend Developer"]
        locations = ["Remote", "United States"]
        
        for keyword in keywords:
            for location in locations:
                try:
                    print(f"\nSearching for {keyword} in {location}...")
                    scraper.search_jobs(keyword, location)
                except Exception as e:
                    print(f"Error searching for {keyword} in {location}: {str(e)}")
                    continue
        
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Clean up
        scraper.close()
        db.close()

if __name__ == "__main__":
    main() 