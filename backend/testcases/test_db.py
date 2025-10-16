# Create a test file: backend/test_db.py

from app.database import engine
from app.core.config import settings

def test_connection():
    try:
        with engine.connect() as connection:
            print("✅ Database connection successful!")
            print(f"Connected to: {settings.DATABASE_URL}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    test_connection()