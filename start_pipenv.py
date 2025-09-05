#!/usr/bin/env python3
"""
Script de inicio usando pipenv para el proyecto de análisis de sentencias.
"""

import subprocess
import sys
import os

def run_with_pipenv():
    """Ejecuta la aplicación usando pipenv"""
    try:
        # Verificar que estamos en el directorio correcto
        if not os.path.exists('Pipfile'):
            print("Error: No se encontró el archivo Pipfile. Asegúrate de estar en el directorio del proyecto.")
            sys.exit(1)
        
        print("🚀 Iniciando aplicación con pipenv...")
        print("📁 Directorio actual:", os.getcwd())
        print("🐍 Usando entorno virtual de pipenv")
        
        # Ejecutar la aplicación con pipenv
        result = subprocess.run([
            'pipenv', 'run', 'python', 'app.py'
        ], capture_output=False, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error al ejecutar la aplicación: {result.returncode}")
            sys.exit(result.returncode)
            
    except FileNotFoundError:
        print("❌ Error: pipenv no está instalado o no está en el PATH")
        print("💡 Instala pipenv con: pip install pipenv")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_with_pipenv()
