from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    OPENAI_API_KEY: str
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    
    class Config:
        env_file = ".env"


settings = Settings()
