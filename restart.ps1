Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    REINICIANDO ANALIZADOR IPP/INSS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Deteniendo procesos existentes..." -ForegroundColor Yellow
Get-Process python* -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Esperando 3 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Iniciando backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python app.py" -WindowStyle Normal

Write-Host ""
Write-Host "Backend iniciado en http://localhost:8000" -ForegroundColor Green
Write-Host ""
Write-Host "Presiona cualquier tecla para abrir en el navegador..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:8000"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    APLICACION REINICIADA EXITOSAMENTE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Presiona Enter para continuar"


