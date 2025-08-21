import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Paper,
  LinearProgress,
  Chip,
  Alert,
  Fade,
  Grow,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
} from '@mui/material';
import {
  ArrowBack,
  Timeline,
  CheckCircle,
  PlayArrow,
  Pause,
  Schedule,
  TrendingUp,
  Star,
  School,
  AccessTime,
  Assessment,
  CalendarToday,
  EmojiEvents,
  ExpandMore,
  Book,
  VideoLibrary,
  Assignment,
  Quiz,
  Psychology,
  AutoAwesome,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { progressService, RoadmapProgress, ProgressData, ModuleProgress } from '../services/progressService';
import { roadmapService } from '../services/roadmapService';

interface Module {
  id: string;
  title: string;
  description: string;
  duration_minutes: number;
  difficulty: string;
  resources: string[];
  quiz_questions?: string[];
}

interface RoadmapData {
  roadmap_id: string;
  title: string;
  description: string;
  modules: Module[];
  created_at: string;
  skill_level: string;
  estimated_duration_hours: number;
}

const RoadmapDetails: React.FC = () => {
  const { roadmapId } = useParams<{ roadmapId: string }>();
  const navigate = useNavigate();
  const { user, isLoading } = useAuth();
  const [roadmapData, setRoadmapData] = useState<RoadmapData | null>(null);
  const [progressData, setProgressData] = useState<RoadmapProgress | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Authentication check
  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login', { state: { from: `/roadmap/${roadmapId}` } });
    }
  }, [user, isLoading, navigate, roadmapId]);

  // Load roadmap and progress data
  useEffect(() => {
    if (user && roadmapId) {
      loadRoadmapData();
      loadProgressData();
    }
  }, [user, roadmapId]);

  const loadRoadmapData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const roadmapResponse = await roadmapService.getRoadmapById(roadmapId!);
      
      // Convert the response to our local format
      const roadmapData: RoadmapData = {
        roadmap_id: roadmapResponse.id || roadmapId!,
        title: roadmapResponse.title || `Roadmap #${roadmapId}`,
        description: roadmapResponse.description || "Bu roadmap, seçilen becerileri geliştirmek için tasarlanmış kapsamlı bir öğrenme yolculuğudur.",
        modules: roadmapResponse.modules?.map((module: any, index: number) => ({
          id: module.id || (index + 1).toString(),
          title: module.title || `Modül ${index + 1}`,
          description: module.description || "Modül açıklaması",
          duration_minutes: module.duration_minutes || module.estimated_hours * 60 || 120,
          difficulty: module.difficulty || "Başlangıç",
          resources: module.resources || ["Video ders", "PDF doküman", "Pratik alıştırmalar"],
          quiz_questions: module.quiz_questions || ["Soru 1", "Soru 2", "Soru 3"]
        })) || [
          {
            id: "1",
            title: "Temel Kavramlar",
            description: "Bu modülde temel kavramları öğreneceksiniz.",
            duration_minutes: 120,
            difficulty: "Başlangıç",
            resources: ["Video ders", "PDF doküman", "Pratik alıştırmalar"],
            quiz_questions: ["Soru 1", "Soru 2", "Soru 3"]
          },
          {
            id: "2",
            title: "İleri Seviye Teknikler",
            description: "İleri seviye teknikleri ve uygulamaları keşfedin.",
            duration_minutes: 180,
            difficulty: "Orta",
            resources: ["Video ders", "Kod örnekleri", "Proje çalışması"],
            quiz_questions: ["Soru 1", "Soru 2", "Soru 3", "Soru 4"]
          },
          {
            id: "3",
            title: "Uygulama Projeleri",
            description: "Öğrendiklerinizi gerçek projelerde uygulayın.",
            duration_minutes: 240,
            difficulty: "İleri",
            resources: ["Proje rehberi", "Kod deposu", "Canlı demo"],
            quiz_questions: ["Soru 1", "Soru 2"]
          }
        ],
        created_at: roadmapResponse.created_at || new Date().toISOString(),
        skill_level: "Başlangıç",
        estimated_duration_hours: roadmapResponse.total_estimated_hours || 9
      };
      
      setRoadmapData(roadmapData);
    } catch (error: any) {
      console.error('Roadmap verisi yüklenirken hata:', error);
      setError(error.message || 'Roadmap verisi yüklenemedi');
    } finally {
      setLoading(false);
    }
  };

  const loadProgressData = async () => {
    try {
      const progress = await progressService.getRoadmapProgress(roadmapId!);
      setProgressData(progress);
    } catch (error: any) {
      console.error('İlerleme verisi yüklenirken hata:', error);
      // Don't set error here as it's not critical
    }
  };

  const handleStartModule = async (moduleId: string) => {
    try {
      const update: ProgressData = {
        module_id: moduleId,
        progress_percentage: 0,
        time_spent_minutes: 0,
        status: 'in_progress'
      };
      await progressService.updateModuleProgress(roadmapId!, update);
      await loadProgressData(); // Refresh progress data
    } catch (error: any) {
      console.error('Modül başlatılırken hata:', error);
    }
  };

  const handleCompleteModule = async (moduleId: string) => {
    try {
      await progressService.completeModule(roadmapId!, moduleId);
      await loadProgressData(); // Refresh progress data
    } catch (error: any) {
      console.error('Modül tamamlanırken hata:', error);
    }
  };

  const getModuleStatus = (moduleId: string) => {
    if (!progressData?.module_progress) return 'not_started';
    const module = progressData.module_progress.find((m: ModuleProgress) => m.module_id === moduleId);
    return module?.status || 'not_started';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'in_progress':
        return 'primary';
      case 'paused':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle />;
      case 'in_progress':
        return <PlayArrow />;
      case 'paused':
        return <Pause />;
      default:
        return <Schedule />;
    }
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}s ${mins}dk`;
    }
    return `${mins}dk`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('tr-TR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

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
            Roadmap detaylarını görüntülemek için lütfen giriş yapın.
          </Typography>
          <Button
            variant="contained"
            onClick={() => navigate('/login')}
            size="large"
          >
            Giriş Yap
          </Button>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 4 }}>
      {/* Back Button */}
      <Box sx={{ mb: 3 }}>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/progress')}
          sx={{ mb: 2 }}
        >
          İlerleme Sayfasına Dön
        </Button>
      </Box>

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }}>
          <Typography variant="body2">
            ❌ {error}
          </Typography>
        </Alert>
      )}

      {loading ? (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6">Roadmap detayları yükleniyor...</Typography>
        </Box>
      ) : roadmapData ? (
        <>
          {/* Roadmap Header */}
          <Fade in={true} timeout={800}>
            <Card sx={{ mb: 4, borderRadius: 4 }}>
              <CardContent sx={{ p: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  <Timeline sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                      {roadmapData.title}
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                      {roadmapData.description}
                    </Typography>
                  </Box>
                </Box>

                {/* Progress Summary */}
                {progressData && (
                  <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr 1fr' }, gap: 3, mb: 3 }}>
                    <Box sx={{ textAlign: 'center', p: 2 }}>
                      <CheckCircle sx={{ fontSize: 32, color: 'success.main', mb: 1 }} />
                      <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                        {progressData.completed_modules}/{progressData.total_modules}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Tamamlanan Modül
                      </Typography>
                    </Box>
                    
                    <Box sx={{ textAlign: 'center', p: 2 }}>
                      <AccessTime sx={{ fontSize: 32, color: 'info.main', mb: 1 }} />
                      <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                        {formatTime(progressData.total_time_spent_minutes)}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Toplam Süre
                      </Typography>
                    </Box>
                    
                    <Box sx={{ textAlign: 'center', p: 2 }}>
                      <EmojiEvents sx={{ fontSize: 32, color: 'warning.main', mb: 1 }} />
                      <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                        {Math.round(progressData.overall_progress)}%
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Tamamlanma Oranı
                      </Typography>
                    </Box>
                  </Box>
                )}

                {/* Overall Progress Bar */}
                {progressData && (
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      Genel İlerleme
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={progressData.overall_progress}
                      sx={{ height: 10, borderRadius: 5 }}
                      color="success"
                    />
                  </Box>
                )}

                {/* Roadmap Info */}
                <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, gap: 2 }}>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Seviye:
                    </Typography>
                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                      {roadmapData.skill_level}
                    </Typography>
                  </Box>
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Tahmini Süre:
                    </Typography>
                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                      {roadmapData.estimated_duration_hours} saat
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Fade>

          {/* Modules */}
          <Grow in={true} timeout={1000}>
            <Box>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                📚 Modüller
              </Typography>
              
              {roadmapData.modules.map((module, index) => {
                const status = getModuleStatus(module.id);
                return (
                  <Accordion key={module.id} sx={{ mb: 2, borderRadius: 2 }}>
                    <AccordionSummary
                      expandIcon={<ExpandMore />}
                      sx={{
                        '&:hover': {
                          backgroundColor: 'action.hover',
                        },
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                        <ListItemIcon>
                          {getStatusIcon(status)}
                        </ListItemIcon>
                        <Box sx={{ flexGrow: 1 }}>
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            {index + 1}. {module.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {module.description}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          <Chip
                            label={module.difficulty}
                            size="small"
                            color={module.difficulty === 'Başlangıç' ? 'success' : module.difficulty === 'Orta' ? 'warning' : 'error'}
                          />
                          <Chip
                            label={formatTime(module.duration_minutes)}
                            size="small"
                            icon={<AccessTime />}
                          />
                          <Chip
                            label={status === 'completed' ? 'Tamamlandı' : status === 'in_progress' ? 'Devam Ediyor' : 'Başlanmadı'}
                            color={getStatusColor(status) as any}
                            size="small"
                          />
                        </Box>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Box sx={{ mb: 3 }}>
                        <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                          📖 İçerik
                        </Typography>
                        <List dense>
                          {module.resources.map((resource, idx) => (
                            <ListItem key={idx} sx={{ py: 0.5 }}>
                              <ListItemIcon sx={{ minWidth: 32 }}>
                                {resource.includes('Video') ? <VideoLibrary fontSize="small" /> :
                                 resource.includes('PDF') ? <Book fontSize="small" /> :
                                 resource.includes('Proje') ? <AutoAwesome fontSize="small" /> :
                                 <Assignment fontSize="small" />}
                              </ListItemIcon>
                              <ListItemText primary={resource} />
                            </ListItem>
                          ))}
                        </List>
                      </Box>

                      {module.quiz_questions && module.quiz_questions.length > 0 && (
                        <Box sx={{ mb: 3 }}>
                          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                            🧠 Quiz Soruları ({module.quiz_questions.length})
                          </Typography>
                          <List dense>
                            {module.quiz_questions.map((question, idx) => (
                              <ListItem key={idx} sx={{ py: 0.5 }}>
                                <ListItemIcon sx={{ minWidth: 32 }}>
                                  <Quiz fontSize="small" />
                                </ListItemIcon>
                                <ListItemText primary={question} />
                              </ListItem>
                            ))}
                          </List>
                        </Box>
                      )}

                      {/* Module Actions */}
                      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                        {status === 'not_started' && (
                          <Button
                            variant="contained"
                            startIcon={<PlayArrow />}
                            onClick={() => handleStartModule(module.id)}
                            color="primary"
                          >
                            Başlat
                          </Button>
                        )}
                        {status === 'in_progress' && (
                          <>
                            <Button
                              variant="outlined"
                              startIcon={<Pause />}
                              color="warning"
                            >
                              Duraklat
                            </Button>
                            <Button
                              variant="contained"
                              startIcon={<CheckCircle />}
                              onClick={() => handleCompleteModule(module.id)}
                              color="success"
                            >
                              Tamamla
                            </Button>
                          </>
                        )}
                        {status === 'completed' && (
                          <Chip
                            label="Tamamlandı"
                            color="success"
                            icon={<CheckCircle />}
                          />
                        )}
                      </Box>
                    </AccordionDetails>
                  </Accordion>
                );
              })}
            </Box>
          </Grow>
        </>
      ) : (
        <Paper sx={{ p: 4, textAlign: 'center', borderRadius: 4 }}>
          <Typography variant="h6" gutterBottom>
            Roadmap bulunamadı
          </Typography>
          <Button
            variant="contained"
            onClick={() => navigate('/progress')}
            sx={{ mt: 2 }}
          >
            İlerleme Sayfasına Dön
          </Button>
        </Paper>
      )}
    </Container>
  );
};

export default RoadmapDetails;
