import os
from dotenv import load_dotenv
from sqlmodel import create_engine


load_dotenv()
MY_SQL_URL = os.getenv("MY_SQL_URL")

engine = create_engine(MY_SQL_URL)