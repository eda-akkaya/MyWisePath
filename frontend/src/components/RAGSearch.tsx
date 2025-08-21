import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  Chip,
  List,
  ListItem,
  ListItemText,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Tooltip,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Search,
  ExpandMore,
  Download,
  FilterList,
  Clear,
  Book,
  School,
  Description,
  TrendingUp,
} from '@mui/icons-material';

interface SearchResult {
  content: string;
  metadata: any;
  similarity_score: number;
  source: string;
  file_type: string;
  chunk_id: number;
}

interface RAGSearchProps {
  onResultSelect?: (result: SearchResult) => void;
}

const RAGSearch: React.FC<RAGSearchProps> = ({ onResultSelect }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    filterByType: '',
    filterBySource: '',
    maxResults: 5,
  });
  const [showFilters, setShowFilters] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError('Lütfen bir arama sorgusu girin');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        query: query,
        k: filters.maxResults.toString(),
      });

      if (filters.filterByType) {
        params.append('filter_by_type', filters.filterByType);
      }
      if (filters.filterBySource) {
        params.append('filter_by_source', filters.filterBySource);
      }

             const token = localStorage.getItem('token');
       const headers: Record<string, string> = {
         'Content-Type': 'application/json',
         'Accept': 'application/json',
       };
       
       if (token) {
         headers['Authorization'] = `Bearer ${token}`;
       }
       
       const response = await fetch(`http://localhost:8000/api/v1/rag/search?${params}`, {
         method: 'GET',
         headers,
         mode: 'cors',
       });

      if (!response.ok) {
        throw new Error('Arama yapılırken bir hata oluştu');
      }

      const data = await response.json();
      setResults(data.results || []);
         } catch (err: any) {
       console.error('RAG Search Error:', err);
       
       // HTML response kontrolü
       if (err.message && err.message.includes('<!DOCTYPE')) {
         setError('Backend bağlantısı kurulamadı. Lütfen backend\'in çalıştığından emin olun.');
       } else if (err.message && err.message.includes('Failed to fetch')) {
         setError('Ağ bağlantısı hatası. Lütfen internet bağlantınızı kontrol edin.');
       } else {
         setError(err.message || 'Arama yapılırken bir hata oluştu');
       }
     } finally {
       setLoading(false);
     }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  const clearSearch = () => {
    setQuery('');
    setResults([]);
    setError(null);
  };

  const getFileTypeIcon = (fileType: string) => {
    switch (fileType) {
      case 'pdf':
        return <Description color="error" />;
      case 'roadmap':
        return <TrendingUp color="primary" />;
      case 'blog':
        return <Book color="success" />;
      case 'text':
        return <School color="info" />;
      default:
        return <Description />;
    }
  };

  const getFileTypeColor = (fileType: string) => {
    switch (fileType) {
      case 'pdf':
        return 'error';
      case 'roadmap':
        return 'primary';
      case 'blog':
        return 'success';
      case 'text':
        return 'info';
      default:
        return 'default';
    }
  };

  const formatScore = (score: number) => {
    return Math.round(score * 100);
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 2 }}>
      {/* Arama Başlığı */}
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
        🔍 Akıllı Arama
      </Typography>

      {/* Arama Formu */}
      <Card sx={{ mb: 3, borderRadius: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 2 }}>
            <TextField
              fullWidth
              label="Ne aramak istiyorsunuz?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Örnek: Python programlama, web geliştirme, veri analizi..."
              variant="outlined"
              size="medium"
            />
            <Button
              variant="contained"
              onClick={handleSearch}
              disabled={loading || !query.trim()}
              startIcon={loading ? <CircularProgress size={20} /> : <Search />}
              sx={{ minWidth: 120 }}
            >
              {loading ? 'Aranıyor...' : 'Ara'}
            </Button>
            <Tooltip title="Filtreleri Göster/Gizle">
              <IconButton
                onClick={() => setShowFilters(!showFilters)}
                color={showFilters ? 'primary' : 'default'}
              >
                <FilterList />
              </IconButton>
            </Tooltip>
            <Tooltip title="Temizle">
              <span>
                <IconButton onClick={clearSearch} disabled={!query && results.length === 0}>
                  <Clear />
                </IconButton>
              </span>
            </Tooltip>
          </Box>

          {/* Filtreler */}
          {showFilters && (
            <Accordion expanded={showFilters} sx={{ mt: 2 }}>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
                  Arama Filtreleri
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 2 }}>
                  <FormControl fullWidth size="small">
                    <InputLabel>Dosya Türü</InputLabel>
                    <Select
                      value={filters.filterByType}
                      onChange={(e) => setFilters({ ...filters, filterByType: e.target.value })}
                      label="Dosya Türü"
                    >
                      <MenuItem value="">Tümü</MenuItem>
                      <MenuItem value="pdf">PDF</MenuItem>
                      <MenuItem value="roadmap">Roadmap</MenuItem>
                      <MenuItem value="blog">Blog</MenuItem>
                      <MenuItem value="text">Metin</MenuItem>
                    </Select>
                  </FormControl>

                  <FormControl fullWidth size="small">
                    <InputLabel>Kaynak</InputLabel>
                    <Select
                      value={filters.filterBySource}
                      onChange={(e) => setFilters({ ...filters, filterBySource: e.target.value })}
                      label="Kaynak"
                    >
                      <MenuItem value="">Tümü</MenuItem>
                      <MenuItem value="roadmap">Roadmap</MenuItem>
                      <MenuItem value="blog">Blog</MenuItem>
                      <MenuItem value="pdf">PDF</MenuItem>
                    </Select>
                  </FormControl>

                  <Box>
                    <Typography gutterBottom>Maksimum Sonuç: {filters.maxResults}</Typography>
                    <Slider
                      value={filters.maxResults}
                      onChange={(_, value) => setFilters({ ...filters, maxResults: value as number })}
                      min={1}
                      max={20}
                      marks
                      valueLabelDisplay="auto"
                    />
                  </Box>
                </Box>
              </AccordionDetails>
            </Accordion>
          )}
        </CardContent>
      </Card>

      {/* Hata Mesajı */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Sonuçlar */}
      {results.length > 0 && (
        <Box>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
            📋 Arama Sonuçları ({results.length})
          </Typography>

          <List sx={{ width: '100%' }}>
            {results.map((result, index) => (
              <Card key={index} sx={{ mb: 2, borderRadius: 2 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {getFileTypeIcon(result.file_type)}
                      <Typography variant="subtitle2" color="text.secondary">
                        {result.source}
                      </Typography>
                    </Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip
                        label={`%${formatScore(result.similarity_score)} Eşleşme`}
                        color={getFileTypeColor(result.file_type)}
                        size="small"
                        variant="outlined"
                      />
                      <Chip
                        label={result.file_type.toUpperCase()}
                        color={getFileTypeColor(result.file_type)}
                        size="small"
                      />
                    </Box>
                  </Box>

                  <Typography
                    variant="body2"
                    sx={{
                      mb: 2,
                      lineHeight: 1.6,
                      maxHeight: 120,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      display: '-webkit-box',
                      WebkitLineClamp: 4,
                      WebkitBoxOrient: 'vertical',
                    }}
                  >
                    {result.content}
                  </Typography>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="caption" color="text.secondary">
                      Chunk ID: {result.chunk_id}
                    </Typography>
                    <Button
                      size="small"
                      onClick={() => onResultSelect?.(result)}
                      variant="outlined"
                    >
                      Detayları Görüntüle
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </List>
        </Box>
      )}

      {/* Sonuç Yok */}
      {!loading && query && results.length === 0 && !error && (
        <Card sx={{ p: 4, textAlign: 'center', borderRadius: 3 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            🔍 Sonuç Bulunamadı
          </Typography>
          <Typography variant="body2" color="text.secondary">
            "{query}" için sonuç bulunamadı. Farklı anahtar kelimeler deneyebilir veya filtreleri değiştirebilirsiniz.
          </Typography>
        </Card>
      )}
    </Box>
  );
};

export default RAGSearch;
