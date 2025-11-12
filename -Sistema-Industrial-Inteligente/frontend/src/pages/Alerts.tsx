import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { RefreshCw, CheckCircle, AlertTriangle, Info, XCircle } from 'lucide-react';

export const Alerts = () => {
  const [loading, setLoading] = useState(true);
  const [alerts, setAlerts] = useState([]);
  const [filter, setFilter] = useState('all');
  const [severityFilter, setSeverityFilter] = useState('all');

  const fetchAlerts = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filter !== 'all') {
        params.acknowledged = filter === 'acknowledged' ? 'true' : 'false';
      }
      if (severityFilter !== 'all') {
        params.severity = severityFilter;
      }
      const response = await apiService.getAlerts(params);
      setAlerts(response.data.alerts);
    } catch (err) {
      console.error('Error fetching alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAcknowledge = async (alertId: number) => {
    const user = prompt('Digite seu nome:');
    if (!user) return;

    try {
      await apiService.acknowledgeAlert(alertId, user);
      fetchAlerts();
    } catch (err) {
      alert('Erro ao reconhecer alerta: ' + err.message);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 10000);
    return () => clearInterval(interval);
  }, [filter, severityFilter]);

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical': return <XCircle size={20} color="#dc3545" />;
      case 'warning': return <AlertTriangle size={20} color="#ffc107" />;
      case 'info': return <Info size={20} color="#17a2b8" />;
      default: return <Info size={20} />;
    }
  };

  const stats = {
    total: alerts.length,
    critical: alerts.filter(a => a.severity === 'critical' && !a.is_acknowledged).length,
    warning: alerts.filter(a => a.severity === 'warning' && !a.is_acknowledged).length,
    unacknowledged: alerts.filter(a => !a.is_acknowledged).length,
  };

  return (
    <div>
      <div className="flex-between mb-20">
        <h1 style={{ fontSize: '28px', fontWeight: '700', color: '#fff' }}>
          Alertas do Sistema
        </h1>
        <button className="btn btn-secondary" onClick={fetchAlerts}>
          <RefreshCw size={16} />
          Atualizar
        </button>
      </div>

      {/* Estatísticas */}
      <div className="grid-4 mb-20">
        <div className="card">
          <div style={styles.statCard}>
            <div>
              <h3 style={styles.statNumber}>{stats.total}</h3>
              <p style={styles.statLabel}>Total de Alertas</p>
            </div>
            <Info size={40} color="#667eea" style={{ opacity: 0.3 }} />
          </div>
        </div>

        <div className="card">
          <div style={styles.statCard}>
            <div>
              <h3 style={{ ...styles.statNumber, color: '#dc3545' }}>{stats.critical}</h3>
              <p style={styles.statLabel}>Críticos Ativos</p>
            </div>
            <XCircle size={40} color="#dc3545" style={{ opacity: 0.3 }} />
          </div>
        </div>

        <div className="card">
          <div style={styles.statCard}>
            <div>
              <h3 style={{ ...styles.statNumber, color: '#ffc107' }}>{stats.warning}</h3>
              <p style={styles.statLabel}>Avisos Ativos</p>
            </div>
            <AlertTriangle size={40} color="#ffc107" style={{ opacity: 0.3 }} />
          </div>
        </div>

        <div className="card">
          <div style={styles.statCard}>
            <div>
              <h3 style={styles.statNumber}>{stats.unacknowledged}</h3>
              <p style={styles.statLabel}>Não Reconhecidos</p>
            </div>
            <CheckCircle size={40} color="#28a745" style={{ opacity: 0.3 }} />
          </div>
        </div>
      </div>

      {/* Filtros */}
      <div className="card mb-20">
        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
          <div>
            <label style={styles.filterLabel}>Status:</label>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              style={styles.select}
            >
              <option value="all">Todos</option>
              <option value="unacknowledged">Não Reconhecidos</option>
              <option value="acknowledged">Reconhecidos</option>
            </select>
          </div>

          <div>
            <label style={styles.filterLabel}>Severidade:</label>
            <select
              value={severityFilter}
              onChange={(e) => setSeverityFilter(e.target.value)}
              style={styles.select}
            >
              <option value="all">Todas</option>
              <option value="critical">Crítica</option>
              <option value="warning">Aviso</option>
              <option value="info">Informação</option>
            </select>
          </div>
        </div>
      </div>

      {/* Lista de Alertas */}
      <div className="card">
        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            <RefreshCw size={24} className="loading-spinner" />
            <p style={{ marginTop: '12px' }}>Carregando alertas...</p>
          </div>
        ) : alerts.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#999' }}>
            <Info size={48} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
            <p>Nenhum alerta encontrado</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {alerts.map((alert) => (
              <div
                key={alert.id}
                style={{
                  ...styles.alertCard,
                  background: alert.severity === 'critical' ? '#ffe5e5' :
                             alert.severity === 'warning' ? '#fff9e5' : '#e5f5ff',
                  borderLeftColor: alert.severity === 'critical' ? '#dc3545' :
                                  alert.severity === 'warning' ? '#ffc107' : '#17a2b8',
                  opacity: alert.is_acknowledged ? 0.6 : 1,
                }}
              >
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '16px', flex: 1 }}>
                  <div style={{ marginTop: '4px' }}>
                    {getSeverityIcon(alert.severity)}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                      <span className={`badge badge-${alert.severity}`}>
                        {alert.severity.toUpperCase()}
                      </span>
                      <span style={{ fontSize: '13px', color: '#666', fontWeight: '500' }}>
                        {alert.equipment_name}
                      </span>
                      {alert.is_acknowledged && (
                        <span style={{ fontSize: '12px', color: '#28a745', display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <CheckCircle size={14} />
                          Reconhecido
                        </span>
                      )}
                    </div>
                    <h4 style={{ fontSize: '16px', fontWeight: '600', color: '#333', marginBottom: '8px' }}>
                      {alert.title}
                    </h4>
                    <p style={{ fontSize: '14px', color: '#666', marginBottom: '8px', lineHeight: '1.5' }}>
                      {alert.description}
                    </p>
                    <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: '#999' }}>
                      <span>📅 {new Date(alert.created_at).toLocaleString('pt-BR')}</span>
                      {alert.rule_triggered && (
                        <span>🔧 Regra: {alert.rule_triggered}</span>
                      )}
                      {alert.acknowledged_by && (
                        <span>👤 {alert.acknowledged_by}</span>
                      )}
                    </div>
                  </div>
                </div>
                {!alert.is_acknowledged && (
                  <button
                    className="btn btn-success"
                    onClick={() => handleAcknowledge(alert.id)}
                    style={{ alignSelf: 'flex-start' }}
                  >
                    <CheckCircle size={16} />
                    Reconhecer
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  statCard: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  statNumber: {
    fontSize: '32px',
    fontWeight: '700',
    color: '#333',
    marginBottom: '4px',
  },
  statLabel: {
    fontSize: '14px',
    color: '#666',
  },
  filterLabel: {
    display: 'block',
    fontSize: '14px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '8px',
  },
  select: {
    padding: '8px 12px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    fontSize: '14px',
    minWidth: '180px',
    cursor: 'pointer',
  },
  alertCard: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: '16px',
    padding: '20px',
    borderRadius: '10px',
    borderLeft: '5px solid',
    transition: 'all 0.3s',
  },
};

export default Alerts;