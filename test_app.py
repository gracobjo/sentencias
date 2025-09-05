#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el Analizador de Sentencias IPP/INSS
Verifica que todos los componentes funcionen correctamente
"""

import os
import sys
import json
from pathlib import Path

def verificar_estructura():
    """Verifica la estructura de directorios y archivos"""
    print("🔍 Verificando estructura del proyecto...")
    
    archivos_requeridos = [
        "app.py",
        "config.py",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "README.md"
    ]
    
    directorios_requeridos = [
        "templates",
        "static",
        "backend",
        "sentencias",
        "models"
    ]
    
    # Verificar archivos
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTANTE")
            return False
    
    # Verificar directorios
    for directorio in directorios_requeridos:
        if Path(directorio).exists():
            print(f"✅ {directorio}/")
        else:
            print(f"❌ {directorio}/ - FALTANTE")
            return False
    
    return True

def verificar_dependencias():
    """Verifica que las dependencias principales estén disponibles"""
    print("\n🔍 Verificando dependencias...")
    
    dependencias = [
        "fastapi",
        "uvicorn",
        "jinja2",
        "python-multipart"
    ]
    
    todas_disponibles = True
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NO INSTALADA")
            todas_disponibles = False
    
    return todas_disponibles

def verificar_configuracion():
    """Verifica la configuración de la aplicación"""
    print("\n🔍 Verificando configuración...")
    
    try:
        from config import config
        print(f"✅ Configuración cargada: {config.APP_NAME} v{config.APP_VERSION}")
        print(f"✅ Puerto: {config.PORT}")
        print(f"✅ Entorno: {os.getenv('ENVIRONMENT', 'development')}")
        return True
    except Exception as e:
        print(f"❌ Error cargando configuración: {e}")
        return False

def verificar_analizador():
    """Verifica el módulo de análisis"""
    print("\n🔍 Verificando módulo de análisis...")
    
    try:
        from backend.analisis import AnalizadorLegal
        analizador = AnalizadorLegal()
        print("✅ Módulo de análisis cargado")
        
        # Verificar si hay modelo de IA
        if analizador.modelo:
            print("✅ Modelo de IA disponible")
        else:
            print("⚠️ Modelo de IA no disponible (usando fallback)")
        
        return True
    except Exception as e:
        print(f"❌ Error cargando módulo de análisis: {e}")
        return False

def verificar_templates():
    """Verifica que los templates HTML estén disponibles"""
    print("\n🔍 Verificando templates...")
    
    templates_requeridos = [
        "templates/index.html",
        "templates/subir.html",
        "templates/resultado.html"
    ]
    
    todos_disponibles = True
    for template in templates_requeridos:
        if Path(template).exists():
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - FALTANTE")
            todos_disponibles = False
    
    return todos_disponibles

def verificar_archivos_estaticos():
    """Verifica que los archivos estáticos estén disponibles"""
    print("\n🔍 Verificando archivos estáticos...")
    
    archivos_estaticos = [
        "static/style.css"
    ]
    
    todos_disponibles = True
    for archivo in archivos_estaticos:
        if Path(archivo).exists():
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTANTE")
            todos_disponibles = False
    
    return todos_disponibles

def verificar_documentos_ejemplo():
    """Verifica que haya documentos de ejemplo para probar"""
    print("\n🔍 Verificando documentos de ejemplo...")
    
    sentencias_dir = Path("sentencias")
    if sentencias_dir.exists():
        archivos = list(sentencias_dir.glob("*.txt"))
        if archivos:
            print(f"✅ {len(archivos)} documentos de ejemplo encontrados")
            for archivo in archivos[:3]:  # Mostrar solo los primeros 3
                print(f"   📄 {archivo.name}")
            return True
        else:
            print("⚠️ No hay documentos de ejemplo en sentencias/")
            return False
    else:
        print("❌ Directorio sentencias/ no existe")
        return False

def verificar_frases_clave():
    """Verifica la configuración de frases clave"""
    print("\n🔍 Verificando configuración de frases clave...")
    
    frases_path = Path("models/frases_clave.json")
    if frases_path.exists():
        try:
            with open(frases_path, 'r', encoding='utf-8') as f:
                frases = json.load(f)
            
            print(f"✅ {len(frases)} categorías de frases clave cargadas")
            for categoria in list(frases.keys())[:3]:  # Mostrar solo las primeras 3
                print(f"   🏷️ {categoria}: {len(frases[categoria])} frases")
            return True
        except Exception as e:
            print(f"❌ Error cargando frases clave: {e}")
            return False
    else:
        print("⚠️ Archivo de frases clave no encontrado")
        return False

def crear_directorios():
    """Crea los directorios necesarios si no existen"""
    print("\n🔧 Creando directorios necesarios...")
    
    directorios = [
        "uploads",
        "logs",
        "models"
    ]
    
    for directorio in directorios:
        Path(directorio).mkdir(exist_ok=True)
        print(f"✅ {directorio}/")

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN DEL ANALIZADOR DE SENTENCIAS IPP/INSS")
    print("=" * 60)
    
    # Verificaciones
    verificaciones = [
        ("Estructura del proyecto", verificar_estructura),
        ("Dependencias", verificar_dependencias),
        ("Configuración", verificar_configuracion),
        ("Módulo de análisis", verificar_analizador),
        ("Templates HTML", verificar_templates),
        ("Archivos estáticos", verificar_archivos_estaticos),
        ("Documentos de ejemplo", verificar_documentos_ejemplo),
        ("Frases clave", verificar_frases_clave)
    ]
    
    resultados = []
    for nombre, funcion in verificaciones:
        try:
            resultado = funcion()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ Error en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Crear directorios si es necesario
    crear_directorios()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    exitosos = 0
    total = len(resultados)
    
    for nombre, resultado in resultados:
        estado = "✅ EXITOSO" if resultado else "❌ FALLIDO"
        print(f"{nombre:<25} {estado}")
        if resultado:
            exitosos += 1
    
    print(f"\n🎯 Resultado: {exitosos}/{total} verificaciones exitosas")
    
    if exitosos == total:
        print("🎉 ¡Todas las verificaciones fueron exitosas!")
        print("🚀 La aplicación está lista para ejecutarse")
        print("\n💡 Para iniciar la aplicación:")
        print("   python app.py")
        print("   o")
        print("   python start_local.py")
        return True
    else:
        print("⚠️ Algunas verificaciones fallaron")
        print("🔧 Revisa los errores antes de ejecutar la aplicación")
        return False

if __name__ == "__main__":
    try:
        exito = main()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Verificación interrumpida por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
