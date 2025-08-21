import axios from 'axios';

// authService'den aynı axios instance'ını kullan
import { api } from './authService';

export interface ProgressData {
  module_id: string;
  progress_percentage: number;
  time_spent_minutes: number;
  status: 'not_started' | 'in_progress' | 'completed' | 'paused';
  notes?: string;
}

export interface QuizSubmission {
  module_id: string;
  quiz_id: string;
  answers: Record<string, string>;
  time_taken_minutes: number;
}

export interface ModuleProgress {
  module_id: string;
  roadmap_id: string;
  user_id: string;
  status: string;
  progress_percentage: number;
  time_spent_minutes: number;
  started_at?: string;
  completed_at?: string;
  last_activity?: string;
  notes?: string;
  quiz_results: any[];
}

export interface RoadmapProgress {
  roadmap_id: string;
  user_id: string;
  overall_progress: number;
  completed_modules: number;
  total_modules: number;
  total_time_spent_minutes: number;
  started_at?: string;
  estimated_completion_date?: string;
  last_activity?: string;
  module_progress: ModuleProgress[];
}

export interface UserProgressSummary {
  total_roadmaps: number;
  total_time_spent_minutes: number;
  total_completed_modules: number;
  total_modules: number;
  overall_completion_rate: number;
  roadmaps: RoadmapProgress[];
}

export interface RoadmapStats {
  roadmap_id: string;
  overall_progress: number;
  completed_modules: number;
  total_modules: number;
  total_time_spent_hours: number;
  total_quiz_attempts: number;
  average_quiz_score: number;
  estimated_completion_date?: string;
  started_at?: string;
  last_activity?: string;
}

class ProgressService {
  async getRoadmapProgress(roadmapId: string): Promise<RoadmapProgress> {
    try {
      const response = await api.get<RoadmapProgress>(`/api/v1/progress/roadmap/${roadmapId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Roadmap ilerlemesi alınamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Roadmap ilerlemesi alınamadı');
    }
  }

  async updateModuleProgress(roadmapId: string, update: ProgressData): Promise<ModuleProgress> {
    try {
      const response = await api.post<{ message: string; module_progress: ModuleProgress }>(
        `/api/v1/progress/roadmap/${roadmapId}/module`,
        update
      );
      return response.data.module_progress;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Modül ilerlemesi güncellenemedi';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Modül ilerlemesi güncellenemedi');
    }
  }

  async submitQuiz(roadmapId: string, submission: QuizSubmission): Promise<any> {
    try {
      const response = await api.post<{ message: string; quiz_result: any; passed: boolean }>(
        `/api/v1/progress/roadmap/${roadmapId}/quiz`,
        submission
      );
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Quiz sonucu gönderilemedi';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Quiz sonucu gönderilemedi');
    }
  }

  async getUserProgressSummary(): Promise<UserProgressSummary> {
    try {
      const response = await api.get<UserProgressSummary>('/api/v1/progress/summary');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'İlerleme özeti alınamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: İlerleme özeti alınamadı');
    }
  }

  async getWeeklyProgress(roadmapId: string): Promise<any> {
    try {
      const response = await api.get(`/api/v1/progress/roadmap/${roadmapId}/weekly`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Haftalık ilerleme alınamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Haftalık ilerleme alınamadı');
    }
  }

  async startRoadmap(roadmapId: string): Promise<RoadmapProgress> {
    try {
      const response = await api.post<{ message: string; roadmap_progress: RoadmapProgress }>(
        `/api/v1/progress/roadmap/${roadmapId}/start`
      );
      return response.data.roadmap_progress;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Roadmap başlatılamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Roadmap başlatılamadı');
    }
  }

  async completeModule(roadmapId: string, moduleId: string): Promise<ModuleProgress> {
    try {
      const response = await api.post<{ message: string; module_progress: ModuleProgress }>(
        `/api/v1/progress/roadmap/${roadmapId}/module/${moduleId}/complete`
      );
      return response.data.module_progress;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Modül tamamlanamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Modül tamamlanamadı');
    }
  }

  async getRoadmapStats(roadmapId: string): Promise<RoadmapStats> {
    try {
      const response = await api.get<RoadmapStats>(`/api/v1/progress/roadmap/${roadmapId}/stats`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const statusCode = error.response?.status;
        const detail = error.response?.data?.detail || 'Roadmap istatistikleri alınamadı';
        throw new Error(`${statusCode}: ${detail}`);
      }
      throw new Error('500: Roadmap istatistikleri alınamadı');
    }
  }
}

export const progressService = new ProgressService();
