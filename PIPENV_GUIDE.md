# Guía de Uso de Pipenv en el Proyecto de Análisis de Sentencias

## ¿Qué es Pipenv?

Pipenv es una herramienta que combina pip y virtualenv para gestionar entornos virtuales y dependencias de Python de manera más eficiente. Proporciona un archivo `Pipfile` para especificar dependencias y un archivo `Pipfile.lock` para versiones exactas.

## Estado Actual del Proyecto

✅ **Pipenv está configurado y funcionando**
✅ **Entorno virtual creado**
✅ **Dependencias principales instaladas**
✅ **Aplicación funcionando con pipenv**

## Comandos Básicos de Pipenv

### 1. Activar el Entorno Virtual
```bash
pipenv shell
```
Esto activa el entorno virtual y te coloca dentro de él.

### 2. Ejecutar Comandos en el Entorno Virtual
```bash
pipenv run python app.py
pipenv run python -c "import fastapi; print('Funciona!')"
pipenv run pytest
```

### 3. Instalar Dependencias
```bash
# Instalar una nueva dependencia
pipenv install nombre_paquete

# Instalar dependencia de desarrollo
pipenv install --dev nombre_paquete

# Instalar desde requirements.txt
pipenv install -r requirements.txt
```

### 4. Ver Dependencias Instaladas
```bash
pipenv run pip list
pipenv graph
```

### 5. Salir del Entorno Virtual
```bash
exit
```
O presiona `Ctrl+D`

## Dependencias Actuales del Proyecto

### Dependencias Principales
- **FastAPI**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI para FastAPI
- **Jinja2**: Motor de plantillas
- **Aiofiles**: Operaciones de archivo asíncronas
- **Python-multipart**: Manejo de formularios multipart
- **Python-docx**: Lectura/escritura de archivos Word
- **PyPDF2**: Procesamiento de archivos PDF
- **Scikit-learn**: Machine learning
- **NumPy & Pandas**: Análisis de datos
- **NLTK & SpaCy**: Procesamiento de lenguaje natural
- **SQLAlchemy**: ORM para bases de datos
- **Redis**: Base de datos en memoria
- **Prometheus**: Monitoreo y métricas

### Herramientas de Desarrollo
- **Pytest**: Framework de testing
- **Black**: Formateador de código
- **Flake8**: Linter de código
- **MyPy**: Verificación de tipos estáticos

## Scripts de Inicio

### Script Principal con Pipenv
```bash
python start_pipenv.py
```

### Scripts de PowerShell (Windows)
```bash
.\start.ps1
```

### Scripts de Batch (Windows)
```bash
start.bat
```

## Estructura del Proyecto con Pipenv

```
sentencias/
├── Pipfile                 # Especificación de dependencias
├── Pipfile.lock           # Versiones exactas (generado automáticamente)
├── .venv/                 # Entorno virtual (creado por pipenv)
├── app.py                 # Aplicación principal
├── start_pipenv.py        # Script de inicio con pipenv
├── requirements.txt        # Dependencias en formato pip
└── ...                    # Otros archivos del proyecto
```

## Solución de Problemas

### Problema: Timeout al instalar dependencias
**Solución**: Usar `pipenv run pip install` directamente
```bash
pipenv run pip install nombre_paquete
```

### Problema: No se puede crear Pipfile.lock
**Solución**: Las dependencias ya están instaladas, usar directamente
```bash
pipenv run python app.py
```

### Problema: Entorno virtual no encontrado
**Solución**: Recrear el entorno
```bash
pipenv --rm
pipenv --python 3.11
pipenv run pip install -r requirements_current.txt
```

## Comandos Útiles para Desarrollo

### Ejecutar Tests
```bash
pipenv run pytest
pipenv run pytest -v
pipenv run pytest tests/ -v
```

### Formatear Código
```bash
pipenv run black .
pipenv run black --check .
```

### Verificar Tipos
```bash
pipenv run mypy .
```

### Linting
```bash
pipenv run flake8 .
```

### Ejecutar la Aplicación
```bash
pipenv run python app.py
pipenv run uvicorn app:app --reload
```

## Ventajas de Usar Pipenv

1. **Gestión Automática de Entornos Virtuales**: No necesitas crear/activar manualmente
2. **Dependencias Determinísticas**: El `Pipfile.lock` garantiza versiones exactas
3. **Separación de Dependencias**: Diferencia entre dependencias de producción y desarrollo
4. **Integración con pip**: Usa pip internamente para instalación
5. **Fácil Reproducción**: Otros desarrolladores pueden recrear el entorno exacto

## Próximos Pasos

1. **Usar pipenv para todas las operaciones de Python**
2. **Agregar nuevas dependencias con `pipenv install`**
3. **Mantener el Pipfile actualizado**
4. **Usar `pipenv run` para ejecutar comandos**
5. **Compartir el Pipfile con el equipo**

## Comandos de Referencia Rápida

```bash
# Activar entorno
pipenv shell

# Ejecutar aplicación
pipenv run python app.py

# Instalar dependencia
pipenv install nombre_paquete

# Ver dependencias
pipenv graph

# Salir entorno
exit

# Ejecutar tests
pipenv run pytest

# Formatear código
pipenv run black .
```

¡Tu proyecto ya está configurado con pipenv y funcionando correctamente! 🎉
