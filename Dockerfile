# Dockerfile para despliegue en Render
FROM python:3.13-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias ligeras
COPY requirements-deploy-lite.txt .

# Instalar dependencias de Python con manejo de errores
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir numpy==1.26.4 && \
    pip install --no-cache-dir -r requirements-deploy-lite.txt

# Sin modelos de spaCy para reducir memoria
# RUN python -m spacy download en_core_web_sm --no-cache-dir || echo "Error descargando en_core_web_sm"
# RUN python -m spacy download es_core_news_sm --no-cache-dir || echo "Error descargando es_core_news_sm"

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p sentencias uploads logs

# Verificar que los archivos del modelo estén presentes
RUN ls -la models/ || echo "Directorio models no encontrado"
RUN ls -la models/*.pkl || echo "Archivos .pkl no encontrados"

# Verificar instalación de NumPy
RUN python -c "import numpy; print(f'NumPy version: {numpy.__version__}')" || echo "Error importando NumPy"

# Ejecutar script de diagnóstico ligero
RUN python test_deploy_lite.py || echo "Script de diagnóstico falló"

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "src.app-deploy:app", "--host", "0.0.0.0", "--port", "8000"]
