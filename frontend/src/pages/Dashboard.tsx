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
} from '@mui/material';
import {
  School,
  Timeline,
  Person,
  Logout,
  Add as AddIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import Chatbot from '../components/Chatbot';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleCreateRoadmap = () => {
    navigate('/roadmap');
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <School sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
          <Typography variant="h4" component="h1">
            MyWisePath
          </Typography>
        </Box>
        <Button
          variant="outlined"
          startIcon={<Logout />}
          onClick={handleLogout}
        >
          Çıkış Yap
        </Button>
      </Box>

      {/* Kullanıcı Bilgileri */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
              <Person />
            </Avatar>
            <Box>
              <Typography variant="h6">
                Hoş geldin, {user?.username}!
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {user?.email}
              </Typography>
            </Box>
          </Box>
          
          {user?.learning_goals && user.learning_goals.length > 0 && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Öğrenme Hedeflerin:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {user.learning_goals.map((goal, index) => (
                  <Chip
                    key={index}
                    label={goal}
                    color="primary"
                    variant="outlined"
                    size="small"
                  />
                ))}
              </Box>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Ana İçerik */}
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
        {/* Yol Haritası Oluştur */}
        <Paper
          sx={{
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            height: 240,
            cursor: 'pointer',
            transition: 'transform 0.2s',
            '&:hover': {
              transform: 'translateY(-4px)',
            },
          }}
          onClick={handleCreateRoadmap}
        >
          <Timeline sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
          <Typography variant="h5" gutterBottom>
            Yeni Yol Haritası Oluştur
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            İlgi alanlarınız ve hedeflerinize göre kişiselleştirilmiş bir öğrenme yol haritası oluşturun.
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{ mt: 'auto' }}
          >
            Başla
          </Button>
        </Paper>

        {/* Hızlı Başlangıç */}
        <Paper sx={{ p: 3, height: 240 }}>
          <Typography variant="h5" gutterBottom>
            Hızlı Başlangıç
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Popüler öğrenme alanlarından birini seçin:
          </Typography>
          
          <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
            <Button
              variant="outlined"
              fullWidth
              sx={{ height: 60 }}
              onClick={() => navigate('/roadmap')}
            >
              Veri Bilimi
            </Button>
            <Button
              variant="outlined"
              fullWidth
              sx={{ height: 60 }}
              onClick={() => navigate('/roadmap')}
            >
              Web Geliştirme
            </Button>
            <Button
              variant="outlined"
              fullWidth
              sx={{ height: 60 }}
              onClick={() => navigate('/roadmap')}
            >
              Mobil Uygulama
            </Button>
            <Button
              variant="outlined"
              fullWidth
              sx={{ height: 60 }}
              onClick={() => navigate('/roadmap')}
            >
              AI & ML
            </Button>
          </Box>
        </Paper>
      </Box>

      {/* İstatistikler */}
      <Box sx={{ mt: 3 }}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Öğrenme İstatistikleriniz
          </Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr 1fr' }, gap: 3 }}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary.main">
                0
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Tamamlanan Modül
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary.main">
                0
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Toplam Saat
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary.main">
                0%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Genel İlerleme
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Box>
      
      {/* Chatbot */}
      <Chatbot />
    </Container>
  );
};

export default Dashboard; 