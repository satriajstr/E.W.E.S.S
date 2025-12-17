import os
from dotenv import load_dotenv

# Load file .env
load_dotenv()

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")