import os

from aiogram import Router
from dotenv import load_dotenv
from google.cloud import vision


router = Router()
load_dotenv()
GOOGLE_CLOUD_VISION_CREDENTIALS=os.getenv("GOOGLE_CLOUD_VISION_CREDENTIALS")


