#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test directo de la función web
"""

import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def test_web_function():
    """Test directo de la función web"""
    
    print("🧪 TEST DIRECTO DE LA FUNCIÓN WEB")
    print("=" * 50)
    
    try:
        # Importar la función directamente
        from app import analizar_sentencias_existentes
        
        print("✅ Función importada correctamente")
        
        # Ejecutar la función
        print("\n🚀 Ejecutando analizar_sentencias_existentes()...")
        resultado = analizar_sentencias_existentes()
        
        print("\n📊 RESULTADO:")
        print(f"   Archivos analizados: {resultado.get('archivos_analizados', 0)}")
        print(f"   Total apariciones: {resultado.get('total_apariciones', 0)}")
        
        if resultado.get('resultados_por_archivo'):
            print(f"\n📄 ARCHIVOS PROCESADOS:")
            for nombre, datos in resultado['resultados_por_archivo'].items():
                if isinstance(datos, dict) and datos.get('procesado'):
                    print(f"   ✅ {nombre}: {datos.get('longitud_texto', 0)} chars, {datos.get('total_frases_clave', 0)} frases")
                else:
                    print(f"   ❌ {nombre}: {datos.get('error', 'Error desconocido')}")
        
        if resultado.get('ranking_global'):
            print(f"\n🏆 RANKING GLOBAL:")
            for categoria, datos in resultado['ranking_global'].items():
                print(f"   {categoria}: {datos['total']} apariciones")
        
        return resultado
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_web_function()

