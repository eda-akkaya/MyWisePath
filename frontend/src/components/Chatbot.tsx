import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
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
  hasComprehensiveLearning?: boolean;
  comprehensiveLearningData?: any;
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
  // Theme context'ten tema bilgilerini al
  const { darkMode } = useTheme();

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
      // Öğrenme isteği kontrolü
      const learningKeywords = [
        'öğren', 'öğrenmek', 'öğrenmek istiyorum', 'nasıl öğrenirim',
        'kurs', 'eğitim', 'ders', 'tutorial', 'rehber', 'yol haritası',
        'roadmap', 'başla', 'başlamak', 'geliştir', 'geliştirmek',
        'çalış', 'çalışmak', 'araştır', 'araştırmak'
      ];
      
      const isLearningRequest = learningKeywords.some(keyword => 
        inputMessage.toLowerCase().includes(keyword.toLowerCase())
      );
      
      // Eğer öğrenme isteği varsa, comprehensive learning'i tetikle
      if (isLearningRequest) {
        // Mesajdan konuyu çıkar
        const topic = extractTopicFromMessage(inputMessage);
        if (topic) {
          await handleComprehensiveLearning(topic);
          return;
        }
      }
      
      // Normal chatbot yanıtı - public endpoint kullan
      let response;
      try {
        // Önce authenticated endpoint'i dene
        if (user) {
          response = await chatbotService.sendMessage(inputMessage);
        } else {
          // Kullanıcı giriş yapmamışsa public endpoint kullan
          response = await chatbotService.sendMessagePublic(inputMessage);
        }
      } catch (authError) {
        console.log('Authenticated endpoint failed, trying public endpoint:', authError);
        // Authenticated endpoint başarısız olursa public endpoint'i dene
        response = await chatbotService.sendMessagePublic(inputMessage);
      }
      
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
      let errorText = 'Üzgünüm, şu anda cevap veremiyorum. Lütfen daha sonra tekrar deneyin.';
      
      if (error instanceof Error) {
        if (error.message.includes('timeout')) {
          errorText = 'Bağlantı zaman aşımı. Lütfen internet bağlantınızı kontrol edin.';
        } else if (error.message.includes('network')) {
          errorText = 'Ağ bağlantısı hatası. Backend servisi çalışıyor mu kontrol edin.';
        } else if (error.message.includes('CORS')) {
          errorText = 'CORS hatası. Backend CORS ayarlarını kontrol edin.';
        } else {
          errorText = `Hata: ${error.message}`;
        }
      }
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: errorText,
        isUser: false,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const extractTopicFromMessage = (message: string): string | null => {
    // Basit konu çıkarma algoritması
    const words = message.toLowerCase().split(' ');
    
    // Öğrenme anahtar kelimelerini çıkar
    const learningWords = ['öğren', 'öğrenmek', 'öğrenmek istiyorum', 'nasıl öğrenirim', 'kurs', 'eğitim', 'ders', 'tutorial', 'rehber', 'yol haritası', 'roadmap', 'başla', 'başlamak', 'geliştir', 'geliştirmek', 'çalış', 'çalışmak', 'araştır', 'araştırmak'];
    
    const filteredWords = words.filter(word => 
      !learningWords.some(learningWord => word.includes(learningWord))
    );
    
    // Kalan kelimeleri birleştir
    const topic = filteredWords.join(' ').trim();
    
    return topic.length > 0 ? topic : null;
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

  const handleComprehensiveLearning = async (topic: string) => {
    try {
      setIsLoading(true);
      const response = await chatbotService.getComprehensiveLearning(topic);
      
      const comprehensiveMessage: Message = {
        id: Date.now().toString(),
        text: `"${topic}" konusu için kapsamlı öğrenme içeriği ve yol haritası hazırladım:`,
        isUser: false,
        timestamp: new Date(response.timestamp),
        hasComprehensiveLearning: true,
        comprehensiveLearningData: response,
        hasSerpResults: true,
        serpResults: response.serp_results,
        hasRoadmap: true,
        roadmapData: response.roadmap,
        extractedConcepts: response.extracted_concepts,
      };
      
      setMessages(prev => [...prev, comprehensiveMessage]);
    } catch (error) {
      console.error('Comprehensive learning error:', error);
      let errorText = 'Kapsamlı öğrenme içeriği oluşturulurken bir hata oluştu. Lütfen tekrar deneyin.';
      
      if (error instanceof Error) {
        if (error.message.includes('401')) {
          errorText = 'Oturum süreniz dolmuş. Lütfen tekrar giriş yapın.';
        } else if (error.message.includes('500')) {
          errorText = 'Sunucu hatası. Lütfen daha sonra tekrar deneyin.';
        } else if (error.message.includes('timeout')) {
          errorText = 'İstek zaman aşımına uğradı. Lütfen tekrar deneyin.';
        } else if (error.message.includes('network')) {
          errorText = 'Ağ bağlantısı hatası. Backend servisi çalışıyor mu kontrol edin.';
        } else {
          errorText = error.message;
        }
      }
      
      // Fallback: Basit chatbot yanıtı dene
      try {
        const fallbackResponse = await chatbotService.sendMessagePublic(
          `${topic} konusu hakkında bilgi ver`
        );
        
        const fallbackMessage: Message = {
          id: Date.now().toString(),
          text: fallbackResponse.message,
          isUser: false,
          timestamp: new Date(fallbackResponse.timestamp),
        };
        
        setMessages(prev => [...prev, fallbackMessage]);
        return;
      } catch (fallbackError) {
        console.error('Fallback error:', fallbackError);
      }
      
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: errorText,
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
          <Paper 
            key={index} 
            sx={{ 
              mb: 1, 
              bgcolor: darkMode ? 'background.paper' : 'primary.50', 
              border: '1px solid', 
              borderColor: darkMode ? 'divider' : 'primary.200' 
            }}
          >
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
          <Paper 
            key={index} 
            sx={{ 
              mb: 1, 
              bgcolor: darkMode ? 'background.paper' : 'grey.50' 
            }}
          >
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
        <Paper sx={{ 
          bgcolor: darkMode ? 'background.paper' : 'primary.50', 
          border: '1px solid', 
          borderColor: darkMode ? 'divider' : 'primary.200' 
        }}>
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

  const renderComprehensiveLearning = (message: Message) => {
    if (!message.hasComprehensiveLearning || !message.comprehensiveLearningData) return null;

    const data = message.comprehensiveLearningData;
    
    return (
      <Box sx={{ mt: 2 }}>
        {/* Çıkarılan Kavramlar */}
        {data.extracted_concepts && data.extracted_concepts.length > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" color="primary" sx={{ mb: 1 }}>
              <School sx={{ mr: 0.5, fontSize: 16 }} />
              Çıkarılan Öğrenme Kavramları
            </Typography>
            <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
              {data.extracted_concepts.map((concept: string, index: number) => (
                <Chip 
                  key={index}
                  label={concept} 
                  size="small" 
                  color="info" 
                  variant="outlined" 
                />
              ))}
            </Box>
          </Box>
        )}

        {/* Güncel Eğitim Kaynakları */}
        {data.serp_results && data.serp_results.length > 0 && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" color="primary" sx={{ mb: 1 }}>
              <Web sx={{ mr: 0.5, fontSize: 16 }} />
              Güncel Eğitim Kaynakları ({data.total_serp_count} adet)
            </Typography>
            {data.serp_results.slice(0, 3).map((result: any, index: number) => (
              <Paper 
                key={index} 
                sx={{ 
                  mb: 1, 
                  bgcolor: darkMode ? 'background.paper' : 'primary.50', 
                  border: '1px solid', 
                  borderColor: darkMode ? 'divider' : 'primary.200' 
                }}
              >
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
            {data.serp_results.length > 3 && (
              <Typography variant="caption" color="text.secondary">
                ... ve {data.serp_results.length - 3} kaynak daha
              </Typography>
            )}
          </Box>
        )}

        {/* Yol Haritası */}
        {data.roadmap && (
          <Box sx={{ mb: 2 }}>
            <Paper sx={{ 
              bgcolor: darkMode ? 'background.paper' : 'primary.50', 
              border: '1px solid', 
              borderColor: darkMode ? 'divider' : 'primary.200' 
            }}>
              <Box sx={{ p: 2 }}>
                <Typography variant="h6" color="primary" gutterBottom>
                  <Web sx={{ mr: 1, verticalAlign: 'middle' }} />
                  {data.roadmap.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {data.roadmap.description}
                </Typography>
                
                <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                  <Chip 
                    label={`${data.roadmap.modules.length} Modül`} 
                    size="small" 
                    color="primary" 
                    variant="outlined" 
                  />
                  <Chip 
                    label={`${data.roadmap.total_estimated_hours} Saat`} 
                    size="small" 
                    color="secondary" 
                    variant="outlined" 
                  />
                  <Chip 
                    label="AI Oluşturuldu" 
                    size="small" 
                    color="success" 
                    variant="outlined" 
                  />
                </Box>

                <Typography variant="subtitle2" gutterBottom>
                  Öğrenme Modülleri:
                </Typography>
                {data.roadmap.modules.slice(0, 3).map((module: any, index: number) => (
                  <Box key={module.id} sx={{ mb: 1, pl: 1 }}>
                    <Typography variant="body2" fontWeight="medium">
                      {index + 1}. {module.title}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {module.estimated_hours} saat • {module.difficulty}
                    </Typography>
                    {module.description && (
                      <Typography variant="caption" color="text.secondary" display="block">
                        {module.description}
                      </Typography>
                    )}
                  </Box>
                ))}
                
                {data.roadmap.modules.length > 3 && (
                  <Typography variant="caption" color="text.secondary">
                    ... ve {data.roadmap.modules.length - 3} modül daha
                  </Typography>
                )}
              </Box>
            </Paper>
          </Box>
        )}
      </Box>
    );
  };

  const renderEducationSearch = () => {
    if (!showEducationSearch) return null;

    return (
      <Box sx={{ 
        mt: 2, 
        p: 2, 
        bgcolor: darkMode ? 'background.paper' : 'grey.50', 
        borderRadius: 2,
        border: darkMode ? '1px solid' : 'none',
        borderColor: darkMode ? 'divider' : 'transparent'
      }}>
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
      <Box sx={{ 
        mt: 2, 
        p: 2, 
        bgcolor: darkMode ? 'background.paper' : 'primary.50', 
        borderRadius: 2,
        border: darkMode ? '1px solid' : 'none',
        borderColor: darkMode ? 'divider' : 'transparent'
      }}>
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
        <Button
          variant="contained"
          size="small"
          startIcon={<Web />}
          onClick={() => {
            const topic = prompt("Hangi konu hakkında kapsamlı öğrenme içeriği istiyorsunuz?");
            if (topic && topic.trim()) {
              handleComprehensiveLearning(topic.trim());
            }
          }}
          disabled={isLoading}
          sx={{ 
            bgcolor: 'success.main', 
            '&:hover': { bgcolor: 'success.dark' } 
          }}
        >
          Kapsamlı Öğrenme
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
          boxShadow: darkMode 
            ? '0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3)'
            : '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
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
            bgcolor: darkMode ? 'background.paper' : 'background.paper',
            border: darkMode ? '1px solid' : 'none',
            borderColor: darkMode ? 'divider' : 'transparent',
            boxShadow: darkMode 
              ? '0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3)'
              : '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
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
            bgcolor: darkMode ? 'background.default' : 'grey.50',
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
                      bgcolor: message.isUser ? 'primary.main' : (darkMode ? 'background.paper' : 'white'),
                      color: message.isUser ? 'white' : 'text.primary',
                      borderRadius: 2,
                      boxShadow: darkMode ? 3 : 1,
                      maxWidth: '100%',
                      border: darkMode && !message.isUser ? '1px solid' : 'none',
                      borderColor: darkMode && !message.isUser ? 'divider' : 'transparent',
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

                    {/* Comprehensive Learning */}
                    {renderComprehensiveLearning(message)}
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
        <Box sx={{ 
          p: 2, 
          bgcolor: darkMode ? 'background.paper' : 'white',
          borderTop: darkMode ? '1px solid' : 'none',
          borderColor: darkMode ? 'divider' : 'transparent'
        }}>
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
              sx={{ 
                bgcolor: 'primary.main', 
                color: 'white', 
                '&:hover': { bgcolor: 'primary.dark' },
                '&:disabled': {
                  bgcolor: darkMode ? 'action.disabledBackground' : 'action.disabledBackground',
                  color: darkMode ? 'action.disabled' : 'action.disabled'
                }
              }}
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