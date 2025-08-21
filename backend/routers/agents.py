"""
Agent Router - REST API endpoints for agent management and task execution
Provides interface for interacting with learning agents
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any, Optional
from datetime import datetime

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agent_manager import agent_manager
from utils.auth import verify_token

router = APIRouter(prefix="/api/v1/agents", tags=["Agents"])
security = HTTPBearer()

# Pydantic models for request/response
class TaskRequest:
    type: str
    agent: Optional[str] = None
    user_info: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None

class AgentStatus:
    name: str
    description: str
    is_active: bool
    memory_count: int
    tools_count: int
    tasks_executed: int
    success_rate: float
    framework: str

@router.get("/status")
async def get_agents_status(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get status of all agents
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        statuses = agent_manager.get_all_agent_statuses()
        system_status = agent_manager.get_system_status()
        
        return {
            "success": True,
            "system_status": system_status,
            "agents": statuses,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")

@router.get("/{agent_name}/status")
async def get_agent_status(
    agent_name: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get status of a specific agent
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        status = agent_manager.get_agent_status(agent_name)
        if not status:
            raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
        
        return {
            "success": True,
            "agent": agent_name,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")

@router.post("/execute")
async def execute_task(
    task: Dict[str, Any],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Execute a task using the appropriate agent
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        result = await agent_manager.execute_task(task)
        
        if result.get("success"):
            return {
                "success": True,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Task execution failed"))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task execution error: {str(e)}")

@router.post("/langchain/create-roadmap")
async def create_roadmap_with_langchain(
    user_info: Dict[str, Any],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create roadmap using LangChain agent
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        # LangChain agent'ı bul
        langchain_agent = agent_manager.get_agent("LangChainRoadmapAgent")
        if not langchain_agent:
            raise HTTPException(status_code=404, detail="LangChain agent not found")
        
        # Roadmap oluştur
        result = await langchain_agent.create_roadmap(user_info)
        
        if result.get("success"):
            return {
                "success": True,
                "result": result,
                "agent": "LangChainRoadmapAgent",
                "framework": "LangChain",
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Roadmap creation failed"))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roadmap creation error: {str(e)}")

@router.post("/langchain/analyze-roadmap")
async def analyze_roadmap_with_langchain(
    roadmap_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Analyze roadmap using LangChain agent
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        # LangChain agent'ı bul
        langchain_agent = agent_manager.get_agent("LangChainRoadmapAgent")
        if not langchain_agent:
            raise HTTPException(status_code=404, detail="LangChain agent not found")
        
        # Roadmap analiz et
        result = await langchain_agent.analyze_roadmap(roadmap_id)
        
        if result.get("success"):
            return {
                "success": True,
                "result": result,
                "agent": "LangChainRoadmapAgent",
                "framework": "LangChain",
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Roadmap analysis failed"))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Roadmap analysis error: {str(e)}")

@router.get("/langchain/roadmaps")
async def get_langchain_roadmaps(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get all roadmaps created by LangChain agent
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        # LangChain agent'ı bul
        langchain_agent = agent_manager.get_agent("LangChainRoadmapAgent")
        if not langchain_agent:
            raise HTTPException(status_code=404, detail="LangChain agent not found")
        
        roadmaps = langchain_agent.get_all_roadmaps()
        
        return {
            "success": True,
            "roadmaps": roadmaps,
            "count": len(roadmaps),
            "agent": "LangChainRoadmapAgent",
            "framework": "LangChain",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roadmaps: {str(e)}")

@router.get("/langchain/roadmaps/{roadmap_id}")
async def get_langchain_roadmap(
    roadmap_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get specific roadmap by ID
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        # LangChain agent'ı bul
        langchain_agent = agent_manager.get_agent("LangChainRoadmapAgent")
        if not langchain_agent:
            raise HTTPException(status_code=404, detail="LangChain agent not found")
        
        roadmap = langchain_agent.get_roadmap(roadmap_id)
        if not roadmap:
            raise HTTPException(status_code=404, detail=f"Roadmap '{roadmap_id}' not found")
        
        return {
            "success": True,
            "roadmap": roadmap,
            "roadmap_id": roadmap_id,
            "agent": "LangChainRoadmapAgent",
            "framework": "LangChain",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roadmap: {str(e)}")

@router.post("/batch-execute")
async def execute_batch_tasks(
    tasks: List[Dict[str, Any]],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Execute multiple tasks in parallel
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        results = await agent_manager.execute_batch_tasks(tasks)
        
        return {
            "success": True,
            "results": results,
            "total_tasks": len(tasks),
            "successful_tasks": len([r for r in results if r.get("success")]),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch execution error: {str(e)}")

@router.get("/frameworks")
async def get_framework_info(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get information about supported agent frameworks
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        frameworks = {
            "LangChain": {
                "description": "Modern AI agent framework with tool integration",
                "features": [
                    "Tool-based reasoning",
                    "Memory management",
                    "Conversation history",
                    "Multi-modal support",
                    "Extensible architecture"
                ],
                "agents": ["LangChainRoadmapAgent"],
                "status": "active"
            },
            "Custom": {
                "description": "Legacy custom agent implementation",
                "features": [
                    "Basic task handling",
                    "Simple memory system",
                    "Template-based responses"
                ],
                "agents": ["RoadmapAgent"],
                "status": "legacy"
            }
        }
        
        return {
            "success": True,
            "frameworks": frameworks,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get framework info: {str(e)}")

@router.post("/restart")
async def restart_agent_manager(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Restart the agent manager
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        agent_manager.stop()
        agent_manager.start()
        
        return {
            "success": True,
            "message": "Agent manager restarted successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart agent manager: {str(e)}")

@router.post("/clear-stats")
async def clear_agent_statistics(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Clear all agent statistics
    """
    # Token doğrulama
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    try:
        agent_manager.clear_stats()
        
        return {
            "success": True,
            "message": "Agent statistics cleared successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear statistics: {str(e)}")
