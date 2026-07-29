from pathlib import Path
import os

from dotenv import load_dotenv

from services.api import APIClient

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000/api/",
)

api = APIClient(API_BASE_URL)