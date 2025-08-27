#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicio para desarrollo local
Analizador de Sentencias IPP/INSS
"""

import os
import sys
import subprocess
from pathlib import Path

def crear_directorios():
    """Crea los directorios necesarios"""
    directorios = [
        "sentencias",
        "uploads", 
        "models",
        "logs",
        "static",
        "templates"
    ]
    
    for directorio in directorios:
        Path(directorio).mkdir(exist_ok=True)
        print(f"✅ Directorio {directorio} creado/verificado")

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencias principales verificadas")
        return True
    except ImportError as e:
        print(f"❌ Dependencias faltantes: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def verificar_archivos():
    """Verifica que los archivos principales existan"""
    archivos_requeridos = [
        "app.py",
        "config.py",
        "templates/index.html",
        "static/style.css"
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if not Path(archivo).exists():
            faltantes.append(archivo)
    
    if faltantes:
        print(f"❌ Archivos faltantes: {', '.join(faltantes)}")
        return False
    
    print("✅ Archivos principales verificados")
    return True

def iniciar_aplicacion():
    """Inicia la aplicación FastAPI"""
    try:
        print("🚀 Iniciando Analizador de Sentencias IPP/INSS...")
        
        # Importar y ejecutar la aplicación
        from app import app
        import uvicorn
        
        print("📁 Directorios:")
        print(f"   - Sentencias: {Path('sentencias').absolute()}")
        print(f"   - Uploads: {Path('uploads').absolute()}")
        print(f"   - Models: {Path('models').absolute()}")
        
        print("\n🌐 URLs disponibles:")
        print(f"   - Aplicación: http://localhost:8000")
        print(f"   - API Docs: http://localhost:8000/docs")
        print(f"   - Health Check: http://localhost:8000/health")
        
        print("\n⏹️  Para detener: Ctrl+C")
        print("=" * 50)
        
        # Iniciar servidor
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=True
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")
        print("💡 Verifica que todas las dependencias estén instaladas")

def main():
    """Función principal"""
    print("🔍 Verificando entorno de desarrollo...")
    
    # Verificar directorios
    crear_directorios()
    
    # Verificar dependencias
    if not verificar_dependencias():
        sys.exit(1)
    
    # Verificar archivos
    if not verificar_archivos():
        sys.exit(1)
    
    print("\n✅ Entorno verificado correctamente")
    
    # Preguntar si iniciar
    respuesta = input("\n¿Deseas iniciar la aplicación? (s/n): ").lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        iniciar_aplicacion()
    else:
        print("👋 Hasta luego!")

if __name__ == "__main__":
    main()
