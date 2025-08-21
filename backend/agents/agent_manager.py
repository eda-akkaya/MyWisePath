"""
Agent Manager - Coordinates all learning agents and provides unified interface
Manages agent lifecycle, task routing, and agent communication
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .base_agent import BaseAgent
from .roadmap_agent import RoadmapAgent
from .langchain_agent import LangChainRoadmapAgent, langchain_roadmap_agent

class AgentManager:
    """Manages all learning agents and coordinates their activities"""
    
    def __init__(self):
        self.agents = {}
        self.task_queue = []
        self.is_running = False
        self.agent_stats = {}
        self.created_at = datetime.now()
        
        # Register default agents
        self._register_default_agents()
    
    def _register_default_agents(self):
        """Register default agents"""
        # Legacy agent (eski sistem)
        roadmap_agent_instance = RoadmapAgent()
        self.register_agent(roadmap_agent_instance)
        
        # LangChain agent (yeni modern sistem)
        self.register_langchain_agent(langchain_roadmap_agent)
        
        print(f"Default agents registered: {list(self.agents.keys())}")
    
    def register_agent(self, agent: BaseAgent):
        """Register a new agent"""
        if not isinstance(agent, BaseAgent):
            raise ValueError("Agent must inherit from BaseAgent")
        
        self.agents[agent.name] = agent
        self.agent_stats[agent.name] = {
            "tasks_executed": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "last_task": None,
            "total_execution_time": 0,
            "framework": "Custom"
        }
        
        print(f"Agent '{agent.name}' registered successfully")
    
    def register_langchain_agent(self, langchain_agent):
        """Register a LangChain agent"""
        self.agents[langchain_agent.name] = langchain_agent
        self.agent_stats[langchain_agent.name] = {
            "tasks_executed": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "last_task": None,
            "total_execution_time": 0,
            "framework": "LangChain"
        }
        
        print(f"LangChain Agent '{langchain_agent.name}' registered successfully")
    
    def unregister_agent(self, agent_name: str) -> bool:
        """Unregister an agent"""
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            if hasattr(agent, 'deactivate'):
                agent.deactivate()
            del self.agents[agent_name]
            del self.agent_stats[agent_name]
            print(f"Agent '{agent_name}' unregistered")
            return True
        return False
    
    def get_agent(self, agent_name: str) -> Optional[Any]:
        """Get a specific agent by name"""
        return self.agents.get(agent_name)
    
    def get_all_agents(self) -> Dict[str, Any]:
        """Get all registered agents"""
        return self.agents.copy()
    
    def get_agent_status(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent"""
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            
            # LangChain agent için özel durum kontrolü
            if hasattr(agent, 'get_status'):
                status = agent.get_status()
            else:
                # Legacy agent için
                status = {
                    "name": agent.name,
                    "description": getattr(agent, 'description', ''),
                    "is_active": getattr(agent, 'is_active', False),
                    "created_at": getattr(agent, 'created_at', datetime.now()).isoformat(),
                    "last_activity": getattr(agent, 'last_activity', datetime.now()).isoformat(),
                    "memory_count": len(getattr(agent, 'memory', [])),
                    "tools_count": len(getattr(agent, 'tools', {}))
                }
            
            stats = self.agent_stats.get(agent_name, {})
            
            # Calculate success rate
            tasks_executed = stats.get('tasks_executed', 0)
            successful_tasks = stats.get('successful_tasks', 0)
            success_rate = (successful_tasks / tasks_executed * 100) if tasks_executed > 0 else 0
            
            status.update(stats)
            status['success_rate'] = round(success_rate, 2)
            return status
        return None
    
    def get_all_agent_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all agents"""
        statuses = {}
        for agent_name in self.agents:
            statuses[agent_name] = self.get_agent_status(agent_name)
        return statuses
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the appropriate agent"""
        
        task_type = task.get('type', '').lower()
        target_agent = task.get('agent', None)
        
        # Find the best agent for the task
        if target_agent and target_agent in self.agents:
            agent = self.agents[target_agent]
        else:
            agent = self._find_best_agent_for_task(task)
        
        if not agent:
            return {
                "error": f"No suitable agent found for task type: {task_type}",
                "available_agents": list(self.agents.keys())
            }
        
        # Execute task and track performance
        start_time = datetime.now()
        
        try:
            # LangChain agent için özel işlem
            if hasattr(agent, 'create_roadmap') and task_type == 'create_roadmap':
                result = await agent.create_roadmap(task.get('user_info', {}))
            elif hasattr(agent, 'analyze_roadmap') and task_type == 'analyze_roadmap':
                result = await agent.analyze_roadmap(task.get('roadmap_id', ''))
            elif hasattr(agent, 'execute_task'):
                # Legacy agent için
                result = await agent.execute_task(task)
            else:
                result = {"error": "Agent does not support this task type"}
            
            # Update agent statistics
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_agent_stats(agent.name, True, execution_time)
            
            return {
                "success": True,
                "agent": agent.name,
                "result": result,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
                "framework": self.agent_stats[agent.name].get('framework', 'Unknown')
            }
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_agent_stats(agent.name, False, execution_time)
            
            return {
                "success": False,
                "error": str(e),
                "agent": agent.name,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
                "framework": self.agent_stats[agent.name].get('framework', 'Unknown')
            }
    
    def _find_best_agent_for_task(self, task: Dict[str, Any]) -> Optional[Any]:
        """Find the best agent for a given task"""
        best_agent = None
        best_score = 0
        
        for agent_name, agent in self.agents.items():
            # LangChain agent için özel kontrol
            if hasattr(agent, 'create_roadmap') and task.get('type') == 'create_roadmap':
                score = self._calculate_langchain_agent_score(agent, task)
            elif hasattr(agent, 'can_handle_task'):
                # Legacy agent için
                if agent.can_handle_task(task):
                    score = self._calculate_agent_score(agent, task)
                else:
                    continue
            else:
                continue
            
            if score > best_score:
                best_score = score
                best_agent = agent
        
        return best_agent
    
    def _calculate_langchain_agent_score(self, agent: Any, task: Dict[str, Any]) -> int:
        """Calculate how well a LangChain agent can handle a task"""
        score = 0
        
        # LangChain agent'lar için yüksek öncelik
        score += 50
        
        # Task type kontrolü
        task_type = task.get('type', '').lower()
        if task_type == 'create_roadmap' and hasattr(agent, 'create_roadmap'):
            score += 30
        elif task_type == 'analyze_roadmap' and hasattr(agent, 'analyze_roadmap'):
            score += 30
        
        # Active agent bonus
        if getattr(agent, 'is_active', True):
            score += 10
        
        # Tools count bonus
        if hasattr(agent, 'tools'):
            score += min(len(agent.tools), 10)
        
        return score
    
    def _calculate_agent_score(self, agent: BaseAgent, task: Dict[str, Any]) -> int:
        """Calculate how well an agent can handle a task"""
        score = 0
        
        # Base score for being able to handle the task
        score += 10
        
        # Bonus for recent successful tasks
        stats = self.agent_stats.get(agent.name, {})
        success_rate = stats.get('successful_tasks', 0) / max(stats.get('tasks_executed', 1), 1)
        score += int(success_rate * 20)
        
        # Bonus for active agents
        if agent.is_active:
            score += 5
        
        # Bonus for agents with more tools
        score += min(len(agent.tools), 5)
        
        return score
    
    def _update_agent_stats(self, agent_name: str, success: bool, execution_time: float):
        """Update agent performance statistics"""
        if agent_name in self.agent_stats:
            stats = self.agent_stats[agent_name]
            stats["tasks_executed"] += 1
            stats["total_execution_time"] += execution_time
            
            if success:
                stats["successful_tasks"] += 1
            
            stats["last_task"] = datetime.now().isoformat()
    
    async def execute_batch_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple tasks in parallel"""
        if not tasks:
            return []
        
        # Group tasks by agent for better efficiency
        agent_tasks = {}
        for task in tasks:
            agent = self._find_best_agent_for_task(task)
            if agent:
                agent_name = agent.name
                if agent_name not in agent_tasks:
                    agent_tasks[agent_name] = []
                agent_tasks[agent_name].append(task)
        
        # Execute tasks in parallel
        results = []
        for agent_name, agent_task_list in agent_tasks.items():
            agent = self.agents[agent_name]
            
            # Execute tasks for this agent
            agent_results = []
            for task in agent_task_list:
                try:
                    if hasattr(agent, 'create_roadmap') and task.get('type') == 'create_roadmap':
                        result = await agent.create_roadmap(task.get('user_info', {}))
                    elif hasattr(agent, 'analyze_roadmap') and task.get('type') == 'analyze_roadmap':
                        result = await agent.analyze_roadmap(task.get('roadmap_id', ''))
                    elif hasattr(agent, 'execute_task'):
                        result = await agent.execute_task(task)
                    else:
                        result = {"error": "Agent does not support this task type"}
                    
                    agent_results.append({
                        "success": True,
                        "agent": agent_name,
                        "result": result,
                        "task": task
                    })
                except Exception as e:
                    agent_results.append({
                        "success": False,
                        "error": str(e),
                        "agent": agent_name,
                        "task": task
                    })
            
            results.extend(agent_results)
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        total_agents = len(self.agents)
        active_agents = sum(1 for agent in self.agents.values() 
                          if getattr(agent, 'is_active', True))
        
        total_tasks = sum(stats.get('tasks_executed', 0) for stats in self.agent_stats.values())
        total_success = sum(stats.get('successful_tasks', 0) for stats in self.agent_stats.values())
        success_rate = (total_success / total_tasks * 100) if total_tasks > 0 else 0
        
        # Framework breakdown
        framework_stats = {}
        for stats in self.agent_stats.values():
            framework = stats.get('framework', 'Unknown')
            if framework not in framework_stats:
                framework_stats[framework] = 0
            framework_stats[framework] += 1
        
        return {
            "system_status": "running" if self.is_running else "stopped",
            "total_agents": total_agents,
            "active_agents": active_agents,
            "total_tasks_executed": total_tasks,
            "success_rate": round(success_rate, 2),
            "uptime": (datetime.now() - self.created_at).total_seconds(),
            "created_at": self.created_at.isoformat(),
            "last_updated": datetime.now().isoformat(),
            "framework_distribution": framework_stats
        }
    
    def start(self):
        """Start the agent manager"""
        self.is_running = True
        print("Agent Manager started")
    
    def stop(self):
        """Stop the agent manager"""
        self.is_running = False
        print("Agent Manager stopped")
    
    def clear_stats(self):
        """Clear all agent statistics"""
        for agent_name in self.agent_stats:
            self.agent_stats[agent_name] = {
                "tasks_executed": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "last_task": None,
                "total_execution_time": 0,
                "framework": self.agent_stats[agent_name].get('framework', 'Unknown')
            }
        print("Agent statistics cleared")

# Global Agent Manager instance
agent_manager = AgentManager()
