import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  TextField,
  Paper,
  Chip,
  Alert,
  Divider,
} from '@mui/material';
import {
  School,
  Map,
  Lightbulb,
  PlayArrow,
  ArrowForward,
} from '@mui/icons-material';
import EducationalContent, { EducationalContentItem } from '../components/EducationalContent';
import { chatbotService } from '../services/chatbotService';

const Demo: React.FC = () => {
  const [userInput, setUserInput] = useState('');
  const [roadmap, setRoadmap] = useState<any>(null);
  const [contentRecommendations, setContentRecommendations] = useState<EducationalContentItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const exampleQueries = [
    "Python öğrenmek istiyorum",
    "Veri bilimi alanında kariyer yapmak istiyorum",
    "Web geliştirme öğrenmek istiyorum",
    "Makine öğrenmesi konusunda uzmanlaşmak istiyorum",
    "React.js öğrenmek istiyorum",
  ];

  const handleGenerateRoadmap = async () => {
    if (!userInput.trim()) return;

    setLoading(true);
    setError('');
    
    try {
      const response = await chatbotService.generateRoadmap(userInput);
      setRoadmap(response.roadmap);
      
      // İlk öğrenme alanı için içerik önerilerini al
      if (response.analysis.learning_areas.length > 0) {
        const area = response.analysis.learning_areas[0];
        const contentResponse = await chatbotService.getContentRecommendations(area, response.analysis.skill_level);
        setContentRecommendations(contentResponse.recommendations);
      }
    } catch (err) {
      setError('Yol haritası oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.');
      console.error('Roadmap generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example: string) => {
    setUserInput(example);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
        <School sx={{ mr: 2, verticalAlign: 'middle' }} />
                 MyWisePath Demo - Bilge Rehber ✨
      </Typography>

      <Alert severity="info" sx={{ mb: 4 }}>
        <Typography variant="body1">
          Bu demo, MyWisePath'in yapay zeka destekli öğrenme asistanının nasıl çalıştığını gösterir. 
          Bir konu hakkında yazın ve size özel yol haritası ile eğitim içerik önerileri alın!
        </Typography>
      </Alert>

      {/* Input Section */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Lightbulb color="primary" />
            Ne Öğrenmek İstiyorsunuz?
          </Typography>
          
          <TextField
            fullWidth
            multiline
            rows={3}
            placeholder="Örnek: Python programlama öğrenmek istiyorum, veri bilimi alanında kariyer yapmak istiyorum..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            sx={{ mb: 2 }}
          />

          <Box sx={{ mb: 2 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Örnek sorgular:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {exampleQueries.map((example, index) => (
                <Chip
                  key={index}
                  label={example}
                  onClick={() => handleExampleClick(example)}
                  variant="outlined"
                  clickable
                  size="small"
                />
              ))}
            </Box>
          </Box>

          <Button
            variant="contained"
            size="large"
            onClick={handleGenerateRoadmap}
            disabled={!userInput.trim() || loading}
            startIcon={loading ? null : <Map />}
            sx={{ minWidth: 200 }}
          >
            {loading ? 'Oluşturuluyor...' : 'Yol Haritası Oluştur'}
          </Button>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Results Section */}
      {roadmap && (
        <>
          {/* Roadmap Display */}
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Map color="primary" />
                {roadmap.title}
              </Typography>
              
              <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                {roadmap.description}
              </Typography>

              <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
                <Chip 
                  label={`${roadmap.modules.length} Modül`} 
                  color="primary" 
                  variant="outlined" 
                />
                <Chip 
                  label={`${roadmap.total_estimated_hours} Saat`} 
                  color="secondary" 
                  variant="outlined" 
                />
                <Chip 
                  label={`%${roadmap.overall_progress} Tamamlandı`} 
                  color="success" 
                  variant="outlined" 
                />
              </Box>

              <Typography variant="h6" gutterBottom>
                Modüller:
              </Typography>
              
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2 }}>
                {roadmap.modules.map((module: any, index: number) => (
                  <Paper key={module.id} sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Typography variant="subtitle1" fontWeight="medium" gutterBottom>
                      {index + 1}. {module.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      {module.description}
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      <Chip 
                        label={module.difficulty} 
                        size="small" 
                        color={module.difficulty === 'beginner' ? 'success' : module.difficulty === 'intermediate' ? 'warning' : 'error'}
                        variant="outlined"
                      />
                      <Chip 
                        label={`${module.estimated_hours} saat`} 
                        size="small" 
                        variant="outlined"
                      />
                    </Box>
                  </Paper>
                ))}
              </Box>
            </CardContent>
          </Card>

          {/* Educational Content Recommendations */}
          {contentRecommendations.length > 0 && (
            <Card>
              <CardContent>
                <EducationalContent
                  title="Önerilen Eğitim İçerikleri"
                  content={contentRecommendations}
                />
              </CardContent>
            </Card>
          )}
        </>
      )}

      {/* Features Section */}
      <Box sx={{ mt: 6 }}>
        <Typography variant="h5" gutterBottom sx={{ textAlign: 'center', mb: 4 }}>
          Özellikler
        </Typography>
        
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr 1fr' }, gap: 3 }}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <School sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Akıllı Analiz
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Yapay zeka ile kullanıcı isteklerini analiz eder ve uygun öğrenme alanlarını belirler.
              </Typography>
            </CardContent>
          </Card>

          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Map sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Kişiselleştirilmiş Yol Haritası
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Kullanıcının seviyesine ve hedeflerine uygun detaylı öğrenme yol haritası oluşturur.
              </Typography>
            </CardContent>
          </Card>

          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <PlayArrow sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Eğitim İçerik Önerileri
              </Typography>
              <Typography variant="body2" color="text.secondary">
                En iyi eğitim platformlarından seçilmiş içeriklerle öğrenme sürecini destekler.
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Container>
  );
};

export default Demo; 