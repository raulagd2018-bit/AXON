import os

class Config:
    DEBUG = False
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(BASE_DIR, "security/audit.log")
    VERSION = "1.0.0"

config = Config()
