from pathlib import Path
from dotenv import dotenv_values


BASE_DIR = Path(__file__).resolve().parent

ENV_PATH = BASE_DIR / ".env"

env = dotenv_values(ENV_PATH)


class Config:

    MYSQL_HOST = env.get("MYSQL_HOST")
    MYSQL_USER = env.get("MYSQL_USER")
    MYSQL_PASSWORD = env.get("MYSQL_PASSWORD")
    MYSQL_DB = env.get("MYSQL_DB")

    JWT_SECRET_KEY = env.get("JWT_SECRET_KEY")