
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load .env from inside .venv-1
env_path = Path(__file__).resolve().parent / ".venv-1" / ".env"

load_dotenv(dotenv_path=env_path)

# Get MySQL URL
MY_SQL_URL = os.getenv("MY_SQL_URL")

if not MY_SQL_URL:
    print("ERROR: Could not find MY_SQL_URL in .env")
    exit()

print("Environment file found!")
print("MySQL URL loaded!")

# Connect to MySQL
try:
    engine = create_engine(MY_SQL_URL)

    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE()"))
        print("Successfully connected to MySQL!")
        print("Database:", result.fetchone()[0])

except Exception as e:
    print("Connection failed:")
    print(e)
