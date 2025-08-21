import React, { useState } from 'react';
import { agentService, RoadmapInfo, Roadmap } from '../services/agentService';
import LoadingSpinner from './LoadingSpinner';
import './RoadmapCreator.css';

const RoadmapCreator: React.FC = () => {
  const [formData, setFormData] = useState<RoadmapInfo>({
    interests: [''],
    skill_level: 'beginner',
    learning_goals: [''],
    available_hours_per_week: 10,
    target_timeline_months: 6
  });

  const [loading, setLoading] = useState(false);
  const [createdRoadmap, setCreatedRoadmap] = useState<{ roadmap_id: string; roadmap: Roadmap } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const skillLevels = [
    { value: 'beginner', label: 'Başlangıç' },
    { value: 'intermediate', label: 'Orta Seviye' },
    { value: 'advanced', label: 'İleri Seviye' }
  ];

  const handleInputChange = (field: keyof RoadmapInfo, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleArrayInputChange = (field: keyof RoadmapInfo, index: number, value: string) => {
    setFormData(prev => {
      const newArray = [...(prev[field] as string[])];
      newArray[index] = value;
      return {
        ...prev,
        [field]: newArray
      };
    });
  };

  const addArrayItem = (field: keyof RoadmapInfo) => {
    setFormData(prev => ({
      ...prev,
      [field]: [...(prev[field] as string[]), '']
    }));
  };

  const removeArrayItem = (field: keyof RoadmapInfo, index: number) => {
    setFormData(prev => ({
      ...prev,
      [field]: (prev[field] as string[]).filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    console.log('🚀 Roadmap creation started');
    console.log('Form data:', formData);
    
    // Validate form
    if (!formData.interests[0] || !formData.learning_goals[0]) {
      setError('Lütfen en az bir ilgi alanı ve öğrenme hedefi girin');
      return;
    }

    // Filter out empty strings
    const filteredData = {
      ...formData,
      interests: formData.interests.filter(interest => interest.trim() !== ''),
      learning_goals: formData.learning_goals.filter(goal => goal.trim() !== '')
    };

    console.log('Filtered data:', filteredData);

    try {
      setLoading(true);
      setError(null);
      
      console.log('Calling agentService.createRoadmap...');
      const result = await agentService.createRoadmap(filteredData);
      console.log('Roadmap creation result:', result);
      
      setCreatedRoadmap(result);
      
      // Reset form
      setFormData({
        interests: [''],
        skill_level: 'beginner',
        learning_goals: [''],
        available_hours_per_week: 10,
        target_timeline_months: 6
      });
      
    } catch (err) {
      console.error('❌ Error creating roadmap:', err);
      setError('Roadmap oluşturulurken hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNew = () => {
    setCreatedRoadmap(null);
    setError(null);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (createdRoadmap) {
    return (
      <div className="roadmap-creator">
        <div className="success-card">
          <div className="success-header">
            <h2>🎉 Roadmap Başarıyla Oluşturuldu!</h2>
            <p>Kişiselleştirilmiş öğrenme yol haritanız hazır</p>
          </div>
          
          <div className="roadmap-preview">
            <h3>{createdRoadmap.roadmap.title}</h3>
            <p className="roadmap-description">{createdRoadmap.roadmap.description}</p>
            
            <div className="roadmap-meta">
              <div className="meta-item">
                <span className="meta-label">📅 Süre:</span>
                <span className="meta-value">{createdRoadmap.roadmap.estimated_duration_weeks} hafta</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">⏰ Haftalık:</span>
                <span className="meta-value">{createdRoadmap.roadmap.weekly_hours} saat</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">📚 Modüller:</span>
                <span className="meta-value">{createdRoadmap.roadmap.modules.length} adet</span>
              </div>
            </div>

            <div className="roadmap-modules">
              <h4>📖 Öğrenme Modülleri</h4>
              <div className="modules-grid">
                {createdRoadmap.roadmap.modules.map((module, index) => (
                  <div key={index} className="module-card">
                    <h5>{module.title}</h5>
                    <p>{module.description}</p>
                    <div className="module-details">
                      <span className="difficulty-badge">{module.difficulty}</span>
                      <span className="hours-badge">{module.estimated_hours} saat</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="roadmap-strategy">
              <h4>🎯 Öğrenme Stratejisi</h4>
              <p>{createdRoadmap.roadmap.learning_strategy}</p>
            </div>

            <div className="roadmap-milestones">
              <h4>🏁 Kilometre Taşları</h4>
              <ul>
                {createdRoadmap.roadmap.milestones.map((milestone, index) => (
                  <li key={index}>{milestone}</li>
                ))}
              </ul>
            </div>

            <div className="roadmap-metrics">
              <h4>📊 Başarı Kriterleri</h4>
              <ul>
                {createdRoadmap.roadmap.success_metrics.map((metric, index) => (
                  <li key={index}>{metric}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="action-buttons">
            <button onClick={handleCreateNew} className="btn btn-primary">
              🆕 Yeni Roadmap Oluştur
            </button>
            <button 
              onClick={() => window.print()} 
              className="btn btn-secondary"
            >
              🖨️ Yazdır
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="roadmap-creator">
      <div className="creator-header">
        <h2>🗺️ Kişiselleştirilmiş Öğrenme Yol Haritası Oluştur</h2>
        <p>AI destekli agent sistemi ile size özel öğrenme planı hazırlayalım</p>
      </div>

      {error && (
        <div className="error-message">
          <p>❌ {error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="roadmap-form">
        <div className="form-section">
          <h3>🎯 İlgi Alanlarınız</h3>
          <p>Hangi konularda öğrenmek istiyorsunuz?</p>
          
          {formData.interests.map((interest, index) => (
            <div key={index} className="input-group">
              <input
                type="text"
                value={interest}
                onChange={(e) => handleArrayInputChange('interests', index, e.target.value)}
                placeholder="Örn: Python, Web Geliştirme, Veri Bilimi..."
                className="form-input"
              />
              {formData.interests.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeArrayItem('interests', index)}
                  className="remove-btn"
                >
                  ✕
                </button>
              )}
            </div>
          ))}
          
          <button
            type="button"
            onClick={() => addArrayItem('interests')}
            className="add-btn"
          >
            ➕ İlgi Alanı Ekle
          </button>
        </div>

        <div className="form-section">
          <h3>📚 Seviye Belirleme</h3>
          <p>Hangi seviyede olduğunuzu belirtin</p>
          
          <div className="radio-group">
            {skillLevels.map(level => (
              <label key={level.value} className="radio-label">
                <input
                  type="radio"
                  name="skill_level"
                  value={level.value}
                  checked={formData.skill_level === level.value}
                  onChange={(e) => handleInputChange('skill_level', e.target.value)}
                />
                <span className="radio-text">{level.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="form-section">
          <h3>🎯 Öğrenme Hedefleriniz</h3>
          <p>Ne öğrenmek istiyorsunuz?</p>
          
          {formData.learning_goals.map((goal, index) => (
            <div key={index} className="input-group">
              <input
                type="text"
                value={goal}
                onChange={(e) => handleArrayInputChange('learning_goals', index, e.target.value)}
                placeholder="Örn: Full-stack developer olmak, ML projeleri geliştirmek..."
                className="form-input"
              />
              {formData.learning_goals.length > 1 && (
                <button
                  type="button"
                  onClick={() => removeArrayItem('learning_goals', index)}
                  className="remove-btn"
                >
                  ✕
                </button>
              )}
            </div>
          ))}
          
          <button
            type="button"
            onClick={() => addArrayItem('learning_goals')}
            className="add-btn"
          >
            ➕ Hedef Ekle
          </button>
        </div>

        <div className="form-section">
          <h3>⏰ Zaman Planlaması</h3>
          <p>Haftalık ne kadar zaman ayırabilirsiniz?</p>
          
          <div className="range-group">
            <label htmlFor="hours" className="range-label">
              Haftalık Çalışma Saati: <span className="range-value">{formData.available_hours_per_week} saat</span>
            </label>
            <input
              id="hours"
              type="range"
              min="1"
              max="40"
              value={formData.available_hours_per_week}
              onChange={(e) => handleInputChange('available_hours_per_week', parseInt(e.target.value))}
              className="range-input"
            />
            <div className="range-labels">
              <span>1 saat</span>
              <span>40 saat</span>
            </div>
          </div>

          <div className="range-group">
            <label htmlFor="timeline" className="range-label">
              Hedef Süre: <span className="range-value">{formData.target_timeline_months} ay</span>
            </label>
            <input
              id="timeline"
              type="range"
              min="1"
              max="24"
              value={formData.target_timeline_months}
              onChange={(e) => handleInputChange('target_timeline_months', parseInt(e.target.value))}
              className="range-input"
            />
            <div className="range-labels">
              <span>1 ay</span>
              <span>24 ay</span>
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            🚀 Roadmap Oluştur
          </button>
          <button type="reset" className="btn btn-secondary">
            🔄 Sıfırla
          </button>
        </div>
      </form>
    </div>
  );
};

export default RoadmapCreator;
