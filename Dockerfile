# Dockerfile para despliegue en Render
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements-deploy.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-deploy.txt

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p sentencias uploads logs

# Verificar que los archivos del modelo estén presentes
RUN ls -la models/ || echo "Directorio models no encontrado"
RUN ls -la models/*.pkl || echo "Archivos .pkl no encontrados"

# Ejecutar script de diagnóstico
RUN python test_deploy.py || echo "Script de diagnóstico falló"

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app-deploy:app", "--host", "0.0.0.0", "--port", "8000"]