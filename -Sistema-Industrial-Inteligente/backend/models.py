from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Equipment(db.Model):
    """Modelo de Equipamento Industrial"""
    __tablename__ = 'equipments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # rotativo, aquecimento, compressor
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='operational')  # operational, warning, critical, maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    sensors = db.relationship('Sensor', backref='equipment', lazy='dynamic', cascade='all, delete-orphan')
    readings = db.relationship('SensorReading', backref='equipment', lazy='dynamic', cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='equipment', lazy='dynamic', cascade='all, delete-orphan')
    maintenance_records = db.relationship('MaintenanceRecord', backref='equipment', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Equipment {self.name}>'


class Sensor(db.Model):
    """Modelo de Sensor IoT"""
    __tablename__ = 'sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)  # temperature, vibration, current, runtime
    unit = db.Column(db.String(20))  # °C, mm/s, A, hours
    min_threshold = db.Column(db.Float)
    max_threshold = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    mqtt_topic = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    readings = db.relationship('SensorReading', backref='sensor', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Sensor {self.sensor_type} - Equipment {self.equipment_id}>'


class SensorReading(db.Model):
    """Modelo de Leitura de Sensor"""
    __tablename__ = 'sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_anomaly = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Reading {self.value} at {self.timestamp}>'


class Alert(db.Model):
    """Modelo de Alerta"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # info, warning, critical
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    rule_triggered = db.Column(db.String(200))
    is_acknowledged = db.Column(db.Boolean, default=False)
    acknowledged_by = db.Column(db.String(100))
    acknowledged_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Alert {self.severity} - {self.title}>'


class MaintenanceRecord(db.Model):
    """Modelo de Registro de Manutenção"""
    __tablename__ = 'maintenance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable=False)
    maintenance_type = db.Column(db.String(50), nullable=False)  # preventive, corrective, predictive
    description = db.Column(db.Text)
    technician = db.Column(db.String(100))
    duration_hours = db.Column(db.Float)
    cost = db.Column(db.Float)
    parts_replaced = db.Column(db.Text)
    scheduled_date = db.Column(db.DateTime)
    completed_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Maintenance {self.maintenance_type} - Equipment {self.equipment_id}>'


class KnowledgeRule(db.Model):
    """Modelo de Regra de Conhecimento"""
    __tablename__ = 'knowledge_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    conditions = db.Column(db.Text, nullable=False)  # JSON com condições
    actions = db.Column(db.Text, nullable=False)  # JSON com ações
    severity = db.Column(db.String(20), default='warning')
    is_active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Rule {self.name}>'