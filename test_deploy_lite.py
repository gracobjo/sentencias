#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico ligero para verificar dependencias básicas en producción
"""

import sys
import os
from pathlib import Path

def test_basic_imports():
    """Prueba las importaciones básicas"""
    print("🔍 Probando importaciones básicas...")
    
    # Test NumPy
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} - OK")
    except Exception as e:
        print(f"❌ NumPy - Error: {e}")
        return False
    
    # Test scikit-learn
    try:
        import sklearn
        print(f"✅ scikit-learn {sklearn.__version__} - OK")
    except Exception as e:
        print(f"❌ scikit-learn - Error: {e}")
        return False
    
    # Test PyPDF2
    try:
        import PyPDF2
        print("✅ PyPDF2 - OK")
    except Exception as e:
        print(f"❌ PyPDF2 - Error: {e}")
        return False
    
    # Test NLTK
    try:
        import nltk
        print(f"✅ NLTK {nltk.__version__} - OK")
    except Exception as e:
        print(f"❌ NLTK - Error: {e}")
        return False
    
    return True

def test_model_files():
    """Verifica que los archivos del modelo estén presentes"""
    print("\n🔍 Verificando archivos del modelo...")
    
    model_files = [
        "models/modelo_legal.pkl",
        "models/modelo_legal_sbert.pkl", 
        "models/frases_clave.json",
        "models/labels.json"
    ]
    
    all_present = True
    for file_path in model_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - No encontrado")
            all_present = False
    
    return all_present

def test_model_loading():
    """Prueba la carga del modelo TF-IDF"""
    print("\n🔍 Probando carga del modelo TF-IDF...")
    
    try:
        from backend.analisis import AnalizadorLegal
        analizador = AnalizadorLegal()
        
        if analizador.modelo is not None:
            print("✅ Modelo TF-IDF cargado correctamente")
        else:
            print("⚠️ Modelo TF-IDF no cargado - usando reglas")
        
        # No probar SBERT para evitar problemas de memoria
        print("✅ Saltando prueba de SBERT para evitar problemas de memoria")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🚀 Iniciando diagnóstico ligero de dependencias...")
    print(f"Python: {sys.version}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Verificar archivos
    files_ok = test_model_files()
    
    # Verificar importaciones básicas
    imports_ok = test_basic_imports()
    
    # Verificar carga del modelo TF-IDF
    model_ok = test_model_loading()
    
    print(f"\n📊 Resumen del diagnóstico ligero:")
    print(f"- Archivos del modelo: {'✅' if files_ok else '❌'}")
    print(f"- Importaciones básicas: {'✅' if imports_ok else '❌'}")
    print(f"- Carga del modelo TF-IDF: {'✅' if model_ok else '❌'}")
    
    if files_ok and imports_ok:
        print("\n🎉 Diagnóstico completado - Sistema básico listo")
        return 0
    else:
        print("\n⚠️ Diagnóstico completado - Hay problemas que resolver")
        return 1

if __name__ == "__main__":
    sys.exit(main())
