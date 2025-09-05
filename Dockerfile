# Dockerfile para el Analizador de Sentencias IPP/INSS
# Aplicación FastAPI robusta para análisis de documentos legales

# Usar imagen base de Python oficial
FROM python:3.13-slim

# Metadatos de la imagen
LABEL maintainer="Equipo de Desarrollo IPP/INSS"
LABEL description="Analizador de Sentencias IPP/INSS - FastAPI"
LABEL version="2.0.0"

# Configurar variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmagic1 \
    libsnappy1v5 \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p sentencias uploads models logs static templates

# Cambiar permisos de directorios
RUN chown -R appuser:appuser /app

# Cambiar al usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
