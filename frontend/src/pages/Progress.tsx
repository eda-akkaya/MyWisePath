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
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
} from '@mui/material';
import {
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
  Search,
  PictureAsPdf,
  Close,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { progressService, UserProgressSummary, RoadmapProgress } from '../services/progressService';
import RAGSearch from '../components/RAGSearch';
import PDFGenerator from '../components/PDFGenerator';

const Progress: React.FC = () => {
  const navigate = useNavigate();
  const { user, isLoading } = useAuth();
  const [progressSummary, setProgressSummary] = useState<UserProgressSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showRAGSearch, setShowRAGSearch] = useState(false);
  const [showPDFGenerator, setShowPDFGenerator] = useState(false);

  // Authentication check
  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login', { state: { from: '/progress' } });
    }
  }, [user, isLoading, navigate]);

  // Load progress data
  useEffect(() => {
    if (user) {
      loadProgressData();
    }
  }, [user]);

  const loadProgressData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const summary = await progressService.getUserProgressSummary();
      setProgressSummary(summary);
    } catch (error: any) {
      console.error('İlerleme verisi yüklenirken hata:', error);
      setError(error.message || 'İlerleme verisi yüklenemedi');
    } finally {
      setLoading(false);
    }
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
            İlerleme verilerinizi görüntülemek için lütfen giriş yapın.
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
      {/* Page Title */}
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
            <TrendingUp sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              Öğrenme İlerlemesi
            </Typography>
          </Box>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Öğrenme yolculuğunuzdaki ilerlemenizi takip edin
          </Typography>
          <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
            <Button
              variant="outlined"
              onClick={() => setShowRAGSearch(!showRAGSearch)}
              startIcon={<Search />}
              size="small"
            >
              {showRAGSearch ? 'Aramayı Gizle' : 'Akıllı Arama'}
            </Button>
            
            <Button
              variant="outlined"
              onClick={() => setShowPDFGenerator(true)}
              startIcon={<PictureAsPdf />}
              size="small"
              color="secondary"
            >
              PDF Raporu
            </Button>
          </Box>
        </Box>
      </Fade>

      {/* RAG Search Component */}
      {showRAGSearch && (
        <Fade in={showRAGSearch} timeout={500}>
          <Box sx={{ mb: 4 }}>
            <RAGSearch />
          </Box>
        </Fade>
      )}

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
          <Typography variant="h6">İlerleme verileri yükleniyor...</Typography>
        </Box>
      ) : progressSummary ? (
        <>
          {/* Overall Progress Summary */}
          <Grow in={true} timeout={800}>
            <Card sx={{ mb: 4, borderRadius: 4 }}>
              <CardContent sx={{ p: 4 }}>
                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                  📊 Genel İlerleme Özeti
                </Typography>
                
                <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: '1fr 1fr 1fr 1fr' }, gap: 3 }}>
                  <Box sx={{ textAlign: 'center', p: 2 }}>
                    <School sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                      {progressSummary.total_roadmaps}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Toplam Roadmap
                    </Typography>
                  </Box>
                  
                  <Box sx={{ textAlign: 'center', p: 2 }}>
                    <CheckCircle sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                      {progressSummary.total_completed_modules}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Tamamlanan Modül
                    </Typography>
                  </Box>
                  
                  <Box sx={{ textAlign: 'center', p: 2 }}>
                    <AccessTime sx={{ fontSize: 40, color: 'info.main', mb: 1 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                      {formatTime(progressSummary.total_time_spent_minutes)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Toplam Süre
                    </Typography>
                  </Box>
                  
                  <Box sx={{ textAlign: 'center', p: 2 }}>
                    <EmojiEvents sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                      {Math.round(progressSummary.overall_completion_rate)}%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Tamamlanma Oranı
                    </Typography>
                  </Box>
                </Box>
                
                <Box sx={{ mt: 3 }}>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    Genel İlerleme
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={progressSummary.overall_completion_rate}
                    sx={{ height: 10, borderRadius: 5 }}
                    color="success"
                  />
                </Box>
              </CardContent>
            </Card>
          </Grow>

          {/* Individual Roadmap Progress */}
          {progressSummary.roadmaps.length > 0 ? (
            <Grow in={true} timeout={1000}>
              <Box>
                <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                  🗓️ Roadmap İlerlemeleri
                </Typography>
                
                <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
                  {progressSummary.roadmaps.map((roadmap: RoadmapProgress, index: number) => (
                    <Card key={roadmap.roadmap_id} sx={{ borderRadius: 4, height: '100%' }}>
                      <CardContent sx={{ p: 3 }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            Roadmap #{index + 1}
                          </Typography>
                          <Chip
                            label={`${roadmap.overall_progress}%`}
                            color={roadmap.overall_progress >= 100 ? 'success' : 'primary'}
                            variant="filled"
                          />
                        </Box>
                        
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            İlerleme
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={roadmap.overall_progress}
                            sx={{ height: 8, borderRadius: 4 }}
                          />
                        </Box>
                        
                        <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mb: 2 }}>
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              Tamamlanan:
                            </Typography>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                              {roadmap.completed_modules}/{roadmap.total_modules}
                            </Typography>
                          </Box>
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              Süre:
                            </Typography>
                            <Typography variant="body1" sx={{ fontWeight: 500 }}>
                              {formatTime(roadmap.total_time_spent_minutes)}
                            </Typography>
                          </Box>
                        </Box>
                        
                        {roadmap.started_at && (
                          <Typography variant="caption" color="text.secondary">
                            Başlangıç: {formatDate(roadmap.started_at)}
                          </Typography>
                        )}
                        
                        <Box sx={{ mt: 2 }}>
                          <Button
                            variant="outlined"
                            size="small"
                            onClick={() => navigate(`/roadmap/${roadmap.roadmap_id}`)}
                            fullWidth
                          >
                            Detayları Görüntüle
                          </Button>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              </Box>
            </Grow>
          ) : (
            <Grow in={true} timeout={1000}>
              <Paper sx={{ p: 4, textAlign: 'center', borderRadius: 4 }}>
                <School sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                  Henüz İlerleme Yok
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                  İlk roadmap'inizi oluşturup öğrenmeye başlayın!
                </Typography>
                <Button
                  variant="contained"
                  onClick={() => navigate('/roadmap')}
                  size="large"
                  startIcon={<PlayArrow />}
                >
                  Roadmap Oluştur
                </Button>
              </Paper>
            </Grow>
          )}
        </>
      ) : (
        <Paper sx={{ p: 4, textAlign: 'center', borderRadius: 4 }}>
          <Typography variant="h6" gutterBottom>
            İlerleme verisi bulunamadı
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            İlerleme verilerinizi yüklemek için tekrar deneyin.
          </Typography>
          <Button
            variant="contained"
            onClick={loadProgressData}
            sx={{ mt: 2 }}
          >
            Tekrar Dene
          </Button>
        </Paper>
      )}

      {/* PDF Generator Dialog */}
      {showPDFGenerator && progressSummary && (
        <Dialog 
          open={showPDFGenerator} 
          onClose={() => setShowPDFGenerator(false)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6">PDF Raporu Oluşturucu</Typography>
            <IconButton onClick={() => setShowPDFGenerator(false)}>
              <Close />
            </IconButton>
          </DialogTitle>
          <DialogContent>
            <PDFGenerator 
              progressData={progressSummary}
              onClose={() => setShowPDFGenerator(false)}
            />
          </DialogContent>
        </Dialog>
      )}
    </Container>
  );
};

export default Progress;
