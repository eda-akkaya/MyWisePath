import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import {
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  IconButton,
  Chip,
  Dialog,
  List,
  ListItem,
  CircularProgress,
  Fab,
} from '@mui/material';
import {
  Send,
  Close,
  Search,
  TrendingUp,
  School,
  Web,
} from '@mui/icons-material';
import { chatbotService, SerpContentResult } from '../services/chatbotService';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  hasRoadmap?: boolean;
  roadmapData?: any;
  hasContentRecommendations?: boolean;
  contentRecommendations?: any[];
  hasSerpResults?: boolean;
  serpResults?: SerpContentResult[];
  extractedConcepts?: string[];
}

interface ContentRecommendation {
  title: string;
  platform: string;
  url: string;
  type: string;
  duration: string;
  free: boolean;
  description: string;
}



const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showEducationSearch, setShowEducationSearch] = useState(false);
  const [educationSearchQuery, setEducationSearchQuery] = useState('');
  const [showSerpSearch, setShowSerpSearch] = useState(false);
  const [serpSearchQuery, setSerpSearchQuery] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Auth context'ten kullanıcı bilgilerini al
  const { user } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      loadWelcomeMessage();
    }
  }, [isOpen, messages.length]);

  const loadWelcomeMessage = async () => {
    try {
      const response = await chatbotService.getWelcomeMessage();
      const welcomeMessage: Message = {
        id: 'welcome',
        text: response.message,
        isUser: false,
        timestamp: new Date(response.timestamp),
      };
      setMessages([welcomeMessage]);
    } catch (error) {
      console.error('Welcome message error:', error);
      const fallbackMessage: Message = {
        id: 'welcome-fallback',
        text: 'Merhaba öğrenme tutkusu hiç bitmeyen insan ! Ne öğrenmek istersin?',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages([fallbackMessage]);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Roadmap bilgileri artık backend'de otomatik olarak kullanılıyor
      // Kullanıcının roadmap oluşturup oluşturmadığını kontrol et
      if (!user) {
        console.log('User not authenticated');
      }
      
      const response = await chatbotService.sendMessage(inputMessage);
      
      // Mesajda yol haritası veya içerik önerileri var mı kontrol et
      const hasRoadmap = response.message.includes('yol haritası') || response.message.includes('roadmap');
      const hasContentRecommendations = response.message.includes('Önerilen eğitim kaynakları') || response.message.includes('Güncel Eğitim Kaynakları');
      const hasSerpResults = response.message.includes('Güncel Eğitim Kaynakları') || response.message.includes('İlgili Eğitim Kaynakları');
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.message,
        isUser: false,
        timestamp: new Date(response.timestamp),
        hasRoadmap,
        hasContentRecommendations,
        hasSerpResults,
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Üzgünüm, şu anda cevap veremiyorum. Lütfen daha sonra tekrar deneyin.',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateRoadmap = async (userMessage: string) => {
    try {
      setIsLoading(true);
      const response = await chatbotService.generateRoadmap(userMessage);
      
      const roadmapMessage: Message = {
        id: (Date.now() + 2).toString(),
        text: response.message,
        isUser: false,
        timestamp: new Date(response.timestamp),
        hasRoadmap: true,
        roadmapData: response.roadmap,
      };
      
      setMessages(prev => [...prev, roadmapMessage]);
    } catch (error) {
      console.error('Roadmap generation error:', error);
      let errorText = 'Yol haritası oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.';
      
      // Hata mesajını daha spesifik hale getir
      if (error instanceof Error) {
        if (error.message.includes('401')) {
          errorText = 'Oturum süreniz dolmuş. Lütfen tekrar giriş yapın.';
        } else if (error.message.includes('400')) {
          errorText = 'Öğrenme isteği tespit edilemedi. Lütfen daha spesifik bir mesaj yazın.';
        } else if (error.message.includes('500')) {
          errorText = 'Sunucu hatası. Lütfen daha sonra tekrar deneyin.';
        }
      }
      
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        text: errorText,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEducationSearch = async () => {
    if (!educationSearchQuery.trim()) return;
    
    try {
      setIsLoading(true);
      const response = await chatbotService.searchEducationContent({
        query: educationSearchQuery,
        skill_level: 'beginner',
        limit: 5
      });
      

      
      const searchMessage: Message = {
        id: Date.now().toString(),
        text: `"${educationSearchQuery}" için ${response.total_count} eğitim kaynağı buldum:`,
        isUser: false,
        timestamp: new Date(response.timestamp),
        hasContentRecommendations: true,
        contentRecommendations: response.results,
      };
      
      setMessages(prev => [...prev, searchMessage]);
      setShowEducationSearch(false);
      setEducationSearchQuery('');
    } catch (error) {
      console.error('Education search error:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Eğitim araması yapılırken bir hata oluştu. Lütfen tekrar deneyin.',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSerpSearch = async () => {
    if (!serpSearchQuery.trim()) return;
    
    try {
      setIsLoading(true);
      const response = await chatbotService.searchWithSerp(serpSearchQuery);
      

      
      const searchMessage: Message = {
        id: Date.now().toString(),
        text: `"${serpSearchQuery}" için ${response.total_count} güncel eğitim kaynağı buldum:`,
        isUser: false,
        timestamp: new Date(response.timestamp),
        hasSerpResults: true,
        serpResults: response.results,
        extractedConcepts: response.extracted_concepts,
      };
      
      setMessages(prev => [...prev, searchMessage]);
      setShowSerpSearch(false);
      setSerpSearchQuery('');
    } catch (error) {
      console.error('Serp search error:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Web araması yapılırken bir hata oluştu. Lütfen tekrar deneyin.',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetTrendingTopics = async () => {
    try {
      setIsLoading(true);
      const response = await chatbotService.getTrendingEducationalTopics();
      

      
      const trendingMessage: Message = {
        id: Date.now().toString(),
        text: `Şu anda trend olan ${response.total_count} eğitim konusu:`,
        isUser: false,
        timestamp: new Date(response.timestamp),
        hasSerpResults: true,
        serpResults: response.trending_topics,
      };
      
      setMessages(prev => [...prev, trendingMessage]);

    } catch (error) {
      console.error('Trending topics error:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Trend konular alınırken bir hata oluştu. Lütfen tekrar deneyin.',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetPopularEducation = async () => {
    try {
      setIsLoading(true);
      const response = await chatbotService.getPopularEducation(5);
      
      const popularMessage: Message = {
        id: Date.now().toString(),
        text: `Şu anda en popüler ${response.total_count} eğitim kaynağı:`,
        isUser: false,
        timestamp: new Date(response.timestamp),
        hasContentRecommendations: true,
        contentRecommendations: response.popular_content,
      };
      
      setMessages(prev => [...prev, popularMessage]);
    } catch (error) {
      console.error('Popular education error:', error);
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: 'Popüler eğitimler alınırken bir hata oluştu. Lütfen tekrar deneyin.',
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const renderSerpResults = (message: Message) => {
    if (!message.hasSerpResults || !message.serpResults) return null;

    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="subtitle2" color="primary" sx={{ mb: 1 }}>
          <Web sx={{ mr: 0.5, fontSize: 16 }} />
          Güncel Eğitim Kaynakları
        </Typography>
        {message.extractedConcepts && message.extractedConcepts.length > 0 && (
          <Box sx={{ mb: 1 }}>
            <Typography variant="caption" color="text.secondary">
              Çıkarılan kavramlar: {message.extractedConcepts.join(', ')}
            </Typography>
          </Box>
        )}
        {message.serpResults.map((result, index) => (
          <Paper key={index} sx={{ mb: 1, bgcolor: 'primary.50', border: '1px solid', borderColor: 'primary.200' }}>
            <Box sx={{ py: 1, px: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="body2" fontWeight="medium">
                    {result.title}
                  </Typography>
                  <Typography variant="caption" color="text.secondary" display="block">
                    {result.platform} • {result.type} • {result.skill_level}
                  </Typography>
                  <Typography variant="caption" color="text.secondary" display="block">
                    {result.snippet}
                  </Typography>
                </Box>
                <IconButton size="small" color="primary">
                  <Web fontSize="small" />
                </IconButton>
              </Box>
            </Box>
          </Paper>
        ))}
      </Box>
    );
  };

  const renderContentRecommendations = (message: Message) => {
    if (!message.hasContentRecommendations) return null;

    // Mesaj metninden önerileri çıkar
    const lines = message.text.split('\n');
    const recommendations: ContentRecommendation[] = [];
    
    for (const line of lines) {
      if (line.match(/^\d+\./)) {
        const match = line.match(/^\d+\. (.+?) \((.+?)\) - (.+)$/);
        if (match) {
          recommendations.push({
            title: match[1],
            platform: match[2],
            url: match[3],
            type: 'course',
            duration: 'Varies',
            free: true,
            description: `${match[1]} - ${match[2]} platformunda`
          });
        }
      }
    }

    return (
      <Box sx={{ mt: 2 }}>
        <Typography variant="subtitle2" color="primary" sx={{ mb: 1 }}>
          <School sx={{ mr: 0.5, fontSize: 16 }} />
          Önerilen Eğitim Kaynakları
        </Typography>
        {recommendations.map((rec, index) => (
          <Paper key={index} sx={{ mb: 1, bgcolor: 'grey.50' }}>
            <Box sx={{ py: 1, px: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="body2" fontWeight="medium">
                    {rec.title}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {rec.platform} • {rec.duration}
                  </Typography>
                </Box>
                <IconButton size="small" color="primary">
                  <Web fontSize="small" />
                </IconButton>
              </Box>
            </Box>
          </Paper>
        ))}
      </Box>
    );
  };

  const renderRoadmapSuggestion = (message: Message) => {
    if (!message.hasRoadmap) return null;

    return (
      <Box sx={{ mt: 2 }}>
        <Button
          variant="contained"
          size="small"
          startIcon={<Web />}
          onClick={() => handleGenerateRoadmap(message.text)}
          sx={{ mb: 1 }}
        >
          Yol Haritası Oluştur
        </Button>
        <Typography variant="caption" color="text.secondary" display="block">
          Bu butona tıklayarak detaylı bir yol haritası oluşturabilirsiniz.
        </Typography>
      </Box>
    );
  };

  const renderRoadmapData = (message: Message) => {
    if (!message.roadmapData) return null;

    const roadmap = message.roadmapData;
    
    return (
      <Box sx={{ mt: 2 }}>
        <Paper sx={{ bgcolor: 'primary.50', border: '1px solid', borderColor: 'primary.200' }}>
          <Box sx={{ p: 2 }}>
            <Typography variant="h6" color="primary" gutterBottom>
              <Web sx={{ mr: 1, verticalAlign: 'middle' }} />
              {roadmap.title}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              {roadmap.description}
            </Typography>
            
            <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
              <Chip 
                label={`${roadmap.modules.length} Modül`} 
                size="small" 
                color="primary" 
                variant="outlined" 
              />
              <Chip 
                label={`${roadmap.total_estimated_hours} Saat`} 
                size="small" 
                color="secondary" 
                variant="outlined" 
              />
              <Chip 
                label={`%${roadmap.overall_progress} Tamamlandı`} 
                size="small" 
                color="success" 
                variant="outlined" 
              />
            </Box>

            <Typography variant="subtitle2" gutterBottom>
              Modüller:
            </Typography>
            {roadmap.modules.slice(0, 3).map((module: any, index: number) => (
              <Box key={module.id} sx={{ mb: 1, pl: 1 }}>
                <Typography variant="body2" fontWeight="medium">
                  {index + 1}. {module.title}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {module.estimated_hours} saat • {module.difficulty}
                </Typography>
              </Box>
            ))}
            
            {roadmap.modules.length > 3 && (
              <Typography variant="caption" color="text.secondary">
                ... ve {roadmap.modules.length - 3} modül daha
              </Typography>
            )}
          </Box>
        </Paper>
      </Box>
    );
  };

  const renderEducationSearch = () => {
    if (!showEducationSearch) return null;

    return (
      <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 2 }}>
        <Typography variant="subtitle2" color="primary" sx={{ mb: 1 }}>
          <Search sx={{ mr: 0.5, fontSize: 16 }} />
          Eğitim Ara
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            size="small"
            placeholder="Aramak istediğiniz konuyu yazın..."
            value={educationSearchQuery}
            onChange={(e) => setEducationSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleEducationSearch()}
            disabled={isLoading}
          />
          <IconButton
            color="primary"
            onClick={handleEducationSearch}
            disabled={!educationSearchQuery.trim() || isLoading}
          >
            <Search />
          </IconButton>
        </Box>
      </Box>
    );
  };

  const renderSerpSearch = () => {
    if (!showSerpSearch) return null;

    return (
      <Box sx={{ mt: 2, p: 2, bgcolor: 'primary.50', borderRadius: 2 }}>
        <Typography variant="subtitle2" color="primary" sx={{ mb: 1 }}>
          <Web sx={{ mr: 0.5, fontSize: 16 }} />
          Web'de Eğitim Ara
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            fullWidth
            size="small"
            placeholder="Web'de aramak istediğiniz konuyu yazın..."
            value={serpSearchQuery}
            onChange={(e) => setSerpSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSerpSearch()}
            disabled={isLoading}
          />
          <IconButton
            color="primary"
            onClick={handleSerpSearch}
            disabled={!serpSearchQuery.trim() || isLoading}
          >
            <Search />
          </IconButton>
        </Box>
      </Box>
    );
  };

  const renderQuickActions = () => {
    return (
      <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Button
          variant="outlined"
          size="small"
          startIcon={<Search />}
          onClick={() => setShowEducationSearch(!showEducationSearch)}
        >
          Eğitim Ara
        </Button>
        <Button
          variant="outlined"
          size="small"
          startIcon={<Web />}
          onClick={() => setShowSerpSearch(!showSerpSearch)}
        >
          Web'de Ara
        </Button>
        <Button
          variant="outlined"
          size="small"
          startIcon={<TrendingUp />}
          onClick={handleGetTrendingTopics}
          disabled={isLoading}
        >
          Trend Konular
        </Button>
        <Button
          variant="outlined"
          size="small"
          startIcon={<School />}
          onClick={handleGetPopularEducation}
          disabled={isLoading}
        >
          Popüler Eğitimler
        </Button>
      </Box>
    );
  };

  return (
    <>
      {/* Floating Chat Button */}
      <Fab
        color="primary"
        aria-label="chat"
        onClick={() => setIsOpen(!isOpen)}
        sx={{
          position: 'fixed',
          bottom: 16,
          right: 16,
          zIndex: 1000,
        }}
      >
        {isOpen ? <Close /> : <Web />}
      </Fab>

      {/* Chat Window */}
      <Dialog
        open={isOpen}
        onClose={() => setIsOpen(false)}
        PaperProps={{
          sx: {
            position: 'fixed',
            bottom: 80,
            right: 16,
            width: 400,
            height: 600,
            zIndex: 999,
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
          },
        }}
      >
        {/* Header */}
        <Box
          sx={{
            bgcolor: 'primary.main',
            color: 'white',
            p: 2,
            display: 'flex',
            alignItems: 'center',
            gap: 1,
          }}
        >
          <Web />
                      <Typography variant="h6">Bilge Rehber ✨</Typography>
        </Box>

        {/* Messages */}
        <Box
          sx={{
            flex: 1,
            overflow: 'auto',
            p: 2,
            bgcolor: 'grey.50',
          }}
        >
          <List sx={{ p: 0 }}>
            {messages.map((message) => (
              <ListItem
                key={message.id}
                sx={{
                  flexDirection: 'column',
                  alignItems: message.isUser ? 'flex-end' : 'flex-start',
                  p: 0,
                  mb: 1,
                }}
              >
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: 1,
                    maxWidth: '90%',
                  }}
                >
                  {!message.isUser && (
                    <Chip
                      sx={{
                        width: 32,
                        height: 32,
                        bgcolor: 'primary.main',
                      }}
                      icon={<Web fontSize="small" />}
                    />
                  )}
                  <Paper
                    sx={{
                      p: 1.5,
                      bgcolor: message.isUser ? 'primary.main' : 'white',
                      color: message.isUser ? 'white' : 'text.primary',
                      borderRadius: 2,
                      boxShadow: 1,
                      maxWidth: '100%',
                    }}
                  >
                    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                      {message.text}
                    </Typography>
                    
                    {/* Serp Results */}
                    {renderSerpResults(message)}
                    
                    {/* Content Recommendations */}
                    {renderContentRecommendations(message)}
                    
                    {/* Roadmap Suggestion */}
                    {renderRoadmapSuggestion(message)}
                    
                    {/* Roadmap Data */}
                    {renderRoadmapData(message)}
                  </Paper>
                  {message.isUser && (
                    <Chip
                      sx={{
                        width: 32,
                        height: 32,
                        bgcolor: 'secondary.main',
                      }}
                      icon={<Typography variant="caption">U</Typography>}
                    />
                  )}
                </Box>
              </ListItem>
            ))}
            {isLoading && (
              <ListItem sx={{ justifyContent: 'flex-start', p: 0, mb: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Chip
                    sx={{
                      width: 32,
                      height: 32,
                      bgcolor: 'primary.main',
                    }}
                    icon={<Web fontSize="small" />}
                  />
                  <CircularProgress size={20} />
                </Box>
              </ListItem>
            )}
          </List>
          <div ref={messagesEndRef} />
        </Box>

        {/* Input */}
        <Box sx={{ p: 2, bgcolor: 'white' }}>
          {/* Quick Actions */}
          {renderQuickActions()}
          
          {/* Education Search */}
          {renderEducationSearch()}
          
          {/* Serp Search */}
          {renderSerpSearch()}
          
          <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Mesajınızı yazın..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 3,
                },
              }}
            />
            <IconButton
              color="primary"
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              sx={{ bgcolor: 'primary.main', color: 'white', '&:hover': { bgcolor: 'primary.dark' } }}
            >
              <Send />
            </IconButton>
          </Box>
        </Box>
      </Dialog>
    </>
  );
};

export default Chatbot; 