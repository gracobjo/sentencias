# Analizador de Sentencias IPP/INSS

Aplicación FastAPI para análisis de resoluciones legales, gestión de frases clave (CRUD), análisis predictivo con IA (TF‑IDF y SBERT) y generación automática de borradores de demanda laboral.

## Arranque

1) Instalar dependencias
```bash
pip install -r requirements.txt
```
2) Ejecutar servidor
```bash
python app.py
```
Alternativa desarrollo (autoreload):
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

UI: `http://localhost:8000`  ·  Docs API: `http://localhost:8000/docs`

## Funcionalidades

- Gestión de documentos
  - Subida de sentencias: página `/subir` y endpoint `POST /upload`
  - Listado y eliminación: `GET /api/documentos`, `DELETE /api/documentos`
  - Visualización con resaltado y búsqueda: `GET /archivo/{nombre}`
  - Badges de instancia (TS/TSJ) inferidos por nombre en home y gestor

- Frases clave (CRUD)
  - Listar: `GET /api/frases`
  - Reemplazar set: `POST /api/frases`
  - Categorías: `POST /api/frases/categoria`, `DELETE /api/frases/categoria/{nombre}`, `PATCH /api/frases/categoria`
  - Frases: `POST /api/frases/frase`, `DELETE /api/frases/frase`, `PATCH /api/frases/frase`
  - Modal de gestión con búsqueda/paginación, edición de categorías/frases

- Análisis
  - Análisis básico (fallback) y con IA (TF‑IDF + Logistic Regression) `models/modelo_legal.pkl`
  - Análisis con embeddings (SBERT + clasificador) `models/modelo_legal_sbert.pkl`
  - Reentrenar TF‑IDF: `python backend/train_model.py`
  - Reentrenar SBERT: `python backend/train_embeddings.py`
  - Salud: `GET /health`
  - Analizar set actual: `GET /api/analizar`

- Análisis predictivo avanzado
  - Página: `GET /analisis-predictivo`
  - API: `GET /api/analisis-predictivo`
  - Cálculo de riesgo (backend/analisis_predictivo.py):
    - Agrupa categorías en alto/medio/bajo a partir de `ranking_global`
    - Fórmula: `(alto×3 + medio×2 + bajo) × factor_instancia`
    - `factor_instancia = 1.0 + 0.5·ratio_TS + 0.2·ratio_TSJ`
    - Nivel: >100=alto, >50=medio, si no=bajo
    - Interpretación y recomendaciones por nivel (texto fijo)

- Generación de “Demanda base”
  - Endpoints:
    - `POST /api/demanda-base` → devuelve JSON con borrador
    - `POST /api/demanda-base/txt` → descarga `.txt`
  - Parámetros:
    ```json
    {
      "nombres_archivo": ["STS_2384_2025.pdf", "..."],
      "meta": {
        "nombre": "",
        "dni": "",
        "domicilio": "",
        "letrado": "",
        "empresa": "",
        "profesion": "",
        "grado_principal": "IPT",
        "grado_subsidiario": "IPP",
        "base_reguladora": "",
        "indemnizacion_parcial": "24 mensualidades",
        "mutua": ""
      }
    }
    ```
  - Construcción del borrador:
    - Encabezado y parte: con `meta`
    - Hechos: narrativa propia (relación laboral, contingencia, actuaciones INSS, cuadro clínico)
    - Jurisprudencia de apoyo: extracto breve (fallo y 1–2 fundamentos) de documentos seleccionados (fallo/“parte dispositiva” y fundamentos resumidos)
    - Fundamentos de Derecho: LGSS 193–194, STS/TSJ de apoyo, CE 24/9.3
    - Suplico: principal/subsidiario, unificando la base reguladora de `meta`
    - Anexos: relación de documentos (fallos)

- Extractor estructurado para demanda
  - `POST /api/extract/demanda` body `{ "nombres_archivo": [ ... ] }`
  - Devuelve:
    ```json
    {
      "documentos": [
        {"archivo":"...","instancia":"TS/TSJ/otra","fecha":"...","organo":"...","fallo":"...","fundamentos_resumen":["..."]}
      ],
      "sugerencias_meta": {"profesion":"","empresa":"","mutua":"","base_reguladora":""}
    }
    ```
  - Uso en UI: el botón “Generar Demanda base” llama al extractor y pasa `meta` al generador `.txt`

## Notas técnicas

- IA activa si existe `models/modelo_legal.pkl` (TF‑IDF) o `models/modelo_legal_sbert.pkl` (SBERT). Si ambos, prioriza SBERT.
- Detección flexible de frases: acepta espacios/guiones/underscores intercambiables (e.g., “manguito rotador”/“manguito_rotador”).
- Badges TS/TSJ: inferidos por nombre; la ponderación real de instancia se hace leyendo el contenido.

## Desarrollo

- Estructura principal:
  - `app.py`: API, vistas, CRUD, generador demanda y extractor
  - `backend/analisis.py`: analizador (IA/regex)
  - `backend/analisis_predictivo.py`: riesgo, tendencias, recomendaciones
  - `backend/train_model.py`, `backend/train_embeddings.py`: entrenamiento
  - `templates/*.html`: UI
  - `models/frases_clave.json`: almacenamiento de frases

## Roadmap

- Formulario previo para completar `meta` antes de descargar la demanda
- Exportación a `.docx`
- Etiquetado asistido de BR y contingencia desde la UI

# 📋 Analizador de Sentencias IPP/INSS

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

Sistema inteligente de análisis automático de resoluciones administrativas y sentencias judiciales para casos de Incapacidad Permanente Parcial (IPP), Reclamación Administrativa Previa (RAP) y otros procedimientos del INSS.

## 🚀 Características Principales

- **Análisis Automático**: Procesamiento inteligente de documentos legales (.txt, .pdf, .doc, .docx)
- **IA Pre-entrenada**: Modelo de machine learning para identificación de frases clave
- **Dashboard Interactivo**: Interfaz web moderna con Bootstrap 5 y actualizaciones en tiempo real
- **7 Categorías de Análisis**: IPP, RAP, INSS, LPNI, Limpieza, Lesiones de Hombro, Procedimientos Legales
- **API REST**: Endpoints para integración con sistemas externos
- **Docker Ready**: Despliegue simplificado con contenedores

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   Análisis      │
│   Bootstrap 5   │◄──►│   Backend       │◄──►│   IA + Básico   │
│   JavaScript    │    │   Jinja2        │    │   Fallback      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Modales       │    │   Base de       │    │   Archivos      │
│   Interactivos  │    │   Datos SQLite  │    │   Documentos    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **Python 3.8+**: Lenguaje de programación principal
- **Jinja2**: Motor de templates HTML
- **SQLite**: Base de datos ligera
- **Uvicorn**: Servidor ASGI de alto rendimiento

### Frontend
- **Bootstrap 5**: Framework CSS responsive
- **Bootstrap Icons**: Iconografía moderna
- **JavaScript ES6+**: Lógica del lado del cliente
- **Event Delegation**: Manejo eficiente de eventos dinámicos

### IA y Análisis
- **Scikit-learn**: Algoritmos de machine learning
- **NLTK**: Procesamiento de lenguaje natural
- **PyPDF2**: Extracción de texto de PDFs
- **python-docx**: Procesamiento de documentos Word

### DevOps
- **Docker**: Contenedores para despliegue
- **Docker Compose**: Orquestación de servicios
- **Nginx**: Proxy reverso y servidor web
- **Prometheus**: Monitoreo y métricas

## 📦 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- Docker y Docker Compose (opcional)
- Git

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/analizador-sentencias-ipp.git
cd analizador-sentencias-ipp
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar directorios**
```bash
mkdir -p sentencias uploads models logs
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

### Instalación con Docker

1. **Clonar y navegar al directorio**
```bash
git clone https://github.com/tu-usuario/analizador-sentencias-ipp.git
cd analizador-sentencias-ipp
```

2. **Ejecutar con Docker Compose**
```bash
docker-compose up -d
```

3. **Acceder a la aplicación**
```
http://localhost:8000
```

## 🎯 Uso de la Aplicación

### 1. Análisis Automático
- Coloca documentos en la carpeta `sentencias/`
- Accede a la página principal `/`
- La aplicación analiza automáticamente todos los archivos
- Visualiza resultados en tiempo real

### 2. Subida de Documentos
- Navega a `/subir`
- Selecciona archivo y tipo de documento
- Sube y procesa automáticamente
- Visualiza resultados inmediatamente

### 3. Exploración de Detalles
- Haz clic en tarjetas de estadísticas para ver detalles
- Usa botones "Ver detalles" para información específica
- Navega a archivos completos con "Ver archivo completo"
- Explora ocurrencias específicas de frases clave

## 🔍 Funcionalidades de Análisis

### Categorías de Frases Clave
1. **Incapacidad Permanente Parcial (IPP)**
   - Frases relacionadas con incapacidades permanentes
   - Identificación de secuelas y limitaciones

2. **Reclamación Administrativa Previa (RAP)**
   - Procedimientos administrativos
   - Recursos y reclamaciones

3. **INSS / Seguridad Social**
   - Referencias al Instituto Nacional
   - Procedimientos de la Seguridad Social

4. **Lesiones Permanentes No Incapacitantes (LPNI)**
   - Secuelas que no impiden el trabajo
   - Evaluación de daños permanentes

5. **Personal de Limpieza**
   - Casos específicos del sector
   - Condiciones laborales particulares

6. **Lesiones de Hombro**
   - Manguito rotador
   - Tendón supraespinoso
   - Hombro derecho

7. **Procedimientos Legales**
   - Términos jurídicos clave
   - Resoluciones y sentencias

### Características del Análisis
- **Búsqueda insensible a mayúsculas**
- **Contexto de ocurrencias** con posiciones exactas
- **Predicción de resultado** (favorable/desfavorable)
- **Insights jurídicos** automáticos
- **Argumentos identificados** en el texto

## 📊 API REST

### Endpoints Disponibles

#### `GET /`
- **Descripción**: Página principal con dashboard
- **Respuesta**: HTML con estadísticas en tiempo real

#### `GET /api/analizar`
- **Descripción**: Análisis programático de documentos
- **Respuesta**: JSON con resultados estructurados

#### `GET /archivo/{archivo_id}`
- **Descripción**: Vista completa de un archivo específico
- **Respuesta**: HTML con contenido y frases resaltadas

#### `GET /health`
- **Descripción**: Estado del sistema
- **Respuesta**: JSON con métricas y estado

#### `POST /upload`
- **Descripción**: Subida de nuevos documentos
- **Parámetros**: `file`, `document_type`, `extract_entities`, `analyze_arguments`
- **Respuesta**: JSON con resultado del procesamiento

### Ejemplo de Uso de la API

```python
import requests

# Analizar documentos existentes
response = requests.get('http://localhost:8000/api/analizar')
resultados = response.json()

# Subir nuevo documento
files = {'file': open('documento.pdf', 'rb')}
data = {
    'document_type': 'sentencia',
    'extract_entities': True,
    'analyze_arguments': True
}
response = requests.post('http://localhost:8000/upload', files=files, data=data)
```

## 🐳 Docker

### Estructura de Contenedores

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./sentencias:/app/sentencias
      - ./uploads:/app/uploads
      - ./models:/app/models
      - ./logs:/app/logs
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app
```

### Comandos Docker Útiles

```bash
# Construir imagen
docker build -t analizador-sentencias .

# Ejecutar contenedor
docker run -p 8000:8000 -v $(pwd)/sentencias:/app/sentencias analizador-sentencias

# Ver logs
docker-compose logs -f app

# Reiniciar servicios
docker-compose restart
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Directorios de la aplicación
SENTENCIAS_DIR=./sentencias
UPLOADS_DIR=./uploads
MODELS_DIR=./models
LOGS_DIR=./logs

# Configuración de la aplicación
MAX_FILE_SIZE=52428800  # 50MB
ALLOWED_EXTENSIONS=.txt,.pdf,.doc,.docx
LOG_LEVEL=INFO
```

### Configuración de Logging

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

## 📈 Monitoreo y Métricas

### Endpoint de Salud (`/health`)

```json
{
  "status": "ok",
  "version": "2.0.0",
  "timestamp": "2024-01-15T10:30:00",
  "ia_disponible": true,
  "directorios": {
    "sentencias": "./sentencias",
    "uploads": "./uploads",
    "models": "./models"
  }
}
```

### Métricas Disponibles
- Estado del sistema
- Disponibilidad de IA
- Espacio en disco
- Archivos procesados
- Tiempo de respuesta

## 🚨 Solución de Problemas

### Problemas Comunes

#### 1. Botones "Ver Detalles" No Funcionan
- **Síntoma**: Los botones no responden al clic
- **Solución**: Verificar que JavaScript esté habilitado y revisar la consola del navegador
- **Prevención**: Usar event delegation implementado

#### 2. Errores de Parsing JSON
- **Síntoma**: "Error parsing data" en consola
- **Solución**: Verificar formato de datos en el backend
- **Prevención**: Validación robusta de datos

#### 3. Archivos No Se Analizan
- **Síntoma**: Archivos no aparecen en el dashboard
- **Solución**: Verificar permisos de carpeta y formato de archivo
- **Prevención**: Validación de archivos al inicio

### Logs y Debugging

```bash
# Ver logs de la aplicación
tail -f logs/app.log

# Ver logs de Docker
docker-compose logs -f app

# Verificar estado del sistema
curl http://localhost:8000/health
```

## 🤝 Contribución

### Cómo Contribuir

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Estándares de Código

- **Python**: PEP 8
- **JavaScript**: ESLint con configuración estándar
- **HTML**: HTML5 válido
- **CSS**: Bootstrap 5 con personalizaciones mínimas

### Estructura de Commits

```
feat: agregar nueva categoría de análisis
fix: corregir error en parsing de PDF
docs: actualizar documentación de API
style: mejorar diseño del dashboard
refactor: optimizar algoritmo de búsqueda
test: agregar tests para análisis de frases
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Autores

- **Tu Nombre** - *Desarrollo inicial* - [tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- **FastAPI** por el framework web excepcional
- **Bootstrap** por el sistema de diseño responsive
- **Comunidad Python** por las librerías de análisis de texto
- **Sector Legal** por la validación de casos de uso

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/analizador-sentencias-ipp/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/tu-usuario/analizador-sentencias-ipp/discussions)
- **Email**: tu-email@ejemplo.com

---

⭐ **Si este proyecto te es útil, por favor dale una estrella en GitHub!**
