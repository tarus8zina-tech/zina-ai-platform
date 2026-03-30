from dataclasses import dataclass
import os


@dataclass
class PlatformConfig:
    app_name: str = os.getenv("APP_NAME", "Zina AI Platform")
    environment: str = os.getenv("ENVIRONMENT", "development")
    default_agent: str = os.getenv("DEFAULT_AGENT", "general_agent")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"


config = PlatformConfig()