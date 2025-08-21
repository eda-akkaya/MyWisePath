import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
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
  TextField,
  FormControlLabel,
  Checkbox,
  IconButton,
  Divider,
  Alert,
  Fade,
  Grow,
} from '@mui/material';
import {
  ArrowBack,
  PlayArrow,
  Pause,
  Stop,
  Refresh,
  Settings,
  MusicNote,
  Psychology,
  Timer,
  TrendingUp,
  CheckCircle,
  EmojiEvents,
  School,
  AccessTime,
  Assessment,
  CalendarToday,
  EmojiEvents as EmojiEventsIcon,
  Search,
  VolumeUp,
  SkipPrevious,
  SkipNext,
} from '@mui/icons-material';

interface TimerSession {
  id: string;
  user_id: string;
  timer_type: 'pomodoro' | 'break' | 'long_break';
  duration_minutes: number;
  start_time: string;
  end_time?: string;
  completed: boolean;
  notes?: string;
}

interface AmbientSound {
  id: string;
  name: string;
  genre: string;
  description: string;
  duration_minutes?: number;
  url?: string;
  tags: string[];
}

interface MotivationalMessage {
  id: string;
  message: string;
  category: string;
  author?: string;
  tags: string[];
}

interface FocusTechnique {
  name: string;
  description: string;
  steps: string[];
}

interface TimerSettings {
  pomodoroDuration: number;
  shortBreakDuration: number;
  longBreakDuration: number;
  autoStartBreaks: boolean;
  eyeCareReminders: boolean;
  targetPomodoros: number;
}

const LearningEnvironment: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [currentSession, setCurrentSession] = useState<TimerSession | null>(null);
  const [timeLeft, setTimeLeft] = useState<number>(0);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [currentSound, setCurrentSound] = useState<AmbientSound | null>(null);
  const [motivationalMessage, setMotivationalMessage] = useState<MotivationalMessage | null>(null);
  const [focusTechniques, setFocusTechniques] = useState<Record<string, FocusTechnique>>({});
  const [showSettings, setShowSettings] = useState<boolean>(false);
  const [timerSettings, setTimerSettings] = useState<TimerSettings>({
    pomodoroDuration: 25,
    shortBreakDuration: 5,
    longBreakDuration: 15,
    autoStartBreaks: true,
    eyeCareReminders: true,
    targetPomodoros: 4
  });
  const [completedPomodoros, setCompletedPomodoros] = useState<number>(0);
  const [currentPomodoroCount, setCurrentPomodoroCount] = useState<number>(0);
  const [currentTechniqueIndex, setCurrentTechniqueIndex] = useState<number>(0);

  useEffect(() => {
    // Sayfa yüklendiğinde motivasyonel mesaj getir
    fetchMotivationalMessage();
    fetchFocusTechniques();
    // Sayfa yüklendiğinde ambient ses önerisi getir
    fetchAmbientSoundRecommendation('focus');
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleSessionComplete();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning, timeLeft]);

  // Klavye navigasyonu için useEffect
  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      const techniquesArray = Object.values(focusTechniques);
      if (techniquesArray.length === 0) return;

      if (event.key === 'ArrowLeft') {
        setCurrentTechniqueIndex(prev => 
          prev > 0 ? prev - 1 : techniquesArray.length - 1
        );
      } else if (event.key === 'ArrowRight') {
        setCurrentTechniqueIndex(prev => 
          prev < techniquesArray.length - 1 ? prev + 1 : 0
        );
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [focusTechniques]);

  const fetchMotivationalMessage = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/learning-environment/motivational-messages/random?category=daily', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const message = await response.json();
        setMotivationalMessage(message);
      } else {
        console.error('Motivasyonel mesaj alınamadı:', response.status);
      }
    } catch (error) {
      console.error('Motivasyonel mesaj alınamadı:', error);
    }
  };

  const fetchFocusTechniques = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/learning-environment/focus-techniques', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const techniques = await response.json();
        setFocusTechniques(techniques);
      } else {
        console.error('Odaklanma teknikleri alınamadı:', response.status);
      }
    } catch (error) {
      console.error('Odaklanma teknikleri alınamadı:', error);
    }
  };

  const startPomodoroSession = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/learning-environment/timer/pomodoro', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ duration: timerSettings.pomodoroDuration })
      });
      
      if (response.ok) {
        const session = await response.json();
        setCurrentSession(session);
        setTimeLeft(timerSettings.pomodoroDuration * 60);
        setIsRunning(true);
        setCurrentPomodoroCount(prev => prev + 1);
        
        // Ambient ses önerisi al
        fetchAmbientSoundRecommendation('focus');
      } else {
        console.error('Pomodoro oturumu başlatılamadı:', response.status);
        // Fallback: Local timer başlat
        const localSession = {
          id: 'local-' + Date.now(),
          user_id: 'local',
          timer_type: 'pomodoro' as const,
          duration_minutes: timerSettings.pomodoroDuration,
          start_time: new Date().toISOString(),
          completed: false
        };
        setCurrentSession(localSession);
        setTimeLeft(timerSettings.pomodoroDuration * 60);
        setIsRunning(true);
        setCurrentPomodoroCount(prev => prev + 1);
        fetchAmbientSoundRecommendation('focus');
      }
    } catch (error) {
      console.error('Pomodoro oturumu başlatılamadı:', error);
      // Fallback: Local timer başlat
      const localSession = {
        id: 'local-' + Date.now(),
        user_id: 'local',
        timer_type: 'pomodoro' as const,
        duration_minutes: timerSettings.pomodoroDuration,
        start_time: new Date().toISOString(),
        completed: false
      };
      setCurrentSession(localSession);
      setTimeLeft(timerSettings.pomodoroDuration * 60);
      setIsRunning(true);
      setCurrentPomodoroCount(prev => prev + 1);
      fetchAmbientSoundRecommendation('focus');
    }
  };

  const startBreakSession = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/learning-environment/timer/break', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ duration: timerSettings.shortBreakDuration })
      });
      
      if (response.ok) {
        const session = await response.json();
        setCurrentSession(session);
        setTimeLeft(timerSettings.shortBreakDuration * 60);
        setIsRunning(true);
      } else {
        console.error('Mola oturumu başlatılamadı:', response.status);
        // Fallback: Local timer başlat
        const localSession = {
          id: 'local-' + Date.now(),
          user_id: 'local',
          timer_type: 'break' as const,
          duration_minutes: timerSettings.shortBreakDuration,
          start_time: new Date().toISOString(),
          completed: false
        };
        setCurrentSession(localSession);
        setTimeLeft(timerSettings.shortBreakDuration * 60);
        setIsRunning(true);
      }
    } catch (error) {
      console.error('Mola oturumu başlatılamadı:', error);
      // Fallback: Local timer başlat
      const localSession = {
        id: 'local-' + Date.now(),
        user_id: 'local',
        timer_type: 'break' as const,
        duration_minutes: timerSettings.shortBreakDuration,
        start_time: new Date().toISOString(),
        completed: false
      };
      setCurrentSession(localSession);
      setTimeLeft(timerSettings.shortBreakDuration * 60);
      setIsRunning(true);
    }
  };

  const startLongBreakSession = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/learning-environment/timer/long-break', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ duration: timerSettings.longBreakDuration })
      });
      
      if (response.ok) {
        const session = await response.json();
        setCurrentSession(session);
        setTimeLeft(timerSettings.longBreakDuration * 60);
        setIsRunning(true);
      } else {
        console.error('Uzun mola oturumu başlatılamadı:', response.status);
        // Fallback: Local timer başlat
        const localSession = {
          id: 'local-' + Date.now(),
          user_id: 'local',
          timer_type: 'long_break' as const,
          duration_minutes: timerSettings.longBreakDuration,
          start_time: new Date().toISOString(),
          completed: false
        };
        setCurrentSession(localSession);
        setTimeLeft(timerSettings.longBreakDuration * 60);
        setIsRunning(true);
      }
    } catch (error) {
      console.error('Uzun mola oturumu başlatılamadı:', error);
      // Fallback: Local timer başlat
      const localSession = {
        id: 'local-' + Date.now(),
        user_id: 'local',
        timer_type: 'long_break' as const,
        duration_minutes: timerSettings.longBreakDuration,
        start_time: new Date().toISOString(),
        completed: false
      };
      setCurrentSession(localSession);
      setTimeLeft(timerSettings.longBreakDuration * 60);
      setIsRunning(true);
    }
  };

  const pauseSession = () => {
    setIsRunning(false);
  };

  const resumeSession = () => {
    setIsRunning(true);
  };

  const stopSession = () => {
    setIsRunning(false);
    setCurrentSession(null);
    setTimeLeft(0);
  };

  const handleSessionComplete = () => {
    setIsRunning(false);
    if (currentSession?.timer_type === 'pomodoro') {
      setCompletedPomodoros(prev => prev + 1);
    }
    setCurrentSession(null);
    setTimeLeft(0);
    
    // Otomatik mola başlatma
    if (timerSettings.autoStartBreaks && currentSession?.timer_type === 'pomodoro') {
      if (completedPomodoros + 1 >= timerSettings.targetPomodoros) {
        startLongBreakSession();
      } else {
        startBreakSession();
      }
    }
  };

  const handleSettingsChange = (setting: keyof TimerSettings, value: any) => {
    setTimerSettings(prev => ({
      ...prev,
      [setting]: value
    }));
  };

  const resetPomodoroCount = () => {
    setCompletedPomodoros(0);
    setCurrentPomodoroCount(0);
  };

  const fetchAmbientSoundRecommendation = async (mood: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/learning-environment/ambient-sounds/recommend?mood=${mood}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const sound = await response.json();
        setCurrentSound(sound);
      } else {
        console.error('Ambient ses önerisi alınamadı:', response.status);
      }
    } catch (error) {
      console.error('Ambient ses önerisi alınamadı:', error);
    }
  };

  const handlePlaySound = (sound: AmbientSound) => {
    if (sound.url) {
      window.open(sound.url, '_blank');
    } else {
      alert('Bu ses için link henüz eklenmemiş.');
    }
  };

  const handleBackToDashboard = () => {
    navigate('/dashboard');
  };

  const getSessionTypeText = (type: string) => {
    switch (type) {
      case 'pomodoro':
        return '🍅 Pomodoro';
      case 'break':
        return '☕ Kısa Mola';
      case 'long_break':
        return '🌴 Uzun Mola';
      default:
        return '⏰ Timer';
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const techniquesArray = Object.values(focusTechniques);
  const currentTechnique = techniquesArray[currentTechniqueIndex];

  const handleNextTechnique = () => {
    setCurrentTechniqueIndex(prev => 
      prev < techniquesArray.length - 1 ? prev + 1 : 0
    );
  };

  const handlePreviousTechnique = () => {
    setCurrentTechniqueIndex(prev => 
      prev > 0 ? prev - 1 : techniquesArray.length - 1
    );
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 4 }}>
      {/* Page Header */}
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
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Button
              variant="outlined"
              onClick={handleBackToDashboard}
              startIcon={<ArrowBack />}
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
              Geri Dön
            </Button>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flex: 1, justifyContent: 'center' }}>
              <Timer sx={{ fontSize: 32, color: 'primary.main' }} />
              <Typography variant="h4" sx={{ fontWeight: 700 }}>
                Çalışma Alanı
              </Typography>
            </Box>
          </Box>
        </Box>
      </Fade>

      {/* Motivational Message */}
      {motivationalMessage && (
        <Grow in={true} timeout={800}>
          <Paper sx={{ 
            mb: 4, 
            p: 3, 
            borderRadius: 4,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            textAlign: 'center',
          }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
              {motivationalMessage.message}
            </Typography>
            {motivationalMessage.author && (
              <Typography variant="body2" sx={{ opacity: 0.8, fontStyle: 'italic', mb: 2 }}>
                - {motivationalMessage.author}
              </Typography>
            )}
            <Button
              variant="contained"
              onClick={() => fetchMotivationalMessage()}
              startIcon={<Refresh />}
              sx={{
                bgcolor: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                border: '2px solid rgba(255, 255, 255, 0.3)',
                '&:hover': {
                  bgcolor: 'rgba(255, 255, 255, 0.3)',
                  borderColor: 'rgba(255, 255, 255, 0.5)',
                },
              }}
            >
              💪 Yeni Motivasyon
            </Button>
          </Paper>
        </Grow>
      )}

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
        {/* Left Column - Timer and Settings */}
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {/* Timer Section */}
          <Card sx={{ borderRadius: 4 }}>
            <CardContent sx={{ p: 4 }}>
              {currentSession ? (
                <Box sx={{ textAlign: 'center' }}>
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" sx={{ fontWeight: 600, mb: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                      {getSessionTypeText(currentSession.timer_type)}
                      {currentSession.timer_type === 'pomodoro' && (
                        <Chip
                          label={`#${currentPomodoroCount}`}
                          color="error"
                          size="small"
                          sx={{ fontWeight: 600 }}
                        />
                      )}
                    </Typography>
                    <Typography variant="h2" sx={{ fontWeight: 700, color: 'error.main', fontFamily: 'monospace', mb: 2 }}>
                      {formatTime(timeLeft)}
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={((currentSession.duration_minutes * 60 - timeLeft) / (currentSession.duration_minutes * 60)) * 100}
                      sx={{ height: 8, borderRadius: 4 }}
                      color="primary"
                    />
                  </Box>
                  
                  <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                    {isRunning ? (
                      <Button
                        variant="contained"
                        onClick={pauseSession}
                        startIcon={<Pause />}
                        color="warning"
                        sx={{
                          '&:hover': {
                            transform: 'translateY(-2px)',
                            boxShadow: 4,
                          },
                        }}
                      >
                        Duraklat
                      </Button>
                    ) : (
                      <Button
                        variant="contained"
                        onClick={resumeSession}
                        startIcon={<PlayArrow />}
                        color="success"
                        sx={{
                          '&:hover': {
                            transform: 'translateY(-2px)',
                            boxShadow: 4,
                          },
                        }}
                      >
                        Devam Et
                      </Button>
                    )}
                    <Button
                      variant="outlined"
                      onClick={stopSession}
                      startIcon={<Stop />}
                      sx={{
                        '&:hover': {
                          transform: 'translateY(-2px)',
                          boxShadow: 4,
                        },
                      }}
                    >
                      Durdur
                    </Button>
                  </Box>
                </Box>
              ) : (
                <Box sx={{ textAlign: 'center' }}>
                  <Button
                    variant="contained"
                    onClick={startPomodoroSession}
                    disabled={completedPomodoros >= timerSettings.targetPomodoros}
                    startIcon={<PlayArrow />}
                    size="large"
                    sx={{
                      py: 2,
                      px: 4,
                      fontSize: '1.1rem',
                      '&:hover': {
                        transform: 'translateY(-2px)',
                        boxShadow: 4,
                      },
                    }}
                  >
                    Pomodoro Başlat ({timerSettings.pomodoroDuration}dk)
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>

          {/* Settings Section */}
          <Card sx={{ borderRadius: 4 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Settings /> Öğrenme Ortamı Ayarları
              </Typography>
              <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
                <TextField
                  fullWidth
                  label="Pomodoro Süresi (dk)"
                  type="number"
                  value={timerSettings.pomodoroDuration}
                  onChange={(e) => handleSettingsChange('pomodoroDuration', parseInt(e.target.value))}
                  inputProps={{ min: 15, max: 60 }}
                />
                <TextField
                  fullWidth
                  label="Kısa Mola (dk)"
                  type="number"
                  value={timerSettings.shortBreakDuration}
                  onChange={(e) => handleSettingsChange('shortBreakDuration', parseInt(e.target.value))}
                  inputProps={{ min: 3, max: 10 }}
                />
                <TextField
                  fullWidth
                  label="Uzun Mola (dk)"
                  type="number"
                  value={timerSettings.longBreakDuration}
                  onChange={(e) => handleSettingsChange('longBreakDuration', parseInt(e.target.value))}
                  inputProps={{ min: 10, max: 30 }}
                />
                <TextField
                  fullWidth
                  label="Hedef Pomodoro"
                  type="number"
                  value={timerSettings.targetPomodoros}
                  onChange={(e) => handleSettingsChange('targetPomodoros', parseInt(e.target.value))}
                  inputProps={{ min: 1, max: 20 }}
                />
                <Box sx={{ gridColumn: 'span 2' }}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={timerSettings.autoStartBreaks}
                        onChange={(e) => handleSettingsChange('autoStartBreaks', e.target.checked)}
                      />
                    }
                    label="Otomatik mola başlat"
                  />
                </Box>
                <Box sx={{ gridColumn: 'span 2' }}>
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={timerSettings.eyeCareReminders}
                        onChange={(e) => handleSettingsChange('eyeCareReminders', e.target.checked)}
                      />
                    }
                    label="Göz bakımı hatırlatıcıları"
                  />
                </Box>
              </Box>
            </CardContent>
          </Card>

          {/* Pomodoro Progress */}
          <Card sx={{ borderRadius: 4 }}>
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Tamamlanan: {completedPomodoros}/{timerSettings.targetPomodoros}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Hedef: {timerSettings.targetPomodoros} Pomodoro
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={(completedPomodoros / timerSettings.targetPomodoros) * 100}
                  sx={{ height: 10, borderRadius: 5 }}
                  color="success"
                />
              </Box>
              <Button
                variant="outlined"
                onClick={resetPomodoroCount}
                startIcon={<Refresh />}
                size="small"
                sx={{
                  '&:hover': {
                    transform: 'translateY(-1px)',
                    boxShadow: 2,
                  },
                }}
              >
                Sıfırla
              </Button>
            </CardContent>
          </Card>
        </Box>

        {/* Right Column - Ambient Sound and Focus Techniques */}
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          {/* Ambient Sound Section */}
          <Card sx={{ borderRadius: 4 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <MusicNote /> Önerilen Ses
              </Typography>
              {currentSound ? (
                <Paper sx={{ 
                  p: 3, 
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  textAlign: 'center',
                }}>
                  <Typography variant="h6" sx={{ mb: 1 }}>
                    {currentSound.name}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 2, opacity: 0.9 }}>
                    {currentSound.description}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', flexWrap: 'wrap', mb: 2 }}>
                    {currentSound.tags.map((tag, index) => (
                      <Chip
                        key={index}
                        label={tag}
                        size="small"
                        sx={{
                          bgcolor: 'rgba(255, 255, 255, 0.2)',
                          color: 'white',
                          fontSize: '0.75rem',
                        }}
                      />
                    ))}
                  </Box>
                  <Button
                    variant="contained"
                    onClick={() => handlePlaySound(currentSound)}
                    startIcon={<VolumeUp />}
                    sx={{
                      bgcolor: 'rgba(255, 255, 255, 0.2)',
                      color: 'white',
                      border: '2px solid rgba(255, 255, 255, 0.3)',
                      '&:hover': {
                        bgcolor: 'rgba(255, 255, 255, 0.3)',
                        borderColor: 'rgba(255, 255, 255, 0.5)',
                      },
                    }}
                  >
                    Dinle
                  </Button>
                </Paper>
              ) : (
                <Paper sx={{ 
                  p: 3, 
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #95a5a6, #7f8c8d)',
                  color: 'white',
                  textAlign: 'center',
                  opacity: 0.8,
                }}>
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    🎵 Ses önerisi yükleniyor...
                  </Typography>
                  <Button
                    variant="contained"
                    onClick={() => fetchAmbientSoundRecommendation('focus')}
                    startIcon={<Refresh />}
                    sx={{
                      bgcolor: 'rgba(255, 255, 255, 0.2)',
                      color: 'white',
                      border: '2px solid rgba(255, 255, 255, 0.3)',
                      '&:hover': {
                        bgcolor: 'rgba(255, 255, 255, 0.3)',
                        borderColor: 'rgba(255, 255, 255, 0.5)',
                      },
                    }}
                  >
                    Yenile
                  </Button>
                </Paper>
              )}
            </CardContent>
          </Card>

          {/* Focus Techniques Section */}
          <Card sx={{ borderRadius: 4 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Psychology /> Odaklanma Teknikleri
              </Typography>
              {currentTechnique ? (
                <Paper sx={{ 
                  p: 3, 
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                  color: 'white',
                }}>
                  <Typography variant="h6" sx={{ mb: 1 }}>
                    {currentTechnique.name}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 2, opacity: 0.9 }}>
                    {currentTechnique.description}
                  </Typography>
                  <Box component="ul" sx={{ pl: 2, mb: 2 }}>
                    {currentTechnique.steps.map((step, index) => (
                      <Typography key={index} component="li" variant="body2" sx={{ mb: 1, opacity: 0.9 }}>
                        {step}
                      </Typography>
                    ))}
                  </Box>
                  <Divider sx={{ my: 2, borderColor: 'rgba(255, 255, 255, 0.2)' }} />
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <IconButton
                      onClick={handlePreviousTechnique}
                      disabled={techniquesArray.length <= 1}
                      sx={{
                        color: 'white',
                        bgcolor: 'rgba(255, 255, 255, 0.2)',
                        '&:hover': {
                          bgcolor: 'rgba(255, 255, 255, 0.3)',
                        },
                        '&:disabled': {
                          opacity: 0.4,
                        },
                      }}
                    >
                      <SkipPrevious />
                    </IconButton>
                    <Chip
                      label={`${currentTechniqueIndex + 1} / ${techniquesArray.length}`}
                      size="small"
                      sx={{
                        bgcolor: 'rgba(255, 255, 255, 0.2)',
                        color: 'white',
                        fontWeight: 600,
                      }}
                    />
                    <IconButton
                      onClick={handleNextTechnique}
                      disabled={techniquesArray.length <= 1}
                      sx={{
                        color: 'white',
                        bgcolor: 'rgba(255, 255, 255, 0.2)',
                        '&:hover': {
                          bgcolor: 'rgba(255, 255, 255, 0.3)',
                        },
                        '&:disabled': {
                          opacity: 0.4,
                        },
                      }}
                    >
                      <SkipNext />
                    </IconButton>
                  </Box>
                </Paper>
              ) : (
                <Paper sx={{ 
                  p: 3, 
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #95a5a6, #7f8c8d)',
                  color: 'white',
                  textAlign: 'center',
                  opacity: 0.8,
                }}>
                  <Typography variant="body1">
                    🧠 Odaklanma teknikleri yükleniyor...
                  </Typography>
                </Paper>
              )}
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Container>
  );
};

export default LearningEnvironment; 