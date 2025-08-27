# Script de inicio para el Analizador de Resoluciones IPP/INSS
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ANALIZADOR DE RESOLUCIONES IPP/INSS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Iniciando servidor..." -ForegroundColor Green
Write-Host ""
Write-Host "URL: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API: http://localhost:8000/api/analizar" -ForegroundColor Yellow
Write-Host "Estado: http://localhost:8000/health" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Red
Write-Host ""

try {
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
}
catch {
    Write-Host "Error al iniciar el servidor: $_" -ForegroundColor Red
    Write-Host "Asegúrate de tener instaladas las dependencias con: pip install -r requirements.txt" -ForegroundColor Yellow
}

Read-Host "Presiona Enter para continuar"
