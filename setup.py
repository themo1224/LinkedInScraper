from setuptools import setup, find_packages

setup(
    name="linkedin-scraper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "sqlalchemy",
        "psycopg2-binary",
        "python-dotenv",
    ],
) 