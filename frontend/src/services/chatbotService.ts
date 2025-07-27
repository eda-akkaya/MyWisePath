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

export interface ChatRequest {
  message: string;
  user_id?: string;
}

export interface ChatResponse {
  message: string;
  timestamp: string;
  success: boolean;
}

export interface WelcomeMessage {
  message: string;
  timestamp: string;
}

export interface RoadmapGenerationResponse {
  roadmap: any;
  analysis: any;
  message: string;
  timestamp: string;
  success: boolean;
}

export interface ContentRecommendation {
  title: string;
  platform: string;
  url: string;
  type: string;
  duration: string;
  free: boolean;
  description: string;
}

export interface ContentRecommendationsResponse {
  topic: string;
  skill_level: string;
  recommendations: ContentRecommendation[];
  total_count: number;
  timestamp: string;
}

export interface EducationSearchRequest {
  query: string;
  skill_level?: string;
  limit?: number;
}

export interface EducationSearchResponse {
  query: string;
  skill_level: string;
  results: ContentRecommendation[];
  total_count: number;
  timestamp: string;
  ai_generated: boolean;
}

export interface PopularEducationResponse {
  popular_content: ContentRecommendation[];
  total_count: number;
  timestamp: string;
  ai_generated: boolean;
}

class ChatbotService {
  async sendMessage(message: string): Promise<ChatResponse> {
    try {
      const response = await api.post<ChatResponse>('/api/v1/chatbot/query', {
        message,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Mesaj gönderilemedi');
      }
      throw new Error('Mesaj gönderilemedi');
    }
  }

  async generateRoadmap(message: string): Promise<RoadmapGenerationResponse> {
    try {
      const response = await api.post<RoadmapGenerationResponse>('/api/v1/chatbot/generate-roadmap', {
        message,
      });
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

  async getContentRecommendations(topic: string, skillLevel: string = 'beginner'): Promise<ContentRecommendationsResponse> {
    try {
      const response = await api.get<ContentRecommendationsResponse>(`/api/v1/chatbot/content-recommendations/${topic}`, {
        params: { skill_level: skillLevel }
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'İçerik önerileri alınamadı');
      }
      throw new Error('İçerik önerileri alınamadı');
    }
  }

  async getWelcomeMessage(): Promise<WelcomeMessage> {
    try {
      const response = await api.get<WelcomeMessage>('/api/v1/chatbot/welcome');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Karşılama mesajı alınamadı');
      }
      throw new Error('Karşılama mesajı alınamadı');
    }
  }

  async searchEducationContent(request: EducationSearchRequest): Promise<EducationSearchResponse> {
    try {
      const response = await api.post<EducationSearchResponse>('/api/v1/chatbot/search-education', {
        query: request.query,
        skill_level: request.skill_level || 'beginner',
        limit: request.limit || 5
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Eğitim araması yapılamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Eğitim araması yapılamadı');
    }
  }

  async getPopularEducation(limit: number = 5): Promise<PopularEducationResponse> {
    try {
      const response = await api.get<PopularEducationResponse>('/api/v1/chatbot/popular-education', {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Popüler eğitimler alınamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Popüler eğitimler alınamadı');
    }
  }
}

export const chatbotService = new ChatbotService(); 