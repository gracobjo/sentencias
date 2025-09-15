# ⚙️ Configuración del Sistema

## Descripción General

Esta guía detalla la configuración completa del Analizador de Sentencias, incluyendo variables de entorno, parámetros de análisis y personalización del sistema.

## 🔧 Variables de Entorno

### **Configuración Principal**

```bash
# Aplicación
APP_NAME="Analizador de Sentencias IPP/INSS"
APP_VERSION="1.0.0"
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Base de datos (si se implementa)
DATABASE_URL="sqlite:///sentencias.db"
# DATABASE_URL="postgresql://user:pass@localhost/sentencias"

# Almacenamiento
UPLOAD_DIR="uploads"
SENTENCIAS_DIR="sentencias"
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_EXTENSIONS="pdf,txt,docx"

# Seguridad
SECRET_KEY="your-secret-key-here"
CORS_ORIGINS="http://localhost:3000,https://sentencias.onrender.com"
```

### **Configuración de IA**

```bash
# Modelos de IA
ANALIZADOR_IA_DISPONIBLE=true
MODELO_IA_PATH="models/modelo_legal.pkl"
MODELO_SBERT_PATH="models/modelo_legal_sbert.pkl"
FRASES_CLAVE_PATH="models/frases_clave.json"

# Configuración de análisis
CONFIANZA_MINIMA=0.6
FACTOR_REALISMO_JURIDICO=true
MAX_PROBABILIDAD=0.85
MIN_PROBABILIDAD=0.15

# Análisis predictivo
PESO_TS=1.5
PESO_TSJ=1.2
PESO_OTRAS=1.0
FACTOR_INCERTIDUMBRE=0.3
RIESGO_ALTO=100
RIESGO_MEDIO=50
```

### **Configuración de Logging**

```bash
# Logging
LOG_LEVEL="INFO"
LOG_FILE="logs/sentencias.log"
LOG_MAX_SIZE=10485760  # 10MB
LOG_BACKUP_COUNT=5
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## 📁 Estructura de Archivos de Configuración

### **config.py**
```python
import os
from pathlib import Path

class Config:
    """Configuración principal de la aplicación"""
    
    # Aplicación
    APP_NAME = os.getenv('APP_NAME', 'Analizador de Sentencias IPP/INSS')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    
    # Directorios
    BASE_DIR = Path(__file__).parent
    UPLOAD_DIR = BASE_DIR / os.getenv('UPLOAD_DIR', 'uploads')
    SENTENCIAS_DIR = BASE_DIR / os.getenv('SENTENCIAS_DIR', 'sentencias')
    MODELS_DIR = BASE_DIR / 'models'
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Archivos
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'pdf,txt,docx').split(',')
    
    # IA
    ANALIZADOR_IA_DISPONIBLE = os.getenv('ANALIZADOR_IA_DISPONIBLE', 'true').lower() == 'true'
    MODELO_IA_PATH = MODELS_DIR / os.getenv('MODELO_IA_PATH', 'modelo_legal.pkl')
    FRASES_CLAVE_PATH = MODELS_DIR / os.getenv('FRASES_CLAVE_PATH', 'frases_clave.json')
    
    # Análisis
    CONFIANZA_MINIMA = float(os.getenv('CONFIANZA_MINIMA', 0.6))
    FACTOR_REALISMO_JURIDICO = os.getenv('FACTOR_REALISMO_JURIDICO', 'true').lower() == 'true'
    
    # Análisis predictivo
    PESO_TS = float(os.getenv('PESO_TS', 1.5))
    PESO_TSJ = float(os.getenv('PESO_TSJ', 1.2))
    PESO_OTRAS = float(os.getenv('PESO_OTRAS', 1.0))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = LOGS_DIR / os.getenv('LOG_FILE', 'sentencias.log')
    
    @classmethod
    def create_directories(cls):
        """Crear directorios necesarios"""
        cls.UPLOAD_DIR.mkdir(exist_ok=True)
        cls.SENTENCIAS_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
```

## 🎯 Configuración de Análisis

### **Frases Clave Personalizadas**

Archivo: `models/frases_clave.json`

```json
{
  "incapacidad_permanente_parcial": [
    "incapacidad permanente parcial",
    "IPP",
    "permanente parcial",
    "secuela permanente"
  ],
  "reclamacion_administrativa": [
    "reclamación administrativa previa",
    "RAP",
    "reclamación previa",
    "vía administrativa"
  ],
  "lesiones_hombro": [
    "rotura del manguito rotador",
    "supraespinoso",
    "hombro derecho",
    "manguito rotador"
  ],
  "personal_limpieza": [
    "limpiadora",
    "personal de limpieza",
    "servicios de limpieza",
    "trabajador de limpieza"
  ]
}
```

### **Categorías de Riesgo**

Archivo: `backend/analisis_predictivo.py`

```python
CATEGORIAS_RIESGO = {
    "alto": [
        "reclamacion_administrativa",
        "procedimiento_legal", 
        "fundamentos_juridicos"
    ],
    "medio": [
        "lesiones_permanentes",
        "accidente_laboral",
        "prestaciones"
    ],
    "bajo": [
        "inss",
        "personal_limpieza",
        "lesiones_hombro"
    ]
}
```

### **Patrones de Análisis**

Archivo: `backend/analisis.py`

```python
PATRONES_FAVORABLES = [
    "estimamos", "estimando", "se estima", "procedente",
    "concedemos", "acogemos", "reconocemos", "se reconoce"
]

PATRONES_DESFAVORABLES = [
    "desestimamos", "desestimando", "se desestima", "improcedente",
    "no ha lugar", "confirmamos", "absolvemos", "denegamos"
]
```

## 🔧 Configuración de Modelos de IA

### **Modelo TF-IDF**

```python
# Configuración del vectorizador TF-IDF
TFIDF_CONFIG = {
    "max_features": 10000,
    "ngram_range": (1, 3),
    "min_df": 2,
    "max_df": 0.95,
    "stop_words": "spanish"
}

# Configuración del clasificador
CLASIFICADOR_CONFIG = {
    "random_state": 42,
    "max_iter": 1000,
    "C": 1.0
}
```

### **Modelo Sentence-BERT**

```python
# Configuración de Sentence-BERT
SBERT_CONFIG = {
    "model_name": "paraphrase-multilingual-MiniLM-L12-v2",
    "max_seq_length": 512,
    "batch_size": 16,
    "normalize_embeddings": True
}
```

## 📊 Configuración de Rendimiento

### **Límites de Recursos**

```python
# Límites de procesamiento
PROCESSING_LIMITS = {
    "max_documents_per_request": 50,
    "max_text_length": 1000000,  # 1MB
    "max_analysis_time": 300,    # 5 minutos
    "max_concurrent_requests": 10
}

# Configuración de caché
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 3600,  # 1 hora
    "max_size": 1000,
    "backend": "memory"  # o "redis"
}
```

### **Optimizaciones**

```python
# Configuración de optimización
OPTIMIZATION_CONFIG = {
    "enable_multiprocessing": True,
    "max_workers": 4,
    "chunk_size": 1000,
    "enable_caching": True,
    "lazy_loading": True
}
```

## 🗄️ Configuración de Base de Datos

### **SQLite (Desarrollo)**

```python
DATABASE_CONFIG = {
    "url": "sqlite:///sentencias.db",
    "echo": False,
    "pool_size": 5,
    "max_overflow": 10
}
```

### **PostgreSQL (Producción)**

```python
DATABASE_CONFIG = {
    "url": "postgresql://user:pass@localhost/sentencias",
    "echo": False,
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "pool_recycle": 3600
}
```

## 🔒 Configuración de Seguridad

### **Autenticación**

```python
SECURITY_CONFIG = {
    "secret_key": "your-secret-key-here",
    "algorithm": "HS256",
    "access_token_expire_minutes": 30,
    "refresh_token_expire_days": 7
}
```

### **CORS**

```python
CORS_CONFIG = {
    "allow_origins": [
        "http://localhost:3000",
        "https://sentencias.onrender.com"
    ],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["*"]
}
```

### **Rate Limiting**

```python
RATE_LIMIT_CONFIG = {
    "requests_per_minute": 60,
    "burst_size": 10,
    "window_size": 60
}
```

## 📝 Configuración de Logging

### **Configuración Básica**

```python
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/sentencias.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console", "file"]
        }
    }
}
```

## 🚀 Configuración de Despliegue

### **Docker**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app-deploy.py"]
```

### **Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - DATABASE_URL=postgresql://user:pass@db:5432/sentencias
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=sentencias
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### **Render**

```yaml
# render.yaml
services:
  - type: web
    name: sentencias-app
    env: python
    buildCommand: pip install -r requirements-deploy.txt
    startCommand: python app-deploy.py
    envVars:
      - key: DEBUG
        value: false
      - key: ANALIZADOR_IA_DISPONIBLE
        value: true
```

## 🔍 Configuración de Monitoreo

### **Métricas**

```python
METRICS_CONFIG = {
    "enabled": True,
    "port": 9090,
    "path": "/metrics",
    "collectors": [
        "document_analysis_duration",
        "prediction_accuracy",
        "error_rate",
        "memory_usage"
    ]
}
```

### **Health Checks**

```python
HEALTH_CHECK_CONFIG = {
    "enabled": True,
    "endpoint": "/health",
    "checks": [
        "database_connection",
        "model_loading",
        "disk_space",
        "memory_usage"
    ]
}
```

## 📋 Checklist de Configuración

### **Desarrollo**
- [ ] Variables de entorno configuradas
- [ ] Directorios creados
- [ ] Modelos de IA cargados
- [ ] Logging configurado
- [ ] Base de datos inicializada

### **Producción**
- [ ] Variables de entorno de producción
- [ ] Base de datos configurada
- [ ] Logging en archivos
- [ ] Monitoreo habilitado
- [ ] Seguridad configurada
- [ ] Backup configurado

---

**Nota**: Esta configuración es un ejemplo base. Ajuste los valores según sus necesidades específicas y entorno de despliegue.
