#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de análisis predictivo para resoluciones legales
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def realizar_analisis_predictivo(resultado_base: Dict[str, Any]) -> Dict[str, Any]:
    """Realiza análisis predictivo basado en patrones históricos"""
    try:
        ranking_global = resultado_base.get("ranking_global", {})
        resultados_por_archivo = resultado_base.get("resultados_por_archivo", {})
        
        # Análisis de tendencias
        tendencias = analizar_tendencias(ranking_global)
        
        # Análisis de correlaciones
        correlaciones = analizar_correlaciones(ranking_global)
        
        # Predicción de resultados (ponderada por instancia)
        predicciones = predecir_resultados(ranking_global, resultados_por_archivo)
        
        # Análisis de riesgo (ajustado por instancia)
        analisis_riesgo = analizar_riesgo_legal(ranking_global, resultados_por_archivo)
        
        return {
            "tendencias": tendencias,
            "correlaciones": correlaciones,
            "predicciones": predicciones,
            "analisis_riesgo": analisis_riesgo,
            "confianza_prediccion": calcular_confianza_prediccion(ranking_global)
        }
        
    except Exception as e:
        logger.error(f"Error en análisis predictivo: {e}")
        return {"error": f"Error en análisis predictivo: {str(e)}"}


def analizar_tendencias(ranking_global: Dict[str, Any]) -> Dict[str, Any]:
    """Analiza tendencias en las frases clave"""
    try:
        # Ordenar por total de apariciones
        if ranking_global:
            ranking_ordenado = sorted(ranking_global.items(), key=lambda x: x[1].get("total", 0) if x[1] and isinstance(x[1], dict) else 0, reverse=True)
            
            # Identificar categorías dominantes
            categorias_dominantes = ranking_ordenado[:3] if len(ranking_ordenado) >= 3 else ranking_ordenado
            
            # Calcular tendencias por categoría
            tendencias = {}
            for categoria, datos in ranking_ordenado:
                if datos and isinstance(datos, dict):
                    total = datos.get("total", 0)
                    ocurrencias = datos.get("ocurrencias", [])
                    
                    # Analizar distribución temporal si hay datos
                    if ocurrencias:
                        tendencias[categoria] = {
                            "total": total,
                            "frecuencia": "alta" if total > 50 else "media" if total > 20 else "baja",
                            "tendencia": "creciente" if total > 30 else "estable" if total > 15 else "decreciente",
                            "impacto": "alto" if total > 40 else "medio" if total > 20 else "bajo"
                        }
                    else:
                        tendencias[categoria] = {
                            "total": total,
                            "frecuencia": "media",
                            "tendencia": "estable",
                            "impacto": "medio"
                        }
        else:
            ranking_ordenado = []
            categorias_dominantes = []
            tendencias = {}
        
        return {
            "categorias_dominantes": [{"categoria": cat, "total": datos["total"]} for cat, datos in categorias_dominantes],
            "tendencias_por_categoria": tendencias,
            "resumen_tendencias": {
                "total_categorias": len(tendencias),
                "categoria_mas_frecuente": max(tendencias.items(), key=lambda x: x[1]["total"])[0] if tendencias and any(datos["total"] > 0 for datos in tendencias.values()) else "N/A",
                "promedio_apariciones": sum(datos["total"] for datos in tendencias.values()) / len(tendencias) if tendencias and len(tendencias) > 0 else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error analizando tendencias: {e}")
        return {"error": f"Error analizando tendencias: {str(e)}"}


def analizar_correlaciones(ranking_global: Dict[str, Any]) -> Dict[str, Any]:
    """Analiza correlaciones entre diferentes categorías de frases clave"""
    try:
        categorias = list(ranking_global.keys())
        correlaciones = {}
        
        # Analizar correlaciones entre categorías principales
        categorias_principales = ["incapacidad_permanente_parcial", "reclamacion_administrativa", "inss", "lesiones_permanentes"]
        
        if ranking_global:
            for cat1 in categorias_principales:
                if cat1 in ranking_global and ranking_global[cat1] and isinstance(ranking_global[cat1], dict):
                    correlaciones[cat1] = {}
                    for cat2 in categorias_principales:
                        if cat2 != cat1 and cat2 in ranking_global and ranking_global[cat2] and isinstance(ranking_global[cat2], dict):
                            # Calcular correlación simple basada en apariciones
                            total1 = ranking_global[cat1].get("total", 0)
                            total2 = ranking_global[cat2].get("total", 0)
                            
                            # Correlación basada en frecuencia relativa
                            if total1 > 0 and total2 > 0:
                                correlacion = min(total1, total2) / max(total1, total2)
                                correlaciones[cat1][cat2] = {
                                    "valor": round(correlacion, 3),
                                    "fuerza": "fuerte" if correlacion > 0.7 else "moderada" if correlacion > 0.4 else "débil",
                                    "tipo": "positiva" if correlacion > 0.5 else "negativa"
                                }
                            else:
                                correlaciones[cat1][cat2] = {"valor": 0, "fuerza": "nula", "tipo": "sin correlación"}
        else:
            correlaciones = {}
        
        return {
            "matriz_correlaciones": correlaciones,
            "resumen_correlaciones": {
                "correlaciones_fuertes": sum(1 for cat1 in correlaciones.values() for cat2 in cat1.values() if cat2["fuerza"] == "fuerte"),
                "correlaciones_moderadas": sum(1 for cat1 in correlaciones.values() for cat2 in cat1.values() if cat2["fuerza"] == "moderada"),
                "categoria_mas_correlacionada": max(correlaciones.items(), key=lambda x: len([v for v in x[1].values() if v["fuerza"] in ["fuerte", "moderada"]]))[0] if correlaciones and any(len([v for v in cat.values() if v["fuerza"] in ["fuerte", "moderada"]]) > 0 for cat in correlaciones.values()) else "N/A"
            }
        }
        
    except Exception as e:
        logger.error(f"Error analizando correlaciones: {e}")
        return {"error": f"Error analizando correlaciones: {str(e)}"}


def _inferir_instancia(texto: str) -> str:
    t = (texto or '').lower()
    if 'tribunal supremo' in t or 'sala de lo social del tribunal supremo' in t:
        return 'ts'
    if 'tribunal superior de justicia' in t or 'tsj' in t:
        return 'tsj'
    return 'otra'

def _inferir_instancia_por_nombre(nombre_archivo: str) -> str:
    """Infiere la instancia basándose en el nombre del archivo"""
    if not nombre_archivo:
        return 'otra'
    
    nombre_lower = nombre_archivo.lower()
    
    # Detectar STS (Sentencias del Tribunal Supremo)
    if 'sts_' in nombre_lower or 'sts-' in nombre_lower or 'sts ' in nombre_lower:
        return 'ts'
    
    # Detectar TSJ (Tribunal Superior de Justicia)
    if 'tsj_' in nombre_lower or 'tsj-' in nombre_lower or 'tsj ' in nombre_lower:
        return 'tsj'
    
    # Detectar por patrones más específicos
    if 'tribunal_supremo' in nombre_lower or 'tribunal-supremo' in nombre_lower:
        return 'ts'
    
    if 'tribunal_superior' in nombre_lower or 'tribunal-superior' in nombre_lower:
        return 'tsj'
    
    return 'otra'


def predecir_resultados(ranking_global: Dict[str, Any], resultados_por_archivo: Dict[str, Any]) -> Dict[str, Any]:
    """Predice resultados basándose en patrones históricos"""
    try:
        # Analizar patrones de resoluciones favorables/desfavorables
        patrones_favorables = []
        patrones_desfavorables = []
        
        if resultados_por_archivo:
            for archivo, resultado in resultados_por_archivo.items():
                if resultado and isinstance(resultado, dict) and resultado.get("procesado") and resultado.get("prediccion"):
                    prediccion = resultado["prediccion"]
                    frases_clave = resultado.get("frases_clave", {})
                    instancia = _inferir_instancia_por_nombre(archivo)
                    peso = 1.5 if instancia == 'ts' else 1.2 if instancia == 'tsj' else 1.0
                    
                    if prediccion.get("es_favorable"):
                        patrones_favorables.append({
                            "archivo": archivo,
                            "confianza": prediccion.get("confianza", 0),
                            "frases_clave": list(frases_clave.keys()) if frases_clave else [],
                            "total_frases": sum(datos["total"] for datos in frases_clave.values()) if frases_clave else 0,
                            "instancia": instancia,
                            "peso": peso
                        })
                    else:
                        patrones_desfavorables.append({
                            "archivo": archivo,
                            "confianza": prediccion.get("confianza", 0),
                            "frases_clave": list(frases_clave.keys()) if frases_clave else [],
                            "total_frases": sum(datos["total"] for datos in frases_clave.values()) if frases_clave else 0,
                            "instancia": instancia,
                            "peso": peso
                        })
        
        # Calcular probabilidades con lógica más realista
        total_documentos = len(patrones_favorables) + len(patrones_desfavorables)
        
        if total_documentos == 0:
            # Sin datos suficientes
            prob_favorable = 0.5
            confianza_datos = 0.1
        elif total_documentos < 3:
            # Datos insuficientes - aplicar factor de incertidumbre
            peso_fav = sum(p.get('peso', 1.0) for p in patrones_favorables)
            peso_des = sum(p.get('peso', 1.0) for p in patrones_desfavorables)
            total_peso = peso_fav + peso_des
            
            if total_peso > 0:
                prob_base = peso_fav / total_peso
                # Aplicar factor de incertidumbre para datos limitados
                factor_incertidumbre = 0.3  # Reducir confianza en datos limitados
                prob_favorable = 0.5 + (prob_base - 0.5) * factor_incertidumbre
            else:
                prob_favorable = 0.5
            confianza_datos = 0.3
        else:
            # Datos suficientes - cálculo normal con ponderación por instancia
            peso_fav = sum(p.get('peso', 1.0) for p in patrones_favorables)
            peso_des = sum(p.get('peso', 1.0) for p in patrones_desfavorables)
            total_peso = peso_fav + peso_des
            
            if total_peso > 0:
                prob_favorable = peso_fav / total_peso
                # Aplicar factor de realismo jurídico
                if prob_favorable > 0.9:
                    prob_favorable = 0.85  # Máximo 85% para ser realista
                elif prob_favorable < 0.1:
                    prob_favorable = 0.15  # Mínimo 15% para ser realista
            else:
                prob_favorable = 0.5
            confianza_datos = min(0.8, total_documentos / 10)  # Máximo 80% de confianza
        
        # Identificar factores clave para predicción
        factores_clave_favorables = identificar_factores_clave(patrones_favorables)
        factores_clave_desfavorables = identificar_factores_clave(patrones_desfavorables)
        
        # Generar explicación detallada del cálculo
        explicacion_calculo = generar_explicacion_probabilidad(
            prob_favorable, total_documentos, patrones_favorables, patrones_desfavorables, confianza_datos
        )
        
        return {
            "probabilidad_favorable": round(prob_favorable * 100, 1),
            "probabilidad_desfavorable": round((1 - prob_favorable) * 100, 1),
            "patrones_favorables": patrones_favorables,
            "patrones_desfavorables": patrones_desfavorables,
            "factores_clave_favorables": factores_clave_favorables,
            "factores_clave_desfavorables": factores_clave_desfavorables,
            "confianza_prediccion": calcular_confianza_prediccion_especifica(patrones_favorables, patrones_desfavorables),
            "confianza_datos": round(confianza_datos * 100, 1),
            "advertencia_datos": "Datos insuficientes para predicción confiable" if total_documentos < 3 else None,
            "explicacion_calculo": explicacion_calculo,
            "resumen": {
                "total_resoluciones": len(patrones_favorables) + len(patrones_desfavorables),
                "resoluciones_favorables": len(patrones_favorables),
                "resoluciones_desfavorables": len(patrones_desfavorables),
                "tendencia_general": "favorable" if prob_favorable > 0.6 else "desfavorable" if prob_favorable < 0.4 else "equilibrada",
                "realismo_juridico": "Aplicado factor de realismo jurídico" if total_documentos >= 3 else "Factor de incertidumbre aplicado"
            }
        }
        
    except Exception as e:
        logger.error(f"Error prediciendo resultados: {e}")
        return {"error": f"Error prediciendo resultados: {str(e)}"}


def identificar_factores_clave(patrones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identifica factores clave en patrones de resoluciones"""
    try:
        if not patrones:
            return []
        
        # Contar frecuencia de frases clave
        frecuencia_frases = {}
        for patron in patrones:
            frases_clave = patron.get("frases_clave", [])
            if frases_clave and isinstance(frases_clave, list):
                for frase in frases_clave:
                    if frase:
                        frecuencia_frases[frase] = frecuencia_frases.get(frase, 0) + 1
        
        # Ordenar por frecuencia
        factores_ordenados = sorted(frecuencia_frases.items(), key=lambda x: x[1], reverse=True)
        
        # Convertir a formato estructurado
        factores_clave = []
        if patrones and len(patrones) > 0:
            for frase, frecuencia in factores_ordenados[:5]:  # Top 5
                porcentaje = round(frecuencia / len(patrones) * 100, 1) if len(patrones) > 0 else 0
                factores_clave.append({
                    "frase": frase,
                    "frecuencia": frecuencia,
                    "porcentaje": porcentaje,
                    "impacto": "alto" if frecuencia > len(patrones) * 0.7 else "medio" if frecuencia > len(patrones) * 0.4 else "bajo"
                })
        
        return factores_clave
        
    except Exception as e:
        logger.error(f"Error identificando factores clave: {e}")
        return []


def analizar_riesgo_legal(ranking_global: Dict[str, Any], resultados_por_archivo: Dict[str, Any]) -> Dict[str, Any]:
    """Analiza el riesgo legal basándose en patrones de frases clave"""
    try:
        # Categorías de alto riesgo
        categorias_riesgo = {
            "alto": ["reclamacion_administrativa", "procedimiento_legal", "fundamentos_juridicos"],
            "medio": ["lesiones_permanentes", "accidente_laboral", "prestaciones"],
            "bajo": ["inss", "personal_limpieza", "lesiones_hombro"]
        }
        
        analisis_riesgo = {}
        # Factor de instancia: TS = 1.5, TSJ = 1.2
        factor_instancia = 1.0
        try:
            if resultados_por_archivo:
                # Si la mayoría de documentos son TS/TSJ, subir el factor
                total = len([r for r in resultados_por_archivo.values() if isinstance(r, dict)])
                ts = 0
                tsj = 0
                for archivo, r in resultados_por_archivo.items():
                    if isinstance(r, dict):
                        inst = _inferir_instancia_por_nombre(archivo)
                        ts += 1 if inst == 'ts' else 0
                        tsj += 1 if inst == 'tsj' else 0
                if total > 0:
                    ratio_ts = ts / total
                    ratio_tsj = tsj / total
                    factor_instancia = 1.0 + 0.5 * ratio_ts + 0.2 * ratio_tsj
        except Exception:
            factor_instancia = 1.0
        if ranking_global:
            for nivel, categorias in categorias_riesgo.items():
                riesgo_total = 0
                for categoria in categorias:
                    if categoria in ranking_global and ranking_global[categoria] and isinstance(ranking_global[categoria], dict):
                        riesgo_total += ranking_global[categoria].get("total", 0)
                
                analisis_riesgo[nivel] = {
                    "total_apariciones": riesgo_total,
                    "categorias": categorias,
                    "nivel_riesgo": nivel
                }
        else:
            # Si no hay datos de ranking_global, inicializar con valores por defecto
            for nivel, categorias in categorias_riesgo.items():
                analisis_riesgo[nivel] = {
                    "total_apariciones": 0,
                    "categorias": categorias,
                    "nivel_riesgo": nivel
                }
        
        # Calcular riesgo general con lógica más coherente
        riesgo_general = (
            analisis_riesgo.get("alto", {}).get("total_apariciones", 0) * 3 +
            analisis_riesgo.get("medio", {}).get("total_apariciones", 0) * 2 +
            analisis_riesgo.get("bajo", {}).get("total_apariciones", 0)
        ) * factor_instancia
        
        # Ajustar nivel de riesgo según la cantidad de datos disponibles
        total_documentos = len([r for r in resultados_por_archivo.values() if isinstance(r, dict)]) if resultados_por_archivo else 0
        
        if total_documentos < 3:
            # Con pocos datos, el riesgo es más conservador
            nivel_riesgo_general = "medio" if riesgo_general > 30 else "bajo"
        else:
            # Con datos suficientes, usar lógica normal
            nivel_riesgo_general = "alto" if riesgo_general > 100 else "medio" if riesgo_general > 50 else "bajo"
        
        return {
            "riesgo_por_nivel": analisis_riesgo,
            "riesgo_general": {
                "valor": riesgo_general,
                "nivel": nivel_riesgo_general,
                "interpretacion": interpretar_nivel_riesgo(nivel_riesgo_general, riesgo_general, analisis_riesgo)
            },
            "recomendaciones_riesgo": generar_recomendaciones_riesgo(nivel_riesgo_general, analisis_riesgo)
        }
        
    except Exception as e:
        logger.error(f"Error analizando riesgo legal: {e}")
        return {"error": f"Error analizando riesgo legal: {str(e)}"}


def interpretar_nivel_riesgo(nivel: str, valor_riesgo: float, riesgo_por_nivel: Dict[str, Any]) -> str:
    """Interpreta el nivel de riesgo legal con contexto específico"""
    
    # Obtener detalles de cada nivel
    alto_count = riesgo_por_nivel.get("alto", {}).get("total_apariciones", 0)
    medio_count = riesgo_por_nivel.get("medio", {}).get("total_apariciones", 0)
    bajo_count = riesgo_por_nivel.get("bajo", {}).get("total_apariciones", 0)
    
    interpretaciones = {
        "alto": f"""
        <strong>🔴 ALTO RIESGO LEGAL</strong><br>
        <strong>Puntuación:</strong> {valor_riesgo:.1f} puntos<br>
        <strong>Análisis:</strong> Se detectaron {alto_count} indicadores de alto riesgo relacionados con reclamaciones administrativas, procedimientos legales complejos y fundamentos jurídicos críticos.<br>
        <strong>Impacto:</strong> Este caso presenta múltiples factores que aumentan significativamente la probabilidad de resolución desfavorable.<br>
        <strong>Recomendación:</strong> Requiere revisión exhaustiva por especialista y preparación de estrategia de defensa robusta.
        """,
        "medio": f"""
        <strong>🟡 RIESGO LEGAL MODERADO</strong><br>
        <strong>Puntuación:</strong> {valor_riesgo:.1f} puntos<br>
        <strong>Análisis:</strong> Se identificaron {medio_count} elementos de riesgo medio relacionados con lesiones permanentes, accidentes laborales y prestaciones.<br>
        <strong>Impacto:</strong> El caso presenta algunos factores de complejidad que requieren atención especializada.<br>
        <strong>Recomendación:</strong> Revisión cuidadosa de áreas críticas y preparación de argumentos sólidos.
        """,
        "bajo": f"""
        <strong>🟢 RIESGO LEGAL BAJO</strong><br>
        <strong>Puntuación:</strong> {valor_riesgo:.1f} puntos<br>
        <strong>Análisis:</strong> Se detectaron {bajo_count} indicadores de bajo riesgo relacionados con procedimientos estándar del INSS y casos rutinarios.<br>
        <strong>Impacto:</strong> Este caso presenta características típicas de resolución favorable.<br>
        <strong>Recomendación:</strong> Procedimiento estándar con seguimiento regular.
        """
    }
    
    return interpretaciones.get(nivel, "Nivel de riesgo no determinado.")


def generar_recomendaciones_riesgo(nivel_riesgo: str, riesgo_por_nivel: Dict[str, Any]) -> List[Dict[str, str]]:
    """Genera recomendaciones específicas según el nivel de riesgo con contexto detallado"""
    
    recomendaciones = {
        "alto": [
            {
                "titulo": "🔍 Revisión Exhaustiva de Fundamentos Jurídicos",
                "descripcion": "Analizar cada fundamento jurídico mencionado en la documentación, verificando su aplicabilidad y solidez.",
                "prioridad": "Crítica",
                "tiempo_estimado": "2-3 días"
            },
            {
                "titulo": "⚖️ Consulta con Especialista en Derecho Administrativo",
                "descripcion": "Obtener asesoramiento especializado para casos complejos de derecho administrativo y procedimientos legales.",
                "prioridad": "Alta",
                "tiempo_estimado": "1-2 días"
            },
            {
                "titulo": "📋 Verificación de Cumplimiento de Plazos",
                "descripcion": "Revisar exhaustivamente todos los plazos procesales y administrativos para evitar caducidades.",
                "prioridad": "Crítica",
                "tiempo_estimado": "1 día"
            },
            {
                "titulo": "🛡️ Preparación de Estrategia de Defensa",
                "descripcion": "Desarrollar argumentos sólidos y contraargumentos para cada punto crítico identificado.",
                "prioridad": "Alta",
                "tiempo_estimado": "3-5 días"
            },
            {
                "titulo": "🤝 Evaluación de Alternativas Extrajudiciales",
                "descripcion": "Considerar negociación, mediación o conciliación antes de procedimientos contenciosos.",
                "prioridad": "Media",
                "tiempo_estimado": "2-3 días"
            }
        ],
        "medio": [
            {
                "titulo": "🎯 Revisión de Áreas Críticas Identificadas",
                "descripcion": "Enfocar la atención en los puntos específicos que presentan mayor complejidad.",
                "prioridad": "Alta",
                "tiempo_estimado": "1-2 días"
            },
            {
                "titulo": "📄 Verificación de Documentación de Respaldo",
                "descripcion": "Asegurar que toda la documentación médica y administrativa esté completa y actualizada.",
                "prioridad": "Media",
                "tiempo_estimado": "1 día"
            },
            {
                "titulo": "💪 Fortalecimiento de Argumentos Débiles",
                "descripcion": "Desarrollar argumentos adicionales para los puntos que puedan ser cuestionados.",
                "prioridad": "Media",
                "tiempo_estimado": "2-3 días"
            },
            {
                "titulo": "📞 Comunicación Regular con el Cliente",
                "descripcion": "Mantener informado al cliente sobre el progreso y cualquier desarrollo importante.",
                "prioridad": "Baja",
                "tiempo_estimado": "Ongoing"
            }
        ],
        "bajo": [
            {
                "titulo": "📋 Seguimiento de Procedimiento Estándar",
                "descripcion": "Continuar con el proceso habitual, manteniendo la documentación actualizada.",
                "prioridad": "Baja",
                "tiempo_estimado": "Ongoing"
            },
            {
                "titulo": "📁 Organización de Documentación",
                "descripcion": "Mantener todos los documentos organizados y accesibles para futuras referencias.",
                "prioridad": "Baja",
                "tiempo_estimado": "1 día"
            },
            {
                "titulo": "📅 Seguimiento Regular del Caso",
                "descripcion": "Realizar seguimiento periódico para asegurar que no se produzcan retrasos.",
                "prioridad": "Baja",
                "tiempo_estimado": "Ongoing"
            }
        ]
    }
    
    return recomendaciones.get(nivel_riesgo, [])


def generar_insights_juridicos(resultado_base: Dict[str, Any], analisis_predictivo: Dict[str, Any]) -> Dict[str, Any]:
    """Genera insights jurídicos basados en el análisis"""
    try:
        ranking_global = resultado_base.get("ranking_global", {})
        
        insights = {
            "patrones_identificados": [],
            "tendencias_emergentes": [],
            "alertas": [],
            "oportunidades": [],
            "recomendaciones_generales": []
        }
        
        # Analizar patrones de frases clave
        if ranking_global:
            for categoria, datos in ranking_global.items():
                if datos and isinstance(datos, dict):
                    total = datos.get("total", 0)
                    
                    if total > 30:
                        insights["patrones_identificados"].append({
                            "categoria": categoria,
                            "descripcion": f"Patrón fuerte identificado en {categoria} con {total} apariciones",
                            "impacto": "alto",
                            "accion_recomendada": "Monitorear y analizar en detalle"
                        })
                    elif total > 15:
                        insights["tendencias_emergentes"].append({
                            "categoria": categoria,
                            "descripcion": f"Tendencia emergente en {categoria} con {total} apariciones",
                            "impacto": "medio",
                            "accion_recomendada": "Seguir de cerca"
                        })
        
        # Generar alertas basadas en análisis de riesgo
        analisis_riesgo = analisis_predictivo.get("analisis_riesgo", {})
        if analisis_riesgo and analisis_riesgo.get("riesgo_general", {}).get("nivel") == "alto":
            insights["alertas"].append({
                "tipo": "riesgo_alto",
                "descripcion": "Nivel de riesgo legal alto detectado",
                "accion_requerida": "Revisión inmediata y consulta con especialista",
                "urgencia": "alta"
            })
        
        # Identificar oportunidades
        patrones_identificados = insights.get("patrones_identificados", [])
        if patrones_identificados and len(patrones_identificados) > 3:
            insights["oportunidades"].append({
                "tipo": "patrones_fuertes",
                "descripcion": "Múltiples patrones fuertes identificados",
                "beneficio": "Mayor precisión en predicciones",
                "accion_recomendada": "Aprovechar para mejorar modelo predictivo"
            })
        
        # Recomendaciones generales
        insights["recomendaciones_generales"] = [
            "Mantener actualizada la base de datos de frases clave",
            "Revisar regularmente los patrones emergentes",
            "Validar predicciones con expertos legales",
            "Documentar casos exitosos para aprendizaje continuo"
        ]
        
        return insights
        
    except Exception as e:
        logger.error(f"Error generando insights: {e}")
        return {"error": f"Error generando insights: {str(e)}"}


def extraer_factores_clave(resultado_base: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extrae factores clave que determinan el resultado de las resoluciones"""
    try:
        ranking_global = resultado_base.get("ranking_global", {})
        resultados_por_archivo = resultado_base.get("resultados_por_archivo", {})
        
        factores_clave = []
        
        # Analizar cada categoría
        if ranking_global:
            for categoria, datos in ranking_global.items():
                if datos and isinstance(datos, dict):
                    total = datos.get("total", 0)
                    ocurrencias = datos.get("ocurrencias", [])
                    
                    # Calcular impacto de la categoría
                    impacto = "alto" if total > 40 else "medio" if total > 20 else "bajo"
                    
                    # Analizar contexto de las ocurrencias
                    contextos = []
                    if ocurrencias and len(ocurrencias) > 0:
                        for ocurrencia in ocurrencias[:5]:  # Top 5 contextos
                            contexto_texto = ocurrencia.get("contexto", "")
                            if contexto_texto:
                                texto_truncado = contexto_texto[:100] + "..." if len(contexto_texto) > 100 else contexto_texto
                            else:
                                texto_truncado = "Sin contexto disponible"
                            
                            contextos.append({
                                "texto": texto_truncado,
                                "posicion": ocurrencia.get("posicion", 0),
                                "archivo": ocurrencia.get("archivo", "N/A")
                            })
                    
                    factores_clave.append({
                        "categoria": categoria,
                        "total_apariciones": total,
                        "impacto": impacto,
                        "contextos_ejemplo": contextos,
                        "descripcion": generar_descripcion_factor(categoria, total),
                        "recomendaciones": generar_recomendaciones_factor(categoria, total)
                    })
        else:
            factores_clave = []
        
        # Ordenar por impacto
        factores_clave.sort(key=lambda x: x["total_apariciones"], reverse=True)
        
        return factores_clave
        
    except Exception as e:
        logger.error(f"Error extrayendo factores clave: {e}")
        return []


def generar_descripcion_factor(categoria: str, total: int) -> str:
    """Genera descripción del factor clave"""
    descripciones = {
        "incapacidad_permanente_parcial": f"Factor crítico con {total} apariciones. Fundamental para determinar la gravedad de las lesiones.",
        "reclamacion_administrativa": f"Procedimiento clave con {total} apariciones. Define el camino legal a seguir.",
        "inss": f"Entidad central con {total} apariciones. Sus resoluciones son determinantes.",
        "lesiones_permanentes": f"Factor médico-jurídico con {total} apariciones. Base para la valoración.",
        "personal_limpieza": f"Categoría laboral específica con {total} apariciones. Requiere consideraciones especiales.",
        "lesiones_hombro": f"Lesión específica con {total} apariciones. Impacta en la capacidad laboral."
    }
    return descripciones.get(categoria, f"Factor importante con {total} apariciones en el análisis.")


def generar_recomendaciones_factor(categoria: str, total: int) -> List[str]:
    """Genera recomendaciones específicas para cada factor"""
    recomendaciones = {
        "incapacidad_permanente_parcial": [
            "Verificar documentación médica exhaustiva",
            "Validar con peritos médicos",
            "Revisar criterios de valoración"
        ],
        "reclamacion_administrativa": [
            "Verificar cumplimiento de plazos",
            "Revisar fundamentos jurídicos",
            "Preparar argumentos sólidos"
        ],
        "inss": [
            "Mantener comunicación regular",
            "Verificar resoluciones oficiales",
            "Documentar todas las interacciones"
        ],
        "lesiones_permanentes": [
            "Obtener informes médicos detallados",
            "Validar con especialistas",
            "Documentar evolución de las lesiones"
        ]
    }
    return recomendaciones.get(categoria, ["Revisar documentación relacionada", "Consultar con especialista"])


def generar_recomendaciones(resultado_base: Dict[str, Any], analisis_predictivo: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Genera recomendaciones generales basadas en el análisis"""
    try:
        recomendaciones = []
        
        # Recomendaciones basadas en patrones
        predicciones = analisis_predictivo.get("predicciones", {})
        if predicciones and predicciones.get("probabilidad_favorable", 0) > 70:
            recomendaciones.append({
                "tipo": "optimista",
                "titulo": "Alta probabilidad de resolución favorable",
                "descripcion": "Los patrones históricos sugieren un resultado positivo",
                "acciones": [
                    "Preparar argumentos de respaldo",
                    "Mantener documentación actualizada",
                    "Monitorear cambios en la normativa"
                ],
                "prioridad": "alta"
            })
        elif predicciones and predicciones.get("probabilidad_desfavorable", 0) > 70:
            recomendaciones.append({
                "tipo": "precaución",
                "titulo": "Alta probabilidad de resolución desfavorable",
                "descripcion": "Los patrones históricos sugieren un resultado negativo",
                "acciones": [
                    "Revisar exhaustivamente la documentación",
                    "Consultar con especialista legal",
                    "Considerar alternativas de resolución",
                    "Preparar argumentos de defensa sólidos"
                ],
                "prioridad": "crítica"
            })
        
        # Recomendaciones basadas en riesgo
        analisis_riesgo = analisis_predictivo.get("analisis_riesgo", {})
        nivel_riesgo = analisis_riesgo.get("riesgo_general", {}).get("nivel", "medio") if analisis_riesgo and analisis_riesgo.get("riesgo_general") else "medio"
        
        if nivel_riesgo == "alto":
            recomendaciones.append({
                "tipo": "riesgo",
                "titulo": "Riesgo legal alto detectado",
                "descripcion": "Se requiere atención especial y posible consulta con especialista",
                "acciones": [
                    "Revisión inmediata de toda la documentación",
                    "Consulta urgente con especialista legal",
                    "Preparación de argumentos de defensa",
                    "Evaluación de alternativas de resolución"
                ],
                "prioridad": "crítica"
            })
        
        # Recomendaciones generales
        recomendaciones.append({
            "tipo": "general",
            "titulo": "Mantenimiento del sistema",
            "descripcion": "Acciones recomendadas para mantener la calidad del análisis",
            "acciones": [
                "Actualizar regularmente la base de datos de frases clave",
                "Validar predicciones con expertos legales",
                "Documentar casos exitosos para aprendizaje",
                "Revisar y ajustar el modelo predictivo"
            ],
            "prioridad": "media"
        })
        
        return recomendaciones
        
    except Exception as e:
        logger.error(f"Error generando recomendaciones: {e}")
        return [{"error": f"Error generando recomendaciones: {str(e)}"}]


def calcular_confianza_analisis(resultado_base: Dict[str, Any]) -> float:
    """Calcula el nivel de confianza del análisis"""
    try:
        archivos_analizados = resultado_base.get("archivos_analizados", 0)
        total_apariciones = resultado_base.get("total_apariciones", 0)
        
        # Factores que aumentan la confianza
        confianza = 0.5  # Base
        
        if archivos_analizados >= 10:
            confianza += 0.2
        elif archivos_analizados >= 5:
            confianza += 0.15
        elif archivos_analizados >= 3:
            confianza += 0.1
        
        if total_apariciones >= 100:
            confianza += 0.2
        elif total_apariciones >= 50:
            confianza += 0.15
        elif total_apariciones >= 20:
            confianza += 0.1
        
        # Ajustar por calidad de datos
        ranking_global = resultado_base.get("ranking_global", {})
        if ranking_global and len(ranking_global) >= 5:
            confianza += 0.1
        
        return min(0.95, max(0.1, confianza))
        
    except Exception as e:
        logger.error(f"Error calculando confianza: {e}")
        return 0.5


def calcular_confianza_prediccion(ranking_global: Dict[str, Any]) -> float:
    """Calcula la confianza en las predicciones"""
    try:
        if not ranking_global:
            return 0.1
        
        # Calcular confianza basada en la consistencia de los datos
        if ranking_global:
            totales = [datos.get("total", 0) for datos in ranking_global.values() if datos and isinstance(datos, dict)]
            if not totales:
                return 0.1
            
            # Desviación estándar relativa
            promedio = sum(totales) / len(totales)
            if promedio > 0:
                varianza = sum((x - promedio) ** 2 for x in totales) / len(totales)
                desviacion = varianza ** 0.5
                
                # Menor desviación = mayor confianza
                confianza = max(0.1, 1 - (desviacion / promedio))
            else:
                confianza = 0.1
        else:
            confianza = 0.1
        
        return min(0.95, confianza)
        
    except Exception as e:
        logger.error(f"Error calculando confianza de predicción: {e}")
        return 0.5


def calcular_confianza_prediccion_especifica(patrones_favorables: List[Dict[str, Any]], patrones_desfavorables: List[Dict[str, Any]]) -> float:
    """Calcula confianza específica para predicciones de resultados"""
    try:
        total_patrones = len(patrones_favorables) + len(patrones_desfavorables)
        if total_patrones == 0:
            return 0.1
        
        # Calcular confianza basada en la consistencia de los patrones
        confianzas_favorables = [p.get("confianza", 0.5) for p in patrones_favorables]
        confianzas_desfavorables = [p.get("confianza", 0.5) for p in patrones_desfavorables]
        
        # Promedio de confianzas
        if total_patrones > 0:
            confianza_promedio = (sum(confianzas_favorables) + sum(confianzas_desfavorables)) / total_patrones
            
            # Ajustar por cantidad de datos
            factor_cantidad = min(1.0, total_patrones / 10)  # Máximo 10 patrones
            
            confianza_final = confianza_promedio * factor_cantidad
        else:
            confianza_final = 0.1
        
        return min(0.95, max(0.1, confianza_final))
        
    except Exception as e:
        logger.error(f"Error calculando confianza específica: {e}")
        return 0.5


def identificar_patrones_favorables(resultado_base: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identifica patrones que suelen llevar a resoluciones favorables"""
    try:
        resultados_por_archivo = resultado_base.get("resultados_por_archivo", {})
        patrones = []
        
        if resultados_por_archivo:
            for archivo, resultado in resultados_por_archivo.items():
                if resultado and isinstance(resultado, dict) and resultado.get("procesado") and resultado.get("prediccion", {}).get("es_favorable"):
                    frases_clave = resultado.get("frases_clave", {})
                    patrones.append({
                        "archivo": archivo,
                        "frases_clave": list(frases_clave.keys()) if frases_clave else [],
                        "total_frases": sum(datos["total"] for datos in frases_clave.values()) if frases_clave else 0,
                        "confianza": resultado.get("prediccion", {}).get("confianza", 0)
                    })
        
        return patrones
        
    except Exception as e:
        logger.error(f"Error identificando patrones favorables: {e}")
        return []


def generar_explicacion_probabilidad(prob_favorable: float, total_documentos: int, 
                                   patrones_favorables: List[Dict[str, Any]], 
                                   patrones_desfavorables: List[Dict[str, Any]], 
                                   confianza_datos: float) -> Dict[str, Any]:
    """Genera una explicación detallada del cálculo de probabilidades"""
    try:
        explicacion = {
            "metodologia": "Análisis predictivo basado en patrones históricos de resoluciones legales",
            "datos_analizados": {
                "total_documentos": total_documentos,
                "documentos_favorables": len(patrones_favorables),
                "documentos_desfavorables": len(patrones_desfavorables),
                "confianza_datos": round(confianza_datos * 100, 1)
            },
            "calculo_probabilidad": {},
            "factores_aplicados": [],
            "limitaciones": [],
            "recomendaciones": []
        }
        
        # Explicar el cálculo según el escenario
        if total_documentos == 0:
            explicacion["calculo_probabilidad"] = {
                "metodo": "Sin datos disponibles",
                "probabilidad_base": "50% (neutral)",
                "justificacion": "No hay documentos analizados para realizar predicción"
            }
            explicacion["limitaciones"].append("Sin datos históricos para análisis")
            explicacion["recomendaciones"].append("Subir más documentos para mejorar la predicción")
            
        elif total_documentos < 3:
            # Calcular probabilidad base sin factores
            peso_fav = sum(p.get('peso', 1.0) for p in patrones_favorables)
            peso_des = sum(p.get('peso', 1.0) for p in patrones_desfavorables)
            total_peso = peso_fav + peso_des
            prob_base = (peso_fav / total_peso) if total_peso > 0 else 0.5
            
            explicacion["calculo_probabilidad"] = {
                "metodo": "Factor de incertidumbre aplicado",
                "probabilidad_base": f"{round(prob_base * 100, 1)}%",
                "factor_incertidumbre": "30%",
                "probabilidad_final": f"{round(prob_favorable * 100, 1)}%",
                "formula": f"50% + ({prob_base:.3f} - 0.5) × 0.3 = {prob_favorable:.3f}"
            }
            explicacion["factores_aplicados"].extend([
                "Factor de incertidumbre: 30% (datos limitados)",
                "Ponderación por instancia: TS (x1.5), TSJ (x1.2)"
            ])
            explicacion["limitaciones"].append("Datos insuficientes para predicción confiable")
            explicacion["recomendaciones"].append("Subir al menos 3 documentos para análisis más preciso")
            
        else:
            # Calcular probabilidad base sin factores de realismo
            peso_fav = sum(p.get('peso', 1.0) for p in patrones_favorables)
            peso_des = sum(p.get('peso', 1.0) for p in patrones_desfavorables)
            total_peso = peso_fav + peso_des
            prob_base = (peso_fav / total_peso) if total_peso > 0 else 0.5
            
            explicacion["calculo_probabilidad"] = {
                "metodo": "Factor de realismo jurídico aplicado",
                "probabilidad_base": f"{round(prob_base * 100, 1)}%",
                "probabilidad_final": f"{round(prob_favorable * 100, 1)}%",
                "ajuste_realismo": "Aplicado límite máximo del 85%"
            }
            
            if prob_base > 0.9:
                explicacion["calculo_probabilidad"]["justificacion"] = "Probabilidad base >90% ajustada a 85% por realismo jurídico"
            elif prob_base < 0.1:
                explicacion["calculo_probabilidad"]["justificacion"] = "Probabilidad base <10% ajustada a 15% por realismo jurídico"
            else:
                explicacion["calculo_probabilidad"]["justificacion"] = "Probabilidad base dentro del rango realista"
            
            explicacion["factores_aplicados"].extend([
                "Factor de realismo jurídico: límites 15%-85%",
                "Ponderación por instancia: TS (x1.5), TSJ (x1.2)",
                f"Confianza de datos: {round(confianza_datos * 100, 1)}%"
            ])
            explicacion["recomendaciones"].append("Análisis basado en datos suficientes")
        
        # Agregar detalles de instancias
        instancias_ts = sum(1 for p in patrones_favorables + patrones_desfavorables if p.get('instancia') == 'ts')
        instancias_tsj = sum(1 for p in patrones_favorables + patrones_desfavorables if p.get('instancia') == 'tsj')
        
        if instancias_ts > 0 or instancias_tsj > 0:
            explicacion["instancias_analizadas"] = {
                "tribunal_supremo": instancias_ts,
                "tribunal_superior_justicia": instancias_tsj,
                "otras_instancias": total_documentos - instancias_ts - instancias_tsj
            }
        
        # Agregar resumen de factores clave
        if patrones_favorables:
            frases_favorables = []
            for patron in patrones_favorables:
                frases_favorables.extend(patron.get('frases_clave', []))
            
            if frases_favorables:
                explicacion["factores_clave_favorables"] = list(set(frases_favorables))[:5]
        
        if patrones_desfavorables:
            frases_desfavorables = []
            for patron in patrones_desfavorables:
                frases_desfavorables.extend(patron.get('frases_clave', []))
            
            if frases_desfavorables:
                explicacion["factores_clave_desfavorables"] = list(set(frases_desfavorables))[:5]
        
        return explicacion
        
    except Exception as e:
        logger.error(f"Error generando explicación de probabilidad: {e}")
        return {
            "error": f"Error generando explicación: {str(e)}",
            "metodologia": "Análisis predictivo basado en patrones históricos",
            "datos_analizados": {"total_documentos": total_documentos}
        }
