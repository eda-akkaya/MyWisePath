import { authService } from './authService';

export interface PDFGenerationRequest {
  type: 'roadmap' | 'progress' | 'summary';
  data: any;
  userInfo?: {
    name: string;
    email: string;
  };
}

export interface PDFGenerationResponse {
  success: boolean;
  message: string;
  fileUrl?: string;
  error?: string;
}

class PDFService {
  private baseURL = 'http://localhost:8000/api/v1';

  async generateRoadmapPDF(roadmapData: any): Promise<PDFGenerationResponse> {
    try {
      console.log('PDF oluşturma isteği gönderiliyor:', roadmapData);

      const response = await fetch(`${this.baseURL}/rag/generate-pdf/roadmap`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(roadmapData),
      });

      console.log('PDF response status:', response.status);
      console.log('PDF response headers:', response.headers);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'PDF oluşturma hatası');
      }

      // PDF dosyasını indir
      const blob = await response.blob();
      console.log('PDF blob size:', blob.size);
      console.log('PDF blob type:', blob.type);

      if (blob.size === 0) {
        throw new Error('PDF dosyası boş oluşturuldu');
      }

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `roadmap_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      return {
        success: true,
        message: 'Roadmap PDF\'i başarıyla oluşturuldu ve indirildi!',
        fileUrl: url
      };

    } catch (error: any) {
      console.error('Roadmap PDF oluşturma hatası:', error);
      return {
        success: false,
        message: error.message || 'PDF oluşturulurken bir hata oluştu',
        error: error.message
      };
    }
  }

  async generateProgressPDF(progressData: any): Promise<PDFGenerationResponse> {
    try {
      const response = await fetch(`${this.baseURL}/rag/generate-pdf/progress`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(progressData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'PDF oluşturma hatası');
      }

      // PDF dosyasını indir
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `progress_report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      return {
        success: true,
        message: 'İlerleme raporu PDF\'i başarıyla oluşturuldu ve indirildi!',
        fileUrl: url
      };

    } catch (error: any) {
      console.error('İlerleme raporu PDF oluşturma hatası:', error);
      return {
        success: false,
        message: error.message || 'PDF oluşturulurken bir hata oluştu',
        error: error.message
      };
    }
  }

  async generateSummaryPDF(summaryData: any): Promise<PDFGenerationResponse> {
    try {
      const response = await fetch(`${this.baseURL}/rag/generate-pdf/summary`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(summaryData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'PDF oluşturma hatası');
      }

      // PDF dosyasını indir
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `learning_summary_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      return {
        success: true,
        message: 'Öğrenme özeti PDF\'i başarıyla oluşturuldu ve indirildi!',
        fileUrl: url
      };

    } catch (error: any) {
      console.error('Öğrenme özeti PDF oluşturma hatası:', error);
      return {
        success: false,
        message: error.message || 'PDF oluşturulurken bir hata oluştu',
        error: error.message
      };
    }
  }

  async cleanupOldPDFs(daysToKeep: number = 7): Promise<PDFGenerationResponse> {
    try {
      const token = authService.getToken();
      if (!token) {
        throw new Error('Oturum bulunamadı');
      }

      const response = await fetch(`${this.baseURL}/rag/cleanup-pdfs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ days_to_keep: daysToKeep }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'PDF temizleme hatası');
      }

      const data = await response.json();

      return {
        success: true,
        message: data.message || 'Eski PDF dosyaları başarıyla temizlendi!'
      };

    } catch (error: any) {
      console.error('PDF temizleme hatası:', error);
      return {
        success: false,
        message: error.message || 'PDF temizleme sırasında bir hata oluştu',
        error: error.message
      };
    }
  }

  async getPDFStats(): Promise<any> {
    try {
      const token = authService.getToken();
      if (!token) {
        throw new Error('Oturum bulunamadı');
      }

      const response = await fetch(`${this.baseURL}/rag/stats`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'İstatistik alma hatası');
      }

      return await response.json();

    } catch (error: any) {
      console.error('PDF istatistik alma hatası:', error);
      throw error;
    }
  }
}

export const pdfService = new PDFService();
