import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Axios instance oluştur
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - token ekle
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface RoadmapRequest {
  skill_level: string;
  interests: string[];
  learning_goals: string[];
  available_hours_per_week: number;
  target_timeline_months: number;
}

export interface RoadmapResponse {
  id: string;
  user_id: string;
  title: string;
  description: string;
  created_at: string;
  modules: any[];
  learning_goals: any[];
  skill_assessments: any[];
  total_estimated_hours: number;
  completed_modules: number;
  overall_progress: number;
}

class RoadmapService {
  async generateRoadmap(request: RoadmapRequest): Promise<RoadmapResponse> {
    try {
      const response = await api.post<RoadmapResponse>('/api/v1/roadmap/generate', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Yol haritası oluşturulamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Yol haritası oluşturulamadı');
    }
  }

  async getUserRoadmaps(): Promise<RoadmapResponse[]> {
    try {
      const response = await api.get<RoadmapResponse[]>('/api/v1/roadmap/user');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Yol haritaları alınamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Yol haritaları alınamadı');
    }
  }

  async getRoadmapById(roadmapId: string): Promise<RoadmapResponse> {
    try {
      const response = await api.get<RoadmapResponse>(`/api/v1/roadmap/${roadmapId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Yol haritası bulunamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Yol haritası bulunamadı');
    }
  }
}

export const roadmapService = new RoadmapService(); 