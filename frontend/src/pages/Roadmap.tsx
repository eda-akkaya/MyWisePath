import React, { useState, useEffect } from 'react';
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
  Dialog,
  DialogTitle,
  DialogContent,
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
  Login as LoginIcon,
  Launch,
  Link,
  PictureAsPdf,
  Close,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { roadmapService, RoadmapRequest } from '../services/roadmapService';
import { progressService } from '../services/progressService';
import PDFGenerator from '../components/PDFGenerator';

interface RoadmapForm {
  skill_level: string;
  interests: string[];
  learning_goals: string[];
  available_hours_per_week: number;
  target_timeline_months: number;
}

const Roadmap: React.FC = () => {
  const navigate = useNavigate();
  const { user, isLoading } = useAuth();
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
  const [error, setError] = useState<string | null>(null);
  const [showAgentHelp, setShowAgentHelp] = useState(false);
  const [showPDFGenerator, setShowPDFGenerator] = useState(false);

  // Authentication check
  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login', { state: { from: '/roadmap' } });
    }
  }, [user, isLoading, navigate]);

  // Show loading while checking authentication
  if (isLoading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, textAlign: 'center' }}>
        <Typography variant="h6">Yükleniyor...</Typography>
      </Container>
    );
  }

  // Show login prompt if not authenticated
  if (!user) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, textAlign: 'center' }}>
        <Paper sx={{ p: 4, borderRadius: 4, maxWidth: 600, mx: 'auto' }}>
          <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
            🔐 Giriş Gerekli
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
            Yol haritası oluşturmak için lütfen giriş yapın.
          </Typography>
          
          <Alert severity="info" sx={{ mb: 3, borderRadius: 2 }}>
            <Typography variant="body2">
              💡 <strong>Demo Kullanıcı:</strong><br/>
              Hızlı test için: demo@mywisepath.com / demo123
            </Typography>
          </Alert>
          
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Button
              variant="contained"
              onClick={() => navigate('/login')}
              startIcon={<LoginIcon />}
              size="large"
            >
              Giriş Yap
            </Button>
            <Button
              variant="outlined"
              onClick={() => navigate('/register')}
              size="large"
            >
              Kayıt Ol
            </Button>
          </Box>
        </Paper>
      </Container>
    );
  }

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
    if (activeStep === 0 && !formData.skill_level) {
      alert('Lütfen bilgi seviyenizi seçin');
      return;
    } else if (activeStep === 1 && formData.interests.length === 0) {
      alert('Lütfen en az bir ilgi alanı seçin');
      return;
    } else if (activeStep === 2 && formData.learning_goals.length === 0) {
      alert('Lütfen en az bir öğrenme hedefi seçin');
      return;
    } else if (activeStep === 3) {
      if (formData.available_hours_per_week <= 0) {
        alert('Lütfen haftalık çalışma saatinizi belirleyin');
        return;
      }
      if (formData.target_timeline_months <= 0) {
        alert('Lütfen hedef sürenizi belirleyin');
        return;
      }
    }
    
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
    setError(null);
    
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setError('Oturum süreniz dolmuş. Lütfen tekrar giriş yapın.');
        navigate('/login');
        return;
      }

      const request: RoadmapRequest = {
        skill_level: formData.skill_level,
        interests: formData.interests,
        learning_goals: formData.learning_goals,
        available_hours_per_week: formData.available_hours_per_week,
        target_timeline_months: formData.target_timeline_months,
      };

      const response = await roadmapService.generateRoadmap(request);
      
      if (response) {
        setRoadmap(response);
        setError(null);
        handleNext();
      } else {
        setError('Yol haritası oluşturulamadı. Lütfen tekrar deneyin.');
      }
    } catch (error: any) {
      console.error('Yol haritası oluşturma hatası:', error);
      
      let errorMessage = 'Yol haritası oluşturulurken hata oluştu';
      
      if (error.message) {
        if (error.message.includes('403') || error.message.includes('Not authenticated')) {
          errorMessage = 'Oturum süreniz dolmuş. Lütfen tekrar giriş yapın.';
          localStorage.removeItem('token');
          navigate('/login');
        } else if (error.message.includes('401')) {
          errorMessage = 'Yetkilendirme hatası. Lütfen tekrar giriş yapın.';
          localStorage.removeItem('token');
          navigate('/login');
        } else if (error.message.includes('500')) {
          errorMessage = 'Sunucu hatası. Lütfen daha sonra tekrar deneyin.';
        } else {
          errorMessage = error.message;
        }
      }
      
      setError(errorMessage);
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
                📊 Bilgi Seviyesi Belirleyin
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Mevcut bilgi seviyenizi seçin, böylece size en uygun yol haritasını oluşturabiliriz.
              </Typography>
              
              <Alert severity="info" sx={{ mb: 3, borderRadius: 2 }}>
                <Typography variant="body2">
                  🤖 Agent Önerisi: Bilgi seviyenizi gerçekçi olarak değerlendirin. Başlangıç seviyesindeyseniz, temel kavramlardan başlayın.
                </Typography>
              </Alert>
              
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
              
              <Alert severity="info" sx={{ mb: 3, borderRadius: 2 }}>
                <Typography variant="body2">
                  🤖 Agent Önerisi: İlgi alanlarınızı seçerken, kariyer hedeflerinizi ve mevcut becerilerinizi göz önünde bulundurun.
                </Typography>
              </Alert>
              
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
              
              <Alert severity="info" sx={{ mb: 3, borderRadius: 2 }}>
                <Typography variant="body2">
                  🤖 Agent Önerisi: Öğrenme hedeflerinizi ölçülebilir ve gerçekçi tutun. Kısa ve uzun vadeli hedefler belirleyin.
                </Typography>
              </Alert>
              
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
              
              <Alert severity="info" sx={{ mb: 3, borderRadius: 2 }}>
                <Typography variant="body2">
                  🤖 Agent Önerisi: Zaman planınızı mevcut programınıza göre ayarlayın. Tutarlı çalışma rutini oluşturun.
                </Typography>
              </Alert>
              
                             <Paper sx={{ p: 3, mb: 4, bgcolor: 'action.hover', borderRadius: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                  📋 Seçimlerinizin Özeti
                </Typography>
                <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2 }}>
                  <Box>
                    <Typography variant="body2" color="text.secondary">Bilgi Seviyesi:</Typography>
                    <Typography variant="body1" sx={{ fontWeight: 500, mb: 1 }}>
                      {skillLevels.find(level => level.value === formData.skill_level)?.label || 'Seçilmedi'}
                    </Typography>
                    
                    <Typography variant="body2" color="text.secondary">İlgi Alanları:</Typography>
                    <Typography variant="body1" sx={{ fontWeight: 500, mb: 1 }}>
                      {formData.interests.length > 0 ? formData.interests.join(', ') : 'Seçilmedi'}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="body2" color="text.secondary">Öğrenme Hedefleri:</Typography>
                    <Typography variant="body1" sx={{ fontWeight: 500, mb: 1 }}>
                      {formData.learning_goals.length > 0 ? formData.learning_goals.join(', ') : 'Seçilmedi'}
                    </Typography>
                  </Box>
                </Box>
              </Paper>
              
              {canGenerateRoadmap() && (
                <Alert severity="success" sx={{ mt: 3, borderRadius: 2 }}>
                  <Typography variant="body2">
                    ✅ Tüm bilgiler tamamlandı! Artık yol haritanızı oluşturabilirsiniz.
                  </Typography>
                </Alert>
              )}
              
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
                      {roadmap.description}
                    </Typography>
                    <Divider sx={{ my: 3 }} />
                    <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                      📚 Eğitim Modülleri
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      {roadmap.modules?.map((module: any, index: number) => (
                        <Paper key={index} sx={{ p: 3, borderRadius: 3 }}>
                          <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                            Modül {index + 1}: {module.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {module.description}
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 2 }}>
                            <Chip
                              label={`${module.difficulty} seviye`}
                              size="small"
                              variant="outlined"
                              color="primary"
                            />
                            <Chip
                              label={`${module.estimated_hours} saat`}
                              size="small"
                              variant="outlined"
                              color="secondary"
                            />
                          </Box>
                          {module.prerequisites && module.prerequisites.length > 0 && (
                            <Box sx={{ mb: 2 }}>
                              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                Ön Koşullar:
                              </Typography>
                              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                                {module.prerequisites.map((prereq: string, prereqIndex: number) => (
                                  <Chip
                                    key={prereqIndex}
                                    label={prereq}
                                    size="small"
                                    variant="outlined"
                                    icon={<CheckCircle />}
                                  />
                                ))}
                              </Box>
                            </Box>
                          )}
                          {module.resources && module.resources.length > 0 && (
                            <Box>
                              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                📚 Önerilen Eğitim Kaynakları:
                              </Typography>
                              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                                {module.resources.map((resource: any, resourceIndex: number) => {
                                  // Resource string ise eski format, object ise yeni format
                                  const resourceName = typeof resource === 'string' ? resource : resource.name;
                                  const resourceUrl = typeof resource === 'string' ? '#' : resource.url;
                                  

                                  
                                  return (
                                    <Box
                                      key={resourceIndex}
                                      sx={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'space-between',
                                        p: 1,
                                        border: '1px solid',
                                        borderColor: 'divider',
                                        borderRadius: 1,
                                        bgcolor: 'background.paper',
                                        '&:hover': {
                                          bgcolor: 'action.hover',
                                          borderColor: 'primary.main'
                                        }
                                      }}
                                    >
                                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flex: 1 }}>
                                        <Link color="primary" sx={{ fontSize: 16 }} />
                                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                                          {resourceName}
                                        </Typography>
                                      </Box>
                                      <Button
                                        variant="contained"
                                        size="small"
                                        startIcon={<Launch />}
                                        onClick={() => {
                                          if (resourceUrl && resourceUrl !== '#') {
                                            window.open(resourceUrl, '_blank', 'noopener,noreferrer');
                                          } else {
                                            alert('Bu kaynak için link henüz eklenmemiş.');
                                          }
                                        }}
                                        sx={{
                                          minWidth: 'auto',
                                          px: 2,
                                          py: 0.5,
                                          fontSize: '0.75rem',
                                          bgcolor: 'primary.main',
                                          '&:hover': {
                                            bgcolor: 'primary.dark'
                                          }
                                        }}
                                      >
                                        Eğitime Git
                                      </Button>
                                    </Box>
                                  );
                                })}
                              </Box>
                            </Box>
                          )}
                          
                          <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                            <Button
                              variant="outlined"
                              size="small"
                              startIcon={<PlayArrow />}
                              onClick={async () => {
                                try {
                                  await progressService.updateModuleProgress(
                                    roadmap.id || 'roadmap_1',
                                    {
                                      module_id: `module_${index + 1}`,
                                      progress_percentage: 25,
                                      time_spent_minutes: 30,
                                      status: 'in_progress'
                                    }
                                  );
                                  alert('Modül başlatıldı! İlerleme kaydedildi.');
                                } catch (error) {
                                  console.error('İlerleme güncellenirken hata:', error);
                                }
                              }}
                            >
                              Başlat
                            </Button>
                            <Button
                              variant="outlined"
                              size="small"
                              startIcon={<CheckCircle />}
                              onClick={async () => {
                                try {
                                  await progressService.completeModule(
                                    roadmap.id || 'roadmap_1',
                                    `module_${index + 1}`
                                  );
                                  alert('Modül tamamlandı! Tebrikler!');
                                } catch (error) {
                                  console.error('Modül tamamlanırken hata:', error);
                                }
                              }}
                            >
                              Tamamla
                            </Button>
                            <Button
                              variant="outlined"
                              size="small"
                              startIcon={<TrendingUp />}
                              onClick={() => navigate('/progress')}
                            >
                              İlerlemeyi Görüntüle
                            </Button>
                          </Box>
                        </Paper>
                      ))}
                    </Box>
                    
                    {roadmap.learning_goals && roadmap.learning_goals.length > 0 && (
                      <>
                        <Divider sx={{ my: 3 }} />
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                          🎯 Öğrenme Hedefleri
                        </Typography>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                          {roadmap.learning_goals.map((goal: any, index: number) => (
                            <Paper key={index} sx={{ p: 2, borderRadius: 2 }}>
                              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                {goal.title}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                {goal.description}
                              </Typography>
                            </Paper>
                          ))}
                        </Box>
                      </>
                    )}
                    
                    {roadmap.skill_assessments && roadmap.skill_assessments.length > 0 && (
                      <>
                        <Divider sx={{ my: 3 }} />
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                          📊 Beceri Değerlendirmeleri
                        </Typography>
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                          {roadmap.skill_assessments.map((assessment: any, index: number) => (
                            <Paper key={index} sx={{ p: 2, borderRadius: 2 }}>
                              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                {assessment.skill_name}
                              </Typography>
                              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                Mevcut Seviye: {assessment.current_level} → Hedef: {assessment.target_level}
                              </Typography>
                              <LinearProgress 
                                variant="determinate" 
                                value={assessment.progress_percentage}
                                sx={{ height: 6, borderRadius: 3 }}
                              />
                            </Paper>
                          ))}
                        </Box>
                      </>
                    )}
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

  const canProceed = () => {
    switch (activeStep) {
      case 0:
        return !!formData.skill_level;
      case 1:
        return formData.interests.length > 0;
      case 2:
        return formData.learning_goals.length > 0;
      case 3:
        return formData.available_hours_per_week > 0 && formData.target_timeline_months > 0;
      default:
        return true;
    }
  };

  const canGenerateRoadmap = () => {
    return formData.skill_level && 
           formData.interests.length > 0 && 
           formData.learning_goals.length > 0 && 
           formData.available_hours_per_week > 0 && 
           formData.target_timeline_months > 0;
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 4 }}>
      <Fade in={true} timeout={800}>
        <Box sx={{ 
          mb: 4,
          p: 3,
          borderRadius: 4,
          backgroundColor: 'background.paper',
          backdropFilter: 'blur(10px)',
          border: 1,
          borderColor: 'divider',
          boxShadow: 3,
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
          
          <Box sx={{ mt: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2" color="text.secondary">
                Form Tamamlanma Durumu
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {canGenerateRoadmap() ? '100%' : 'Eksik'}
              </Typography>
            </Box>
            <LinearProgress 
              variant="determinate" 
              value={canGenerateRoadmap() ? 100 : 0}
              sx={{ height: 8, borderRadius: 4 }}
              color={canGenerateRoadmap() ? 'success' : 'primary'}
            />
          </Box>
        </Box>
      </Fade>

      <Paper sx={{ p: 3, mb: 4, borderRadius: 4 }}>
        <Stepper activeStep={activeStep} alternativeLabel>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary">
            Adım {activeStep + 1} / {steps.length}
          </Typography>
        </Box>
      </Paper>

      <Paper sx={{ 
        p: 4, 
        borderRadius: 4,
        backgroundColor: 'background.paper',
        backdropFilter: 'blur(10px)',
        border: 1,
        borderColor: 'divider',
        boxShadow: 3,
      }}>
        {renderStepContent(activeStep)}

        {error && (
          <Alert severity="error" sx={{ mt: 3, mb: 3, borderRadius: 2 }}>
            <Typography variant="body2">
              ❌ {error}
            </Typography>
          </Alert>
        )}

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
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, alignItems: 'center' }}>
                <Button
                  variant="contained"
                  onClick={generateRoadmap}
                  disabled={loading || !canGenerateRoadmap()}
                  startIcon={<AutoAwesome />}
                  size="large"
                  sx={{
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: 4,
                    },
                  }}
                >
                  {loading ? 'Oluşturuluyor...' : 'Yol Haritası Oluştur'}
                </Button>
                
                <Button
                  variant="outlined"
                  onClick={() => setShowAgentHelp(!showAgentHelp)}
                  startIcon={<Psychology />}
                  size="small"
                  sx={{ mt: 1 }}
                >
                  {showAgentHelp ? 'Agent Yardımını Gizle' : 'Agent Yardımı Al'}
                </Button>
                
                {showAgentHelp && (
                  <Alert severity="info" sx={{ mt: 2, borderRadius: 2, maxWidth: 400 }}>
                    <Typography variant="body2">
                      🤖 <strong>AI Agent Önerisi:</strong><br/>
                      Seçimlerinize göre kişiselleştirilmiş bir yol haritası oluşturacağım. 
                      Bu yol haritası, mevcut bilgi seviyeniz, ilgi alanlarınız ve hedeflerinize 
                      göre optimize edilmiş olacak. Hemen başlayalım!
                    </Typography>
                  </Alert>
                )}
              </Box>
            ) : activeStep === steps.length - 1 ? (
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, alignItems: 'center' }}>
                <Button
                  variant="contained"
                  onClick={() => navigate('/dashboard')}
                  startIcon={<PlayArrow />}
                  size="large"
                  color="success"
                  sx={{
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: 4,
                    },
                  }}
                >
                  Başla
                </Button>
                
                <Button
                  variant="outlined"
                  onClick={() => setShowPDFGenerator(true)}
                  startIcon={<PictureAsPdf />}
                  size="small"
                  sx={{ mt: 1 }}
                >
                  PDF İndir
                </Button>
              </Box>
            ) : (
              <Button
                variant="contained"
                onClick={handleNext}
                disabled={!canProceed()}
                endIcon={<PlayArrow />}
                size="large"
                sx={{
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: 4,
                  },
                }}
              >
                İleri
              </Button>
            )}
          </Box>
        </Box>
      </Paper>

      {/* PDF Generator Dialog */}
      {showPDFGenerator && roadmap && (
        <Dialog 
          open={showPDFGenerator} 
          onClose={() => setShowPDFGenerator(false)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6">PDF Oluşturucu</Typography>
            <IconButton onClick={() => setShowPDFGenerator(false)}>
              <Close />
            </IconButton>
          </DialogTitle>
          <DialogContent>
            <PDFGenerator 
              roadmapData={roadmap}
              onClose={() => setShowPDFGenerator(false)}
            />
          </DialogContent>
        </Dialog>
      )}
    </Container>
  );
};

export default Roadmap; 