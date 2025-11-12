from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Equipment, Sensor, SensorReading, Alert, MaintenanceRecord, KnowledgeRule
from expert_system import analyze_equipment_data
from config import config
from datetime import datetime, timedelta
import random
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app)
    
    # ==================== ROTAS API ====================
    
    @app.route('/api/health')
    def health():
        """Health check"""
        return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})
    
    @app.route('/api/dashboard')
    def dashboard_data():
        """Dados do dashboard principal"""
        try:
            total_equipments = Equipment.query.count()
            active_alerts = Alert.query.filter_by(is_acknowledged=False).count()
            critical_alerts = Alert.query.filter_by(
                severity='critical',
                is_acknowledged=False
            ).count()
            
            # Equipamentos por status
            equipment_status = db.session.query(
                Equipment.status,
                db.func.count(Equipment.id)
            ).group_by(Equipment.status).all()
            
            # Alertas recentes (últimos 15)
            recent_alerts = Alert.query.order_by(
                Alert.created_at.desc()
            ).limit(15).all()
            
            # Todos os equipamentos
            equipments = Equipment.query.all()
            
            return jsonify({
                'summary': {
                    'total_equipments': total_equipments,
                    'active_alerts': active_alerts,
                    'critical_alerts': critical_alerts,
                    'equipment_status': [
                        {'status': status, 'count': count}
                        for status, count in equipment_status
                    ]
                },
                'recent_alerts': [
                    {
                        'id': alert.id,
                        'equipment_id': alert.equipment_id,
                        'equipment_name': alert.equipment.name,
                        'severity': alert.severity,
                        'title': alert.title,
                        'description': alert.description,
                        'is_acknowledged': alert.is_acknowledged,
                        'created_at': alert.created_at.isoformat()
                    }
                    for alert in recent_alerts
                ],
                'equipments': [
                    {
                        'id': eq.id,
                        'name': eq.name,
                        'type': eq.type,
                        'status': eq.status,
                        'location': eq.location,
                        'sensors_count': eq.sensors.count(),
                        'active_alerts': eq.alerts.filter_by(is_acknowledged=False).count()
                    }
                    for eq in equipments
                ]
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/equipment/<int:equipment_id>')
    def equipment_details(equipment_id):
        """Detalhes completos de um equipamento"""
        try:
            equipment = Equipment.query.get_or_404(equipment_id)
            
            # Últimas leituras (últimas 24 horas)
            last_24h = datetime.utcnow() - timedelta(hours=24)
            readings = SensorReading.query.filter(
                SensorReading.equipment_id == equipment_id,
                SensorReading.timestamp >= last_24h
            ).order_by(SensorReading.timestamp.asc()).all()
            
            # Agrupar por tipo de sensor
            readings_by_sensor = {}
            for reading in readings:
                sensor_type = reading.sensor.sensor_type
                if sensor_type not in readings_by_sensor:
                    readings_by_sensor[sensor_type] = []
                readings_by_sensor[sensor_type].append({
                    'value': float(reading.value),
                    'timestamp': reading.timestamp.isoformat(),
                    'is_anomaly': reading.is_anomaly
                })
            
            # Alertas do equipamento (últimos 30)
            alerts = Alert.query.filter_by(
                equipment_id=equipment_id
            ).order_by(Alert.created_at.desc()).limit(30).all()
            
            # Manutenções
            maintenance_records = MaintenanceRecord.query.filter_by(
                equipment_id=equipment_id
            ).order_by(MaintenanceRecord.created_at.desc()).limit(10).all()
            
            return jsonify({
                'equipment': {
                    'id': equipment.id,
                    'name': equipment.name,
                    'type': equipment.type,
                    'location': equipment.location,
                    'status': equipment.status,
                    'created_at': equipment.created_at.isoformat(),
                    'updated_at': equipment.updated_at.isoformat()
                },
                'sensors': [
                    {
                        'id': sensor.id,
                        'type': sensor.sensor_type,
                        'unit': sensor.unit,
                        'min_threshold': float(sensor.min_threshold) if sensor.min_threshold else None,
                        'max_threshold': float(sensor.max_threshold) if sensor.max_threshold else None,
                        'is_active': sensor.is_active,
                        'mqtt_topic': sensor.mqtt_topic
                    }
                    for sensor in equipment.sensors
                ],
                'readings': readings_by_sensor,
                'alerts': [
                    {
                        'id': alert.id,
                        'severity': alert.severity,
                        'title': alert.title,
                        'description': alert.description,
                        'rule_triggered': alert.rule_triggered,
                        'is_acknowledged': alert.is_acknowledged,
                        'acknowledged_by': alert.acknowledged_by,
                        'created_at': alert.created_at.isoformat()
                    }
                    for alert in alerts
                ],
                'maintenance': [
                    {
                        'id': record.id,
                        'type': record.maintenance_type,
                        'description': record.description,
                        'technician': record.technician,
                        'status': record.status,
                        'completed_date': record.completed_date.isoformat() if record.completed_date else None
                    }
                    for record in maintenance_records
                ]
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/equipment/<int:equipment_id>/sensors')
    def equipment_sensors(equipment_id):
        """Lista de sensores de um equipamento"""
        try:
            equipment = Equipment.query.get_or_404(equipment_id)
            sensors = equipment.sensors.all()
            
            return jsonify({
                'equipment_id': equipment_id,
                'equipment_name': equipment.name,
                'sensors': [
                    {
                        'id': sensor.id,
                        'type': sensor.sensor_type,
                        'unit': sensor.unit,
                        'is_active': sensor.is_active,
                        'min_threshold': float(sensor.min_threshold) if sensor.min_threshold else None,
                        'max_threshold': float(sensor.max_threshold) if sensor.max_threshold else None
                    }
                    for sensor in sensors
                ]
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/alerts')
    def get_alerts():
        """Lista todos os alertas com filtros"""
        try:
            # Parâmetros de filtro
            acknowledged = request.args.get('acknowledged', type=str)
            severity = request.args.get('severity', type=str)
            equipment_id = request.args.get('equipment_id', type=int)
            limit = request.args.get('limit', 50, type=int)
            
            query = Alert.query
            
            # Aplicar filtros
            if acknowledged == 'true':
                query = query.filter_by(is_acknowledged=True)
            elif acknowledged == 'false':
                query = query.filter_by(is_acknowledged=False)
            
            if severity:
                query = query.filter_by(severity=severity)
            
            if equipment_id:
                query = query.filter_by(equipment_id=equipment_id)
            
            alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
            
            return jsonify({
                'alerts': [
                    {
                        'id': alert.id,
                        'equipment_id': alert.equipment_id,
                        'equipment_name': alert.equipment.name,
                        'severity': alert.severity,
                        'title': alert.title,
                        'description': alert.description,
                        'rule_triggered': alert.rule_triggered,
                        'is_acknowledged': alert.is_acknowledged,
                        'acknowledged_by': alert.acknowledged_by,
                        'acknowledged_at': alert.acknowledged_at.isoformat() if alert.acknowledged_at else None,
                        'created_at': alert.created_at.isoformat()
                    }
                    for alert in alerts
                ],
                'count': len(alerts)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/alert/<int:alert_id>/acknowledge', methods=['POST'])
    def acknowledge_alert(alert_id):
        """Reconhecer um alerta"""
        try:
            alert = Alert.query.get_or_404(alert_id)
            data = request.get_json() or {}
            
            alert.is_acknowledged = True
            alert.acknowledged_by = data.get('user', 'Sistema')
            alert.acknowledged_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Alerta reconhecido com sucesso',
                'alert_id': alert_id
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/equipment/<int:equipment_id>/simulate', methods=['POST'])
    def simulate_readings(equipment_id):
        """Simular leituras de sensores e análise"""
        try:
            equipment = Equipment.query.get_or_404(equipment_id)
            sensors = equipment.sensors.filter_by(is_active=True).all()
            
            if not sensors:
                return jsonify({'error': 'Equipamento sem sensores ativos'}), 400
            
            # Criar leituras simuladas
            sensor_data = {}
            readings_created = []
            
            for sensor in sensors:
                # Gerar valor baseado no tipo
                if sensor.sensor_type == 'temperature':
                    value = random.uniform(40, 95)
                elif sensor.sensor_type == 'vibration':
                    value = random.uniform(0.2, 4.5)
                elif sensor.sensor_type == 'current':
                    value = random.uniform(3, 55)
                elif sensor.sensor_type == 'runtime':
                    value = random.uniform(100, 2500)
                else:
                    value = random.uniform(0, 100)
                
                # Detectar anomalia
                is_anomaly = False
                if sensor.max_threshold and value > sensor.max_threshold:
                    is_anomaly = True
                if sensor.min_threshold and value < sensor.min_threshold:
                    is_anomaly = True
                
                # Salvar leitura
                reading = SensorReading(
                    sensor_id=sensor.id,
                    equipment_id=equipment_id,
                    value=value,
                    is_anomaly=is_anomaly
                )
                db.session.add(reading)
                
                sensor_data[sensor.sensor_type] = value
                readings_created.append({
                    'sensor_type': sensor.sensor_type,
                    'value': float(value),
                    'unit': sensor.unit,
                    'is_anomaly': is_anomaly
                })
            
            db.session.commit()
            
            # Analisar com sistema especialista
            alerts_count = analyze_equipment_data(equipment_id, sensor_data)
            
            return jsonify({
                'success': True,
                'equipment_id': equipment_id,
                'equipment_name': equipment.name,
                'readings': readings_created,
                'alerts_generated': alerts_count,
                'timestamp': datetime.utcnow().isoformat()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/init-data', methods=['POST'])
    def init_sample_data():
        """Inicializar banco com dados de exemplo"""
        try:
            # Verificar se já existem dados
            if Equipment.query.count() > 0:
                return jsonify({
                    'success': False,
                    'message': 'Banco de dados já contém dados'
                }), 400
            
            # Criar equipamentos
            equipments_data = [
                {
                    'name': 'Compressor Principal A1',
                    'type': 'compressor',
                    'location': 'Linha de Produção 1',
                    'status': 'operational'
                },
                {
                    'name': 'Motor Rotativo B2',
                    'type': 'rotativo',
                    'location': 'Setor de Estampagem',
                    'status': 'operational'
                },
                {
                    'name': 'Sistema de Aquecimento C3',
                    'type': 'aquecimento',
                    'location': 'Área de Tratamento Térmico',
                    'status': 'operational'
                }
            ]
            
            equipments = []
            for eq_data in equipments_data:
                eq = Equipment(**eq_data)
                db.session.add(eq)
                equipments.append(eq)
            
            db.session.flush()  # Para obter os IDs
            
            # Criar sensores
            sensors_data = []
            
            # Sensores para Compressor A1
            sensors_data.extend([
                {'equipment_id': equipments[0].id, 'sensor_type': 'temperature', 'unit': '°C',
                 'min_threshold': 20, 'max_threshold': 85, 'mqtt_topic': 'sensor/comp_a1/temp'},
                {'equipment_id': equipments[0].id, 'sensor_type': 'vibration', 'unit': 'mm/s',
                 'min_threshold': 0, 'max_threshold': 3, 'mqtt_topic': 'sensor/comp_a1/vib'},
                {'equipment_id': equipments[0].id, 'sensor_type': 'current', 'unit': 'A',
                 'min_threshold': 5, 'max_threshold': 50, 'mqtt_topic': 'sensor/comp_a1/curr'},
                {'equipment_id': equipments[0].id, 'sensor_type': 'runtime', 'unit': 'hours',
                 'min_threshold': 0, 'max_threshold': 10000, 'mqtt_topic': 'sensor/comp_a1/runtime'}
            ])
            
            # Sensores para Motor B2
            sensors_data.extend([
                {'equipment_id': equipments[1].id, 'sensor_type': 'temperature', 'unit': '°C',
                 'min_threshold': 20, 'max_threshold': 85, 'mqtt_topic': 'sensor/motor_b2/temp'},
                {'equipment_id': equipments[1].id, 'sensor_type': 'vibration', 'unit': 'mm/s',
                 'min_threshold': 0, 'max_threshold': 3, 'mqtt_topic': 'sensor/motor_b2/vib'},
                {'equipment_id': equipments[1].id, 'sensor_type': 'current', 'unit': 'A',
                 'min_threshold': 5, 'max_threshold': 50, 'mqtt_topic': 'sensor/motor_b2/curr'}
            ])
            
            # Sensores para Sistema C3
            sensors_data.extend([
                {'equipment_id': equipments[2].id, 'sensor_type': 'temperature', 'unit': '°C',
                 'min_threshold': 20, 'max_threshold': 150, 'mqtt_topic': 'sensor/heat_c3/temp'},
                {'equipment_id': equipments[2].id, 'sensor_type': 'current', 'unit': 'A',
                 'min_threshold': 5, 'max_threshold': 80, 'mqtt_topic': 'sensor/heat_c3/curr'}
            ])
            
            for sensor_data in sensors_data:
                sensor = Sensor(**sensor_data)
                db.session.add(sensor)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Dados de exemplo criados com sucesso',
                'equipments_created': len(equipments),
                'sensors_created': len(sensors_data)
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso não encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)