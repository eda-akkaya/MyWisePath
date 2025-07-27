import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  Link,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  School as SchoolIcon,
  PlayCircle as VideoIcon,
  Book as BookIcon,
  Computer as InteractiveIcon,
  Link as LinkIcon,
  Star as StarIcon,
  AccessTime as TimeIcon,
} from '@mui/icons-material';

export interface EducationalContentItem {
  title: string;
  platform: string;
  url: string;
  type: string;
  duration: string;
  free: boolean;
  description: string;
  difficulty?: string;
  rating?: number;
  language?: string;
  tags?: string[];
}

interface EducationalContentProps {
  title?: string;
  content: EducationalContentItem[];
  showFilters?: boolean;
  onContentClick?: (content: EducationalContentItem) => void;
}

const EducationalContent: React.FC<EducationalContentProps> = ({
  title = "Eğitim İçerikleri",
  content,
  showFilters = false,
  onContentClick,
}) => {
  const getContentIcon = (type: string) => {
    switch (type.toLowerCase()) {
      case 'video':
        return <VideoIcon fontSize="small" />;
      case 'course':
        return <SchoolIcon fontSize="small" />;
      case 'interactive':
        return <InteractiveIcon fontSize="small" />;
      case 'book':
        return <BookIcon fontSize="small" />;
      default:
        return <SchoolIcon fontSize="small" />;
    }
  };

  const getDifficultyColor = (difficulty?: string) => {
    switch (difficulty?.toLowerCase()) {
      case 'beginner':
        return 'success';
      case 'intermediate':
        return 'warning';
      case 'advanced':
        return 'error';
      default:
        return 'default';
    }
  };

  const getPlatformColor = (platform: string) => {
    const platformColors: { [key: string]: string } = {
      'coursera': '#0056D2',
      'udemy': '#A435F0',
      'edx': '#2A73CC',
      'freecodecamp': '#0A0A23',
      'youtube': '#FF0000',
      'khan academy': '#14BF96',
    };
    return platformColors[platform.toLowerCase()] || '#666';
  };

  const handleContentClick = (item: EducationalContentItem) => {
    if (onContentClick) {
      onContentClick(item);
    } else {
      window.open(item.url, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <Box>
      {title && (
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <SchoolIcon color="primary" />
          {title}
        </Typography>
      )}

      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(3, 1fr)' },
        gap: 2 
      }}>
        {content.map((item, index) => (
          <Card 
            key={index}
            sx={{ 
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              transition: 'transform 0.2s, box-shadow 0.2s',
              '&:hover': {
                transform: 'translateY(-2px)',
                boxShadow: 4,
              },
              cursor: 'pointer',
            }}
            onClick={() => handleContentClick(item)}
          >
            <CardContent sx={{ flexGrow: 1, p: 2 }}>
              {/* Header */}
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  {getContentIcon(item.type)}
                  <Typography variant="caption" color="text.secondary">
                    {item.type}
                  </Typography>
                </Box>
                <Chip
                  label={item.free ? 'Ücretsiz' : 'Ücretli'}
                  size="small"
                  color={item.free ? 'success' : 'default'}
                  variant="outlined"
                />
              </Box>

              {/* Title */}
              <Typography variant="subtitle1" fontWeight="medium" gutterBottom sx={{ mb: 1 }}>
                {item.title}
              </Typography>

              {/* Platform */}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                <Box
                  sx={{
                    width: 12,
                    height: 12,
                    borderRadius: '50%',
                    bgcolor: getPlatformColor(item.platform),
                  }}
                />
                <Typography variant="body2" color="text.secondary">
                  {item.platform}
                </Typography>
              </Box>

              {/* Description */}
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2, lineHeight: 1.4 }}>
                {item.description}
              </Typography>

              {/* Tags and Info */}
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 1 }}>
                {item.difficulty && (
                  <Chip
                    label={item.difficulty}
                    size="small"
                    color={getDifficultyColor(item.difficulty) as any}
                    variant="outlined"
                  />
                )}
                <Chip
                  icon={<TimeIcon />}
                  label={item.duration}
                  size="small"
                  variant="outlined"
                />
                {item.rating && (
                  <Chip
                    icon={<StarIcon />}
                    label={item.rating.toFixed(1)}
                    size="small"
                    variant="outlined"
                  />
                )}
              </Box>

              {/* Action Button */}
              <Button
                variant="outlined"
                size="small"
                fullWidth
                startIcon={<LinkIcon />}
                sx={{ mt: 'auto' }}
              >
                İçeriği Görüntüle
              </Button>
            </CardContent>
          </Card>
        ))}
      </Box>

      {content.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <SchoolIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            Henüz içerik bulunamadı
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Bu konu için henüz eğitim içeriği önerisi bulunmuyor.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default EducationalContent; 