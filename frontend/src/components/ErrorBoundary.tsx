import React, { Component, ErrorInfo, ReactNode } from 'react';
import {
  Box,
  Typography,
  Button,
  Paper,
  Container,
  Fade,
} from '@mui/material';
import {
  Error,
  Refresh,
  Home,
  Report,
} from '@mui/icons-material';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined });
  };

  handleGoHome = () => {
    window.location.href = '/dashboard';
  };

  render() {
    if (this.state.hasError) {
      return (
        <Container maxWidth="sm" sx={{ mt: 8 }}>
          <Fade in={true} timeout={800}>
            <Paper
              sx={{
                p: 4,
                textAlign: 'center',
                borderRadius: 4,
                background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(0, 0, 0, 0.08)',
              }}
            >
              <Error
                sx={{
                  fontSize: 80,
                  color: 'error.main',
                  mb: 3,
                  filter: 'drop-shadow(0 4px 8px rgba(239, 68, 68, 0.3))',
                }}
              />
              <Typography variant="h4" gutterBottom sx={{ fontWeight: 700, mb: 2 }}>
                Oops! Bir Hata Oluştu
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin veya ana sayfaya dönün.
              </Typography>
              
              {this.state.error && (
                <Box sx={{ mb: 4, p: 2, bgcolor: 'grey.50', borderRadius: 2 }}>
                  <Typography variant="body2" color="text.secondary" sx={{ fontFamily: 'monospace' }}>
                    {this.state.error.message}
                  </Typography>
                </Box>
              )}

              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  startIcon={<Refresh />}
                  onClick={this.handleRetry}
                  sx={{
                    background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                      transform: 'translateY(-2px)',
                      boxShadow: '0 8px 25px rgba(99, 102, 241, 0.3)',
                    },
                  }}
                >
                  Tekrar Dene
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Home />}
                  onClick={this.handleGoHome}
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
                  Ana Sayfa
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Report />}
                  onClick={() => window.open('mailto:support@mywisepath.com', '_blank')}
                  sx={{
                    borderColor: 'secondary.main',
                    color: 'secondary.main',
                    '&:hover': {
                      borderColor: 'secondary.dark',
                      backgroundColor: 'secondary.main',
                      color: 'white',
                    },
                  }}
                >
                  Rapor Et
                </Button>
              </Box>
            </Paper>
          </Fade>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
