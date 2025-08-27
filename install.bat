@echo off
echo ========================================
echo    INSTALACION RAPIDA - IPP/INSS
echo ========================================
echo.

echo 🔍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo 💡 Descarga Python desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

echo.
echo 🔍 Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip no está disponible
    echo 💡 Reinstala Python o actualiza pip
    pause
    exit /b 1
)

echo ✅ pip encontrado

echo.
echo 📦 Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error instalando dependencias
    echo 💡 Verifica que tienes permisos de administrador
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas

echo.
echo 🔧 Creando directorios...
python config.py

echo.
echo 🧪 Verificando instalación...
python test_app.py

if errorlevel 1 (
    echo.
    echo ⚠️ Algunas verificaciones fallaron
    echo 💡 Revisa los errores antes de continuar
    pause
    exit /b 1
)

echo.
echo 🎉 ¡Instalación completada exitosamente!
echo.
echo 🚀 Para iniciar la aplicación:
echo    python app.py
echo    o
echo    python start_local.py
echo.
echo 📚 Documentación: README.md
echo 🌐 URL: http://localhost:8000
echo.
pause


