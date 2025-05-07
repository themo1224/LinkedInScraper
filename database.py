import psycopg2
from psycopg2 import Error
import os
import time

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

    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            insert_query = """
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
            ))
            
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