#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para debuggear el análisis de discrepancias
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.analisis_discrepancias import AnalizadorDiscrepancias

def test_discrepancy_analysis():
    """Test del análisis de discrepancias con diferentes textos"""
    
    analizador = AnalizadorDiscrepancias()
    
    # Texto 1 - Documento con supraespinoso
    texto1 = """
    INFORME MÉDICO
    Paciente presenta rotura completa del supraespinoso con retracción fibrilar de 15mm.
    Limitación activa de flexión a 90 grados. Fuerza insuficiente para vencer la gravedad.
    Se recomienda cirugía reconstructiva con anclajes.
    """
    
    # Texto 2 - Documento diferente
    texto2 = """
    INFORME MÉDICO DIFERENTE
    Paciente presenta lesión de rodilla con limitación de movilidad.
    No se observan lesiones del supraespinoso. Movilidad normal del hombro.
    Se recomienda tratamiento conservador.
    """
    
    print("=== TEST ANÁLISIS DE DISCREPANCIAS ===\n")
    
    # Analizar documento 1
    print("📄 ANALIZANDO DOCUMENTO 1:")
    resultado1 = analizador.analizar_discrepancias(texto1, "informe_medico_1.pdf")
    print(f"Discrepancias: {len(resultado1.get('discrepancias_detectadas', []))}")
    print(f"Evidencia: {len(resultado1.get('evidencia_favorable', []))}")
    print(f"Puntuación: {resultado1.get('puntuacion_discrepancia', 0)}")
    print(f"Probabilidad IPP: {resultado1.get('probabilidad_ipp', 0):.1%}")
    print(f"Resumen: {resultado1.get('resumen_ejecutivo', '')[:100]}...")
    print()
    
    # Analizar documento 2
    print("📄 ANALIZANDO DOCUMENTO 2:")
    resultado2 = analizador.analizar_discrepancias(texto2, "informe_medico_2.pdf")
    print(f"Discrepancias: {len(resultado2.get('discrepancias_detectadas', []))}")
    print(f"Evidencia: {len(resultado2.get('evidencia_favorable', []))}")
    print(f"Puntuación: {resultado2.get('puntuacion_discrepancia', 0)}")
    print(f"Probabilidad IPP: {resultado2.get('probabilidad_ipp', 0):.1%}")
    print(f"Resumen: {resultado2.get('resumen_ejecutivo', '')[:100]}...")
    print()
    
    # Comparar resultados
    print("🔍 COMPARACIÓN:")
    print(f"¿Mismos resultados? {resultado1 == resultado2}")
    print(f"¿Misma puntuación? {resultado1.get('puntuacion_discrepancia') == resultado2.get('puntuacion_discrepancia')}")
    print(f"¿Misma probabilidad? {resultado1.get('probabilidad_ipp') == resultado2.get('probabilidad_ipp')}")
    
    # Mostrar detalles de evidencia
    print("\n📊 EVIDENCIA DOCUMENTO 1:")
    for ev in resultado1.get('evidencia_favorable', []):
        print(f"  - {ev.get('descripcion', '')}")
    
    print("\n📊 EVIDENCIA DOCUMENTO 2:")
    for ev in resultado2.get('evidencia_favorable', []):
        print(f"  - {ev.get('descripcion', '')}")

if __name__ == "__main__":
    test_discrepancy_analysis()
