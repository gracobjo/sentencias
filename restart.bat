@echo off
echo ========================================
echo    REINICIANDO ANALIZADOR IPP/INSS
echo ========================================
echo.

echo Deteniendo procesos existentes...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo.
echo Esperando 3 segundos...
timeout /t 3 /nobreak >nul

echo.
echo Iniciando backend...
start "Backend FastAPI" cmd /k "python app.py"

echo.
echo Backend iniciado en http://localhost:8000
echo.
echo Presiona cualquier tecla para abrir en el navegador...
pause >nul

start http://localhost:8000

echo.
echo ========================================
echo    APLICACION REINICIADA EXITOSAMENTE
echo ========================================
pause


