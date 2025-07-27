from datetime import datetime

# Dummy user data
DUMMY_USER = {
    "id": "1",
    "username": "demo_user",
    "email": "demo@mywisepath.com",
    "password": "demo123",  # Gerçek uygulamada hash'lenmiş olacak
    "created_at": datetime.now().isoformat()
} 