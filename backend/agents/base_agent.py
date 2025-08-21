"""
Base Agent Class for MyWisePath Learning Agents
Provides common functionality and interface for all agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime

class BaseAgent(ABC):
    """Base class for all learning agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.memory = []
        self.tools = {}
        self.is_active = False
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def can_handle_task(self, task: Dict[str, Any]) -> bool:
        """Check if this agent can handle the given task"""
        pass
    
    def add_tool(self, tool_name: str, tool_function):
        """Add a tool to the agent's toolkit"""
        self.tools[tool_name] = tool_function
        print(f"Tool '{tool_name}' added to {self.name}")
    
    def add_to_memory(self, item: Dict[str, Any]):
        """Add an item to agent's memory"""
        item['timestamp'] = datetime.now().isoformat()
        self.memory.append(item)
        # Keep only last 100 items
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
    
    def get_memory(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent memory items"""
        return self.memory[-limit:] if self.memory else []
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "memory_count": len(self.memory),
            "tools_count": len(self.tools)
        }
    
    def activate(self):
        """Activate the agent"""
        self.is_active = True
        print(f"Agent '{self.name}' activated")
    
    def deactivate(self):
        """Deactivate the agent"""
        self.is_active = False
        print(f"Agent '{self.name}' deactivated")
    
    def clear_memory(self):
        """Clear agent memory"""
        self.memory.clear()
        print(f"Memory cleared for agent '{self.name}'")
