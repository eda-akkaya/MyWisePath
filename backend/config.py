import os
from dotenv import load_dotenv

# Load environment variables (with error handling)
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    print("Using default configuration values.")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Serp AI API Configuration
SERP_API_KEY = os.getenv("SERP_API_KEY")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mywisepath-secret-key-2024")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database Configuration (for future use)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "mywisepath")

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@mywisepath.com")
EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "MyWisePath")

# Email Automation Settings
WEEKLY_REMINDER_ENABLED = os.getenv("WEEKLY_REMINDER_ENABLED", "true").lower() == "true"
PROGRESS_REPORT_ENABLED = os.getenv("PROGRESS_REPORT_ENABLED", "true").lower() == "true" 