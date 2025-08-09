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
  Chip,
  Avatar,
  Divider,
  IconButton,
  Grid,
  Fade,
  Grow,
  LinearProgress,
  Badge,
} from '@mui/material';
import {
  School,
  Timeline,
  Person,
  Logout,
  Add as AddIcon,
  Timer,
  Settings,
  TrendingUp,
  Psychology,
  AutoAwesome,
  Star,
  CheckCircle,
  PlayArrow,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import Chatbot from '../components/Chatbot';
import UserProfile from '../components/UserProfile';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [profileOpen, setProfileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleCreateRoadmap = () => {
    navigate('/roadmap');
  };

  const handleLearningEnvironment = () => {
    navigate('/learning-environment');
  };

  const handleOpenProfile = () => {
    setProfileOpen(true);
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
      {/* Welcome Section */}
      <Fade in={true} timeout={800}>
        <Box sx={{ 
          mb: 4,
          p: 3,
          borderRadius: 4,
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(0, 0, 0, 0.08)',
        }}>
          <Typography 
            variant="h4" 
            component="h1"
            sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              mb: 1,
            }}
          >
            Hoş Geldiniz! 👋
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Kişiselleştirilmiş öğrenme yolculuğunuza başlayın
          </Typography>
        </Box>
      </Fade>

      {/* Kullanıcı Bilgileri */}
      <Grow in={true} timeout={1000}>
        <Card sx={{ 
          mb: 4,
          borderRadius: 4,
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(0, 0, 0, 0.08)',
        }}>
          <CardContent sx={{ p: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
              <Badge
                overlap="circular"
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                badgeContent={
                  <Star sx={{ fontSize: 16, color: 'secondary.main' }} />
                }
              >
                <Avatar 
                  sx={{ 
                    mr: 3, 
                    bgcolor: 'primary.main',
                    width: 64,
                    height: 64,
                    fontSize: '1.5rem',
                  }}
                >
                  <Person />
                </Avatar>
              </Badge>
              <Box sx={{ flexGrow: 1 }}>
                <Typography variant="h5" sx={{ fontWeight: 600, mb: 1 }}>
                  Hoş geldin, {user?.username}! 👋
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  {user?.email}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Chip 
                    icon={<TrendingUp />} 
                    label="Aktif Öğrenci" 
                    color="success" 
                    variant="outlined"
                    size="small"
                  />
                  <Chip 
                    icon={<Psychology />} 
                    label="Kişiselleştirilmiş" 
                    color="primary" 
                    variant="outlined"
                    size="small"
                  />
                </Box>
              </Box>
              <IconButton 
                onClick={handleOpenProfile} 
                size="large"
                sx={{
                  bgcolor: 'grey.100',
                  '&:hover': {
                    bgcolor: 'primary.main',
                    color: 'white',
                  },
                }}
              >
                <Settings />
              </IconButton>
            </Box>
            
            <Divider sx={{ my: 3 }} />
            
            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
              {user?.learning_goals && user.learning_goals.length > 0 && (
                <Box>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                    🎯 Öğrenme Hedeflerin
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {user.learning_goals.map((goal, index) => (
                      <Chip
                        key={index}
                        label={goal}
                        color="primary"
                        variant="outlined"
                        size="small"
                        icon={<CheckCircle />}
                      />
                    ))}
                  </Box>
                </Box>
              )}

              {user?.interests && user.interests.length > 0 && (
                <Box>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                    🔥 İlgi Alanların
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                    {user.interests.map((interest, index) => (
                      <Chip
                        key={index}
                        label={interest}
                        color="secondary"
                        variant="outlined"
                        size="small"
                        icon={<AutoAwesome />}
                      />
                    ))}
                  </Box>
                </Box>
              )}
            </Box>

            {user?.skill_level && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
                  📊 Seviye Durumu
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <Chip 
                    label={
                      user.skill_level === 'beginner' ? 'Başlangıç' : 
                      user.skill_level === 'intermediate' ? 'Orta Seviye' : 'İleri Seviye'
                    }
                    color={
                      user.skill_level === 'beginner' ? 'warning' :
                      user.skill_level === 'intermediate' ? 'info' : 'success'
                    }
                    variant="filled"
                    icon={<TrendingUp />}
                  />
                  <LinearProgress 
                    variant="determinate" 
                    value={
                      user.skill_level === 'beginner' ? 30 :
                      user.skill_level === 'intermediate' ? 60 : 90
                    }
                    sx={{ 
                      flexGrow: 1,
                      height: 8,
                      borderRadius: 4,
                      bgcolor: 'grey.200',
                      '& .MuiLinearProgress-bar': {
                        borderRadius: 4,
                      },
                    }}
                  />
                </Box>
              </Box>
            )}
          </CardContent>
        </Card>
      </Grow>

      {/* Ana İçerik */}
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
        {/* Yol Haritası Oluştur */}
        <Box>
          <Grow in={true} timeout={1200}>
            <Paper
              sx={{
                p: 4,
                display: 'flex',
                flexDirection: 'column',
                height: 280,
                cursor: 'pointer',
                transition: 'all 0.3s ease-in-out',
                borderRadius: 4,
                background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(0, 0, 0, 0.08)',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: '0 20px 40px rgba(99, 102, 241, 0.15)',
                  borderColor: 'primary.main',
                },
              }}
              onClick={handleCreateRoadmap}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Box sx={{ 
                  p: 2, 
                  bgcolor: 'primary.main', 
                  borderRadius: 3,
                  mr: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}>
                  <Timeline sx={{ fontSize: 32, color: 'white' }} />
                </Box>
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                  Yeni Yol Haritası
                </Typography>
              </Box>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 3, flexGrow: 1 }}>
                İlgi alanlarınız ve hedeflerinize göre kişiselleştirilmiş bir öğrenme yol haritası oluşturun. 
                AI destekli önerilerle en uygun yolu keşfedin.
              </Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                endIcon={<PlayArrow />}
                size="large"
                sx={{ 
                  alignSelf: 'flex-start',
                  background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 25px rgba(99, 102, 241, 0.3)',
                  },
                }}
              >
                Başla
              </Button>
            </Paper>
          </Grow>
        </Box>

        {/* Öğrenme Ortamı Agent'ı */}
        <Box>
          <Grow in={true} timeout={1400}>
            <Paper
              sx={{
                p: 4,
                display: 'flex',
                flexDirection: 'column',
                height: 280,
                cursor: 'pointer',
                transition: 'all 0.3s ease-in-out',
                borderRadius: 4,
                background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(0, 0, 0, 0.08)',
                '&:hover': {
                  transform: 'translateY(-8px)',
                  boxShadow: '0 20px 40px rgba(245, 158, 11, 0.15)',
                  borderColor: 'secondary.main',
                },
              }}
              onClick={handleLearningEnvironment}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <Box sx={{ 
                  p: 2, 
                  bgcolor: 'secondary.main', 
                  borderRadius: 3,
                  mr: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}>
                  <Timer sx={{ fontSize: 32, color: 'white' }} />
                </Box>
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                  Öğrenme Ortamı
                </Typography>
              </Box>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 3, flexGrow: 1 }}>
                AI destekli öğrenme ortamında interaktif deneyimler yaşayın. 
                Kişiselleştirilmiş içerikler ve gerçek zamanlı geri bildirimlerle öğrenin.
              </Typography>
              <Button
                variant="contained"
                startIcon={<PlayArrow />}
                size="large"
                sx={{ 
                  alignSelf: 'flex-start',
                  background: 'linear-gradient(135deg, #f59e0b 0%, #f97316 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #d97706 0%, #ea580c 100%)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 25px rgba(245, 158, 11, 0.3)',
                  },
                }}
              >
                Keşfet
              </Button>
            </Paper>
          </Grow>
        </Box>
      </Box>

      {/* Chatbot */}
      <Box sx={{ mt: 4 }}>
        <Chatbot />
      </Box>

      {/* Profil Modal */}
      <UserProfile open={profileOpen} onClose={() => setProfileOpen(false)} />
    </Container>
  );
};

export default Dashboard; 