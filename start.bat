@echo off
echo ========================================
echo   ANALIZADOR DE RESOLUCIONES IPP/INSS
echo ========================================
echo.
echo Iniciando servidor...
echo.
echo URL: http://localhost:8000
echo API: http://localhost:8000/api/analizar
echo Estado: http://localhost:8000/health
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
pause
