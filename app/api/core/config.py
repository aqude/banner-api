import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(".env")

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL")


settings = Settings()

