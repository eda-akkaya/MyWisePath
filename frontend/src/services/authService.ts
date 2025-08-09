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
  // Email automation preferences
  email_frequency?: string;
  weekly_reminders_enabled?: boolean;
  progress_reports_enabled?: boolean;
  instant_email_enabled?: boolean;
}

export interface UserProfileUpdate {
  skill_level?: string;
  interests?: string[];
  learning_goals?: string[];
  // Email automation preferences
  email_frequency?: string;
  weekly_reminders_enabled?: boolean;
  progress_reports_enabled?: boolean;
  instant_email_enabled?: boolean;
}

export interface EmailSettings {
  email_frequency: string;
  weekly_reminders_enabled: boolean;
  progress_reports_enabled: boolean;
  instant_email_enabled: boolean;
}

export interface InstantEmailRequest {
  email_type: string;
  custom_message?: string;
}

export const authService = {
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
  },

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
  },

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
  },

  async updateUserProfile(profileUpdate: UserProfileUpdate): Promise<UserProfile> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token bulunamadı');
    }

    const response = await fetch(`${API_BASE_URL}/auth/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(profileUpdate)
    });

    if (!response.ok) {
      throw new Error('Profil güncellenemedi');
    }

    return response.json();
  },

  // Email automation methods
  async getEmailSettings(): Promise<EmailSettings> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token bulunamadı');
    }

    const response = await fetch(`${API_BASE_URL}/automation/email-settings`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('E-posta ayarları alınamadı');
    }

    return response.json();
  },

  async updateEmailSettings(settings: EmailSettings): Promise<{ message: string; settings: EmailSettings }> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token bulunamadı');
    }

    const response = await fetch(`${API_BASE_URL}/automation/email-settings`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(settings)
    });

    if (!response.ok) {
      throw new Error('E-posta ayarları güncellenemedi');
    }

    return response.json();
  },

  async sendInstantEmail(request: InstantEmailRequest): Promise<{ message: string; email_type: string }> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token bulunamadı');
    }

    const response = await fetch(`${API_BASE_URL}/automation/send-instant-email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error('Anında e-posta gönderilemedi');
    }

    return response.json();
  }
}; 