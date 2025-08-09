import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Paper,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
  Stepper,
  Step,
  StepLabel,
  Alert,
  Fade,
  Grow,
  IconButton,
  Divider,
} from '@mui/material';
import {
  School,
  ArrowBack,
  Timeline,
  CheckCircle,
  PlayArrow,
  AutoAwesome,
  TrendingUp,
  Psychology,
  Schedule,
  Star,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { roadmapService, RoadmapRequest } from '../services/roadmapService';

interface RoadmapForm {
  skill_level: string;
  interests: string[];
  learning_goals: string[];
  available_hours_per_week: number;
  target_timeline_months: number;
}

const Roadmap: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState<RoadmapForm>({
    skill_level: 'beginner',
    interests: [],
    learning_goals: [],
    available_hours_per_week: 10,
    target_timeline_months: 6,
  });
  const [roadmap, setRoadmap] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const steps = ['Bilgi Seviyesi', 'İlgi Alanları', 'Hedefler', 'Zaman Planı', 'Yol Haritası'];

  const skillLevels = [
    { value: 'beginner', label: 'Başlangıç', icon: '🌱', description: 'Yeni başlayanlar için' },
    { value: 'intermediate', label: 'Orta', icon: '🚀', description: 'Temel bilgisi olanlar için' },
    { value: 'advanced', label: 'İleri', icon: '⚡', description: 'Deneyimli kullanıcılar için' },
  ];

  const interestOptions = [
    'Veri Bilimi',
    'Web Geliştirme',
    'Mobil Uygulama',
    'AI & Machine Learning',
    'Siber Güvenlik',
    'DevOps',
    'UI/UX Tasarım',
    'Blockchain',
  ];

  const goalOptions = [
    'Kariyer Değişikliği',
    'Yeni Teknoloji Öğrenme',
    'Sertifika Alma',
    'Proje Geliştirme',
    'Freelance İş',
    'Araştırma',
  ];

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const handleGoalToggle = (goal: string) => {
    setFormData(prev => ({
      ...prev,
      learning_goals: prev.learning_goals.includes(goal)
        ? prev.learning_goals.filter(g => g !== goal)
        : [...prev.learning_goals, goal]
    }));
  };

  const generateRoadmap = async () => {
    setLoading(true);
    try {
      const request: RoadmapRequest = {
        skill_level: formData.skill_level,
        interests: formData.interests,
        learning_goals: formData.learning_goals,
        available_hours_per_week: formData.available_hours_per_week,
        target_timeline_months: formData.target_timeline_months,
      };

      const response = await roadmapService.generateRoadmap(request);
      setRoadmap(response);
      handleNext();
    } catch (error) {
      console.error('Yol haritası oluşturma hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Grow in={true} timeout={800}>
            <Box>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                📊 Bilgi Seviyenizi Belirleyin
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Mevcut bilgi seviyenizi seçin, böylece size en uygun yol haritasını oluşturabiliriz.
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr 1fr' }, gap: 3 }}>
                {skillLevels.map((level) => (
                  <Card
                    key={level.value}
                    sx={{
                      cursor: 'pointer',
                      transition: 'all 0.3s ease-in-out',
                      border: formData.skill_level === level.value ? '2px solid' : '1px solid',
                      borderColor: formData.skill_level === level.value ? 'primary.main' : 'grey.300',
                      '&:hover': {
                        transform: 'translateY(-4px)',
                        boxShadow: '0 8px 25px rgba(0, 0, 0, 0.1)',
                      },
                    }}
                    onClick={() => setFormData(prev => ({ ...prev, skill_level: level.value }))}
                  >
                    <CardContent sx={{ textAlign: 'center', p: 3 }}>
                      <Typography variant="h3" sx={{ mb: 1 }}>
                        {level.icon}
                      </Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                        {level.label}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {level.description}
                      </Typography>
                    </CardContent>
                  </Card>
                ))}
              </Box>
            </Box>
          </Grow>
        );

      case 1:
        return (
          <Grow in={true} timeout={800}>
            <Box>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                🔥 İlgi Alanlarınızı Seçin
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Hangi teknoloji alanlarında kendinizi geliştirmek istiyorsunuz?
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                {interestOptions.map((interest) => (
                  <Chip
                    key={interest}
                    label={interest}
                    onClick={() => handleInterestToggle(interest)}
                    color={formData.interests.includes(interest) ? 'primary' : 'default'}
                    variant={formData.interests.includes(interest) ? 'filled' : 'outlined'}
                    icon={formData.interests.includes(interest) ? <AutoAwesome /> : undefined}
                    sx={{
                      fontSize: '1rem',
                      py: 1,
                      '&:hover': {
                        transform: 'scale(1.05)',
                      },
                    }}
                  />
                ))}
              </Box>
            </Box>
          </Grow>
        );

      case 2:
        return (
          <Grow in={true} timeout={800}>
            <Box>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                🎯 Öğrenme Hedeflerinizi Belirleyin
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Bu yolculukta neyi başarmak istiyorsunuz?
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                {goalOptions.map((goal) => (
                  <Chip
                    key={goal}
                    label={goal}
                    onClick={() => handleGoalToggle(goal)}
                    color={formData.learning_goals.includes(goal) ? 'secondary' : 'default'}
                    variant={formData.learning_goals.includes(goal) ? 'filled' : 'outlined'}
                    icon={formData.learning_goals.includes(goal) ? <Star /> : undefined}
                    sx={{
                      fontSize: '1rem',
                      py: 1,
                      '&:hover': {
                        transform: 'scale(1.05)',
                      },
                    }}
                  />
                ))}
              </Box>
            </Box>
          </Grow>
        );

      case 3:
        return (
          <Grow in={true} timeout={800}>
            <Box>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                ⏰ Zaman Planınızı Belirleyin
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Haftalık ne kadar zaman ayırabilirsiniz ve hedefinize ne kadar sürede ulaşmak istiyorsunuz?
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 4 }}>
                <Box>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                    <Schedule sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Haftalık Çalışma Saati
                  </Typography>
                  <TextField
                    fullWidth
                    type="number"
                    value={formData.available_hours_per_week}
                    onChange={(e) => setFormData(prev => ({ 
                      ...prev, 
                      available_hours_per_week: parseInt(e.target.value) 
                    }))}
                    InputProps={{
                      endAdornment: <Typography variant="body2">saat/hafta</Typography>,
                    }}
                    sx={{ mb: 2 }}
                  />
                  <LinearProgress 
                    variant="determinate" 
                    value={(formData.available_hours_per_week / 40) * 100}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
                <Box>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                    <TrendingUp sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Hedef Süre
                  </Typography>
                  <TextField
                    fullWidth
                    type="number"
                    value={formData.target_timeline_months}
                    onChange={(e) => setFormData(prev => ({ 
                      ...prev, 
                      target_timeline_months: parseInt(e.target.value) 
                    }))}
                    InputProps={{
                      endAdornment: <Typography variant="body2">ay</Typography>,
                    }}
                    sx={{ mb: 2 }}
                  />
                  <LinearProgress 
                    variant="determinate" 
                    value={(formData.target_timeline_months / 24) * 100}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>
              </Box>
            </Box>
          </Grow>
        );

      case 4:
        return (
          <Grow in={true} timeout={800}>
            <Box>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                🎉 Yol Haritanız Hazır!
              </Typography>
              {roadmap && (
                <Card sx={{ mb: 3, borderRadius: 4 }}>
                  <CardContent sx={{ p: 4 }}>
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                      📋 Özet
                    </Typography>
                    <Typography variant="body1" sx={{ mb: 3 }}>
                      {roadmap.summary}
                    </Typography>
                    <Divider sx={{ my: 3 }} />
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                      🗓️ Aşamalar
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      {roadmap.phases?.map((phase: any, index: number) => (
                        <Paper key={index} sx={{ p: 3, borderRadius: 3 }}>
                          <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                            Aşama {index + 1}: {phase.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {phase.description}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                            {phase.topics?.map((topic: string, topicIndex: number) => (
                              <Chip
                                key={topicIndex}
                                label={topic}
                                size="small"
                                variant="outlined"
                                icon={<CheckCircle />}
                              />
                            ))}
                          </Box>
                        </Paper>
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              )}
            </Box>
          </Grow>
        );

      default:
        return null;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 4 }}>
      {/* Page Title */}
      <Fade in={true} timeout={800}>
        <Box sx={{ 
          mb: 4,
          p: 3,
          borderRadius: 4,
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(0, 0, 0, 0.08)',
        }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Timeline sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              Yol Haritası Oluştur
            </Typography>
          </Box>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Kişiselleştirilmiş öğrenme yolculuğunuzu planlayın
          </Typography>
        </Box>
      </Fade>

      {/* Stepper */}
      <Paper sx={{ p: 3, mb: 4, borderRadius: 4 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Paper>

      {/* Content */}
      <Paper sx={{ 
        p: 4, 
        borderRadius: 4,
        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(0, 0, 0, 0.08)',
      }}>
        {renderStepContent(activeStep)}

        {/* Navigation */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            disabled={activeStep === 0}
            onClick={handleBack}
            startIcon={<ArrowBack />}
            variant="outlined"
            sx={{
              borderColor: 'primary.main',
              color: 'primary.main',
              '&:hover': {
                borderColor: 'primary.dark',
                backgroundColor: 'primary.main',
                color: 'white',
              },
            }}
          >
            Geri
          </Button>
          <Box>
            {activeStep === steps.length - 2 ? (
              <Button
                variant="contained"
                onClick={generateRoadmap}
                disabled={loading}
                startIcon={<AutoAwesome />}
                size="large"
                sx={{
                  background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 25px rgba(99, 102, 241, 0.3)',
                  },
                }}
              >
                {loading ? 'Oluşturuluyor...' : 'Yol Haritası Oluştur'}
              </Button>
            ) : activeStep === steps.length - 1 ? (
              <Button
                variant="contained"
                onClick={() => navigate('/dashboard')}
                startIcon={<PlayArrow />}
                size="large"
                sx={{
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 25px rgba(16, 185, 129, 0.3)',
                  },
                }}
              >
                Başla
              </Button>
            ) : (
              <Button
                variant="contained"
                onClick={handleNext}
                endIcon={<PlayArrow />}
                size="large"
                sx={{
                  background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 25px rgba(99, 102, 241, 0.3)',
                  },
                }}
              >
                İleri
              </Button>
            )}
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default Roadmap; 