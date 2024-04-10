from dotenv import load_dotenv
import sys, os

load_dotenv()

DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_NAME = os.environ.get("POSTGRES_NAME")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PORT = os.environ.get("POSTGRES_PORT")
