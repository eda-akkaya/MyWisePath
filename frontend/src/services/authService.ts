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

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface UserResponse {
  id: string;
  username: string;
  email: string;
  created_at: string;
  token: string;
}

export interface UserProfile {
  id: string;
  username: string;
  email: string;
  created_at: string;
  learning_goals?: string[];
  skill_level?: string;
  interests?: string[];
}

class AuthService {
  async login(email: string, password: string): Promise<UserResponse> {
    try {
      const response = await api.post<UserResponse>('/api/v1/auth/login', {
        email,
        password,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Giriş başarısız');
      }
      throw new Error('Giriş başarısız');
    }
  }

  async register(username: string, email: string, password: string): Promise<UserResponse> {
    try {
      const response = await api.post<UserResponse>('/api/v1/auth/register', {
        username,
        email,
        password,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Kayıt başarısız');
      }
      throw new Error('Kayıt başarısız');
    }
  }

  async getCurrentUser(token: string): Promise<UserProfile> {
    try {
      const response = await api.get<UserProfile>('/api/v1/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Kullanıcı bilgileri alınamadı');
      }
      throw new Error('Kullanıcı bilgileri alınamadı');
    }
  }
}

export const authService = new AuthService(); 