import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Axios instance oluştur
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 saniye timeout
});

// Request interceptor - token ekle
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - hata yönetimi
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    
    // HTML response kontrolü
    if (error.response && error.response.data && typeof error.response.data === 'string') {
      if (error.response.data.includes('<!DOCTYPE') || error.response.data.includes('<html')) {
        console.error('HTML response received instead of JSON');
        throw new Error('Sunucu hatası: Geçersiz yanıt formatı. Lütfen sayfayı yenileyin.');
      }
    }
    
    // Network hatası
    if (error.code === 'ECONNABORTED') {
      throw new Error('Bağlantı zaman aşımı. Lütfen tekrar deneyin.');
    }
    
    if (error.code === 'ERR_NETWORK') {
      throw new Error('Ağ bağlantısı hatası. Backend çalışıyor mu kontrol edin.');
    }
    
    // HTTP hata kodları
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;
      
      switch (status) {
        case 401:
          localStorage.removeItem('token');
          throw new Error('Oturum süreniz dolmuş. Lütfen tekrar giriş yapın.');
        case 403:
          throw new Error('Bu işlem için yetkiniz yok.');
        case 404:
          throw new Error('İstenen kaynak bulunamadı.');
        case 500:
          throw new Error('Sunucu hatası. Lütfen daha sonra tekrar deneyin.');
        default:
          throw new Error(data?.detail || `HTTP ${status} hatası`);
      }
    }
    
    throw new Error('Beklenmeyen bir hata oluştu.');
  }
);

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
  target_email?: string;
}

export { api };

export const authService = {
  async login(email: string, password: string): Promise<UserResponse> {
    try {
      const response = await api.post<UserResponse>('/api/v1/auth/login', {
        email,
        password,
      });
      
      // Store token in localStorage
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
      }
      
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
      
      // Store token in localStorage
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
      }
      
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

  async updateProfile(userData: UserProfile): Promise<UserProfile> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token bulunamadı');
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/auth/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      throw new Error('Profil güncellenemedi');
    }

    return response.json();
  },

  async changePassword(currentPassword: string, newPassword: string): Promise<{ message: string }> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token bulunamadı');
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/auth/change-password`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword
      })
    });

    if (!response.ok) {
      throw new Error('Şifre değiştirilemedi');
    }

    return response.json();
  },

  async deleteAccount(): Promise<{ message: string }> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token bulunamadı');
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/auth/delete-account`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error('Hesap silinemedi');
    }

    localStorage.removeItem('token');
    return response.json();
  },

  // Email automation methods
  async getEmailSettings(): Promise<EmailSettings> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Token bulunamadı');
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/automation/email-settings`, {
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

    const response = await fetch(`${API_BASE_URL}/api/v1/automation/email-settings`, {
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

    const response = await fetch(`${API_BASE_URL}/api/v1/automation/send-instant-email`, {
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
  },

  // Token yönetimi
  getToken(): string | null {
    return localStorage.getItem('token');
  },

  setToken(token: string): void {
    localStorage.setItem('token', token);
  },

  removeToken(): void {
    localStorage.removeItem('token');
  },

  isLoggedIn(): boolean {
    return this.getToken() !== null;
  }
}; 