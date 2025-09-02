"""
Módulo de observabilidad para el Analizador de Sentencias IPP/INSS
Implementa logging estructurado, métricas y monitoreo
"""

import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import structlog
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse
import psutil
import os

# Configurar logging estructurado
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Métricas de Prometheus
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

UPLOAD_COUNT = Counter(
    'file_uploads_total',
    'Total file uploads',
    ['file_type', 'status']
)

ANALYSIS_COUNT = Counter(
    'document_analysis_total',
    'Total document analyses',
    ['analysis_type', 'model_type', 'status']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

SYSTEM_MEMORY_USAGE = Gauge(
    'system_memory_usage_bytes',
    'System memory usage in bytes'
)

SYSTEM_CPU_USAGE = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage'
)

DISK_USAGE = Gauge(
    'disk_usage_bytes',
    'Disk usage in bytes',
    ['path']
)

class ObservabilityManager:
    """Gestor de observabilidad para la aplicación"""
    
    def __init__(self):
        self.logger = structlog.get_logger()
        self.start_time = time.time()
        self._setup_logging()
    
    def _setup_logging(self):
        """Configurar logging estructurado"""
        # Crear directorio de logs si no existe
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configurar handler para archivo
        file_handler = logging.FileHandler(log_dir / "app.log")
        file_handler.setLevel(logging.INFO)
        
        # Configurar handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato para consola
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # Configurar logger raíz
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    
    def log_request(self, request: Request, response: Response, duration: float):
        """Registrar información de request"""
        self.logger.info(
            "HTTP request",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            duration=duration,
            user_agent=request.headers.get("user-agent"),
            client_ip=request.client.host if request.client else None
        )
        
        # Actualizar métricas
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
    
    def log_upload(self, filename: str, file_type: str, status: str, size: int):
        """Registrar información de upload"""
        self.logger.info(
            "File upload",
            filename=filename,
            file_type=file_type,
            status=status,
            size=size
        )
        
        UPLOAD_COUNT.labels(
            file_type=file_type,
            status=status
        ).inc()
    
    def log_analysis(self, analysis_type: str, model_type: str, status: str, 
                    duration: float, confidence: Optional[float] = None):
        """Registrar información de análisis"""
        self.logger.info(
            "Document analysis",
            analysis_type=analysis_type,
            model_type=model_type,
            status=status,
            duration=duration,
            confidence=confidence
        )
        
        ANALYSIS_COUNT.labels(
            analysis_type=analysis_type,
            model_type=model_type,
            status=status
        ).inc()
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Registrar errores"""
        self.logger.error(
            "Application error",
            error_type=type(error).__name__,
            error_message=str(error),
            context=context or {}
        )
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Registrar eventos de seguridad"""
        self.logger.warning(
            "Security event",
            event_type=event_type,
            details=details
        )
    
    def update_system_metrics(self):
        """Actualizar métricas del sistema"""
        try:
            # Memoria
            memory = psutil.virtual_memory()
            SYSTEM_MEMORY_USAGE.set(memory.used)
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            SYSTEM_CPU_USAGE.set(cpu_percent)
            
            # Disco
            disk_usage = psutil.disk_usage('/')
            DISK_USAGE.labels(path='/').set(disk_usage.used)
            
            # Disco de uploads
            uploads_path = Path("uploads")
            if uploads_path.exists():
                uploads_usage = sum(f.stat().st_size for f in uploads_path.rglob('*') if f.is_file())
                DISK_USAGE.labels(path='uploads').set(uploads_usage)
            
        except Exception as e:
            self.logger.error("Error updating system metrics", error=str(e))
    
    def get_health_status(self) -> Dict[str, Any]:
        """Obtener estado de salud de la aplicación"""
        try:
            uptime = time.time() - self.start_time
            
            # Verificar directorios críticos
            critical_dirs = ["uploads", "models", "templates", "static"]
            dir_status = {}
            for dir_name in critical_dirs:
                dir_path = Path(dir_name)
                dir_status[dir_name] = {
                    "exists": dir_path.exists(),
                    "writable": dir_path.exists() and os.access(dir_path, os.W_OK)
                }
            
            # Verificar archivos críticos
            critical_files = ["models/frases_clave.json"]
            file_status = {}
            for file_name in critical_files:
                file_path = Path(file_name)
                file_status[file_name] = {
                    "exists": file_path.exists(),
                    "readable": file_path.exists() and os.access(file_path, os.R_OK)
                }
            
            # Estado general
            all_dirs_ok = all(status["exists"] and status["writable"] for status in dir_status.values())
            all_files_ok = all(status["exists"] and status["readable"] for status in file_status.values())
            
            health_status = "healthy" if all_dirs_ok and all_files_ok else "unhealthy"
            
            return {
                "status": health_status,
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": uptime,
                "directories": dir_status,
                "files": file_status,
                "system": {
                    "memory_usage_percent": psutil.virtual_memory().percent,
                    "cpu_usage_percent": psutil.cpu_percent(),
                    "disk_usage_percent": psutil.disk_usage('/').percent
                }
            }
            
        except Exception as e:
            self.logger.error("Error getting health status", error=str(e))
            return {
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def get_metrics(self) -> str:
        """Obtener métricas en formato Prometheus"""
        # Actualizar métricas del sistema
        self.update_system_metrics()
        
        return generate_latest()

# Instancia global del gestor de observabilidad
observability = ObservabilityManager()

def get_observability_manager() -> ObservabilityManager:
    """Obtener instancia del gestor de observabilidad"""
    return observability

def log_request_middleware(request: Request, call_next):
    """Middleware para logging de requests"""
    start_time = time.time()
    
    response = call_next(request)
    
    duration = time.time() - start_time
    observability.log_request(request, response, duration)
    
    return response

def setup_observability_routes(app):
    """Configurar rutas de observabilidad en la aplicación"""
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        health_status = observability.get_health_status()
        status_code = 200 if health_status["status"] == "healthy" else 503
        return health_status
    
    @app.get("/metrics")
    async def metrics():
        """Métricas de Prometheus"""
        metrics_data = observability.get_metrics()
        return PlainTextResponse(
            content=metrics_data,
            media_type=CONTENT_TYPE_LATEST
        )
    
    @app.get("/status")
    async def status():
        """Endpoint de estado detallado"""
        return {
            "application": "Analizador de Sentencias IPP/INSS",
            "version": "2.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "health": observability.get_health_status(),
            "timestamp": datetime.now().isoformat()
        }

# Funciones de conveniencia para logging
def log_info(message: str, **kwargs):
    """Log de información"""
    observability.logger.info(message, **kwargs)

def log_warning(message: str, **kwargs):
    """Log de advertencia"""
    observability.logger.warning(message, **kwargs)

def log_error(message: str, **kwargs):
    """Log de error"""
    observability.logger.error(message, **kwargs)

def log_security(event_type: str, **details):
    """Log de evento de seguridad"""
    observability.log_security_event(event_type, details)
