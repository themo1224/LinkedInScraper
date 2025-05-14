# LinkedIn Laravel Job Scraper with Visa Sponsorship Filter

A Flask application that scrapes LinkedIn for Laravel developer job postings, with specific focus on remote positions and visa sponsorship opportunities.

## Features

- Scrapes LinkedIn for Laravel developer jobs
- Filters for remote work opportunities
- Identifies job posts with visa sponsorship mentions
- Stores results in PostgreSQL database
- Clean web interface to view and filter jobs

## Setup

### Option 1: Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Copy the example environment file and edit with your LinkedIn credentials:
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. Build and start the Docker containers:
```bash
docker-compose up -d
```

4. Access the application at http://localhost:5000

### Option 2: Local Setup

#### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- Virtual Environment (recommended)

#### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following content:
```
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password
DB_NAME=linkedin_jobs
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
```

5. Create the PostgreSQL database:
```bash
createdb linkedin_jobs
```

6. Run the application:
```bash
python app.py
```

7. Access the application at http://localhost:5000

## Docker Commands

- Start the application: `docker-compose up -d`
- Stop the application: `docker-compose down`
- View logs: `docker-compose logs -f`
- Rebuild the application: `docker-compose up -d --build`
- Access PostgreSQL CLI: `docker exec -it linkedin-db psql -U postgres -d linkedin_jobs`

## Usage

1. Navigate to "Scrape Jobs" in the navigation menu
2. Enter your search criteria (keywords and location)
3. Check the "Search for jobs with visa sponsorship" option if needed
4. Click "Start Scraping"
5. Once the scraping is complete, browse the jobs on the home page
6. Use the filters to find remote jobs with visa sponsorship

## Finding Jobs with Visa Sponsorship

The application specifically looks for phrases related to visa sponsorship in job descriptions:

- "Visa sponsorship available"
- "Will sponsor visa"
- "Work permit"
- "Relocation assistance"
- "International candidates welcome"

And many more. It also checks for negative phrases like "no visa sponsorship" to avoid false positives.

## For Developers from Iran

If you're looking to relocate from Iran, consider:

1. **Digital Nomad Visas**: Countries like Estonia, Portugal, and Croatia offer special visas for remote workers
2. **Talent Visas**: Germany, Netherlands, and Canada have special immigration pathways for tech professionals
3. **Company Relocation**: Look for companies that specifically mention relocation assistance

## License

MIT License

