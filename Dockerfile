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

# Crear directorio para sentencias si no existe
RUN mkdir -p sentencias

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "app-deploy:app", "--host", "0.0.0.0", "--port", "8000"]