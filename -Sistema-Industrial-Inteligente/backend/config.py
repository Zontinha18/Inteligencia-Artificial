import os
from datetime import timedelta

class Config:
    """Configurações da aplicação"""
    
    # Secret Key
    SECRET_KEY = os.getenv('SECRET_KEY', 'industrial-secret-key-2025')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://industrial_user:industrial_pass@mysql:3306/industrial_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JSON
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    
    # Paginação
    ITEMS_PER_PAGE = 50
    
    # Thresholds padrão
    DEFAULT_TEMP_MAX = 85
    DEFAULT_TEMP_WARNING = 70
    DEFAULT_VIBRATION_MAX = 3.0
    DEFAULT_VIBRATION_WARNING = 2.5
    DEFAULT_CURRENT_MIN = 5
    DEFAULT_CURRENT_MAX = 50
    DEFAULT_RUNTIME_MAINTENANCE = 2000

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    SQLALCHEMY_ECHO = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}