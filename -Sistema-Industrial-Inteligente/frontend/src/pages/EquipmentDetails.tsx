import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import { ArrowLeft, RefreshCw, Play, Thermometer, Activity, Zap, Clock } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export const EquipmentDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const [simulating, setSimulating] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getEquipmentDetails(id);
      setData(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSimulate = async () => {
    try {
      setSimulating(true);
      const response = await apiService.simulateReadings(id);
      alert(`Simulação concluída!\n${response.data.alerts_generated} alerta(s) gerado(s)`);
      fetchData();
    } catch (err) {
      alert('Erro na simulação: ' + err.message);
    } finally {
      setSimulating(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, [id]);

  if (loading) {
    return <div className="loading"><RefreshCw size={32} className="loading-spinner" />Carregando...</div>;
  }

  if (error) {
    return (
      <div className="error">
        <h3>Erro ao carregar dados</h3>
        <p>{error}</p>
      </div>
    );
  }

  const { equipment, sensors, readings, alerts } = data;

  // Preparar dados para gráficos
  const prepareChartData = (sensorType) => {
    const sensorReadings = readings[sensorType] || [];
    return sensorReadings.map(r => ({
      time: new Date(r.timestamp).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }),
      value: r.value,
    })).slice(-20); // Últimas 20 leituras
  };

  const getSensorIcon = (type) => {
    switch (type) {
      case 'temperature': return <Thermometer size={20} />;
      case 'vibration': return <Activity size={20} />;
      case 'current': return <Zap size={20} />;
      case 'runtime': return <Clock size={20} />;
      default: return <Activity size={20} />;
    }
  };

  return (
    <div>
      <div className="flex-between mb-20">
        <div className="flex" style={{ gap: '12px', alignItems: 'center' }}>
          <button className="btn btn-secondary" onClick={() => navigate('/')}>
            <ArrowLeft size={16} />
            Voltar
          </button>
          <div>
            <h1 style={{ fontSize: '24px', fontWeight: '700', color: '#fff', marginBottom: '4px' }}>
              {equipment.name}
            </h1>
            <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '14px' }}>
              {equipment.type} • {equipment.location}
            </p>
          </div>
        </div>
        <div className="flex gap-10">
          <button className="btn btn-success" onClick={handleSimulate} disabled={simulating}>
            <Play size={16} />
            {simulating ? 'Simulando...' : 'Simular Leituras'}
          </button>
          <button className="btn btn-secondary" onClick={fetchData}>
            <RefreshCw size={16} />
            Atualizar
          </button>
        </div>
      </div>

      {/* Sensores */}
      <div className="grid-4 mb-20">
        {sensors.map((sensor) => {
          const latestReading = readings[sensor.type]?.[readings[sensor.type].length - 1];
          return (
            <div key={sensor.id} className="card">
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                <div style={{ color: '#667eea' }}>
                  {getSensorIcon(sensor.type)}
                </div>
                <div>
                  <div style={{ fontSize: '14px', fontWeight: '600', color: '#333', textTransform: 'capitalize' }}>
                    {sensor.type.replace('_', ' ')}
                  </div>
                  <div style={{ fontSize: '12px', color: '#999' }}>
                    {sensor.unit}
                  </div>
                </div>
              </div>
              <div style={{ fontSize: '28px', fontWeight: '700', color: '#333' }}>
                {latestReading ? latestReading.value.toFixed(2) : '--'}
              </div>
              <div style={{ fontSize: '11px', color: '#999', marginTop: '4px' }}>
                Limite: {sensor.min_threshold} - {sensor.max_threshold} {sensor.unit}
              </div>
            </div>
          );
        })}
      </div>

      {/* Gráficos */}
      <div className="grid-2 mb-20">
        {sensors.slice(0, 4).map((sensor) => {
          const chartData = prepareChartData(sensor.type);
          if (chartData.length === 0) return null;

          return (
            <div key={sensor.id} className="card">
              <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', textTransform: 'capitalize' }}>
                {sensor.type.replace('_', ' ')} ({sensor.unit})
              </h3>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" style={{ fontSize: '12px' }} />
                  <YAxis style={{ fontSize: '12px' }} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#667eea" strokeWidth={2} name={sensor.type} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          );
        })}
      </div>

      {/* Alertas */}
      <div className="card">
        <h2 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '16px' }}>Histórico de Alertas</h2>
        {alerts.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#999', padding: '20px' }}>Nenhum alerta registrado</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {alerts.map((alert) => (
              <div
                key={alert.id}
                style={{
                  display: 'flex',
                  gap: '12px',
                  padding: '16px',
                  background: alert.severity === 'critical' ? '#ffe5e5' :
                             alert.severity === 'warning' ? '#fff9e5' : '#e5f5ff',
                  borderRadius: '8px',
                  borderLeft: `4px solid ${
                    alert.severity === 'critical' ? '#dc3545' :
                    alert.severity === 'warning' ? '#ffc107' : '#17a2b8'
                  }`,
                  opacity: alert.is_acknowledged ? 0.6 : 1,
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                    <span className={`badge badge-${alert.severity}`}>
                      {alert.severity.toUpperCase()}
                    </span>
                    {alert.is_acknowledged && (
                      <span style={{ fontSize: '12px', color: '#666' }}>
                        ✓ Reconhecido por {alert.acknowledged_by}
                      </span>
                    )}
                  </div>
                  <h4 style={{ fontSize: '15px', fontWeight: '600', color: '#333', marginBottom: '8px' }}>
                    {alert.title}
                  </h4>
                  <p style={{ fontSize: '13px', color: '#666', marginBottom: '8px' }}>
                    {alert.description}
                  </p>
                  <div style={{ fontSize: '12px', color: '#999' }}>
                    {new Date(alert.created_at).toLocaleString('pt-BR')}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default EquipmentDetails;