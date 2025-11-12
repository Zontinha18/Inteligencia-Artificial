from pyknow import *
from models import db, Alert, Equipment
from datetime import datetime

class IndustrialFact(Fact):
    """Fato para o sistema especialista"""
    pass

class IndustrialExpertSystem(KnowledgeEngine):
    """Sistema Especialista Industrial"""
    
    def __init__(self, equipment_id):
        super().__init__()
        self.equipment_id = equipment_id
        self.alerts_to_create = []
    
    # Regra 1: Temperatura Crítica + Vibração Alta
    @Rule(
        IndustrialFact(temperature=P(lambda x: x > 85)),
        IndustrialFact(vibration=P(lambda x: x > 3))
    )
    def critical_bearing_failure(self):
        """Falha crítica de rolamento detectada"""
        self.alerts_to_create.append({
            'severity': 'critical',
            'title': 'FALHA CRÍTICA DE ROLAMENTO',
            'description': f'Temperatura acima de 85°C e vibração acima de 3mm/s detectadas. Risco iminente de falha catastrófica.',
            'rule_triggered': 'critical_bearing_failure'
        })
        self._update_equipment_status('critical')
    
    # Regra 2: Temperatura Elevada
    @Rule(
        IndustrialFact(temperature=P(lambda x: 70 < x <= 85))
    )
    def high_temperature_warning(self):
        """Temperatura elevada"""
        self.alerts_to_create.append({
            'severity': 'warning',
            'title': 'Temperatura Elevada',
            'description': f'Temperatura entre 70°C e 85°C. Verificar sistema de resfriamento.',
            'rule_triggered': 'high_temperature_warning'
        })
        self._update_equipment_status('warning')
    
    # Regra 3: Vibração Excessiva
    @Rule(
        IndustrialFact(vibration=P(lambda x: x > 2.5))
    )
    def excessive_vibration_warning(self):
        """Vibração excessiva"""
        self.alerts_to_create.append({
            'severity': 'warning',
            'title': 'Vibração Excessiva',
            'description': f'Vibração acima de 2.5mm/s. Possível desalinhamento ou desbalanceamento.',
            'rule_triggered': 'excessive_vibration_warning'
        })
        self._update_equipment_status('warning')
    
    # Regra 4: Corrente Elétrica Anormal
    @Rule(
        IndustrialFact(current=P(lambda x: x > 50 or x < 5))
    )
    def abnormal_current_warning(self):
        """Corrente elétrica anormal"""
        self.alerts_to_create.append({
            'severity': 'warning',
            'title': 'Corrente Elétrica Anormal',
            'description': f'Corrente fora da faixa normal (5A-50A). Verificar motor e conexões elétricas.',
            'rule_triggered': 'abnormal_current_warning'
        })
    
    # Regra 5: Tempo de Funcionamento Alto (necessita manutenção preventiva)
    @Rule(
        IndustrialFact(runtime=P(lambda x: x > 2000))
    )
    def preventive_maintenance_needed(self):
        """Manutenção preventiva necessária"""
        self.alerts_to_create.append({
            'severity': 'info',
            'title': 'Manutenção Preventiva Recomendada',
            'description': f'Equipamento com mais de 2000 horas de funcionamento. Agendar lubrificação e inspeção.',
            'rule_triggered': 'preventive_maintenance_needed'
        })
    
    # Regra 6: Múltiplos Sensores Anormais (Falha Sistêmica)
    @Rule(
        IndustrialFact(temperature=P(lambda x: x > 75)),
        IndustrialFact(vibration=P(lambda x: x > 2)),
        IndustrialFact(current=P(lambda x: x > 45))
    )
    def systemic_failure_critical(self):
        """Falha sistêmica detectada"""
        self.alerts_to_create.append({
            'severity': 'critical',
            'title': 'FALHA SISTÊMICA DETECTADA',
            'description': f'Múltiplos parâmetros anormais. PARADA IMEDIATA recomendada para evitar danos.',
            'rule_triggered': 'systemic_failure_critical'
        })
        self._update_equipment_status('critical')
    
    # Regra 7: Vibração Baixa + Corrente Alta (Problema de Carga)
    @Rule(
        IndustrialFact(vibration=P(lambda x: x < 0.5)),
        IndustrialFact(current=P(lambda x: x > 40))
    )
    def load_problem_warning(self):
        """Problema de carga"""
        self.alerts_to_create.append({
            'severity': 'warning',
            'title': 'Problema de Carga Detectado',
            'description': f'Baixa vibração com alta corrente indica possível travamento ou sobrecarga.',
            'rule_triggered': 'load_problem_warning'
        })
    
    # Regra 8: Descalibração (valores muito constantes)
    @Rule(
        IndustrialFact(temperature_variance=P(lambda x: x < 0.1)),
        IndustrialFact(vibration_variance=P(lambda x: x < 0.05))
    )
    def sensor_calibration_warning(self):
        """Possível descalibração de sensores"""
        self.alerts_to_create.append({
            'severity': 'info',
            'title': 'Verificar Calibração de Sensores',
            'description': f'Variância anormalmente baixa. Sensores podem estar descalibrados ou com falha.',
            'rule_triggered': 'sensor_calibration_warning'
        })
    
    def _update_equipment_status(self, status):
        """Atualiza status do equipamento"""
        equipment = Equipment.query.get(self.equipment_id)
        if equipment:
            # Só atualiza se o novo status for mais crítico
            priority = {'operational': 0, 'warning': 1, 'critical': 2}
            current_priority = priority.get(equipment.status, 0)
            new_priority = priority.get(status, 0)
            
            if new_priority > current_priority:
                equipment.status = status
                db.session.commit()
    
    def create_alerts(self):
        """Cria alertas no banco de dados"""
        for alert_data in self.alerts_to_create:
            alert = Alert(
                equipment_id=self.equipment_id,
                severity=alert_data['severity'],
                title=alert_data['title'],
                description=alert_data['description'],
                rule_triggered=alert_data['rule_triggered']
            )
            db.session.add(alert)
        
        if self.alerts_to_create:
            db.session.commit()
        
        return len(self.alerts_to_create)


def analyze_equipment_data(equipment_id, sensor_data):
    """
    Analisa dados de sensores usando o sistema especialista
    
    Args:
        equipment_id: ID do equipamento
        sensor_data: dict com dados dos sensores {'temperature': 85, 'vibration': 3.2, ...}
    
    Returns:
        número de alertas criados
    """
    engine = IndustrialExpertSystem(equipment_id)
    engine.reset()
    
    # Declara os fatos
    for sensor_type, value in sensor_data.items():
        engine.declare(IndustrialFact(**{sensor_type: value}))
    
    # Executa o motor de inferência
    engine.run()
    
    # Cria os alertas
    alerts_count = engine.create_alerts()
    
    return alerts_count