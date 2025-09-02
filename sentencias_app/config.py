#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivo de configuración para el Analizador de Sentencias IPP/INSS
Configuración centralizada de la aplicación
"""

import os
from pathlib import Path
from typing import Dict, Any

# Configuración base de la aplicación
class Config:
    """Configuración principal de la aplicación"""
    
    # Información de la aplicación
    APP_NAME = "Analizador de Sentencias IPP/INSS"
    APP_VERSION = "2.0.0"
    APP_DESCRIPTION = "Aplicación para análisis inteligente de documentos legales"
    
    # Configuración del servidor
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = False
    
    # Configuración de directorios
    BASE_DIR = Path(__file__).parent
    SENTENCIAS_DIR = BASE_DIR / "sentencias"
    UPLOADS_DIR = BASE_DIR / "uploads"
    MODELS_DIR = BASE_DIR / "models"
    LOGS_DIR = BASE_DIR / "logs"
    STATIC_DIR = BASE_DIR / "static"
    TEMPLATES_DIR = BASE_DIR / "templates"
    
    # Configuración de archivos
    ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.doc', '.docx'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    # Configuración de IA
    MODEL_PATH = MODELS_DIR / "modelo_legal.pkl"
    FRASES_CLAVE_PATH = MODELS_DIR / "frases_clave.json"
    
    # Configuración de logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = LOGS_DIR / "app.log"
    
    # Configuración de seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_aqui_cambiarla_en_produccion")
    CORS_ORIGINS = ["*"]  # Configurar apropiadamente en producción
    
    # Configuración de análisis
    MAX_TEXT_LENGTH = 1000000  # 1MB de texto
    CONTEXT_WINDOW = 150  # Caracteres de contexto para frases clave
    
    # Configuración de frases clave por defecto
    FRASES_CLAVE_DEFAULT = {
        "incapacidad_permanente_parcial": [
            "incapacidad permanente parcial", "IPP", "permanente parcial",
            "incapacidad parcial permanente", "secuela permanente",
            "incapacidad permanente", "secuelas permanentes"
        ],
        "reclamacion_administrativa": [
            "reclamación administrativa previa", "RAP", "reclamación previa",
            "vía administrativa", "recurso administrativo", "reclamación"
        ],
        "inss": [
            "INSS", "Instituto Nacional de la Seguridad Social", "Seguridad Social",
            "Instituto Nacional", "Seguridad Social"
        ],
        "lesiones_permanentes": [
            "lesiones permanentes no incapacitantes", "LPNI", "secuelas",
            "lesiones permanentes", "secuelas permanentes", "lesiones"
        ],
        "personal_limpieza": [
            "limpiadora", "personal de limpieza", "servicios de limpieza",
            "trabajador de limpieza", "empleada de limpieza", "limpieza"
        ],
        "lesiones_hombro": [
            "rotura del manguito rotador", "supraespinoso", "hombro derecho",
            "lesión de hombro", "manguito rotador", "tendón supraespinoso",
            "hombro", "manguito"
        ],
        "procedimiento_legal": [
            "procedente", "desestimamos", "estimamos", "fundada",
            "infundada", "accedemos", "concedemos", "reconocemos"
        ]
    }
    
    @classmethod
    def crear_directorios(cls):
        """Crea los directorios necesarios si no existen"""
        for directory in [cls.SENTENCIAS_DIR, cls.UPLOADS_DIR, cls.MODELS_DIR, cls.LOGS_DIR]:
            directory.mkdir(exist_ok=True)
    
    @classmethod
    def obtener_configuracion(cls) -> Dict[str, Any]:
        """Obtiene la configuración como diccionario"""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "app_description": cls.APP_DESCRIPTION,
            "host": cls.HOST,
            "port": cls.PORT,
            "debug": cls.DEBUG,
            "directorios": {
                "sentencias": str(cls.SENTENCIAS_DIR),
                "uploads": str(cls.UPLOADS_DIR),
                "models": str(cls.MODELS_DIR),
                "logs": str(cls.LOGS_DIR)
            },
            "archivos": {
                "extensiones_permitidas": list(cls.ALLOWED_EXTENSIONS),
                "tamaño_maximo": cls.MAX_FILE_SIZE,
                "longitud_maxima_texto": cls.MAX_TEXT_LENGTH
            },
            "ia": {
                "modelo_path": str(cls.MODEL_PATH),
                "frases_clave_path": str(cls.FRASES_CLAVE_PATH)
            }
        }


# Configuración de desarrollo
class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]


# Configuración de producción
class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    SECRET_KEY = os.getenv("SECRET_KEY")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")


# Configuración de testing
class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    TESTING = True


# Función para obtener la configuración según el entorno
def obtener_configuracion(entorno: str = None) -> Config:
    """
    Obtiene la configuración según el entorno
    
    Args:
        entorno: Entorno de ejecución ('development', 'production', 'testing')
        
    Returns:
        Instancia de configuración
    """
    if not entorno:
        entorno = os.getenv("ENVIRONMENT", "development")
    
    configuraciones = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    config_class = configuraciones.get(entorno.lower(), DevelopmentConfig)
    return config_class()


# Configuración por defecto
config = obtener_configuracion()

if __name__ == "__main__":
    # Mostrar configuración actual
    print("Configuración actual:")
    print(f"Entorno: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"App: {config.APP_NAME} v{config.APP_VERSION}")
    print(f"Servidor: {config.HOST}:{config.PORT}")
    print(f"Debug: {config.DEBUG}")
    print(f"Log Level: {config.LOG_LEVEL}")
    
    # Crear directorios
    config.crear_directorios()
    print("✅ Directorios creados/verificados")
    
    # Mostrar directorios
    for nombre, ruta in config.obtener_configuracion()["directorios"].items():
        print(f"📁 {nombre}: {ruta}")
