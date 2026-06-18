from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL loaded successfully")

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connected successfully!")
except Exception as e:
    print("Connection failed!")
    print(e)