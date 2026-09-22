import os
from dotenv import load_dotenv
env = os.getenv("test_env",'qa')
load_dotenv(f".env.{env}")
BASE_URL=os.getenv("BASE_URL")
USERNAME=os.getenv("USERNAME")
PASSWORD=os.getenv("PASSWORD")

