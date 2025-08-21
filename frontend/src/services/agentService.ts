import axios from 'axios';

// authService'den aynı axios instance'ını kullan
import { api, authService } from './authService';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface AgentStatus {
  name: string;
  description: string;
  is_active: boolean;
  memory_count: number;
  tools_count: number;
  tasks_executed?: number;
  success_rate?: number;
  created_at: string;
  last_activity: string;
}

export interface SystemStatus {
  system_status: string;
  total_agents: number;
  active_agents: number;
  total_tasks_executed: number;
  success_rate: number;
  uptime: number;
  created_at: string;
  last_updated: string;
}

export interface TaskRequest {
  type: string;
  agent?: string;
  user_info?: any;
  data?: any;
}

export interface TaskResult {
  success: boolean;
  agent?: string;
  result?: any;
  execution_time?: number;
  timestamp: string;
  error?: string;
}

export interface RoadmapInfo {
  interests: string[];
  skill_level: string;
  learning_goals: string[];
  available_hours_per_week: number;
  target_timeline_months: number;
}

export interface Roadmap {
  title: string;
  description: string;
  estimated_duration_weeks: number;
  weekly_hours: number;
  modules: any[];
  learning_strategy: string;
  milestones: string[];
  success_metrics: string[];
}

class AgentService {
  private async getAuthHeaders(): Promise<HeadersInit> {
    const token = authService.getToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    };
  }

  // Get all agents status
  async getAgentsStatus(): Promise<{ system_status: SystemStatus; agents: Record<string, AgentStatus> }> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/status`, {
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching agents status:', error);
      throw error;
    }
  }

  // Get specific agent status
  async getAgentStatus(agentName: string): Promise<AgentStatus> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/${agentName}/status`, {
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.status;
    } catch (error) {
      console.error(`Error fetching ${agentName} status:`, error);
      throw error;
    }
  }

  // Execute a task
  async executeTask(task: TaskRequest): Promise<TaskResult> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/execute`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify(task),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error executing task:', error);
      throw error;
    }
  }

  // Execute batch tasks
  async executeBatchTasks(tasks: TaskRequest[]): Promise<TaskResult[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/execute-batch`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify(tasks),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.results;
    } catch (error) {
      console.error('Error executing batch tasks:', error);
      throw error;
    }
  }

  // Create roadmap
  async createRoadmap(userInfo: RoadmapInfo): Promise<{ roadmap_id: string; roadmap: Roadmap }> {
    try {
      console.log('🔧 AgentService: Creating roadmap with data:', userInfo);
      console.log('🔧 AgentService: API URL:', `${API_BASE_URL}/api/v1/agents/roadmap/create`);
      
      const headers = await this.getAuthHeaders();
      console.log('🔧 AgentService: Headers:', headers);
      
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/roadmap/create`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(userInfo),
      });
      
      console.log('🔧 AgentService: Response status:', response.status);
      console.log('🔧 AgentService: Response ok:', response.ok);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('🔧 AgentService: Error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      
      const data = await response.json();
      console.log('🔧 AgentService: Response data:', data);
      
      // The response structure is: data.result.result.roadmap
      const result = data.result.result;
      console.log('🔧 AgentService: Extracted result:', result);
      
      return result;
    } catch (error) {
      console.error('❌ AgentService: Error creating roadmap:', error);
      throw error;
    }
  }

  // Analyze roadmap
  async analyzeRoadmap(roadmapId: string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/roadmap/analyze`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify({ roadmap_id: roadmapId }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.result.result;
    } catch (error) {
      console.error('Error analyzing roadmap:', error);
      throw error;
    }
  }

  // Get roadmap suggestions
  async getRoadmapSuggestions(userInfo: any, currentRoadmap: any): Promise<string[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/roadmap/suggest`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
        body: JSON.stringify({ user_info: userInfo, current_roadmap: currentRoadmap }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.result.result.suggestions;
    } catch (error) {
      console.error('Error getting roadmap suggestions:', error);
      throw error;
    }
  }

  // Get specific roadmap
  async getRoadmap(roadmapId: string): Promise<Roadmap> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/roadmap/${roadmapId}`, {
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.roadmap;
    } catch (error) {
      console.error('Error fetching roadmap:', error);
      throw error;
    }
  }

  // Get all roadmaps
  async getAllRoadmaps(): Promise<Record<string, Roadmap>> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/roadmap`, {
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.roadmaps;
    } catch (error) {
      console.error('Error fetching all roadmaps:', error);
      throw error;
    }
  }

  // Delete roadmap
  async deleteRoadmap(roadmapId: string): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/roadmap/${roadmapId}`, {
        method: 'DELETE',
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.success;
    } catch (error) {
      console.error('Error deleting roadmap:', error);
      throw error;
    }
  }

  // Start agent manager
  async startAgentManager(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/start`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.success;
    } catch (error) {
      console.error('Error starting agent manager:', error);
      throw error;
    }
  }

  // Stop agent manager
  async stopAgentManager(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/stop`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.success;
    } catch (error) {
      console.error('Error stopping agent manager:', error);
      throw error;
    }
  }

  // Get system status
  async getSystemStatus(): Promise<SystemStatus> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/system/status`, {
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.system_status;
    } catch (error) {
      console.error('Error fetching system status:', error);
      throw error;
    }
  }

  // Clear agent statistics
  async clearAgentStatistics(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/agents/clear-stats`, {
        method: 'POST',
        headers: await this.getAuthHeaders(),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.success;
    } catch (error) {
      console.error('Error clearing agent statistics:', error);
      throw error;
    }
  }
}

export const agentService = new AgentService();
