import React, { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Link,
  Card,
  CardContent,
} from '@mui/material';
import { School, Login as LoginIcon } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Giriş başarısız');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = () => {
    setEmail('demo@mywisepath.com');
    setPassword('demo123');
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        {/* Logo ve Başlık */}
        <Box sx={{ mb: 3, textAlign: 'center' }}>
          <School sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
          <Typography component="h1" variant="h4" gutterBottom>
            MyWisePath
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Kişiselleştirilmiş Öğrenme Platformu
          </Typography>
        </Box>

        {/* Login Formu */}
        <Paper
          elevation={3}
          sx={{
            padding: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
          }}
        >
          <Typography component="h2" variant="h5" gutterBottom>
            Giriş Yap
          </Typography>

          {error && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Adresi"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Şifre"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
              startIcon={<LoginIcon />}
            >
              {loading ? 'Giriş Yapılıyor...' : 'Giriş Yap'}
            </Button>
          </Box>

          {/* Demo Kullanıcı Bilgileri */}
          <Card sx={{ width: '100%', mt: 2, bgcolor: 'grey.50' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Demo Kullanıcı
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Test için aşağıdaki bilgileri kullanabilirsiniz:
              </Typography>
              <Typography variant="body2" component="div">
                <strong>Email:</strong> demo@mywisepath.com
              </Typography>
              <Typography variant="body2" component="div">
                <strong>Şifre:</strong> demo123
              </Typography>
              <Button
                variant="outlined"
                size="small"
                onClick={handleDemoLogin}
                sx={{ mt: 1 }}
              >
                Demo Bilgilerini Doldur
              </Button>
            </CardContent>
          </Card>

          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Typography variant="body2">
              Hesabınız yok mu?{' '}
              <Link component={RouterLink} to="/register" variant="body2">
                Kayıt Ol
              </Link>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Login; 