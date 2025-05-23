from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Hard-coded database connection for Docker testing
db_user = "postgres"
db_password = "postgres"
db_host = "postgres"
db_port = "5432"
db_name = "linkedin_jobs"

# Print debugging information
print(f"Database connection: User={db_user}, Host={db_host}, Port={db_port}, Database={db_name}")

# Configure the app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-testing')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(f"SQLAlchemy connection string: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialize database
db = SQLAlchemy(app)

# Import routes after app creation to avoid circular imports
from app import routes, models