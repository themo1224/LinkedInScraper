import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os

def get_database_connection():
    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            connection = psycopg2.connect(
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            print("Database connection successful!")
            return connection
        except Error as e:
            if attempt < max_retries - 1:
                print(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print(f"Error connecting to PostgreSQL after {max_retries} attempts: {e}")
                return None

def init_databases():
    connection= get_database_connection();
    if connection:
        try:
            cursor= connection.cursor();
            # create jobs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id SERIAL PRIMARY KEY, 
                    job_title VARCHAR(255),
                    company_name VARCHAR(255),
                    location VARCHAR(255),
                    job_link TEXT UNIQUE,
                    is_remote BOOLEAN,
                    description TEXT,
                    posted_date TIMESTAMP, 
                    salary_range VARCHAR(255),
                        experience_level VARCHAR(255).
                                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    
                )
            """); 
            connection.commit();
            print("Datebase initialized successfully");
        except Error as e:
            print(f"Error initializing database: {e}")
        finally
            if connection: 
                cursor.close();
                connection.close();

def save_job(job_data):
    connection = get_database_connection();
    if connection:
        try:
            cursor= connection.cursor();

            insert_query= """"
                INSERT INTO jobs (job_title, company_name, location, job_link, is_remote, 
                                description, posted_date, salary_range, experience_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (job_link) DO NOTHING
                RETURNING id
            """

            cursor.execute(insert_query, (
                 job_data['title'],
                job_data['company'],
                job_data['location'],
                job_data['link'],
                job_data['is_remote'],
                job_data['description'],
                job_data['posted_date'],
                job_data.get('salary_range', ''),
                job_data.get('experience_level', '')
            ));
             
            connection.commit()
            result = cursor.fetchone()
            return result[0] if result else None
            
        except Error as e:
            print(f"Error saving job: {e}")
            return None
        finally:
            if connection:
                cursor.close()
                connection.close()


if __name__ == "__main__":
    init_database()