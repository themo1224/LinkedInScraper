from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    job_id = Column(String(255), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255))
    job_url = Column(String(500), nullable=False)
    description = Column(Text)
    salary_range = Column(String(255))
    employment_type = Column(String(100))
    seniority_level = Column(String(100))
    posted_date = Column(DateTime)
    is_remote = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}')>"

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    linkedin_url = Column(String(500))
    website = Column(String(500))
    industry = Column(String(255))
    company_size = Column(String(100))
    headquarters = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Company(name='{self.name}')>"

class SearchQuery(Base):
    __tablename__ = 'search_queries'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(255), nullable=False)
    location = Column(String(255))
    date_searched = Column(DateTime, default=datetime.utcnow)
    results_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<SearchQuery(keyword='{self.keyword}', location='{self.location}')>" 