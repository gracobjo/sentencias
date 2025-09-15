# 🚀 Guía de Despliegue

## Descripción General

Esta guía detalla los diferentes métodos de despliegue del Analizador de Sentencias, desde desarrollo local hasta producción en la nube.

## 🏠 Despliegue Local

### **Requisitos del Sistema**

```bash
# Sistema operativo
- Windows 10/11, macOS 10.15+, o Linux Ubuntu 20.04+

# Software requerido
- Python 3.11+
- pip o pipenv
- Git
- 4GB RAM mínimo
- 2GB espacio en disco
```

### **Instalación Rápida**

```bash
# 1. Clonar repositorio
git clone https://github.com/gracobjo/sentencias.git
cd sentencias

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Crear directorios necesarios
mkdir uploads sentencias logs

# 6. Ejecutar aplicación
python app.py
```

### **Instalación con Pipenv**

```bash
# 1. Instalar pipenv
pip install pipenv

# 2. Instalar dependencias
pipenv install

# 3. Activar entorno
pipenv shell

# 4. Ejecutar aplicación
python app.py
```

### **Verificación de Instalación**

```bash
# Verificar que la aplicación funciona
curl http://localhost:8000/health

# Respuesta esperada
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-15T14:30:22Z"
}
```

## 🐳 Despliegue con Docker

### **Dockerfile**

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements-deploy.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p uploads sentencias logs

# Exponer puerto
EXPOSE 8000

# Comando de inicio
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
      - ANALIZADOR_IA_DISPONIBLE=true
      - LOG_LEVEL=INFO
    volumes:
      - ./uploads:/app/uploads
      - ./sentencias:/app/sentencias
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
```

### **Comandos Docker**

```bash
# Construir imagen
docker build -t sentencias-app .

# Ejecutar contenedor
docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads sentencias-app

# Usar Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Detener servicios
docker-compose down
```

## ☁️ Despliegue en la Nube

### **Render (Recomendado)**

#### **Configuración**

```yaml
# render.yaml
services:
  - type: web
    name: sentencias-app
    env: python
    region: oregon
    plan: starter
    buildCommand: pip install -r requirements-deploy.txt
    startCommand: python app-deploy.py
    envVars:
      - key: DEBUG
        value: false
      - key: ANALIZADOR_IA_DISPONIBLE
        value: true
      - key: LOG_LEVEL
        value: INFO
      - key: MAX_FILE_SIZE
        value: 52428800
```

#### **Pasos de Despliegue**

1. **Conectar repositorio GitHub**
   - Ir a [render.com](https://render.com)
   - Conectar cuenta de GitHub
   - Seleccionar repositorio `sentencias`

2. **Configurar servicio web**
   - Tipo: Web Service
   - Entorno: Python
   - Comando de construcción: `pip install -r requirements-deploy.txt`
   - Comando de inicio: `python app-deploy.py`

3. **Variables de entorno**
   ```
   DEBUG=false
   ANALIZADOR_IA_DISPONIBLE=true
   LOG_LEVEL=INFO
   MAX_FILE_SIZE=52428800
   ```

4. **Desplegar**
   - Hacer clic en "Create Web Service"
   - Esperar a que termine el despliegue
   - Verificar que la aplicación funciona

#### **URL de Producción**
```
https://sentencias.onrender.com
```

### **Heroku**

#### **Procfile**

```
web: python app-deploy.py
```

#### **runtime.txt**

```
python-3.11.0
```

#### **Comandos de Despliegue**

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login en Heroku
heroku login

# Crear aplicación
heroku create sentencias-app

# Configurar variables de entorno
heroku config:set DEBUG=false
heroku config:set ANALIZADOR_IA_DISPONIBLE=true

# Desplegar
git push heroku main

# Ver logs
heroku logs --tail
```

### **AWS EC2**

#### **Configuración de Instancia**

```bash
# 1. Crear instancia EC2
# - Tipo: t3.medium (2 vCPU, 4GB RAM)
# - SO: Ubuntu 22.04 LTS
# - Almacenamiento: 20GB SSD

# 2. Conectar por SSH
ssh -i "key.pem" ubuntu@ec2-xxx-xxx-xxx-xxx.compute-1.amazonaws.com

# 3. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 4. Instalar Python y dependencias
sudo apt install python3.11 python3.11-venv python3-pip git nginx -y

# 5. Clonar repositorio
git clone https://github.com/gracobjo/sentencias.git
cd sentencias

# 6. Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# 7. Instalar dependencias
pip install -r requirements-deploy.txt

# 8. Configurar Nginx
sudo nano /etc/nginx/sites-available/sentencias

# 9. Configuración de Nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 10. Habilitar sitio
sudo ln -s /etc/nginx/sites-available/sentencias /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 11. Configurar systemd service
sudo nano /etc/systemd/system/sentencias.service

[Unit]
Description=Sentencias App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/sentencias
Environment="PATH=/home/ubuntu/sentencias/venv/bin"
ExecStart=/home/ubuntu/sentencias/venv/bin/python app-deploy.py
Restart=always

[Install]
WantedBy=multi-user.target

# 12. Iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable sentencias
sudo systemctl start sentencias
sudo systemctl status sentencias
```

### **Google Cloud Platform**

#### **App Engine**

```yaml
# app.yaml
runtime: python311

env_variables:
  DEBUG: "false"
  ANALIZADOR_IA_DISPONIBLE: "true"
  LOG_LEVEL: "INFO"

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

handlers:
- url: /.*
  script: auto
```

#### **Comandos de Despliegue**

```bash
# Instalar Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Autenticar
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Desplegar
gcloud app deploy

# Ver aplicación
gcloud app browse
```

## 🔧 Configuración de Producción

### **Variables de Entorno de Producción**

```bash
# Aplicación
DEBUG=false
HOST=0.0.0.0
PORT=8000

# IA
ANALIZADOR_IA_DISPONIBLE=true
MODELO_IA_PATH=models/modelo_legal.pkl
CONFIANZA_MINIMA=0.6

# Archivos
MAX_FILE_SIZE=52428800
UPLOAD_DIR=uploads
SENTENCIAS_DIR=sentencias

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/sentencias.log

# Seguridad
SECRET_KEY=your-production-secret-key
CORS_ORIGINS=https://yourdomain.com
```

### **Optimizaciones de Rendimiento**

```python
# app-deploy.py
import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Analizador de Sentencias",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

if __name__ == "__main__":
    uvicorn.run(
        "app-deploy:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # Para producción
        access_log=True,
        log_level="info"
    )
```

### **Configuración de Nginx**

```nginx
# nginx.conf
upstream sentencias_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Límites de tamaño de archivo
    client_max_body_size 50M;

    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    location / {
        proxy_pass http://sentencias_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Archivos estáticos
    location /static/ {
        alias /path/to/sentencias/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 📊 Monitoreo y Logging

### **Configuración de Logging**

```python
# logging_config.py
import logging
import logging.handlers
from pathlib import Path

def setup_logging():
    """Configurar logging para producción"""
    
    # Crear directorio de logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Handler para archivo
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "sentencias.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
```

### **Health Checks**

```python
# health.py
from fastapi import FastAPI
import psutil
import os

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    # Verificar memoria
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    
    # Verificar disco
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    
    # Verificar modelos
    modelo_cargado = os.path.exists("models/modelo_legal.pkl")
    
    status = "healthy"
    if memory_usage > 90 or disk_usage > 90 or not modelo_cargado:
        status = "unhealthy"
    
    return {
        "status": status,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "modelo_cargado": modelo_cargado,
        "timestamp": datetime.now().isoformat()
    }
```

## 🔒 Seguridad en Producción

### **Configuración de Seguridad**

```python
# security.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)
```

### **Rate Limiting**

```python
# rate_limiting.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/upload")
@limiter.limit("10/minute")
async def upload_file(request: Request, file: UploadFile):
    # Lógica de subida
    pass
```

## 📋 Checklist de Despliegue

### **Pre-despliegue**
- [ ] Código probado localmente
- [ ] Tests ejecutados exitosamente
- [ ] Variables de entorno configuradas
- [ ] Dependencias actualizadas
- [ ] Documentación actualizada

### **Despliegue**
- [ ] Servidor configurado
- [ ] Aplicación desplegada
- [ ] Variables de entorno establecidas
- [ ] Servicios iniciados
- [ ] Health check funcionando

### **Post-despliegue**
- [ ] Aplicación accesible
- [ ] Funcionalidades principales probadas
- [ ] Logs monitoreados
- [ ] Backup configurado
- [ ] Monitoreo activo

## 🆘 Troubleshooting

### **Problemas Comunes**

#### **Error de Memoria**
```bash
# Aumentar memoria disponible
export PYTHONHASHSEED=0
export MALLOC_ARENA_MAX=2

# O usar swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### **Error de Permisos**
```bash
# Corregir permisos
sudo chown -R www-data:www-data /path/to/sentencias
sudo chmod -R 755 /path/to/sentencias
```

#### **Error de Dependencias**
```bash
# Reinstalar dependencias
pip install --upgrade pip
pip install -r requirements-deploy.txt --force-reinstall
```

### **Logs de Debug**

```bash
# Ver logs de la aplicación
tail -f logs/sentencias.log

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log

# Ver logs de systemd
sudo journalctl -u sentencias -f
```

---

**Nota**: Esta guía cubre los métodos de despliegue más comunes. Ajuste según su infraestructura específica y necesidades de seguridad.
