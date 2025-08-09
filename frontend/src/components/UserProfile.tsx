import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
  Box,
  Chip,
  IconButton,
  Alert,
  Paper,
  Switch,
  FormControlLabel,
  Divider
} from '@mui/material';
import { Close, Add, Delete, Email, Notifications, Assessment } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { authService, UserProfileUpdate, EmailSettings } from '../services/authService';

interface UserProfileProps {
  open: boolean;
  onClose: () => void;
}

const UserProfile: React.FC<UserProfileProps> = ({ open, onClose }) => {
  const { user, updateUser } = useAuth();
  const [skillLevel, setSkillLevel] = useState(user?.skill_level || 'beginner');
  const [interests, setInterests] = useState<string[]>(user?.interests || []);
  const [learningGoals, setLearningGoals] = useState<string[]>(user?.learning_goals || []);
  const [newInterest, setNewInterest] = useState('');
  const [newGoal, setNewGoal] = useState('');
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [emailAddress, setEmailAddress] = useState(user?.email || 'edaa52116@gmail.com');
  
  // Email settings state
  const [emailSettings, setEmailSettings] = useState<EmailSettings>({
    email_frequency: 'weekly',
    weekly_reminders_enabled: true,
    progress_reports_enabled: true,
    instant_email_enabled: true
  });
  const [isEmailLoading, setIsEmailLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setSkillLevel(user.skill_level || 'beginner');
      setInterests(user.interests || []);
      setLearningGoals(user.learning_goals || []);
    }
    
    // Load email settings
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

  const handleAddInterest = () => {
    if (newInterest.trim() && !interests.includes(newInterest.trim())) {
      setInterests([...interests, newInterest.trim()]);
      setNewInterest('');
    }
  };

  const handleRemoveInterest = (interest: string) => {
    setInterests(interests.filter(i => i !== interest));
  };

  const handleAddGoal = () => {
    if (newGoal.trim() && !learningGoals.includes(newGoal.trim())) {
      setLearningGoals([...learningGoals, newGoal.trim()]);
      setNewGoal('');
    }
  };

  const handleRemoveGoal = (goal: string) => {
    setLearningGoals(learningGoals.filter(g => g !== goal));
  };

  const handleSave = async () => {
    setIsLoading(true);
    setMessage(null);

    try {
      const profileUpdate: UserProfileUpdate = {
        skill_level: skillLevel,
        interests,
        learning_goals: learningGoals
      };

      // API'ye profil güncelleme isteği gönder
      const updatedProfile = await authService.updateUserProfile(profileUpdate);
      
      // Auth context'i güncelle
      if (updateUser) {
        updateUser(updatedProfile);
      }

      // Başarı mesajı göster
      setMessage({
        type: 'success',
        text: 'Profil bilgileriniz başarıyla güncellendi! Bilge Rehber ✨ artık size daha kişiselleştirilmiş cevaplar verecek.'
      });

      // 3 saniye sonra mesajı kaldır
      setTimeout(() => {
        setMessage(null);
        onClose();
      }, 3000);

    } catch (error) {
      console.error('Profile update error:', error);
      setMessage({
        type: 'error',
        text: 'Profil güncellenirken bir hata oluştu. Lütfen tekrar deneyin.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleEmailSettingsSave = async () => {
    setIsEmailLoading(true);
    setMessage(null);

    try {
      await authService.updateEmailSettings(emailSettings);
      
      setMessage({
        type: 'success',
        text: 'E-posta ayarlarınız başarıyla güncellendi!'
      });

      setTimeout(() => {
        setMessage(null);
      }, 3000);

    } catch (error) {
      console.error('Email settings update error:', error);
      setMessage({
        type: 'error',
        text: 'E-posta ayarları güncellenirken bir hata oluştu. Lütfen tekrar deneyin.'
      });
    } finally {
      setIsEmailLoading(false);
    }
  };

  const handleSendInstantEmail = async (emailType: 'reminder' | 'progress') => {
    setIsEmailLoading(true);
    setMessage(null);

    // E-posta adresi kontrolü
    if (!emailAddress || !emailAddress.includes('@')) {
      setMessage({
        type: 'error',
        text: 'Lütfen geçerli bir e-posta adresi girin.'
      });
      setIsEmailLoading(false);
      return;
    }

    try {
      await authService.sendInstantEmail({ 
        email_type: emailType,
        target_email: emailAddress,
        custom_message: `${emailType === 'reminder' ? 'Hatırlatıcı' : 'İlerleme raporu'} e-postası ${emailAddress} adresine gönderiliyor.`
      });
      
      setMessage({
        type: 'success',
        text: `✅ ${emailType === 'reminder' ? 'Hatırlatıcı' : 'İlerleme raporu'} e-postası ${emailAddress} adresine başarıyla gönderildi!`
      });

      setTimeout(() => {
        setMessage(null);
      }, 3000);

    } catch (error) {
      console.error('Instant email error:', error);
      setMessage({
        type: 'error',
        text: 'E-posta gönderilirken bir hata oluştu. Lütfen tekrar deneyin.'
      });
    } finally {
      setIsEmailLoading(false);
    }
  };

  const handleClose = () => {
    // Değişiklikleri geri al
    if (user) {
      setSkillLevel(user.skill_level || 'beginner');
      setInterests(user.interests || []);
      setLearningGoals(user.learning_goals || []);
    }
    setMessage(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">Profil Ayarları</Typography>
          <IconButton onClick={handleClose}>
            <Close />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent>
        {message && (
          <Alert severity={message.type} sx={{ mb: 2 }}>
            {message.text}
          </Alert>
        )}

                 <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
           {/* E-posta Adresi */}
           <Box>
             <Typography variant="h6" gutterBottom>
               E-posta Adresiniz
             </Typography>
             <TextField
               fullWidth
               label="E-posta Adresi"
               value={emailAddress}
               onChange={(e) => setEmailAddress(e.target.value)}
               type="email"
               placeholder="ornek@email.com"
               helperText="E-postalar bu adrese gönderilecek"
             />
             <Box sx={{ mt: 1 }}>
               <Typography variant="caption" color="textSecondary">
                 📧 Mevcut e-posta: {user?.email || 'Belirtilmemiş'}
               </Typography>
             </Box>
           </Box>

           {/* Seviye Seçimi */}
           <Box>
             <FormControl fullWidth>
               <InputLabel>Bilgi Seviyeniz</InputLabel>
               <Select
                 value={skillLevel}
                 onChange={(e) => setSkillLevel(e.target.value)}
                 label="Bilgi Seviyeniz"
               >
                 <MenuItem value="beginner">Başlangıç</MenuItem>
                 <MenuItem value="intermediate">Orta Seviye</MenuItem>
                 <MenuItem value="advanced">İleri Seviye</MenuItem>
               </Select>
             </FormControl>
             <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
               Bu bilgi Bilge Rehber ✨'in size uygun seviyede cevaplar vermesini sağlar.
             </Typography>
           </Box>

          {/* İlgi Alanları */}
          <Box>
            <Typography variant="h6" gutterBottom>
              İlgi Alanlarınız
            </Typography>
            <Box display="flex" gap={1} mb={2}>
              <TextField
                size="small"
                placeholder="Yeni ilgi alanı ekle"
                value={newInterest}
                onChange={(e) => setNewInterest(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddInterest()}
                sx={{ flexGrow: 1 }}
              />
              <Button
                variant="outlined"
                onClick={handleAddInterest}
                disabled={!newInterest.trim()}
                startIcon={<Add />}
              >
                Ekle
              </Button>
            </Box>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {interests.map((interest, index) => (
                <Chip
                  key={index}
                  label={interest}
                  onDelete={() => handleRemoveInterest(interest)}
                  deleteIcon={<Delete />}
                  color="primary"
                  variant="outlined"
                />
              ))}
            </Box>
            <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
              İlgi alanlarınız Bilge Rehber ✨'in size özel öneriler sunmasını sağlar.
            </Typography>
          </Box>

          {/* Öğrenme Hedefleri */}
          <Box>
            <Typography variant="h6" gutterBottom>
              Öğrenme Hedefleriniz
            </Typography>
            <Box display="flex" gap={1} mb={2}>
              <TextField
                size="small"
                placeholder="Yeni hedef ekle"
                value={newGoal}
                onChange={(e) => setNewGoal(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddGoal()}
                sx={{ flexGrow: 1 }}
              />
              <Button
                variant="outlined"
                onClick={handleAddGoal}
                disabled={!newGoal.trim()}
                startIcon={<Add />}
              >
                Ekle
              </Button>
            </Box>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {learningGoals.map((goal, index) => (
                <Chip
                  key={index}
                  label={goal}
                  onDelete={() => handleRemoveGoal(goal)}
                  deleteIcon={<Delete />}
                  color="secondary"
                  variant="outlined"
                />
              ))}
            </Box>
            <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
              Hedefleriniz Bilge Rehber ✨'in size uygun yol haritaları oluşturmasını sağlar.
            </Typography>
          </Box>

          <Divider />

          {/* E-posta Otomasyonu Ayarları */}
          <Box>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Email />
              E-posta Otomasyonu
            </Typography>
            
            <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
              <Typography variant="subtitle2" gutterBottom>
                E-posta Sıklığı
              </Typography>
              <FormControl fullWidth sx={{ mb: 2 }}>
                <Select
                  value={emailSettings.email_frequency}
                  onChange={(e) => setEmailSettings({
                    ...emailSettings,
                    email_frequency: e.target.value
                  })}
                >
                  <MenuItem value="never">E-posta almak istemiyorum</MenuItem>
                  <MenuItem value="daily">Günlük</MenuItem>
                  <MenuItem value="weekly">Haftalık</MenuItem>
                  <MenuItem value="monthly">Aylık</MenuItem>
                </Select>
              </FormControl>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
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
                  label="Haftalık hatırlatıcılar"
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
                  label="İlerleme raporları"
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
                  label="Anında e-posta gönderimi"
                />
              </Box>

              <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                <Button
                  variant="outlined"
                  onClick={handleEmailSettingsSave}
                  disabled={isEmailLoading}
                  startIcon={<Email />}
                >
                  {isEmailLoading ? 'Kaydediliyor...' : 'E-posta Ayarlarını Kaydet'}
                </Button>
              </Box>
            </Paper>

            {/* Anında E-posta Gönderme */}
            {emailSettings.instant_email_enabled && (
              <Paper sx={{ p: 2, mt: 2, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
                <Typography variant="subtitle2" gutterBottom>
                  Anında E-posta Gönder
                </Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  Hemen bir hatırlatıcı veya ilerleme raporu e-postası gönderin.
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="contained"
                    onClick={() => handleSendInstantEmail('reminder')}
                    disabled={isEmailLoading}
                    startIcon={<Notifications />}
                    size="small"
                    sx={{
                      bgcolor: 'success.main',
                      '&:hover': {
                        bgcolor: 'success.dark',
                      },
                    }}
                  >
                    {isEmailLoading ? 'Gönderiliyor...' : 'Hatırlatıcı Gönder'}
                  </Button>
                  <Button
                    variant="contained"
                    onClick={() => handleSendInstantEmail('progress')}
                    disabled={isEmailLoading}
                    startIcon={<Assessment />}
                    size="small"
                    sx={{
                      bgcolor: 'info.main',
                      '&:hover': {
                        bgcolor: 'info.dark',
                      },
                    }}
                  >
                    {isEmailLoading ? 'Gönderiliyor...' : 'İlerleme Raporu Gönder'}
                  </Button>
                </Box>
              </Paper>
            )}
          </Box>

          {/* Bilgi Kutusu */}
          <Box>
            <Paper sx={{ p: 2, bgcolor: 'info.light', color: 'info.contrastText' }}>
              <Typography variant="subtitle2" gutterBottom>
                💡 Kişiselleştirilmiş AI Deneyimi
              </Typography>
              <Typography variant="body2">
                Bu ayarlar Bilge Rehber ✨'in size özel cevaplar vermesini sağlar. 
                Seviyenize, ilgi alanlarınıza ve hedeflerinize göre kişiselleştirilmiş 
                öneriler ve yol haritaları alacaksınız.
              </Typography>
            </Paper>
          </Box>
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={handleClose} disabled={isLoading}>
          İptal
        </Button>
        <Button 
          onClick={handleSave} 
          variant="contained" 
          disabled={isLoading}
        >
          {isLoading ? 'Kaydediliyor...' : 'Kaydet'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default UserProfile; 