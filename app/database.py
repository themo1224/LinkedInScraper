from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from app.models import Base

# Database connection settings
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'linkedin_jobs')

# Create database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def init_db():
    try:
        # Create database engine
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        # Create session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        print("Database initialized successfully!")
        return engine, SessionLocal
    except SQLAlchemyError as e:
        print(f"Error initializing database: {str(e)}")
        raise

def get_db():
    """
    Generator function to get database session
    """
    engine, SessionLocal = init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Done!") 