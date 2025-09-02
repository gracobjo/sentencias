# 📋 Analizador de Sentencias IPP/INSS

[![CI/CD](https://github.com/gracobjo/sentencias/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/gracobjo/sentencias/actions)
[![CodeQL](https://github.com/gracobjo/sentencias/workflows/CodeQL/badge.svg)](https://github.com/gracobjo/sentencias/security/code-scanning)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/gracobjo/sentencias)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Sistema inteligente de análisis automático de resoluciones administrativas y sentencias judiciales para casos de IPP, RAP e INSS. Desarrollado con FastAPI, incluye análisis con IA, generación automática de demandas y observabilidad completa.

## 🚀 Características Principales

### 📄 **Gestión de Documentos**
- **Subida segura** con validación multicapa y sanitización
- **Análisis automático** con IA (TF-IDF + SBERT) y fallback básico
- **Visualización interactiva** con resaltado y búsqueda
- **Detección automática** de instancia (TS/TSJ) por nombre

### 🔍 **Análisis Inteligente**
- **IA Pre-entrenada** con modelos TF-IDF y SBERT
- **Análisis predictivo** con cálculo de riesgo legal
- **Extracción de entidades** y patrones jurídicos
- **Generación de insights** y recomendaciones

### 📝 **Generación de Demandas**
- **Formulario de metadatos** completo y validado
- **Selección inteligente** de documentos
- **Generación automática** de borradores
- **Exportación** en múltiples formatos

### 🛡️ **Seguridad y Observabilidad**
- **Validación robusta** de archivos con escaneo de contenido
- **Logging estructurado** con métricas de Prometheus
- **Health checks** detallados y monitoreo del sistema
- **CI/CD completo** con tests automáticos

## 🏗️ Arquitectura

```
sentencias_app/
├── __init__.py          # Paquete principal
├── main.py              # Aplicación FastAPI
├── config.py            # Configuración
├── security.py          # Validación de archivos
├── observability.py     # Logging y métricas
└── backend/             # Módulos de análisis
    ├── analisis.py      # Analizador de IA
    └── analisis_predictivo.py
```

## 🚀 Instalación y Uso

### Opción 1: Desarrollo Local

```bash
# Clonar repositorio
git clone https://github.com/gracobjo/sentencias.git
cd sentencias

# Instalar dependencias con Pipenv
pipenv install

# Ejecutar aplicación
pipenv run python app.py
```

### Opción 2: Docker

```bash
# Build de imagen
docker build -t sentencias:latest .

# Ejecutar contenedor
docker run -p 8000:8000 sentencias:latest

# O usar docker-compose
docker-compose up
```

### Opción 3: Instalación con pip

```bash
# Instalar desde requirements
pip install -r requirements.DOCKER.txt

# Ejecutar aplicación
python -m sentencias_app.main
```

## 🌐 Acceso a la Aplicación

- **Interfaz Web**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Métricas**: http://localhost:8000/metrics

## 📚 API Endpoints

### Documentos
- `GET /api/documentos` - Listar documentos
- `POST /upload` - Subir documento
- `DELETE /api/documentos/{nombre}` - Eliminar documento

### Análisis
- `GET /api/analisis-predictivo` - Análisis predictivo completo
- `POST /api/analizar` - Analizar documento específico
- `GET /api/frases-clave` - Obtener frases clave

### Generación de Demandas
- `POST /api/demanda-base/txt` - Generar demanda en TXT
- `POST /api/extract/demanda` - Extraer metadatos

### Observabilidad
- `GET /health` - Estado de salud
- `GET /metrics` - Métricas de Prometheus
- `GET /status` - Estado detallado

## 🔧 Configuración

### Variables de Entorno

```bash
# Configuración básica
ENVIRONMENT=production
SECRET_KEY=tu_clave_secreta_aqui
CORS_ORIGINS=http://localhost:3000

# Configuración de logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Configuración de seguridad
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_EXTENSIONS=pdf,txt,doc,docx
```

### Directorios

```
sentencias/
├── sentencias/          # Documentos de análisis
├── uploads/secure/      # Archivos subidos (validados)
├── models/              # Modelos de IA
├── templates/           # Templates HTML
├── static/              # Archivos estáticos
└── logs/                # Logs de aplicación
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pipenv run pytest tests/ -v

# Tests con cobertura
pipenv run pytest tests/ --cov=sentencias_app --cov-report=html

# Tests específicos
pipenv run pytest tests/test_api.py -v
pipenv run pytest tests/test_security.py -v
```

## 🔒 Seguridad

### Validación de Archivos
- **Tipos permitidos**: PDF, TXT, DOC, DOCX
- **Tamaño máximo**: 50MB
- **Sanitización**: Nombres de archivo y contenido
- **Escaneo**: Detección de patrones maliciosos

### Logging de Seguridad
- Eventos de upload y validación
- Intentos de acceso no autorizados
- Errores de seguridad

## 📊 Observabilidad

### Métricas de Prometheus
- `http_requests_total` - Requests HTTP
- `file_uploads_total` - Uploads de archivos
- `document_analysis_total` - Análisis de documentos
- `system_memory_usage_bytes` - Uso de memoria
- `system_cpu_usage_percent` - Uso de CPU

### Health Checks
- Estado de directorios críticos
- Verificación de archivos de configuración
- Métricas del sistema

## 🚀 CI/CD

### GitHub Actions
- **Tests automáticos** en múltiples versiones de Python
- **Build de Docker** con cache optimizado
- **Escaneo de seguridad** con Trivy y CodeQL
- **Deployment automático** a staging y production

### Pre-commit Hooks
- Formateo con Black
- Linting con Flake8
- Type checking con MyPy
- Security checks con Bandit

## 📖 Documentación Adicional

- [Guía de Desarrollo](docs/DEVELOPMENT.md)
- [API Reference](docs/API.md)
- [Configuración](docs/CONFIGURATION.md)
- [Análisis de Riesgo](docs/ANALISIS_RIESGO_PONDERACION.md)
- [Formulario de Metadatos](FORMULARIO_METADATOS_GUIA.md)

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Estándares de Código
- Usar Black para formateo
- Seguir PEP 8
- Añadir tests para nuevas funcionalidades
- Documentar cambios en CHANGELOG.md

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/gracobjo/sentencias/issues)
- **Documentación**: [Wiki](https://github.com/gracobjo/sentencias/wiki)
- **Discusiones**: [GitHub Discussions](https://github.com/gracobjo/sentencias/discussions)

## 🏆 Roadmap

- [ ] Integración con bases de datos
- [ ] API GraphQL
- [ ] Análisis de sentimientos
- [ ] Dashboard de métricas
- [ ] Notificaciones en tiempo real
- [ ] Integración con sistemas legales externos

---

**Desarrollado con ❤️ por [gracobjo](https://github.com/gracobjo)**