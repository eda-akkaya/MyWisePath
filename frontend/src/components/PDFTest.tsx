import React, { useState } from 'react';
import { Box, Button, Typography, Alert } from '@mui/material';
import { pdfService } from '../services/pdfService';

const PDFTest: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const testPDFGeneration = async () => {
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      // Test progress verisi (backend çalışmadığı için mock data kullanıyoruz)
      const testProgress = {
        overall_progress: 75,
        completed_modules: 3,
        total_modules: 4,
        total_time_spent_minutes: 180,
        roadmaps: [
          {
            roadmap_id: "test_1",
            overall_progress: 75,
            completed_modules: 3,
            total_modules: 4,
            total_time_spent_minutes: 180,
            started_at: "2024-01-01"
          }
        ]
      };

      console.log('Test PDF oluşturma başlatılıyor...');
      const response = await pdfService.generateProgressPDF(testProgress);
      
      if (response.success) {
        setResult(response.message);
        console.log('PDF oluşturma başarılı:', response);
      } else {
        setError(response.error || 'PDF oluşturma başarısız');
        console.error('PDF oluşturma hatası:', response);
      }
    } catch (err: any) {
      setError(err.message || 'Beklenmeyen hata');
      console.error('Test hatası:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3, maxWidth: 600, mx: 'auto' }}>
      <Typography variant="h4" gutterBottom>
        PDF Generator Test
      </Typography>
      
      <Typography variant="body1" sx={{ mb: 3 }}>
        Bu sayfa PDF Generator'ı test etmek için oluşturulmuştur.
      </Typography>

      <Button
        variant="contained"
        onClick={testPDFGeneration}
        disabled={loading}
        sx={{ mb: 3 }}
      >
        {loading ? 'PDF Oluşturuluyor...' : 'Test PDF Oluştur'}
      </Button>

      {result && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {result}
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Typography variant="body2" color="text.secondary">
        Test sonuçları console'da da görüntülenir.
      </Typography>
    </Box>
  );
};

export default PDFTest;
