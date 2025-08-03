from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime

# Router'ları import et
from routers import auth, roadmap, chatbot, automation

app = FastAPI(
    title="MyWisePath API",
    description="Kişiselleştirilmiş Öğrenme Platformu API",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(auth.router)
app.include_router(roadmap.router)
app.include_router(chatbot.router)
app.include_router(automation.router)

@app.get("/")
async def root():
    return {"message": "MyWisePath API çalışıyor!", "version": "1.0.0"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 