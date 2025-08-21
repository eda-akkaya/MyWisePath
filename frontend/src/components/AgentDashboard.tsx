import React, { useState, useEffect } from 'react';
import { agentService, AgentStatus, SystemStatus } from '../services/agentService';
import LoadingSpinner from './LoadingSpinner';
import './AgentDashboard.css';

const AgentDashboard: React.FC = () => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [agents, setAgents] = useState<Record<string, AgentStatus>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  useEffect(() => {
    loadAgentData();
  }, []);

  const loadAgentData = async () => {
    try {
      setLoading(true);
      const data = await agentService.getAgentsStatus();
      setSystemStatus(data.system_status);
      setAgents(data.agents);
      setError(null);
    } catch (err) {
      setError('Agent verileri yüklenirken hata oluştu');
      console.error('Error loading agent data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartAgentManager = async () => {
    try {
      await agentService.startAgentManager();
      await loadAgentData();
    } catch (err) {
      setError('Agent Manager başlatılamadı');
    }
  };

  const handleStopAgentManager = async () => {
    try {
      await agentService.stopAgentManager();
      await loadAgentData();
    } catch (err) {
      setError('Agent Manager durdurulamadı');
    }
  };

  const handleClearStats = async () => {
    try {
      await agentService.clearAgentStatistics();
      await loadAgentData();
    } catch (err) {
      setError('İstatistikler temizlenemedi');
    }
  };

  const formatUptime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}s ${minutes}d ${secs}s`;
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString('tr-TR');
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="agent-dashboard">
        <div className="error-message">
          <h3>❌ Hata</h3>
          <p>{error}</p>
          <button onClick={loadAgentData} className="retry-button">
            Tekrar Dene
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="agent-dashboard">
      <div className="dashboard-header">
        <h2>🤖 Agent Sistemi Dashboard</h2>
        <div className="header-actions">
          <button 
            onClick={handleStartAgentManager}
            className={`action-button ${systemStatus?.system_status === 'running' ? 'disabled' : ''}`}
            disabled={systemStatus?.system_status === 'running'}
          >
            ▶️ Başlat
          </button>
          <button 
            onClick={handleStopAgentManager}
            className={`action-button ${systemStatus?.system_status === 'stopped' ? 'disabled' : ''}`}
            disabled={systemStatus?.system_status === 'stopped'}
          >
            ⏹️ Durdur
          </button>
          <button onClick={handleClearStats} className="action-button warning">
            🗑️ İstatistikleri Temizle
          </button>
          <button onClick={loadAgentData} className="action-button">
            🔄 Yenile
          </button>
        </div>
      </div>

      {/* System Status */}
      {systemStatus && (
        <div className="system-status-card">
          <h3>📊 Sistem Durumu</h3>
          <div className="status-grid">
            <div className="status-item">
              <span className="status-label">Durum:</span>
              <span className={`status-value ${systemStatus.system_status}`}>
                {systemStatus.system_status === 'running' ? '🟢 Çalışıyor' : '🔴 Durdu'}
              </span>
            </div>
            <div className="status-item">
              <span className="status-label">Toplam Agent:</span>
              <span className="status-value">{systemStatus.total_agents}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Aktif Agent:</span>
              <span className="status-value">{systemStatus.active_agents}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Toplam Task:</span>
              <span className="status-value">{systemStatus.total_tasks_executed}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Başarı Oranı:</span>
              <span className="status-value">%{systemStatus.success_rate}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Çalışma Süresi:</span>
              <span className="status-value">{formatUptime(systemStatus.uptime)}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Oluşturulma:</span>
              <span className="status-value">{formatDate(systemStatus.created_at)}</span>
            </div>
            <div className="status-item">
              <span className="status-label">Son Güncelleme:</span>
              <span className="status-value">{formatDate(systemStatus.last_updated)}</span>
            </div>
          </div>
        </div>
      )}

      {/* Agents List */}
      <div className="agents-section">
        <h3>🤖 Agent'lar</h3>
        <div className="agents-grid">
          {Object.entries(agents).map(([agentName, agent]) => (
            <div 
              key={agentName} 
              className={`agent-card ${agent.is_active ? 'active' : 'inactive'} ${selectedAgent === agentName ? 'selected' : ''}`}
              onClick={() => setSelectedAgent(selectedAgent === agentName ? null : agentName)}
            >
              <div className="agent-header">
                <h4>{agent.name}</h4>
                <span className={`status-indicator ${agent.is_active ? 'active' : 'inactive'}`}>
                  {agent.is_active ? '🟢' : '🔴'}
                </span>
              </div>
              <p className="agent-description">{agent.description}</p>
              <div className="agent-stats">
                <div className="stat-item">
                  <span className="stat-label">Bellek:</span>
                  <span className="stat-value">{agent.memory_count}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Araçlar:</span>
                  <span className="stat-value">{agent.tools_count}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Task:</span>
                  <span className="stat-value">{agent.tasks_executed}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Başarı:</span>
                  <span className="stat-value">%{agent.success_rate}</span>
                </div>
              </div>
              <div className="agent-details">
                <small>Oluşturulma: {formatDate(agent.created_at)}</small>
                <small>Son Aktivite: {formatDate(agent.last_activity)}</small>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Agent Details */}
      {selectedAgent && agents[selectedAgent] && (
        <div className="agent-details-modal">
          <div className="modal-content">
            <div className="modal-header">
              <h3>{agents[selectedAgent].name} Detayları</h3>
              <button 
                onClick={() => setSelectedAgent(null)}
                className="close-button"
              >
                ✕
              </button>
            </div>
            <div className="modal-body">
              <div className="detail-section">
                <h4>📋 Genel Bilgiler</h4>
                <p><strong>Açıklama:</strong> {agents[selectedAgent].description}</p>
                <p><strong>Durum:</strong> {agents[selectedAgent].is_active ? '🟢 Aktif' : '🔴 Pasif'}</p>
                <p><strong>Oluşturulma:</strong> {formatDate(agents[selectedAgent].created_at)}</p>
                <p><strong>Son Aktivite:</strong> {formatDate(agents[selectedAgent].last_activity)}</p>
              </div>
              
              <div className="detail-section">
                <h4>📊 Performans</h4>
                <p><strong>Toplam Task:</strong> {agents[selectedAgent].tasks_executed}</p>
                <p><strong>Başarı Oranı:</strong> %{agents[selectedAgent].success_rate}</p>
                <p><strong>Bellek Öğeleri:</strong> {agents[selectedAgent].memory_count}</p>
                <p><strong>Araç Sayısı:</strong> {agents[selectedAgent].tools_count}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AgentDashboard;
