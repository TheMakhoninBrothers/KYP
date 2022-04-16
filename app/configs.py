import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['BOT_TOKEN']

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASS = os.environ['POSTGRES_PASS']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']
POSTGRES_DBNAME = os.environ['POSTGRES_DBNAME']

POSTGRES_URI = f'postgresql+asyncpg://{POSTGRES_PASS}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}'
