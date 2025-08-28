# Script de inicio usando pipenv para el proyecto de análisis de sentencias
# Ejecutar con: .\start_pipenv.ps1

Write-Host "🚀 Iniciando proyecto de análisis de sentencias con pipenv..." -ForegroundColor Green
Write-Host "📁 Directorio actual: $(Get-Location)" -ForegroundColor Cyan
Write-Host "🐍 Usando entorno virtual de pipenv" -ForegroundColor Yellow

# Verificar que pipenv esté instalado
try {
    $pipenvVersion = pipenv --version
    Write-Host "✅ Pipenv encontrado: $pipenvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: pipenv no está instalado" -ForegroundColor Red
    Write-Host "💡 Instala pipenv con: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

# Verificar que estemos en el directorio correcto
if (-not (Test-Path "Pipfile")) {
    Write-Host "❌ Error: No se encontró el archivo Pipfile" -ForegroundColor Red
    Write-Host "💡 Asegúrate de estar en el directorio del proyecto" -ForegroundColor Yellow
    exit 1
}

# Verificar que el entorno virtual exista
if (-not (Test-Path ".venv")) {
    Write-Host "⚠️  Entorno virtual no encontrado, creando uno nuevo..." -ForegroundColor Yellow
    pipenv --python 3.11
}

Write-Host "🔧 Verificando dependencias..." -ForegroundColor Cyan

# Verificar que las dependencias principales estén disponibles
try {
    pipenv run python -c "import fastapi, uvicorn, jinja2; print('✅ Dependencias principales verificadas')"
    Write-Host "✅ Todas las dependencias están disponibles" -ForegroundColor Green
} catch {
    Write-Host "❌ Error al verificar dependencias" -ForegroundColor Red
    Write-Host "💡 Ejecuta: pipenv run pip install -r requirements_current.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "🚀 Iniciando aplicación..." -ForegroundColor Green
Write-Host "🌐 La aplicación estará disponible en: http://localhost:8000" -ForegroundColor Cyan
Write-Host "⏹️  Presiona Ctrl+C para detener" -ForegroundColor Yellow

# Ejecutar la aplicación con pipenv
try {
    pipenv run python app.py
} catch {
    Write-Host "❌ Error al ejecutar la aplicación" -ForegroundColor Red
    Write-Host "💡 Verifica que app.py exista y esté configurado correctamente" -ForegroundColor Yellow
    exit 1
}
