"""
RAG Router - RAG sistemi için API endpoint'leri
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import List, Dict, Any, Optional
import os
import logging

from rag import (
    SearchService,
    RecommendationService,
    PDFGenerator
)
from utils.auth import get_current_user
from typing import Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rag", tags=["RAG System"])

# Global RAG components (production'da dependency injection kullanılmalı)
search_service = SearchService()
recommendation_service = RecommendationService(search_service)
pdf_generator = PDFGenerator()

@router.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Belge yükleme ve index'e ekleme
    """
    try:
        # Dosya türü kontrolü
        allowed_extensions = ['.pdf', '.txt', '.md']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Desteklenmeyen dosya formatı. Desteklenen formatlar: {allowed_extensions}"
            )
        
        # Geçici dosya oluştur
        temp_file_path = f"./temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Belgeyi index'e ekle
        result = search_service.add_document_to_index(temp_file_path)
        
        # Geçici dosyayı sil
        os.remove(temp_file_path)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "chunks_created": result["chunks_created"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Belge yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-roadmap")
async def add_roadmap_to_index(
    roadmap_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Roadmap'i index'e ekleme
    """
    try:
        result = search_service.add_roadmap_to_index(roadmap_data)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "roadmap_id": result["roadmap_id"],
                "chunks_created": result["chunks_created"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Roadmap ekleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-blog-content")
async def add_blog_content(
    content: str = Form(...),
    source: str = Form(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Blog içeriğini index'e ekleme
    """
    try:
        result = search_service.add_blog_content_to_index(content, source)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "chunks_created": result["chunks_created"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Blog içeriği ekleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_documents(
    query: str,
    k: int = 5,
    filter_by_source: Optional[str] = None,
    filter_by_type: Optional[str] = None,
    # current_user: Dict[str, Any] = Depends(get_current_user)  # Geçici olarak devre dışı
):
    """
    Belgelerde arama yapma
    """
    try:
        results = search_service.search_documents(
            query=query,
            k=k,
            filter_by_source=filter_by_source,
            filter_by_type=filter_by_type
        )
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        logger.error(f"Arama hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search-roadmaps")
async def search_roadmaps(
    query: str,
    k: int = 5,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Roadmap'lerde arama yapma
    """
    try:
        results = search_service.search_roadmaps(query=query, k=k)
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        logger.error(f"Roadmap arama hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search-educational")
async def search_educational_content(
    query: str,
    k: int = 5,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Eğitim içeriklerinde arama yapma
    """
    try:
        results = search_service.search_educational_content(query=query, k=k)
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        logger.error(f"Eğitim içeriği arama hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-context")
async def get_relevant_context(
    query: str,
    max_chars: int = 2000,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Sorgu için ilgili bağlamı getirme
    """
    try:
        context = search_service.get_relevant_context(query=query, max_chars=max_chars)
        
        return {
            "success": True,
            "query": query,
            "context": context,
            "context_length": len(context)
        }
        
    except Exception as e:
        logger.error(f"Bağlam alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations/learning")
async def get_learning_recommendations(
    user_interests: List[str],
    user_level: str = "beginner",
    max_recommendations: int = 5,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Öğrenme tavsiyeleri alma
    """
    try:
        recommendations = recommendation_service.get_learning_recommendations(
            user_interests=user_interests,
            user_level=user_level,
            max_recommendations=max_recommendations
        )
        
        return {
            "success": True,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Öğrenme tavsiyesi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations/next-steps")
async def get_next_steps_recommendations(
    current_roadmap_id: str,
    completed_modules: List[str],
    user_progress: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Sonraki adım tavsiyeleri alma
    """
    try:
        recommendations = recommendation_service.get_next_steps_recommendations(
            current_roadmap_id=current_roadmap_id,
            completed_modules=completed_modules,
            user_progress=user_progress
        )
        
        return {
            "success": True,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Sonraki adım tavsiyesi hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations/personalized")
async def get_personalized_content(
    user_profile: Dict[str, Any],
    learning_history: List[Dict[str, Any]],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Kişiselleştirilmiş içerik alma
    """
    try:
        recommendations = recommendation_service.get_personalized_content(
            user_profile=user_profile,
            learning_history=learning_history
        )
        
        return {
            "success": True,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Kişiselleştirilmiş içerik hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/daily")
async def get_daily_recommendations(
    date: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Günlük tavsiyeler alma
    """
    try:
        recommendations = recommendation_service.get_daily_recommendations(
            user_id=str(current_user.get("id", "unknown")),
            date=date
        )
        
        return {
            "success": True,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Günlük tavsiye hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/related")
async def get_related_content(
    content_id: str,
    content_type: str,
    max_related: int = 3,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    İlgili içerik alma
    """
    try:
        related_content = recommendation_service.get_related_content(
            content_id=content_id,
            content_type=content_type,
            max_related=max_related
        )
        
        return {
            "success": True,
            "related_content": related_content,
            "total_related": len(related_content)
        }
        
    except Exception as e:
        logger.error(f"İlgili içerik hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-pdf/roadmap")
async def generate_roadmap_pdf(
    roadmap_data: Dict[str, Any],
    current_user: Dict[str, Any] = None  # Geçici olarak authentication'ı kaldır
):
    """
    Roadmap'i PDF olarak oluşturma
    """
    try:
        user_info = {
            "name": current_user.get("username", "Unknown") if current_user else "Test User",
            "email": current_user.get("email", "unknown@example.com") if current_user else "test@example.com"
        }
        
        pdf_path = pdf_generator.generate_roadmap_pdf(
            roadmap_data=roadmap_data,
            user_info=user_info
        )
        
        # PDF dosyasını döndür
        return FileResponse(
            path=pdf_path,
            filename=os.path.basename(pdf_path),
            media_type="application/pdf"
        )
        
    except Exception as e:
        logger.error(f"PDF oluşturma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-pdf/progress")
async def generate_progress_pdf(
    progress_data: Dict[str, Any]
):
    """
    İlerleme raporu PDF'i oluşturma
    """
    try:
        user_info = {
            "name": "Test User",
            "email": "test@example.com"
        }
        
        pdf_path = pdf_generator.generate_progress_report_pdf(
            progress_data=progress_data,
            user_info=user_info
        )
        
        return FileResponse(
            path=pdf_path,
            filename=os.path.basename(pdf_path),
            media_type="application/pdf"
        )
        
    except Exception as e:
        logger.error(f"İlerleme PDF oluşturma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-pdf/summary")
async def generate_learning_summary_pdf(
    summary_data: Dict[str, Any],
    current_user: Dict[str, Any] = None  # Geçici olarak authentication'ı kaldır
):
    """
    Öğrenme özeti PDF'i oluşturma
    """
    try:
        user_info = {
            "name": current_user.get("username", "Unknown") if current_user else "Test User",
            "email": current_user.get("email", "unknown@example.com") if current_user else "test@example.com"
        }
        
        pdf_path = pdf_generator.generate_learning_summary_pdf(
            summary_data=summary_data,
            user_info=user_info
        )
        
        return FileResponse(
            path=pdf_path,
            filename=os.path.basename(pdf_path),
            media_type="application/pdf"
        )
        
    except Exception as e:
        logger.error(f"Özet PDF oluşturma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/stats")
async def get_rag_stats(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    RAG sistemi istatistiklerini alma
    """
    try:
        stats = search_service.get_index_stats()
        
        return {
            "success": True,
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"İstatistik alma hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/clear-index")
async def clear_index(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Index'i temizleme
    """
    try:
        result = search_service.clear_index()
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["error"])
            
    except Exception as e:
        logger.error(f"Index temizleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cleanup-pdfs")
async def cleanup_pdfs(
    days_to_keep: int = 7,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Eski PDF dosyalarını temizleme
    """
    try:
        pdf_generator.cleanup_old_pdfs(days_to_keep=days_to_keep)
        
        return {
            "success": True,
            "message": f"{days_to_keep} günden eski PDF dosyaları temizlendi"
        }
        
    except Exception as e:
        logger.error(f"PDF temizleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

