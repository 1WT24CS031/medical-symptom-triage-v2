from pathlib import Path
from dotenv import dotenv_values


# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# .env file path
ENV_PATH = BASE_DIR / ".env"

# Load environment variables from .env
env = dotenv_values(ENV_PATH)


class Config:

    # MySQL configuration
    MYSQL_HOST = env.get("MYSQL_HOST")
    MYSQL_USER = env.get("MYSQL_USER")
    MYSQL_PASSWORD = env.get("MYSQL_PASSWORD")
    MYSQL_DB = env.get("MYSQL_DB")

    # JWT secret key
    JWT_SECRET_KEY = env.get("JWT_SECRET_KEY")

    # Flask session secret key
    FLASK_SECRET_KEY = env.get("FLASK_SECRET_KEY")