#!/usr/bin/env python3
"""Script de prueba para verificar el despliegue"""

import os
import sys
from pathlib import Path

print("🔍 Verificando entorno de despliegue...")
print(f"📁 Directorio actual: {os.getcwd()}")
print(f"🐍 Python version: {sys.version}")

print("\n📂 Verificando estructura de directorios...")
directories = ['models', 'sentencias', 'uploads', 'backend', 'templates']
for dir_name in directories:
    if Path(dir_name).exists():
        files = list(Path(dir_name).iterdir())
        print(f"✅ {dir_name}/ - {len(files)} archivos")
        if dir_name == 'models':
            pkl_files = [f for f in files if f.suffix == '.pkl']
            print(f"   📄 Archivos .pkl: {[f.name for f in pkl_files]}")
    else:
        print(f"❌ {dir_name}/ - NO EXISTE")

print("\n🧪 Probando importaciones críticas...")
try:
    import fastapi
    print(f"✅ FastAPI: {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI: {e}")

try:
    import sklearn
    print(f"✅ scikit-learn: {sklearn.__version__}")
except ImportError as e:
    print(f"❌ scikit-learn: {e}")

try:
    import torch
    print(f"✅ PyTorch: {torch.__version__}")
except ImportError as e:
    print(f"❌ PyTorch: {e}")

try:
    import sentence_transformers
    print(f"✅ sentence-transformers: {sentence_transformers.__version__}")
except ImportError as e:
    print(f"❌ sentence-transformers: {e}")

print("\n🤖 Probando carga del modelo...")
try:
    from backend.analisis import AnalizadorLegal
    print("✅ AnalizadorLegal importado")
    
    analizador = AnalizadorLegal()
    print("✅ AnalizadorLegal creado")
    
    # Verificar si el modelo está cargado
    if hasattr(analizador, 'modelo') and analizador.modelo is not None:
        print("✅ Modelo de IA cargado correctamente")
    else:
        print("❌ Modelo de IA NO cargado")
        
except Exception as e:
    print(f"❌ Error con AnalizadorLegal: {e}")
    import traceback
    traceback.print_exc()

print("\n📊 Verificando archivos de sentencias...")
sentencias_dir = Path("sentencias")
if sentencias_dir.exists():
    archivos = list(sentencias_dir.glob("*.pdf"))
    print(f"📄 Archivos PDF encontrados: {len(archivos)}")
    for archivo in archivos[:3]:  # Mostrar solo los primeros 3
        print(f"   - {archivo.name}")
else:
    print("❌ Directorio sentencias no existe")

print("\n✅ Verificación completada")
