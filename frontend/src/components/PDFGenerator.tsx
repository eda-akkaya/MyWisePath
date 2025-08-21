import React, { useState } from 'react';
import { pdfService } from '../services/pdfService';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
} from '@mui/material';
import {
  PictureAsPdf,
  Download,
  Description,
  Assessment,
  School,
  CheckCircle,
  Schedule,
  TrendingUp,
  Star,
  Close,
  FileDownload,
} from '@mui/icons-material';

interface PDFGeneratorProps {
  roadmapData?: any;
  progressData?: any;
  summaryData?: any;
  onClose?: () => void;
}

interface PDFGenerationRequest {
  type: 'roadmap' | 'progress' | 'summary';
  data: any;
  userInfo?: {
    name: string;
    email: string;
  };
}

const PDFGenerator: React.FC<PDFGeneratorProps> = ({
  roadmapData,
  progressData,
  summaryData,
  onClose
}) => {
  const getInitialType = () => {
    if (roadmapData) return 'roadmap';
    if (progressData) return 'progress';
    if (summaryData) return 'summary';
    return 'roadmap';
  };

  const [selectedType, setSelectedType] = useState<'roadmap' | 'progress' | 'summary'>(getInitialType());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showDialog, setShowDialog] = useState(false);
  const [customData, setCustomData] = useState<any>({});

  const handleGeneratePDF = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      let result;

      switch (selectedType) {
        case 'roadmap':
          if (!roadmapData) {
            throw new Error('Roadmap verisi bulunamadı');
          }
          result = await pdfService.generateRoadmapPDF(roadmapData);
          break;

        case 'progress':
          if (!progressData) {
            throw new Error('İlerleme verisi bulunamadı');
          }
          result = await pdfService.generateProgressPDF(progressData);
          break;

        case 'summary':
          if (!summaryData) {
            throw new Error('Özet verisi bulunamadı');
          }
          result = await pdfService.generateSummaryPDF(summaryData);
          break;

        default:
          throw new Error('Geçersiz PDF türü');
      }

      if (result.success) {
        setSuccess(result.message);
        setShowDialog(false);
      } else {
        setError(result.error || 'PDF oluşturulurken bir hata oluştu');
      }

    } catch (err: any) {
      console.error('PDF oluşturma hatası:', err);
      setError(err.message || 'PDF oluşturulurken bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const getAvailableTypes = () => {
    const types = [];
    if (roadmapData) types.push('roadmap');
    if (progressData) types.push('progress');
    if (summaryData) types.push('summary');
    return types;
  };

  const getTypeDescription = (type: string) => {
    switch (type) {
      case 'roadmap':
        return 'Seçilen roadmap\'in detaylı PDF versiyonu';
      case 'progress':
        return 'Kullanıcının öğrenme ilerlemesi raporu';
      case 'summary':
        return 'Öğrenme geçmişi ve başarılar özeti';
      default:
        return '';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'roadmap':
        return <Description />;
      case 'progress':
        return <Assessment />;
      case 'summary':
        return <School />;
      default:
        return <PictureAsPdf />;
    }
  };

  const availableTypes = getAvailableTypes();

  if (availableTypes.length === 0) {
    return (
      <Alert severity="info" sx={{ borderRadius: 2 }}>
        <Typography variant="body2">
          PDF oluşturmak için gerekli veriler bulunamadı. Lütfen önce bir roadmap oluşturun veya ilerleme verilerinizi yükleyin.
        </Typography>
      </Alert>
    );
  }

  return (
    <>
      <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
        <CardContent sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <PictureAsPdf sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              PDF Oluşturucu
            </Typography>
          </Box>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Öğrenme materyallerinizi PDF formatında indirin ve offline çalışın.
          </Typography>

          <FormControl fullWidth sx={{ mb: 3 }}>
            <InputLabel>PDF Türü</InputLabel>
            <Select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value as any)}
              label="PDF Türü"
            >
              {availableTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {getTypeIcon(type)}
                    <Box sx={{ ml: 1 }}>
                      <Typography variant="body2">
                        {type === 'roadmap' ? 'Roadmap PDF' : 
                         type === 'progress' ? 'İlerleme Raporu' : 'Öğrenme Özeti'}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {getTypeDescription(type)}
                      </Typography>
                    </Box>
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Seçilen türe göre önizleme */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
              İçerik Önizlemesi:
            </Typography>
            <Card variant="outlined" sx={{ p: 2, backgroundColor: 'grey.50' }}>
              {selectedType === 'roadmap' && roadmapData && (
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    📋 {roadmapData.title || 'Roadmap'}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {roadmapData.description || 'Roadmap açıklaması'}
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    <Chip 
                      label={`${roadmapData.modules?.length || 0} Modül`} 
                      size="small" 
                      color="primary" 
                      variant="outlined"
                    />
                  </Box>
                </Box>
              )}

              {selectedType === 'progress' && progressData && (
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    📊 İlerleme Raporu
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Toplam ilerleme: %{progressData.overall_progress || 0}
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    <Chip 
                      label={`${progressData.completed_modules || 0} Tamamlanan`} 
                      size="small" 
                      color="success" 
                      variant="outlined"
                    />
                  </Box>
                </Box>
              )}

              {selectedType === 'summary' && summaryData && (
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    🎓 Öğrenme Özeti
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {summaryData.learned_topics?.length || 0} konu öğrenildi
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    <Chip 
                      label={`${summaryData.achievements?.length || 0} Başarı`} 
                      size="small" 
                      color="warning" 
                      variant="outlined"
                    />
                  </Box>
                </Box>
              )}
            </Card>
          </Box>

          <Button
            variant="contained"
            fullWidth
            onClick={() => setShowDialog(true)}
            startIcon={<PictureAsPdf />}
            size="large"
            sx={{
              borderRadius: 2,
              py: 1.5,
              '&:hover': {
                transform: 'translateY(-2px)',
                boxShadow: 4,
              },
            }}
          >
            PDF Oluştur ve İndir
          </Button>

          {error && (
            <Alert severity="error" sx={{ mt: 2, borderRadius: 2 }}>
              <Typography variant="body2">
                ❌ {error}
              </Typography>
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mt: 2, borderRadius: 2 }}>
              <Typography variant="body2">
                ✅ {success}
              </Typography>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* PDF Oluşturma Dialog'u */}
      <Dialog 
        open={showDialog} 
        onClose={() => setShowDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <PictureAsPdf sx={{ mr: 1, color: 'primary.main' }} />
            PDF Oluşturuluyor
          </Box>
          <IconButton onClick={() => setShowDialog(false)}>
            <Close />
          </IconButton>
        </DialogTitle>
        
        <DialogContent>
          {loading ? (
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 4 }}>
              <CircularProgress size={60} sx={{ mb: 2 }} />
              <Typography variant="h6" sx={{ mb: 1 }}>
                PDF Oluşturuluyor...
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Lütfen bekleyin, bu işlem birkaç saniye sürebilir.
              </Typography>
            </Box>
          ) : (
            <Box>
              <Typography variant="body1" sx={{ mb: 2 }}>
                <strong>{selectedType === 'roadmap' ? 'Roadmap' : 
                         selectedType === 'progress' ? 'İlerleme Raporu' : 'Öğrenme Özeti'}</strong> PDF'i oluşturulacak.
              </Typography>
              
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Profesyonel tasarım" 
                    secondary="Özel stiller ve renkli başlıklar"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Detaylı içerik" 
                    secondary="Tüm modüller ve kaynaklar dahil"
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircle color="success" />
                  </ListItemIcon>
                  <ListItemText 
                    primary="Otomatik indirme" 
                    secondary="PDF oluşturulduktan sonra otomatik indirilir"
                  />
                </ListItem>
              </List>
            </Box>
          )}
        </DialogContent>
        
        <DialogActions sx={{ p: 3 }}>
          <Button 
            onClick={() => setShowDialog(false)}
            disabled={loading}
          >
            İptal
          </Button>
          <Button
            variant="contained"
            onClick={handleGeneratePDF}
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} /> : <FileDownload />}
          >
            {loading ? 'Oluşturuluyor...' : 'PDF Oluştur'}
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default PDFGenerator;
