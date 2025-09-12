#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para el análisis de discrepancias médicas-legales
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.analisis_discrepancias import AnalizadorDiscrepancias

def test_analisis_discrepancias():
    """Prueba el análisis de discrepancias con un texto de ejemplo"""
    
    # Texto de ejemplo basado en el caso real mencionado
    texto_ejemplo = """
    INFORME MÉDICO DE ALTA
    
    Paciente: María García López
    Fecha: 14.08.2023
    
    ANTECEDENTES:
    La paciente sufrió un accidente laboral el 15.07.2022 durante su jornada de trabajo como limpiadora.
    
    EVOLUCIÓN:
    - 27.01.2023: RMN confirma "Rotura de espesor completo del supraespinoso con retracción fibrilar 16 mm, tenopatía severa del bíceps, artropatía acromioclavicular severa".
    - 10.02.2023: Cirugía reconstructiva con reinserción del supraespinoso usando 3 tornillos corkscrew.
    - Marzo-abril 2023: Flexión activa solo 45-60°, abducción activa 30-45°, con dolor persistente.
    - Junio-julio 2023: Informe de biomecánica confirma fuerza insuficiente para vencer la gravedad ("balance muscular 2/5").
    - Septiembre 2023: Traumatología constata que, pese a movilidad pasiva casi completa, la activa sigue limitada a 90-110° por discinesia escapular y atrofia periescapular.
    
    INFORME DE BIOMECÁNICA (06.07.2023):
    "Prácticamente nulo desarrollo de fuerza con hombro derecho, insuficiente para vencer la gravedad".
    Fuerza de garra solo 11 kg (normal >20 kg).
    
    DURACIÓN DEL PROCESO:
    Desde julio 2022 hasta marzo 2024 con múltiples recaídas, cirugía y secuelas permanentes.
    
    ALTA MÉDICA:
    El paciente no presenta limitación importante que le impida actividades diarias y laborales.
    Se califica como Lesiones Permanentes No Incapacitantes (LPNI).
    
    Sin embargo, el mismo informe señala: limitación activa a 90-110°, discinesia escapular, atrofia muscular.
    """
    
    print("🔍 INICIANDO ANÁLISIS DE DISCREPANCIAS MÉDICAS-LEGALES")
    print("=" * 60)
    
    # Crear analizador
    analizador = AnalizadorDiscrepancias()
    
    # Realizar análisis
    resultado = analizador.analizar_discrepancias(texto_ejemplo)
    
    # Mostrar resultados
    print("\n📊 RESUMEN EJECUTIVO:")
    print("-" * 30)
    print(f"Discrepancias detectadas: {len(resultado['discrepancias_detectadas'])}")
    print(f"Evidencia favorable: {len(resultado['evidencia_favorable'])}")
    print(f"Puntuación discrepancia: {resultado['puntuacion_discrepancia']}/100")
    print(f"Probabilidad IPP: {resultado['probabilidad_ipp']:.1%}")
    
    print("\n🔴 DISCREPANCIAS DETECTADAS:")
    print("-" * 30)
    for i, disc in enumerate(resultado['discrepancias_detectadas'], 1):
        print(f"{i}. {disc['tipo'].replace('_', ' ').title()}")
        print(f"   Descripción: {disc['descripcion']}")
        print(f"   Severidad: {disc['severidad']}")
        print(f"   Argumento: {disc['argumento_juridico']}")
        print()
    
    print("\n🟢 EVIDENCIA FAVORABLE:")
    print("-" * 30)
    for i, ev in enumerate(resultado['evidencia_favorable'], 1):
        print(f"{i}. {ev['tipo'].replace('_', ' ').title()}")
        print(f"   Descripción: {ev['descripcion']}")
        print(f"   Relevancia: {ev['relevancia']}")
        print(f"   Argumento: {ev['argumento']}")
        print()
    
    print("\n🔵 ARGUMENTOS JURÍDICOS GENERADOS:")
    print("-" * 30)
    for i, arg in enumerate(resultado['argumentos_juridicos'], 1):
        print(f"{i}. {arg['titulo']}")
        print(f"   Contenido: {arg['contenido']}")
        print(f"   Fuerza: {arg['fuerza']}")
        print()
    
    print("\n🟡 RECOMENDACIONES DE DEFENSA:")
    print("-" * 30)
    for i, rec in enumerate(resultado['recomendaciones_defensa'], 1):
        print(f"{i}. {rec['titulo']}")
        print(f"   Contenido: {rec['contenido']}")
        print(f"   Prioridad: {rec['prioridad']}")
        if rec.get('acciones'):
            print("   Acciones:")
            for accion in rec['acciones']:
                print(f"     - {accion}")
        print()
    
    print("\n⚫ CONTRADICCIONES INTERNAS:")
    print("-" * 30)
    for i, cont in enumerate(resultado['contradicciones_internas'], 1):
        print(f"{i}. {cont['descripcion']}")
        print(f"   Texto: {cont['texto'][:100]}...")
        print(f"   Argumento: {cont['argumento']}")
        print()
    
    print("\n📋 RESUMEN EJECUTIVO COMPLETO:")
    print("-" * 30)
    print(resultado['resumen_ejecutivo'])
    
    return resultado

if __name__ == "__main__":
    try:
        resultado = test_analisis_discrepancias()
        print("\n✅ Análisis completado exitosamente")
        print(f"🎯 Conclusión: {'ALTA' if resultado['probabilidad_ipp'] >= 0.7 else 'MEDIA' if resultado['probabilidad_ipp'] >= 0.5 else 'BAJA'} probabilidad de IPP")
    except Exception as e:
        print(f"\n❌ Error en el análisis: {e}")
        import traceback
        traceback.print_exc()

