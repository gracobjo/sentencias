#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración principal del Analizador de Sentencias IPP/INSS
"""

import os
from pathlib import Path
from typing import List, Dict, Any

class Config:
    """Configuración principal de la aplicación"""
    
    # Información de la aplicación
    APP_NAME = "Analizador de Sentencias IPP/INSS"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Sistema de análisis inteligente de documentos legales con IA"
    
    # Configuración del servidor
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    
    # Directorios principales
    BASE_DIR = Path(__file__).parent
    UPLOAD_DIR = BASE_DIR / os.getenv('UPLOAD_DIR', 'uploads')
    SENTENCIAS_DIR = BASE_DIR / os.getenv('SENTENCIAS_DIR', 'sentencias')
    MODELS_DIR = BASE_DIR / 'models'
    LOGS_DIR = BASE_DIR / 'logs'
    STATIC_DIR = BASE_DIR / 'static'
    TEMPLATES_DIR = BASE_DIR / 'templates'
    
    # Configuración de archivos
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'pdf,txt,docx').split(',')
    
    # Configuración de IA
    ANALIZADOR_IA_DISPONIBLE = os.getenv('ANALIZADOR_IA_DISPONIBLE', 'true').lower() == 'true'
    MODELO_IA_PATH = MODELS_DIR / os.getenv('MODELO_IA_PATH', 'modelo_legal.pkl')
    MODELO_SBERT_PATH = MODELS_DIR / os.getenv('MODELO_SBERT_PATH', 'modelo_legal_sbert.pkl')
    FRASES_CLAVE_PATH = MODELS_DIR / os.getenv('FRASES_CLAVE_PATH', 'frases_clave.json')
    
    # Configuración de análisis
    CONFIANZA_MINIMA = float(os.getenv('CONFIANZA_MINIMA', 0.6))
    FACTOR_REALISMO_JURIDICO = os.getenv('FACTOR_REALISMO_JURIDICO', 'true').lower() == 'true'
    MAX_PROBABILIDAD = float(os.getenv('MAX_PROBABILIDAD', 0.85))
    MIN_PROBABILIDAD = float(os.getenv('MIN_PROBABILIDAD', 0.15))
    
    # Configuración de análisis predictivo
    PESO_TS = float(os.getenv('PESO_TS', 1.5))
    PESO_TSJ = float(os.getenv('PESO_TSJ', 1.2))
    PESO_OTRAS = float(os.getenv('PESO_OTRAS', 1.0))
    FACTOR_INCERTIDUMBRE = float(os.getenv('FACTOR_INCERTIDUMBRE', 0.3))
    RIESGO_ALTO = int(os.getenv('RIESGO_ALTO', 100))
    RIESGO_MEDIO = int(os.getenv('RIESGO_MEDIO', 50))
    
    # Configuración de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = LOGS_DIR / os.getenv('LOG_FILE', 'sentencias.log')
    LOG_MAX_SIZE = int(os.getenv('LOG_MAX_SIZE', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Configuración de seguridad
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,https://sentencias.onrender.com').split(',')
    
    # Configuración de base de datos (para futuras implementaciones)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sentencias.db')
    
    # Configuración de caché
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hora
    CACHE_MAX_SIZE = int(os.getenv('CACHE_MAX_SIZE', 1000))
    
    # Configuración de rate limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE = int(os.getenv('RATE_LIMIT_REQUESTS_PER_MINUTE', 60))
    RATE_LIMIT_BURST_SIZE = int(os.getenv('RATE_LIMIT_BURST_SIZE', 10))
    
    @classmethod
    def create_directories(cls) -> None:
        """Crear directorios necesarios si no existen"""
        directories = [
            cls.UPLOAD_DIR,
            cls.SENTENCIAS_DIR,
            cls.LOGS_DIR,
            cls.MODELS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
    
    @classmethod
    def get_cors_origins(cls) -> List[str]:
        """Obtener lista de orígenes CORS permitidos"""
        return [origin.strip() for origin in cls.CORS_ORIGINS if origin.strip()]
    
    @classmethod
    def get_allowed_extensions(cls) -> List[str]:
        """Obtener lista de extensiones permitidas"""
        return [ext.strip().lower() for ext in cls.ALLOWED_EXTENSIONS if ext.strip()]
    
    @classmethod
    def is_development(cls) -> bool:
        """Verificar si está en modo desarrollo"""
        return cls.DEBUG
    
    @classmethod
    def is_production(cls) -> bool:
        """Verificar si está en modo producción"""
        return not cls.DEBUG
    
    @classmethod
    def get_model_paths(cls) -> Dict[str, Path]:
        """Obtener rutas de todos los modelos"""
        return {
            'ia': cls.MODELO_IA_PATH,
            'sbert': cls.MODELO_SBERT_PATH,
            'frases_clave': cls.FRASES_CLAVE_PATH
        }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validar configuración y devolver estado"""
        validation = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': {}
        }
        
        # Verificar directorios
        try:
            cls.create_directories()
            validation['info']['directories_created'] = True
        except Exception as e:
            validation['valid'] = False
            validation['errors'].append(f"Error creando directorios: {e}")
        
        # Verificar modelos
        model_paths = cls.get_model_paths()
        for name, path in model_paths.items():
            if path.exists():
                validation['info'][f'model_{name}_exists'] = True
            else:
                validation['warnings'].append(f"Modelo {name} no encontrado en {path}")
        
        # Verificar configuración de seguridad en producción
        if cls.is_production():
            if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
                validation['warnings'].append("SECRET_KEY no configurado para producción")
            
            if cls.DEBUG:
                validation['warnings'].append("DEBUG habilitado en producción")
        
        # Verificar límites de archivos
        if cls.MAX_FILE_SIZE > 100 * 1024 * 1024:  # 100MB
            validation['warnings'].append("MAX_FILE_SIZE muy alto (>100MB)")
        
        return validation


# Configuración específica para desarrollo
class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    CACHE_ENABLED = False


# Configuración específica para producción
class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    CACHE_ENABLED = True


# Configuración específica para testing
class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    CACHE_ENABLED = False
    DATABASE_URL = 'sqlite:///:memory:'


# Función para obtener configuración según el entorno
def get_config() -> Config:
    """Obtener configuración según el entorno"""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()


# Instancia global de configuración
config = get_config()

# Validar configuración al importar
if __name__ == "__main__":
    validation = config.validate_config()
    print("🔧 Validación de Configuración:")
    print(f"✅ Válida: {validation['valid']}")
    
    if validation['errors']:
        print("❌ Errores:")
        for error in validation['errors']:
            print(f"  - {error}")
    
    if validation['warnings']:
        print("⚠️ Advertencias:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    
    if validation['info']:
        print("ℹ️ Información:")
        for key, value in validation['info'].items():
            print(f"  - {key}: {value}")