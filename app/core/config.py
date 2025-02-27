from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM = "HS256"

settings = Settings()
