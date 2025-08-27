# 📋 Analizador de Sentencias IPP/INSS

## 🎯 Descripción

Aplicación robusta de **FastAPI** para análisis inteligente de documentos legales, específicamente diseñada para casos de **Incapacidad Permanente Parcial (IPP)** e **Instituto Nacional de la Seguridad Social (INSS)**.

La aplicación asume que ya tienes un **modelo de IA pre-entrenado** y proporciona análisis basado en reglas como fallback.

## ✨ Características Principales

- 🚀 **FastAPI** - Framework web moderno y rápido
- 🤖 **Análisis con IA** - Modelo pre-entrenado para documentos legales
- 📊 **Análisis basado en reglas** - Fallback robusto cuando no hay IA disponible
- 📁 **Manejo de archivos** - Soporte para PDF, TXT, DOC, DOCX
- 🛡️ **Manejo de errores** - Aplicación robusta con validaciones
- 📱 **Interfaz web** - Templates HTML responsivos con Bootstrap 5
- 🐳 **Docker** - Despliegue fácil y reproducible
- 📈 **Monitoreo** - Métricas y health checks integrados

## 🏗️ Arquitectura

```
📁 analizador-ipp-inss/
├── 🐍 app.py                 # Aplicación principal FastAPI
├── ⚙️ config.py              # Configuración centralizada
├── 🤖 backend/
│   └── 📊 analisis.py        # Módulo de análisis de IA
├── 📁 templates/             # Templates HTML
├── 🎨 static/                # Archivos estáticos (CSS, JS)
├── 📁 sentencias/            # Documentos a analizar
├── 📁 uploads/               # Archivos subidos temporalmente
├── 🧠 models/                # Modelos de IA pre-entrenados
├── 📝 requirements.txt       # Dependencias de Python
├── 🐳 Dockerfile             # Imagen Docker
├── 🚀 docker-compose.yml     # Orquestación de servicios
└── 📖 README.md              # Este archivo
```

## 🚀 Instalación y Uso

### 📋 Prerrequisitos

- **Python 3.11+**
- **Docker** (opcional, para despliegue)
- **Git**

### 🔧 Instalación Local

#### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd analizador-ipp-inss
```

#### 2. Crear entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Crear directorios necesarios
```bash
python config.py
```

#### 5. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:8000**

### 🐳 Instalación con Docker

#### 1. Construir y ejecutar
```bash
# Solo la aplicación principal
docker-compose up app

# Todos los servicios (incluyendo Redis, Nginx, monitoreo)
docker-compose up -d
```

#### 2. Verificar estado
```bash
docker-compose ps
```

#### 3. Ver logs
```bash
docker-compose logs -f app
```

## 📚 Uso de la Aplicación

### 🌐 Interfaz Web

1. **Página Principal** (`/`) - Vista general y análisis de sentencias existentes
2. **Subir Documento** (`/subir`) - Formulario para subir nuevos documentos
3. **Resultados** (`/resultado/{id}`) - Visualización detallada del análisis
4. **API Docs** (`/docs`) - Documentación interactiva de la API

### 🔌 API REST

#### Endpoints principales:

- `GET /` - Página principal
- `GET /subir` - Formulario de subida
- `POST /upload` - Subir y analizar documento
- `GET /resultado/{id}` - Ver resultados del análisis
- `GET /api/analizar` - API JSON para análisis
- `GET /health` - Estado del sistema

#### Ejemplo de uso de la API:

```bash
# Subir documento
curl -X POST "http://localhost:8000/upload" \
  -F "file=@documento.pdf" \
  -F "document_type=sentencia"

# Obtener análisis
curl "http://localhost:8000/api/analizar"
```

### 📁 Estructura de Archivos

#### Documentos de ejemplo:
Coloca archivos `.txt`, `.pdf`, `.doc`, `.docx` en la carpeta `sentencias/`

#### Formato esperado:
- **TXT**: Texto plano con encoding UTF-8
- **PDF**: Documentos PDF estándar
- **DOC/DOCX**: Documentos de Word

## ⚙️ Configuración

### 🔧 Variables de Entorno

```bash
# Entorno de ejecución
ENVIRONMENT=development|production|testing

# Clave secreta (cambiar en producción)
SECRET_KEY=tu_clave_secreta_aqui

# Orígenes CORS permitidos
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Contraseña de Grafana (opcional)
GRAFANA_PASSWORD=admin
```

### 📁 Configuración de Directorios

```python
# En config.py
SENTENCIAS_DIR = "sentencias"      # Documentos a analizar
UPLOADS_DIR = "uploads"            # Archivos subidos temporalmente
MODELS_DIR = "models"              # Modelos de IA
LOGS_DIR = "logs"                  # Archivos de log
```

## 🧠 Modelo de IA

### 📋 Requisitos del Modelo

La aplicación espera un modelo guardado en `models/modelo_legal.pkl` con la siguiente estructura:

```python
{
    'modelo': modelo_entrenado,
    'vectorizador': vectorizador_texto,
    'clasificador': clasificador_binario
}
```

### 🔄 Fallback Automático

Si no hay modelo de IA disponible, la aplicación usa automáticamente:
- **Análisis basado en reglas**
- **Patrones de frases clave**
- **Predicción por palabras clave**
- **Extracción de argumentos legales**

## 🧪 Testing

### 🔍 Ejecutar tests
```bash
# Tests básicos
pytest

# Tests con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_analisis.py
```

### 📊 Verificar calidad del código
```bash
# Formatear código
black .

# Verificar estilo
flake8 .

# Verificar tipos
mypy .
```

## 🚀 Despliegue

### 🌍 Producción

#### 1. Configurar variables de entorno
```bash
export ENVIRONMENT=production
export SECRET_KEY=clave_secreta_muy_segura
export CORS_ORIGINS=https://tudominio.com
```

#### 2. Desplegar con Docker
```bash
docker-compose -f docker-compose.yml up -d
```

#### 3. Verificar despliegue
```bash
curl http://localhost:8000/health
```

### 📊 Monitoreo

#### Servicios disponibles:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Redis**: localhost:6379

#### Métricas principales:
- Tiempo de respuesta de la API
- Número de documentos procesados
- Uso de memoria y CPU
- Errores y excepciones

## 🛠️ Desarrollo

### 🔧 Estructura del Código

- **`app.py`**: Aplicación principal FastAPI
- **`config.py`**: Configuración centralizada
- **`backend/analisis.py`**: Lógica de análisis
- **`templates/`**: Templates HTML con Jinja2
- **`static/`**: Archivos CSS, JS e imágenes

### 📝 Agregar Nuevas Funcionalidades

#### 1. Nuevas frases clave:
```python
# En config.py
FRASES_CLAVE_DEFAULT = {
    "nueva_categoria": [
        "frase1", "frase2", "frase3"
    ]
}
```

#### 2. Nuevos tipos de análisis:
```python
# En backend/analisis.py
def nuevo_analisis(texto: str) -> Dict[str, Any]:
    # Implementar nueva lógica
    pass
```

#### 3. Nuevos endpoints:
```python
# En app.py
@app.get("/nuevo-endpoint")
async def nueva_funcionalidad():
    return {"mensaje": "Nueva funcionalidad"}
```

## 🐛 Solución de Problemas

### ❌ Errores Comunes

#### 1. Puerto ya en uso
```bash
# Cambiar puerto en config.py
PORT = 8001

# O matar proceso existente
lsof -ti:8000 | xargs kill -9
```

#### 2. Dependencias faltantes
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

#### 3. Permisos de archivos
```bash
# En Linux/Mac
chmod +x app.py
chmod -R 755 static/ templates/
```

#### 4. Modelo no encontrado
```bash
# Verificar que existe models/modelo_legal.pkl
# O usar análisis basado en reglas
```

### 📊 Logs y Debugging

#### 1. Ver logs en tiempo real
```bash
# Local
tail -f logs/app.log

# Docker
docker-compose logs -f app
```

#### 2. Modo debug
```bash
export ENVIRONMENT=development
python app.py
```

## 🤝 Contribución

### 📋 Guías de Contribución

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crea** un Pull Request

### 🧪 Testing

- Ejecuta todos los tests antes de hacer commit
- Mantén cobertura de código > 80%
- Documenta nuevas funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

### 🆘 Obtener Ayuda

- **Issues**: Reporta bugs en GitHub Issues
- **Discussions**: Preguntas generales en GitHub Discussions
- **Wiki**: Documentación adicional en GitHub Wiki

### 🔗 Enlaces Útiles

- **FastAPI**: https://fastapi.tiangolo.com/
- **Docker**: https://docs.docker.com/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.0/

## 🎉 Agradecimientos

- Equipo de desarrollo IPP/INSS
- Comunidad FastAPI
- Contribuidores de código abierto

---

**¿Necesitas ayuda?** ¡Abre un issue o únete a las discusiones del proyecto!
