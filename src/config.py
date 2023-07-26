from dataclasses import dataclass


@dataclass
class Config:
    log_level: str = "Debug"
    api_version: str = "0.0.5"
    api_host: str = "localhost"
    api_port: int = 8000


config = Config()   
