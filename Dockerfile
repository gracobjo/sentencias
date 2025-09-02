# Dockerfile para el Analizador de Sentencias IPP/INSS
# Aplicación FastAPI robusta para análisis de documentos legales

# =============================================================================
# Stage 1: Build dependencies
# =============================================================================
FROM python:3.11-slim as builder

# Instalar dependencias del sistema para compilación
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmagic-dev \
    libsnappy-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /build

# Copiar archivos de dependencias
COPY requirements.DOCKER.txt .

# Instalar dependencias de Python en un directorio temporal
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.DOCKER.txt

# =============================================================================
# Stage 2: Runtime
# =============================================================================
FROM python:3.11-slim as runtime

# Metadatos de la imagen
LABEL maintainer="Equipo de Desarrollo IPP/INSS"
LABEL description="Analizador de Sentencias IPP/INSS - FastAPI"
LABEL version="2.0.0"

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    ENVIRONMENT=production \
    PATH="/root/.local/bin:$PATH"

# Instalar dependencias del sistema de runtime
RUN apt-get update && apt-get install -y \
    libmagic1 \
    libsnappy1v5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias instaladas desde el stage de build
COPY --from=builder /root/.local /root/.local

# Copiar código de la aplicación
COPY sentencias_app/ ./sentencias_app/
COPY templates/ ./templates/
COPY static/ ./static/
COPY models/ ./models/
COPY app.py ./

# Crear directorios necesarios con permisos correctos
RUN mkdir -p sentencias uploads logs && \
    chown -R appuser:appuser /app

# Cambiar al usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check mejorado
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio optimizado
CMD ["uvicorn", "sentencias_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]