import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  CardHeader,
  Switch,
  FormControlLabel,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Divider,
  Alert,
  Paper,
  IconButton,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  Settings as SettingsIcon,
  Person,
  Notifications,
  Security,
  Palette,
  Language,
  Email,
  Delete,
  Save,
  Cancel,
  Edit,
  Visibility,
  VisibilityOff,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { authService, EmailSettings } from '../services/authService';

interface SettingsProps {}

const Settings: React.FC<SettingsProps> = () => {
  const { user, updateUser } = useAuth();
  const { darkMode, setDarkMode } = useTheme();
  const [activeTab, setActiveTab] = useState('profile');
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Profile settings
  const [username, setUsername] = useState(user?.username || '');
  const [email, setEmail] = useState(user?.email || '');
  const [skillLevel, setSkillLevel] = useState(user?.skill_level || 'beginner');
  const [interests, setInterests] = useState<string[]>(user?.interests || []);
  const [learningGoals, setLearningGoals] = useState<string[]>(user?.learning_goals || []);

  // Notification settings
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [pushNotifications, setPushNotifications] = useState(true);
  const [weeklyReports, setWeeklyReports] = useState(true);
  const [progressUpdates, setProgressUpdates] = useState(true);

  // Email settings
  const [emailSettings, setEmailSettings] = useState<EmailSettings>({
    email_frequency: 'weekly',
    weekly_reminders_enabled: true,
    progress_reports_enabled: true,
    instant_email_enabled: true
  });

  // Security settings
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPasswords, setShowPasswords] = useState(false);

  // Theme settings
  const [language, setLanguage] = useState('tr');

  useEffect(() => {
    if (user) {
      setUsername(user.username || '');
      setEmail(user.email || '');
      setSkillLevel(user.skill_level || 'beginner');
      setInterests(user.interests || []);
      setLearningGoals(user.learning_goals || []);
    }
    loadEmailSettings();
  }, [user]);

  const loadEmailSettings = async () => {
    try {
      const settings = await authService.getEmailSettings();
      setEmailSettings(settings);
    } catch (error) {
      console.error('Email settings load error:', error);
    }
  };

  const handleSaveProfile = async () => {
    setIsLoading(true);
    setMessage(null);

    try {
      const updatedUser = {
        id: user?.id || '',
        username,
        email,
        created_at: user?.created_at || new Date().toISOString(),
        skill_level: skillLevel,
        interests,
        learning_goals: learningGoals,
      };

      await authService.updateProfile(updatedUser);
      updateUser(updatedUser);
      setMessage({ type: 'success', text: 'Profil başarıyla güncellendi!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Profil güncellenirken bir hata oluştu.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveEmailSettings = async () => {
    setIsLoading(true);
    setMessage(null);

    try {
      await authService.updateEmailSettings(emailSettings);
      setMessage({ type: 'success', text: 'E-posta ayarları başarıyla güncellendi!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'E-posta ayarları güncellenirken bir hata oluştu.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      setMessage({ type: 'error', text: 'Yeni şifreler eşleşmiyor.' });
      return;
    }

    if (newPassword.length < 6) {
      setMessage({ type: 'error', text: 'Şifre en az 6 karakter olmalıdır.' });
      return;
    }

    setIsLoading(true);
    setMessage(null);

    try {
      await authService.changePassword(currentPassword, newPassword);
      setMessage({ type: 'success', text: 'Şifre başarıyla değiştirildi!' });
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (error) {
      setMessage({ type: 'error', text: 'Şifre değiştirilirken bir hata oluştu.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm('Hesabınızı silmek istediğinizden emin misiniz? Bu işlem geri alınamaz.')) {
      setIsLoading(true);
      setMessage(null);

      try {
        await authService.deleteAccount();
        setMessage({ type: 'success', text: 'Hesabınız başarıyla silindi.' });
        // Redirect to login after a delay
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
      } catch (error) {
        setMessage({ type: 'error', text: 'Hesap silinirken bir hata oluştu.' });
      } finally {
        setIsLoading(false);
      }
    }
  };

  const tabs = [
    { id: 'profile', label: 'Profil', icon: <Person /> },
    { id: 'notifications', label: 'Bildirimler', icon: <Notifications /> },
    { id: 'email', label: 'E-posta', icon: <Email /> },
    { id: 'security', label: 'Güvenlik', icon: <Security /> },
    { id: 'appearance', label: 'Görünüm', icon: <Palette /> },
  ];

  const renderProfileTab = () => (
    <Card>
      <CardHeader title="Profil Bilgileri" />
      <CardContent>
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
          <TextField
            fullWidth
            label="Kullanıcı Adı"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            margin="normal"
          />
          <TextField
            fullWidth
            label="E-posta"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            margin="normal"
          />
          <FormControl fullWidth margin="normal">
            <InputLabel>Seviye</InputLabel>
            <Select
              value={skillLevel}
              onChange={(e) => setSkillLevel(e.target.value)}
              label="Seviye"
            >
              <MenuItem value="beginner">Başlangıç</MenuItem>
              <MenuItem value="intermediate">Orta</MenuItem>
              <MenuItem value="advanced">İleri</MenuItem>
            </Select>
          </FormControl>
          <Box />
          <Box sx={{ gridColumn: { xs: '1', md: '1 / -1' } }}>
            <Typography variant="h6" gutterBottom>
              İlgi Alanları
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
              {interests.map((interest, index) => (
                <Chip
                  key={index}
                  label={interest}
                  onDelete={() => setInterests(interests.filter((_, i) => i !== index))}
                  color="primary"
                  variant="outlined"
                />
              ))}
            </Box>
            <TextField
              fullWidth
              label="Yeni İlgi Alanı Ekle"
              onKeyPress={(e) => {
                const target = e.target as HTMLInputElement;
                if (e.key === 'Enter' && target.value.trim()) {
                  setInterests([...interests, target.value.trim()]);
                  target.value = '';
                }
              }}
            />
          </Box>
          <Box sx={{ gridColumn: { xs: '1', md: '1 / -1' } }}>
            <Button
              variant="contained"
              onClick={handleSaveProfile}
              disabled={isLoading}
              startIcon={<Save />}
            >
              Profili Kaydet
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  const renderNotificationsTab = () => (
    <Card>
      <CardHeader title="Bildirim Ayarları" />
      <CardContent>
        <List>
          <ListItem>
            <ListItemIcon>
              <Email />
            </ListItemIcon>
            <ListItemText
              primary="E-posta Bildirimleri"
              secondary="Önemli güncellemeler için e-posta al"
            />
            <ListItemSecondaryAction>
              <Switch
                checked={emailNotifications}
                onChange={(e) => setEmailNotifications(e.target.checked)}
              />
            </ListItemSecondaryAction>
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <Notifications />
            </ListItemIcon>
            <ListItemText
              primary="Push Bildirimleri"
              secondary="Tarayıcı bildirimleri al"
            />
            <ListItemSecondaryAction>
              <Switch
                checked={pushNotifications}
                onChange={(e) => setPushNotifications(e.target.checked)}
              />
            </ListItemSecondaryAction>
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <Notifications />
            </ListItemIcon>
            <ListItemText
              primary="Haftalık Raporlar"
              secondary="Haftalık ilerleme raporları al"
            />
            <ListItemSecondaryAction>
              <Switch
                checked={weeklyReports}
                onChange={(e) => setWeeklyReports(e.target.checked)}
              />
            </ListItemSecondaryAction>
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <Notifications />
            </ListItemIcon>
            <ListItemText
              primary="İlerleme Güncellemeleri"
              secondary="Yeni modül tamamlandığında bildirim al"
            />
            <ListItemSecondaryAction>
              <Switch
                checked={progressUpdates}
                onChange={(e) => setProgressUpdates(e.target.checked)}
              />
            </ListItemSecondaryAction>
          </ListItem>
        </List>
      </CardContent>
    </Card>
  );

  const renderEmailTab = () => (
    <Card>
      <CardHeader title="E-posta Ayarları" />
      <CardContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <FormControl fullWidth margin="normal">
            <InputLabel>E-posta Sıklığı</InputLabel>
            <Select
              value={emailSettings.email_frequency}
              onChange={(e) => setEmailSettings({
                ...emailSettings,
                email_frequency: e.target.value
              })}
              label="E-posta Sıklığı"
            >
              <MenuItem value="daily">Günlük</MenuItem>
              <MenuItem value="weekly">Haftalık</MenuItem>
              <MenuItem value="monthly">Aylık</MenuItem>
            </Select>
          </FormControl>
          <FormControlLabel
            control={
              <Switch
                checked={emailSettings.weekly_reminders_enabled}
                onChange={(e) => setEmailSettings({
                  ...emailSettings,
                  weekly_reminders_enabled: e.target.checked
                })}
              />
            }
            label="Haftalık Hatırlatmalar"
          />
          <FormControlLabel
            control={
              <Switch
                checked={emailSettings.progress_reports_enabled}
                onChange={(e) => setEmailSettings({
                  ...emailSettings,
                  progress_reports_enabled: e.target.checked
                })}
              />
            }
            label="İlerleme Raporları"
          />
          <FormControlLabel
            control={
              <Switch
                checked={emailSettings.instant_email_enabled}
                onChange={(e) => setEmailSettings({
                  ...emailSettings,
                  instant_email_enabled: e.target.checked
                })}
              />
            }
            label="Anlık E-posta Bildirimleri"
          />
          <Button
            variant="contained"
            onClick={handleSaveEmailSettings}
            disabled={isLoading}
            startIcon={<Save />}
            sx={{ alignSelf: 'flex-start' }}
          >
            E-posta Ayarlarını Kaydet
          </Button>
        </Box>
      </CardContent>
    </Card>
  );

  const renderSecurityTab = () => (
    <Card>
      <CardHeader title="Güvenlik Ayarları" />
      <CardContent>
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3 }}>
          <TextField
            fullWidth
            label="Mevcut Şifre"
            type={showPasswords ? 'text' : 'password'}
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            margin="normal"
            InputProps={{
              endAdornment: (
                <IconButton
                  onClick={() => setShowPasswords(!showPasswords)}
                  edge="end"
                >
                  {showPasswords ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              ),
            }}
          />
          <TextField
            fullWidth
            label="Yeni Şifre"
            type={showPasswords ? 'text' : 'password'}
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Yeni Şifre (Tekrar)"
            type={showPasswords ? 'text' : 'password'}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            margin="normal"
          />
          <Box />
          <Box sx={{ gridColumn: { xs: '1', md: '1 / -1' } }}>
            <Button
              variant="contained"
              onClick={handleChangePassword}
              disabled={isLoading}
              startIcon={<Save />}
            >
              Şifreyi Değiştir
            </Button>
          </Box>
          <Box sx={{ gridColumn: { xs: '1', md: '1 / -1' } }}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6" color="error" gutterBottom>
              Tehlikeli Bölge
            </Typography>
            <Button
              variant="outlined"
              color="error"
              onClick={handleDeleteAccount}
              disabled={isLoading}
              startIcon={<Delete />}
            >
              Hesabı Sil
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  const renderAppearanceTab = () => (
    <Card>
      <CardHeader title="Görünüm Ayarları" />
      <CardContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
          <Box>
            <FormControlLabel
              control={
                <Switch
                  checked={darkMode}
                  onChange={(e) => {
                    setDarkMode(e.target.checked);
                    setMessage({ 
                      type: 'success', 
                      text: `${e.target.checked ? 'Karanlık' : 'Açık'} mod aktif edildi!` 
                    });
                  }}
                />
              }
              label="Karanlık Mod"
            />
            <Typography variant="body2" color="text.secondary" sx={{ ml: 4, mt: 0.5 }}>
              {darkMode ? 'Karanlık tema aktif' : 'Açık tema aktif'}
            </Typography>
          </Box>
          <FormControl fullWidth margin="normal">
            <InputLabel>Dil</InputLabel>
            <Select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              label="Dil"
            >
              <MenuItem value="tr">Türkçe</MenuItem>
              <MenuItem value="en">English</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </CardContent>
    </Card>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'profile':
        return renderProfileTab();
      case 'notifications':
        return renderNotificationsTab();
      case 'email':
        return renderEmailTab();
      case 'security':
        return renderSecurityTab();
      case 'appearance':
        return renderAppearanceTab();
      default:
        return renderProfileTab();
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 600, mb: 1 }}>
          Ayarlar
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Hesap ayarlarınızı ve tercihlerinizi yönetin
        </Typography>
      </Box>

      {message && (
        <Alert severity={message.type} sx={{ mb: 3 }}>
          {message.text}
        </Alert>
      )}

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 3fr' }, gap: 3 }}>
        {/* Sidebar */}
        <Paper sx={{ p: 2 }}>
          <List>
            {tabs.map((tab) => (
              <ListItem
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                sx={{
                  borderRadius: 2,
                  mb: 1,
                  cursor: 'pointer',
                  backgroundColor: activeTab === tab.id ? 'primary.main' : 'transparent',
                  color: activeTab === tab.id ? 'white' : 'inherit',
                  '&:hover': {
                    backgroundColor: activeTab === tab.id ? 'primary.dark' : 'action.hover',
                  },
                }}
              >
                <ListItemIcon sx={{ color: 'inherit' }}>
                  {tab.icon}
                </ListItemIcon>
                <ListItemText primary={tab.label} />
              </ListItem>
            ))}
          </List>
        </Paper>

        {/* Main Content */}
        <Box>
          {renderTabContent()}
        </Box>
      </Box>
    </Container>
  );
};

export default Settings;
