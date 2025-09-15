#!/usr/bin/env python3
"""
Script de diagnóstico ligero para despliegue en Render
Verifica que las dependencias básicas estén disponibles
"""

import sys
import os

def test_imports():
    """Prueba imports básicos"""
    print("🔍 Probando imports básicos...")
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn: {e}")
        return False
    
    try:
        import numpy
        print(f"✅ NumPy {numpy.__version__}")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False
    
    try:
        import sklearn
        print(f"✅ Scikit-learn {sklearn.__version__}")
    except ImportError as e:
        print(f"❌ Scikit-learn: {e}")
        return False
    
    try:
        import PyPDF2
        print(f"✅ PyPDF2 {PyPDF2.__version__}")
    except ImportError as e:
        print(f"❌ PyPDF2: {e}")
        return False
    
    try:
        import docx
        print("✅ python-docx")
    except ImportError as e:
        print(f"❌ python-docx: {e}")
        return False
    
    return True

def test_directories():
    """Verifica que los directorios necesarios existan"""
    print("\n📁 Verificando directorios...")
    
    dirs = ['models', 'sentencias', 'uploads', 'logs']
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ existe")
        else:
            print(f"❌ {dir_name}/ no existe")
            return False
    
    return True

def test_model_files():
    """Verifica que los archivos del modelo estén presentes"""
    print("\n🤖 Verificando archivos del modelo...")
    
    model_files = [
        'models/modelo_legal.pkl',
        'models/modelo_legal_sbert.pkl',
        'models/frases_clave.json',
        'models/labels.json'
    ]
    
    for file_path in model_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} no encontrado")
            return False
    
    return True

def test_app_structure():
    """Verifica la estructura de la aplicación"""
    print("\n🏗️ Verificando estructura de la aplicación...")
    
    # Verificar que los archivos principales existan
    app_files = [
        'src/app-deploy.py',
        'src/config.py',
        'src/backend/analisis.py',
        'src/backend/analisis_discrepancias.py',
        'src/backend/analisis_predictivo.py'
    ]
    
    for file_path in app_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} no encontrado")
            return False
    
    return True

def main():
    """Función principal de diagnóstico"""
    print("🚀 Iniciando diagnóstico de despliegue ligero...")
    print(f"Python {sys.version}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Ejecutar todas las pruebas
    tests = [
        test_imports,
        test_directories,
        test_model_files,
        test_app_structure
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ¡Todas las pruebas pasaron! El despliegue debería funcionar.")
        return 0
    else:
        print("❌ Algunas pruebas fallaron. Revisar configuración.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
