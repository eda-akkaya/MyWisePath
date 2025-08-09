import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import './LearningEnvironment.css';

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

  const startBreakSession = async (isLongBreak: boolean = false) => {
    const duration = isLongBreak ? timerSettings.longBreakDuration : timerSettings.shortBreakDuration;
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/learning-environment/timer/break', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ is_long_break: isLongBreak })
      });
      
      if (response.ok) {
        const session = await response.json();
        setCurrentSession(session);
        setTimeLeft(duration * 60);
        setIsRunning(true);
        
        // Rahatlatıcı ses önerisi al
        fetchAmbientSoundRecommendation('relax');
      } else {
        console.error('Mola oturumu başlatılamadı:', response.status);
        // Fallback: Local timer başlat
        const localSession = {
          id: 'local-' + Date.now(),
          user_id: 'local',
          timer_type: isLongBreak ? 'long_break' as const : 'break' as const,
          duration_minutes: duration,
          start_time: new Date().toISOString(),
          completed: false
        };
        setCurrentSession(localSession);
        setTimeLeft(duration * 60);
        setIsRunning(true);
        fetchAmbientSoundRecommendation('relax');
      }
    } catch (error) {
      console.error('Mola oturumu başlatılamadı:', error);
      // Fallback: Local timer başlat
      const localSession = {
        id: 'local-' + Date.now(),
        user_id: 'local',
        timer_type: isLongBreak ? 'long_break' as const : 'break' as const,
        duration_minutes: duration,
        start_time: new Date().toISOString(),
        completed: false
      };
      setCurrentSession(localSession);
      setTimeLeft(duration * 60);
      setIsRunning(true);
      fetchAmbientSoundRecommendation('relax');
    }
  };

  const fetchAmbientSoundRecommendation = async (context: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/learning-environment/ambient-sounds/recommendation?context=${context}`, {
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
        // Fallback: Default ses
        const fallbackSound = {
          id: 'fallback',
          name: 'Lo-Fi Beats',
          genre: 'lo_fi',
          description: 'Rahatlatıcı lo-fi müzik',
          tags: ['lo-fi', 'chill', 'study']
        };
        setCurrentSound(fallbackSound);
      }
    } catch (error) {
      console.error('Ambient ses önerisi alınamadı:', error);
      // Fallback: Default ses
      const fallbackSound = {
        id: 'fallback',
        name: 'Lo-Fi Beats',
        genre: 'lo_fi',
        description: 'Rahatlatıcı lo-fi müzik',
        tags: ['lo-fi', 'chill', 'study']
      };
      setCurrentSound(fallbackSound);
    }
  };

  const handleSessionComplete = () => {
    setIsRunning(false);
    if (currentSession) {
      completeSession(currentSession.id);
      
      // Pomodoro tamamlandıysa sayacı artır
      if (currentSession.timer_type === 'pomodoro') {
        setCompletedPomodoros(prev => prev + 1);
      }
      
      // Otomatik mola başlatma kontrolü
      if (timerSettings.autoStartBreaks && currentSession.timer_type === 'pomodoro') {
        const isLongBreak = completedPomodoros % 4 === 0; // Her 4 pomodoro'da uzun mola
        setTimeout(() => {
          startBreakSession(isLongBreak);
        }, 1000);
      }
    }
  };

  const completeSession = async (sessionId: string) => {
    try {
      await fetch(`http://localhost:8000/api/v1/learning-environment/timer/${sessionId}/complete`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
    } catch (error) {
      console.error('Oturum tamamlanamadı:', error);
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
    setTimeLeft(0);
    setCurrentSession(null);
    setCurrentSound(null);
  };

  const resetPomodoroCount = () => {
    setCompletedPomodoros(0);
    setCurrentPomodoroCount(0);
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getSessionTypeText = (type: string): string => {
    switch (type) {
      case 'pomodoro': return 'Çalışma';
      case 'break': return 'Kısa Mola';
      case 'long_break': return 'Uzun Mola';
      default: return 'Oturum';
    }
  };

  const handlePlaySound = (sound: AmbientSound) => {
    // Ses çalma fonksiyonu - şimdilik sadece console'a yazdırıyoruz
    console.log('Ses çalınıyor:', sound.name);
    
    // Eğer ses URL'i varsa, yeni sekmede aç
    if (sound.url) {
      window.open(sound.url, '_blank');
    } else {
      // Fallback: YouTube'da arama yap
      const searchQuery = encodeURIComponent(`${sound.name} ${sound.genre} music`);
      window.open(`https://www.youtube.com/results?search_query=${searchQuery}`, '_blank');
    }
  };

  const handleBackToDashboard = () => {
    navigate('/dashboard');
  };

  const handleSettingsChange = (field: keyof TimerSettings, value: any) => {
    setTimerSettings(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePreviousTechnique = () => {
    const techniquesArray = Object.values(focusTechniques);
    if (techniquesArray.length === 0) return;
    
    setCurrentTechniqueIndex(prev => 
      prev > 0 ? prev - 1 : techniquesArray.length - 1
    );
  };

  const handleNextTechnique = () => {
    const techniquesArray = Object.values(focusTechniques);
    if (techniquesArray.length === 0) return;
    
    setCurrentTechniqueIndex(prev => 
      prev < techniquesArray.length - 1 ? prev + 1 : 0
    );
  };

  const techniquesArray = Object.values(focusTechniques);
  const currentTechnique = techniquesArray[currentTechniqueIndex];

  return (
    <div className="learning-environment-minimal">
      <div className="minimal-header">
        <button onClick={handleBackToDashboard} className="back-button">
          ← Geri Dön
        </button>
        <div className="header-content-minimal">
          <div className="timer-icon">📚</div>
          <h1>Çalışma Alanı</h1>
        </div>
      </div>

      {/* Motivasyonel Mesaj */}
      {motivationalMessage && (
        <div className="motivational-message">
          <div className="message-content">
            <p>{motivationalMessage.message}</p>
            {motivationalMessage.author && (
              <small>- {motivationalMessage.author}</small>
            )}
          </div>
          <button 
            onClick={() => fetchMotivationalMessage()} 
            className="btn btn-motivation"
          >
            💪 Yeni Motivasyon
          </button>
        </div>
      )}

      <div className="minimal-content">
        <div className="content-grid">
          {/* Sol Taraf - Timer ve Ayarlar */}
          <div className="left-content">
            {/* Timer Bölümü */}
            <div className="timer-section">
              {currentSession ? (
                <div className="active-timer">
                  <div className="timer-display">
                    <div className="timer-type">
                      {getSessionTypeText(currentSession.timer_type)}
                      {currentSession.timer_type === 'pomodoro' && (
                        <span className="pomodoro-number">#{currentPomodoroCount}</span>
                      )}
                    </div>
                    <div className="timer-time">
                      {formatTime(timeLeft)}
                    </div>
                    <div className="timer-progress">
                      <div 
                        className="progress-bar"
                        style={{
                          width: `${((currentSession.duration_minutes * 60 - timeLeft) / (currentSession.duration_minutes * 60)) * 100}%`
                        }}
                      ></div>
                    </div>
                  </div>
                  
                  <div className="timer-controls">
                    {isRunning ? (
                      <button onClick={pauseSession} className="btn btn-pause">
                        ⏸️ Duraklat
                      </button>
                    ) : (
                      <button onClick={resumeSession} className="btn btn-resume">
                        ▶️ Devam Et
                      </button>
                    )}
                    <button onClick={stopSession} className="btn btn-stop">
                      ⏹️ Durdur
                    </button>
                  </div>
                </div>
              ) : (
                <div className="timer-actions">
                  <button 
                    onClick={startPomodoroSession} 
                    className="btn btn-primary"
                    disabled={completedPomodoros >= timerSettings.targetPomodoros}
                  >
                    ⬇️ Pomodoro Başlat ({timerSettings.pomodoroDuration}dk)
                  </button>
                </div>
              )}
            </div>

            {/* Öğrenme Ortamı Ayarları */}
            <div className="settings-section">
              <h2>⚙️ Öğrenme Ortamı Ayarları</h2>
              <div className="settings-grid-minimal">
                <div className="setting-item">
                  <label>Pomodoro Süresi (dk)</label>
                  <input 
                    type="number" 
                    value={timerSettings.pomodoroDuration}
                    onChange={(e) => handleSettingsChange('pomodoroDuration', parseInt(e.target.value))}
                    min={15} 
                    max={60} 
                  />
                </div>
                <div className="setting-item">
                  <label>Kısa Mola (dk)</label>
                  <input 
                    type="number" 
                    value={timerSettings.shortBreakDuration}
                    onChange={(e) => handleSettingsChange('shortBreakDuration', parseInt(e.target.value))}
                    min={3} 
                    max={10} 
                  />
                </div>
                <div className="setting-item">
                  <label>Uzun Mola (dk)</label>
                  <input 
                    type="number" 
                    value={timerSettings.longBreakDuration}
                    onChange={(e) => handleSettingsChange('longBreakDuration', parseInt(e.target.value))}
                    min={10} 
                    max={30} 
                  />
                </div>
                <div className="setting-item">
                  <label>Hedef Pomodoro Sayısı</label>
                  <input 
                    type="number" 
                    value={timerSettings.targetPomodoros}
                    onChange={(e) => handleSettingsChange('targetPomodoros', parseInt(e.target.value))}
                    min={1} 
                    max={20} 
                  />
                </div>
                <div className="setting-item checkbox">
                  <label>
                    <input 
                      type="checkbox" 
                      checked={timerSettings.autoStartBreaks}
                      onChange={(e) => handleSettingsChange('autoStartBreaks', e.target.checked)}
                    /> 
                    Otomatik mola başlat
                  </label>
                </div>
                <div className="setting-item checkbox">
                  <label>
                    <input 
                      type="checkbox" 
                      checked={timerSettings.eyeCareReminders}
                      onChange={(e) => handleSettingsChange('eyeCareReminders', e.target.checked)}
                    /> 
                    Göz bakımı hatırlatıcıları
                  </label>
                </div>
              </div>
            </div>

            {/* Pomodoro İlerleme Durumu */}
            <div className="pomodoro-progress">
              <div className="progress-info">
                <span>Tamamlanan: {completedPomodoros}/{timerSettings.targetPomodoros}</span>
                <span>Hedef: {timerSettings.targetPomodoros} Pomodoro</span>
              </div>
              <div className="progress-bar-container">
                <div 
                  className="progress-bar"
                  style={{
                    width: `${(completedPomodoros / timerSettings.targetPomodoros) * 100}%`
                  }}
                ></div>
              </div>
              <button onClick={resetPomodoroCount} className="btn btn-reset">
                🔄 Sıfırla
              </button>
            </div>
          </div>

          {/* Sağ Taraf - Ambient Music */}
          <div className="right-content">
            {/* Ambient Ses Önerisi */}
            <div className="ambient-sound-section">
              <h2>🎵 Önerilen Ses</h2>
              {currentSound ? (
                <div className="sound-card">
                  <h3>{currentSound.name}</h3>
                  <p>{currentSound.description}</p>
                  <div className="sound-tags">
                    {currentSound.tags.map((tag, index) => (
                      <span key={index} className="tag">{tag}</span>
                    ))}
                  </div>
                  <button 
                    className="btn btn-play"
                    onClick={() => handlePlaySound(currentSound)}
                  >
                    ▶️ Dinle
                  </button>
                </div>
              ) : (
                <div className="sound-card loading">
                  <p>🎵 Ses önerisi yükleniyor...</p>
                  <button 
                    className="btn btn-refresh"
                    onClick={() => fetchAmbientSoundRecommendation('focus')}
                  >
                    🔄 Yenile
                  </button>
                </div>
              )}
            </div>

            {/* Odaklanma Teknikleri */}
            <div className="focus-techniques-section">
              <h2>🧠 Odaklanma Teknikleri</h2>
              {currentTechnique ? (
                <div className="technique-card">
                  <h3>{currentTechnique.name}</h3>
                  <p>{currentTechnique.description}</p>
                  <ul>
                    {currentTechnique.steps.map((step, index) => (
                      <li key={index}>{step}</li>
                    ))}
                  </ul>
                  <div className="technique-navigation">
                    <button 
                      onClick={handlePreviousTechnique} 
                      className="btn btn-navigation"
                      disabled={techniquesArray.length <= 1}
                    >
                      ← Önceki
                    </button>
                    <span className="technique-counter">
                      {currentTechniqueIndex + 1} / {techniquesArray.length}
                    </span>
                    <button 
                      onClick={handleNextTechnique} 
                      className="btn btn-navigation"
                      disabled={techniquesArray.length <= 1}
                    >
                      Sonraki →
                    </button>
                  </div>
                </div>
              ) : (
                <div className="technique-card loading">
                  <p>🧠 Odaklanma teknikleri yükleniyor...</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LearningEnvironment; 