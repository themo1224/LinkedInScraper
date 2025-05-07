# LinkedIn Laravel Job Scraper

A dockerized Python application that scrapes LinkedIn for Laravel developer job postings with remote work options.

## Features

- Searches for Laravel developer positions on LinkedIn
- Filters for remote work opportunities
- Stores results in PostgreSQL database
- Extracts key information including:
  - Job title
  - Company name
  - Location
  - Job description
  - Remote work status
  - Salary range (when available)
  - Experience requirements
  - Posted date

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the LinkedIn credentials and database configuration if needed:
```bash
cp .env.example .env
```

3. Build and start the containers:
```bash
docker-compose up --build
```

## Usage

The scraper will automatically:
1. Connect to LinkedIn
2. Search for Laravel developer positions
3. Filter for remote opportunities
4. Save results to the PostgreSQL database

To view the scraped data, you can connect to the PostgreSQL database using the following credentials:
- Host: localhost
- Port: 5432
- Database: linkedin_jobs
- Username: postgres
- Password: postgres_password

## Database Schema

The jobs table contains the following columns:
- id (SERIAL PRIMARY KEY)
- job_title (VARCHAR)
- company_name (VARCHAR)
- location (VARCHAR)
- job_link (TEXT UNIQUE)
- is_remote (BOOLEAN)
- description (TEXT)
- posted_date (TIMESTAMP)
- salary_range (VARCHAR)
- experience_level (VARCHAR)
- created_at (TIMESTAMP)

## Troubleshooting

1. If the scraper fails to login:
   - Ensure your LinkedIn credentials are correct in the .env file
   - LinkedIn might require additional verification
   - Try running without headless mode for debugging

2. If the database connection fails:
   - Ensure the PostgreSQL container is running
   - Check the database credentials in the .env file
   - Wait a few seconds for the database to initialize

## Security Notes

- Never commit your .env file with real credentials
- Use strong passwords for the database
- Consider implementing rate limiting to avoid LinkedIn restrictions

