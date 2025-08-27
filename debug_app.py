#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug para la aplicación
"""

import os
from pathlib import Path

def debug_app():
    """Debug de la aplicación"""
    
    print("🔍 DEBUG DE LA APLICACIÓN")
    print("=" * 50)
    
    # 1. Verificar directorios
    base_dir = Path(__file__).parent
    sentencias_dir = base_dir / "sentencias"
    
    print(f"📁 Directorio base: {base_dir}")
    print(f"📁 Directorio sentencias: {sentencias_dir}")
    print(f"📁 ¿Existe sentencias?: {sentencias_dir.exists()}")
    
    if sentencias_dir.exists():
        archivos = list(sentencias_dir.iterdir())
        print(f"📄 Total archivos en sentencias: {len(archivos)}")
        
        for archivo in archivos:
            print(f"   - {archivo.name} ({archivo.suffix})")
    
    print("=" * 50)
    
    # 2. Verificar módulos
    print("🔧 Verificando módulos...")
    
    try:
        from backend.analisis import AnalizadorLegal
        print("✅ AnalizadorLegal importado correctamente")
        
        analizador = AnalizadorLegal()
        print("✅ Instancia creada correctamente")
        
    except Exception as e:
        print(f"❌ Error importando AnalizadorLegal: {e}")
    
    print("=" * 50)
    
    # 3. Probar análisis directo
    if sentencias_dir.exists():
        archivos_pdf = [f for f in sentencias_dir.iterdir() if f.suffix.lower() == '.pdf']
        
        if archivos_pdf:
            print("🧪 Probando análisis directo...")
            
            try:
                from backend.analisis import AnalizadorLegal
                analizador = AnalizadorLegal()
                
                for pdf_file in archivos_pdf:
                    print(f"\n📖 Analizando: {pdf_file.name}")
                    
                    try:
                        resultado = analizador.analizar_documento(str(pdf_file))
                        
                        if resultado.get("procesado"):
                            print(f"   ✅ Procesado: {resultado.get('longitud_texto', 0)} caracteres")
                            print(f"   🎯 Frases clave: {resultado.get('total_frases_clave', 0)}")
                        else:
                            print(f"   ❌ No procesado: {resultado.get('error', 'Desconocido')}")
                            
                    except Exception as e:
                        print(f"   ❌ Error en análisis: {e}")
                        
            except Exception as e:
                print(f"❌ Error creando analizador: {e}")
    
    print("=" * 50)
    
    # 4. Verificar la función de la app
    print("🌐 Verificando función de la app...")
    
    try:
        # Simular la función de la app
        if sentencias_dir.exists():
            archivos_soportados = [f for f in sentencias_dir.iterdir() 
                                  if f.suffix.lower() in ['.txt', '.pdf']]
            
            print(f"📊 Archivos soportados encontrados: {len(archivos_soportados)}")
            
            for archivo in archivos_soportados:
                print(f"   - {archivo.name}")
                
    except Exception as e:
        print(f"❌ Error verificando archivos: {e}")

if __name__ == "__main__":
    debug_app()


