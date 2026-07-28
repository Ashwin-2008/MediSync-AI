import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get("DATABASE_URL")
if not url:
    print("NO DATABASE_URL")
    exit(1)

# convert if asyncpg
url = url.replace("postgresql+asyncpg", "postgresql")

print(f"Connecting to {url} ...")
try:
    conn = psycopg2.connect(url)
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print(f"Failed to connect: {e}")
