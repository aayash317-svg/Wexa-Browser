import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Wexa Browser Agent Backend"
    HOST: str = "127.0.0.1"
    PORT: int = 8765
    
    # Model & Embedded Engine Settings (No Ollama daemon)
    MODELS_DIR: Path = BASE_DIR / "models"
    DEFAULT_GGUF_MODEL: str = "Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf"
    CONTEXT_WINDOW: int = 4096
    N_THREADS: int = 4
    
    # Automated Dataset Storage Settings
    DATA_DIR: Path = BASE_DIR / "data"
    DATASETS_DIR: Path = DATA_DIR / "datasets"
    TELEMETRY_LOG_FILE: Path = DATA_DIR / "automated_interactions.jsonl"
    EVALUATION_DIR: Path = DATA_DIR / "evaluation"
    
    # Security & Execution limits
    EXECUTION_TIMEOUT_SECONDS: int = 8
    MAX_ATTEMPTS: int = 3

    class Config:
        env_prefix = "WEXA_"

settings = Settings()

# Ensure directories exist
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
settings.DATASETS_DIR.mkdir(parents=True, exist_ok=True)
settings.EVALUATION_DIR.mkdir(parents=True, exist_ok=True)
