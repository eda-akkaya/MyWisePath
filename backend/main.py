from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime

# Router'ları import et
from routers import auth, roadmap, chatbot, automation, learning_environment, agents, progress, rag

# Agent manager'ı import et ve başlat
from agents.agent_manager import agent_manager

app = FastAPI(
    title="MyWisePath API",
    description="Kişiselleştirilmiş Öğrenme Platformu API",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:3001",  # Alternative port
        "http://127.0.0.1:3001",  # Alternative port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(auth.router, prefix="/api/v1")
app.include_router(roadmap.router, prefix="/api/v1")
app.include_router(chatbot.router, prefix="/api/v1")
app.include_router(automation.router, prefix="/api/v1/automation")
app.include_router(learning_environment.router, prefix="/api/v1")
app.include_router(agents.router, prefix="/api/v1")
app.include_router(progress.router, prefix="/api/v1")
app.include_router(rag.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "MyWisePath API çalışıyor!", "version": "1.0.0"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.on_event("startup")
async def startup_event():
    """Uygulama başladığında agent manager'ı başlat"""
    agent_manager.start()
    print("🤖 Agent Manager başlatıldı ve arka planda çalışıyor")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 