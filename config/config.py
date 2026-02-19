import os

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
