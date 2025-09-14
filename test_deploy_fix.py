#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar las dependencias de IA en producción
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Prueba las importaciones críticas"""
    print("🔍 Probando importaciones críticas...")
    
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
    
    # Test sentence-transformers
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ sentence-transformers - OK")
    except Exception as e:
        print(f"❌ sentence-transformers - Error: {e}")
        return False
    
    # Test huggingface_hub
    try:
        import huggingface_hub
        print(f"✅ huggingface_hub {huggingface_hub.__version__} - OK")
    except Exception as e:
        print(f"❌ huggingface_hub - Error: {e}")
        return False
    
    # Test spaCy
    try:
        import spacy
        print(f"✅ spaCy {spacy.__version__} - OK")
    except Exception as e:
        print(f"❌ spaCy - Error: {e}")
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
    """Prueba la carga del modelo"""
    print("\n🔍 Probando carga del modelo...")
    
    try:
        from backend.analisis import AnalizadorLegal
        analizador = AnalizadorLegal()
        
        if analizador.modelo is not None:
            print("✅ Modelo TF-IDF cargado correctamente")
        else:
            print("⚠️ Modelo TF-IDF no cargado - usando reglas")
        
        if analizador.sbert_encoder is not None:
            print("✅ Modelo SBERT cargado correctamente")
        else:
            print("⚠️ Modelo SBERT no cargado - usando reglas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🚀 Iniciando diagnóstico de dependencias de IA...")
    print(f"Python: {sys.version}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    # Verificar archivos
    files_ok = test_model_files()
    
    # Verificar importaciones
    imports_ok = test_imports()
    
    # Verificar carga del modelo
    model_ok = test_model_loading()
    
    print(f"\n📊 Resumen del diagnóstico:")
    print(f"- Archivos del modelo: {'✅' if files_ok else '❌'}")
    print(f"- Importaciones: {'✅' if imports_ok else '❌'}")
    print(f"- Carga del modelo: {'✅' if model_ok else '❌'}")
    
    if files_ok and imports_ok:
        print("\n🎉 Diagnóstico completado - Sistema listo")
        return 0
    else:
        print("\n⚠️ Diagnóstico completado - Hay problemas que resolver")
        return 1

if __name__ == "__main__":
    sys.exit(main())
