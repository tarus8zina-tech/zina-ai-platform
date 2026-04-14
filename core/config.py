from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class PlatformConfig:
    app_name: str = os.getenv("APP_NAME", "Zina AI Platform")
    environment: str = os.getenv("ENVIRONMENT", "development")
    default_agent: str = os.getenv("DEFAULT_AGENT", "general_agent")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"


config = PlatformConfig()