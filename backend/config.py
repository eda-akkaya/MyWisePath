import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mywisepath-secret-key-2024")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Database Configuration (for future use)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "mywisepath") 