import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Grid,
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
} from '@mui/material';
import {
  School,
  ArrowBack,
  Timeline,
  CheckCircle,
  PlayArrow,
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
    { value: 'beginner', label: 'Başlangıç' },
    { value: 'intermediate', label: 'Orta' },
    { value: 'advanced', label: 'İleri' },
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
      // Backend API çağrısı
      const roadmapRequest: RoadmapRequest = {
        skill_level: formData.skill_level,
        interests: formData.interests,
        learning_goals: formData.learning_goals,
        available_hours_per_week: formData.available_hours_per_week,
        target_timeline_months: formData.target_timeline_months,
      };
      
      const response = await roadmapService.generateRoadmap(roadmapRequest);
      setRoadmap(response);
      setActiveStep(4);
    } catch (error) {
      console.error('Roadmap oluşturma hatası:', error);
      // Hata durumunda kullanıcıya bilgi ver
      alert('Yol haritası oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      setLoading(false);
    }
  };

  const renderStepContent = (step: number) => {
    switch (step) {
      case 0:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Mevcut Bilgi Seviyeniz Nedir?
            </Typography>
            <FormControl fullWidth sx={{ mt: 2 }}>
              <InputLabel>Bilgi Seviyesi</InputLabel>
              <Select
                value={formData.skill_level}
                label="Bilgi Seviyesi"
                onChange={(e) => setFormData(prev => ({ ...prev, skill_level: e.target.value }))}
              >
                {skillLevels.map((level) => (
                  <MenuItem key={level.value} value={level.value}>
                    {level.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        );

      case 1:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Hangi Alanlara İlgi Duyuyorsunuz?
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Birden fazla seçim yapabilirsiniz
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {interestOptions.map((interest) => (
                <Chip
                  key={interest}
                  label={interest}
                  onClick={() => handleInterestToggle(interest)}
                  color={formData.interests.includes(interest) ? 'primary' : 'default'}
                  variant={formData.interests.includes(interest) ? 'filled' : 'outlined'}
                  clickable
                />
              ))}
            </Box>
          </Box>
        );

      case 2:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Öğrenme Hedefleriniz Nelerdir?
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Birden fazla hedef seçebilirsiniz
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {goalOptions.map((goal) => (
                <Chip
                  key={goal}
                  label={goal}
                  onClick={() => handleGoalToggle(goal)}
                  color={formData.learning_goals.includes(goal) ? 'primary' : 'default'}
                  variant={formData.learning_goals.includes(goal) ? 'filled' : 'outlined'}
                  clickable
                />
              ))}
            </Box>
          </Box>
        );

      case 3:
        return (
          <Box>
            <Typography variant="h6" gutterBottom>
              Zaman Planınız
            </Typography>
            <Box sx={{ display: 'flex', gap: 3 }}>
              <TextField
                fullWidth
                label="Haftalık Ayırabileceğiniz Saat"
                type="number"
                value={formData.available_hours_per_week}
                onChange={(e) => setFormData(prev => ({ ...prev, available_hours_per_week: parseInt(e.target.value) }))}
                inputProps={{ min: 1, max: 40 }}
              />
              <TextField
                fullWidth
                label="Hedef Süre (Ay)"
                type="number"
                value={formData.target_timeline_months}
                onChange={(e) => setFormData(prev => ({ ...prev, target_timeline_months: parseInt(e.target.value) }))}
                inputProps={{ min: 1, max: 24 }}
              />
            </Box>
          </Box>
        );

      case 4:
        return roadmap ? (
          <Box>
            <Typography variant="h6" gutterBottom>
              {roadmap.title}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              {roadmap.description}
            </Typography>
            
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Genel İlerleme
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={roadmap.overall_progress} 
                sx={{ height: 10, borderRadius: 5 }}
              />
              <Typography variant="body2" sx={{ mt: 1 }}>
                {roadmap.overall_progress}% tamamlandı
              </Typography>
            </Box>

            <Typography variant="h6" gutterBottom>
              Modüller
            </Typography>
            {roadmap.modules.map((module: any) => (
              <Card key={module.id} sx={{ mb: 2 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="h6">{module.title}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {module.description}
                      </Typography>
                      <Box sx={{ mt: 1 }}>
                        <Chip 
                          label={module.difficulty} 
                          size="small" 
                          color={module.difficulty === 'beginner' ? 'success' : module.difficulty === 'intermediate' ? 'warning' : 'error'}
                        />
                        <Typography variant="body2" sx={{ mt: 1 }}>
                          Tahmini süre: {module.estimated_hours} saat
                        </Typography>
                      </Box>
                    </Box>
                    <Button
                      variant="contained"
                      startIcon={module.completed ? <CheckCircle /> : <PlayArrow />}
                      disabled={module.completed}
                    >
                      {module.completed ? 'Tamamlandı' : 'Başla'}
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        ) : null;

      default:
        return null;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/dashboard')}
          sx={{ mr: 2 }}
        >
          Geri
        </Button>
        <School sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
        <Typography variant="h4">
          Yol Haritası Oluştur
        </Typography>
      </Box>

      {/* Stepper */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {/* Step Content */}
        <Box sx={{ minHeight: 300 }}>
          {renderStepContent(activeStep)}
        </Box>

        {/* Navigation Buttons */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
          <Button
            disabled={activeStep === 0}
            onClick={handleBack}
          >
            Geri
          </Button>
          
          {activeStep === steps.length - 2 ? (
            <Button
              variant="contained"
              onClick={generateRoadmap}
              disabled={loading}
            >
              {loading ? 'Oluşturuluyor...' : 'Yol Haritası Oluştur'}
            </Button>
          ) : activeStep < steps.length - 1 ? (
            <Button
              variant="contained"
              onClick={handleNext}
              disabled={
                (activeStep === 1 && formData.interests.length === 0) ||
                (activeStep === 2 && formData.learning_goals.length === 0)
              }
            >
              İleri
            </Button>
          ) : null}
        </Box>
      </Paper>
    </Container>
  );
};

export default Roadmap; 