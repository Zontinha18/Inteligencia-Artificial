import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import { Activity, AlertTriangle, CheckCircle, XCircle, RefreshCw, Database } from 'lucide-react';

export const Home = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const [initializing, setInitializing] = useState(false);
  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getDashboard();
      setData(response.data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInitData = async () => {
    if (!confirm('Deseja inicializar o banco de dados com dados de exemplo?')) return;
    
    try {
      setInitializing(true);
      await apiService.initSampleData();
      alert('Dados de exemplo criados com sucesso!');
      fetchData();
    } catch (err) {
      alert('Erro ao inicializar dados: ' + err.message);
    } finally {
      setInitializing(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Atualizar a cada 10s
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="loading">
        <RefreshCw size={32} className="loading-spinner" />
        <span style={{ marginLeft: '12px' }}>Carregando...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <h3>Erro ao carregar dados</h3>
        <p>{error}</p>
        <button className="btn btn-primary" onClick={fetchData} style={{ marginTop: '12px' }}>
          <RefreshCw size={16} />
          Tentar Novamente
        </button>
      </div>
    );
  }

  if (!data || data.equipments.length === 0) {
    return (
      <div className="card text-center" style={{ marginTop: '40px', padding: '60px' }}>
        <Database size={64} color="#667eea" style={{ margin: '0 auto 20px' }} />
        <h2>Banco de Dados Vazio</h2>
        <p style={{ margin: '12px 0 24px', color: '#666' }}>
          Inicialize o banco de dados com dados de exemplo para começar
        </p>
        <button
          className="btn btn-primary"
          onClick={handleInitData}
          disabled={initializing}
        >
          <Database size={16} />
          {initializing ? 'Inicializando...' : 'Inicializar Dados de Exemplo'}
        </button>
      </div>
    );
  }

  const { summary, equipments, recent_alerts } = data;

  return (
    <div>
      {/* Cards de Resumo */}
      <div className="grid-4 mb-20">
        <div className="card">
          <div style={styles.statCard}>
            <div>
              <h3 style={styles.statNumber}>{summary.total_equipments}</h3>
              <p style={styles.statLabel}>Total de Equipamentos</p>
            </div>
            <Activity size={40} color="#667eea" style={{ opacity: 0.3 }} />
          </div>
        </div>

        <div className="card">
          <div style={styles.statCard}>
            <div>
              <h3 style={styles.statNumber}>{summary.active_alerts}</h3>
              <p style={styles.statLabel}>Alertas Ativos</p>
            </div>
            <AlertTriangle size={40} color="#ffc107" style={{ opacity: 0.3 }} />
          </div>
        </div>

        <div className="card">
          <div style={styles.statCard}>
            <div>
              <h3 style={styles.statNumber} style={{ color: '#dc3545' }}>
                {summary.critical_alerts}
              </h3>
              <p style={styles.statLabel}>Alertas Críticos</p>
            </div>
            <XCircle size={40} color="#dc3545" style={{ opacity: 0.3 }} />
          </div>
        </div>

        <div className="card">
          <div style={styles.statCard}>
            <div>
              <h3 style={styles.statNumber} style={{ color: '#28a745' }}>
                {summary.equipment_status.find(s => s.status === 'operational')?.count || 0}
              </h3>
              <p style={styles.statLabel}>Operacionais</p>
            </div>
            <CheckCircle size={40} color="#28a745" style={{ opacity: 0.3 }} />
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        {/* Lista de Equipamentos */}
        <div className="card">
          <div className="flex-between mb-20">
            <h2 style={styles.cardTitle}>Equipamentos</h2>
            <button className="btn btn-secondary" onClick={fetchData}>
              <RefreshCw size={16} />
              Atualizar
            </button>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {equipments.map((eq) => (
              <div
                key={eq.id}
                style={{
                  ...styles.equipmentCard,
                  borderLeftColor: eq.status === 'critical' ? '#dc3545' :
                                   eq.status === 'warning' ? '#ffc107' : '#667eea'
                }}
                onClick={() => navigate(`/equipment/${eq.id}`)}
              >
                <div>
                  <h3 style={styles.equipmentName}>{eq.name}</h3>
                  <p style={styles.equipmentInfo}>
                    {eq.type} • {eq.location} • {eq.sensors_count} sensores
                  </p>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '8px' }}>
                  <span className={`badge badge-${eq.status}`}>
                    {eq.status === 'operational' ? 'Operacional' :
                     eq.status === 'warning' ? 'Atenção' : 'Crítico'}
                  </span>
                  {eq.active_alerts > 0 && (
                    <span style={{ fontSize: '12px', color: '#dc3545', fontWeight: '600' }}>
                      {eq.active_alerts} alerta(s)
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Alertas Recentes */}
        <div className="card">
          <h2 style={styles.cardTitle}>Alertas Recentes</h2>
          <div style={{ marginTop: '20px' }}>
            {recent_alerts.length === 0 ? (
              <p style={{ textAlign: 'center', color: '#999', padding: '20px' }}>
                Nenhum alerta recente
              </p>
            ) : (
              recent_alerts.slice(0, 10).map((alert) => (
                <div key={alert.id} style={styles.alertItem}>
                  <div style={{
                    width: '4px',
                    background: alert.severity === 'critical' ? '#dc3545' :
                               alert.severity === 'warning' ? '#ffc107' : '#17a2b8',
                    borderRadius: '2px'
                  }} />
                  <div style={{ flex: 1 }}>
                    <div style={styles.alertTitle}>{alert.title}</div>
                    <div style={styles.alertEquipment}>{alert.equipment_name}</div>
                    <div style={styles.alertTime}>
                      {new Date(alert.created_at).toLocaleString('pt-BR')}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
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
  cardTitle: {
    fontSize: '20px',
    fontWeight: '600',
    color: '#333',
  },
  equipmentCard: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '16px',
    background: '#f8f9fa',
    borderRadius: '8px',
    borderLeft: '4px solid',
    cursor: 'pointer',
    transition: 'all 0.3s',
  },
  equipmentName: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '4px',
  },
  equipmentInfo: {
    fontSize: '13px',
    color: '#666',
  },
  alertItem: {
    display: 'flex',
    gap: '12px',
    padding: '12px',
    background: '#f8f9fa',
    borderRadius: '8px',
    marginBottom: '8px',
  },
  alertTitle: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '4px',
  },
  alertEquipment: {
    fontSize: '12px',
    color: '#666',
    marginBottom: '4px',
  },
  alertTime: {
    fontSize: '11px',
    color: '#999',
  },
};

export default Home;