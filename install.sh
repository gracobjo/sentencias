#!/bin/bash

echo "========================================"
echo "    INSTALACION RAPIDA - IPP/INSS"
echo "========================================"
echo

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar Python
echo "🔍 Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    print_status "Python 3 encontrado"
    python3 --version
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    print_status "Python encontrado"
    python --version
else
    print_error "Python no está instalado"
    echo "💡 Instala Python desde: https://python.org"
    exit 1
fi

# Verificar pip
echo
echo "🔍 Verificando pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    print_status "pip3 encontrado"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    print_status "pip encontrado"
else
    print_error "pip no está disponible"
    echo "💡 Instala pip: sudo apt install python3-pip (Ubuntu/Debian)"
    exit 1
fi

# Crear entorno virtual
echo
echo "🔧 Creando entorno virtual..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    print_status "Entorno virtual creado"
else
    print_status "Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate
print_status "Entorno virtual activado"

# Actualizar pip
echo "📦 Actualizando pip..."
$PIP_CMD install --upgrade pip

# Instalar dependencias
echo
echo "📦 Instalando dependencias..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "Dependencias instaladas"
else
    print_error "Error instalando dependencias"
    echo "💡 Verifica que tienes permisos de administrador"
    exit 1
fi

# Crear directorios
echo
echo "🔧 Creando directorios..."
$PYTHON_CMD config.py

# Verificar instalación
echo
echo "🧪 Verificando instalación..."
$PYTHON_CMD test_app.py

if [ $? -eq 0 ]; then
    echo
    print_status "¡Instalación completada exitosamente!"
    echo
    echo "🚀 Para iniciar la aplicación:"
    echo "   source venv/bin/activate"
    echo "   python app.py"
    echo "   o"
    echo "   python start_local.py"
    echo
    echo "📚 Documentación: README.md"
    echo "🌐 URL: http://localhost:8000"
    echo
else
    echo
    print_warning "Algunas verificaciones fallaron"
    echo "💡 Revisa los errores antes de continuar"
    exit 1
fi

# Dar permisos de ejecución a los scripts
chmod +x start_local.py
chmod +x test_app.py

echo
echo "🔧 Scripts de inicio configurados con permisos de ejecución"
echo "💡 Puedes ejecutar: ./start_local.py o ./test_app.py"


