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
        
        # Predicción de resultados
        predicciones = predecir_resultados(ranking_global, resultados_por_archivo)
        
        # Análisis de riesgo
        analisis_riesgo = analizar_riesgo_legal(ranking_global)
        
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
        ranking_ordenado = sorted(ranking_global.items(), key=lambda x: x[1]["total"], reverse=True)
        
        # Identificar categorías dominantes
        categorias_dominantes = ranking_ordenado[:3] if len(ranking_ordenado) >= 3 else ranking_ordenado
        
        # Calcular tendencias por categoría
        tendencias = {}
        for categoria, datos in ranking_ordenado:
            total = datos["total"]
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
        
        return {
            "categorias_dominantes": [{"categoria": cat, "total": datos["total"]} for cat, datos in categorias_dominantes],
            "tendencias_por_categoria": tendencias,
            "resumen_tendencias": {
                "total_categorias": len(tendencias),
                "categoria_mas_frecuente": max(tendencias.items(), key=lambda x: x[1]["total"])[0] if tendencias else "N/A",
                "promedio_apariciones": sum(datos["total"] for datos in tendencias.values()) / len(tendencias) if tendencias else 0
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
        
        for cat1 in categorias_principales:
            if cat1 in ranking_global:
                correlaciones[cat1] = {}
                for cat2 in categorias_principales:
                    if cat2 != cat1 and cat2 in ranking_global:
                        # Calcular correlación simple basada en apariciones
                        total1 = ranking_global[cat1]["total"]
                        total2 = ranking_global[cat2]["total"]
                        
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
        
        return {
            "matriz_correlaciones": correlaciones,
            "resumen_correlaciones": {
                "correlaciones_fuertes": sum(1 for cat1 in correlaciones.values() for cat2 in cat1.values() if cat2["fuerza"] == "fuerte"),
                "correlaciones_moderadas": sum(1 for cat1 in correlaciones.values() for cat2 in cat1.values() if cat2["fuerza"] == "moderada"),
                "categoria_mas_correlacionada": max(correlaciones.items(), key=lambda x: len([v for v in x[1].values() if v["fuerza"] in ["fuerte", "moderada"]]))[0] if correlaciones else "N/A"
            }
        }
        
    except Exception as e:
        logger.error(f"Error analizando correlaciones: {e}")
        return {"error": f"Error analizando correlaciones: {str(e)}"}


def predecir_resultados(ranking_global: Dict[str, Any], resultados_por_archivo: Dict[str, Any]) -> Dict[str, Any]:
    """Predice resultados basándose en patrones históricos"""
    try:
        # Analizar patrones de resoluciones favorables/desfavorables
        patrones_favorables = []
        patrones_desfavorables = []
        
        for archivo, resultado in resultados_por_archivo.items():
            if resultado.get("procesado") and resultado.get("prediccion"):
                prediccion = resultado["prediccion"]
                frases_clave = resultado.get("frases_clave", {})
                
                if prediccion.get("es_favorable"):
                    patrones_favorables.append({
                        "archivo": archivo,
                        "confianza": prediccion.get("confianza", 0),
                        "frases_clave": list(frases_clave.keys()),
                        "total_frases": sum(datos["total"] for datos in frases_clave.values())
                    })
                else:
                    patrones_desfavorables.append({
                        "archivo": archivo,
                        "confianza": prediccion.get("confianza", 0),
                        "frases_clave": list(frases_clave.keys()),
                        "total_frases": sum(datos["total"] for datos in frases_clave.values())
                    })
        
        # Calcular probabilidades
        total_resoluciones = len(patrones_favorables) + len(patrones_desfavorables)
        prob_favorable = len(patrones_favorables) / total_resoluciones if total_resoluciones > 0 else 0.5
        
        # Identificar factores clave para predicción
        factores_clave_favorables = identificar_factores_clave(patrones_favorables)
        factores_clave_desfavorables = identificar_factores_clave(patrones_desfavorables)
        
        return {
            "probabilidad_favorable": round(prob_favorable * 100, 1),
            "probabilidad_desfavorable": round((1 - prob_favorable) * 100, 1),
            "patrones_favorables": patrones_favorables,
            "patrones_desfavorables": patrones_desfavorables,
            "factores_clave_favorables": factores_clave_favorables,
            "factores_clave_desfavorables": factores_clave_desfavorables,
            "confianza_prediccion": calcular_confianza_prediccion_especifica(patrones_favorables, patrones_desfavorables),
            "resumen": {
                "total_resoluciones": total_resoluciones,
                "resoluciones_favorables": len(patrones_favorables),
                "resoluciones_desfavorables": len(patrones_desfavorables),
                "tendencia_general": "favorable" if prob_favorable > 0.6 else "desfavorable" if prob_favorable < 0.4 else "equilibrada"
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
            for frase in patron.get("frases_clave", []):
                frecuencia_frases[frase] = frecuencia_frases.get(frase, 0) + 1
        
        # Ordenar por frecuencia
        factores_ordenados = sorted(frecuencia_frases.items(), key=lambda x: x[1], reverse=True)
        
        # Convertir a formato estructurado
        factores_clave = []
        for frase, frecuencia in factores_ordenados[:5]:  # Top 5
            factores_clave.append({
                "frase": frase,
                "frecuencia": frecuencia,
                "porcentaje": round(frecuencia / len(patrones) * 100, 1),
                "impacto": "alto" if frecuencia > len(patrones) * 0.7 else "medio" if frecuencia > len(patrones) * 0.4 else "bajo"
            })
        
        return factores_clave
        
    except Exception as e:
        logger.error(f"Error identificando factores clave: {e}")
        return []


def analizar_riesgo_legal(ranking_global: Dict[str, Any]) -> Dict[str, Any]:
    """Analiza el riesgo legal basándose en patrones de frases clave"""
    try:
        # Categorías de alto riesgo
        categorias_riesgo = {
            "alto": ["reclamacion_administrativa", "procedimiento_legal", "fundamentos_juridicos"],
            "medio": ["lesiones_permanentes", "accidente_laboral", "prestaciones"],
            "bajo": ["inss", "personal_limpieza", "lesiones_hombro"]
        }
        
        analisis_riesgo = {}
        for nivel, categorias in categorias_riesgo.items():
            riesgo_total = 0
            for categoria in categorias:
                if categoria in ranking_global:
                    riesgo_total += ranking_global[categoria]["total"]
            
            analisis_riesgo[nivel] = {
                "total_apariciones": riesgo_total,
                "categorias": categorias,
                "nivel_riesgo": nivel
            }
        
        # Calcular riesgo general
        riesgo_general = sum(analisis_riesgo["alto"]["total_apariciones"]) * 3 + \
                        sum(analisis_riesgo["medio"]["total_apariciones"]) * 2 + \
                        sum(analisis_riesgo["bajo"]["total_apariciones"])
        
        nivel_riesgo_general = "alto" if riesgo_general > 100 else "medio" if riesgo_general > 50 else "bajo"
        
        return {
            "riesgo_por_nivel": analisis_riesgo,
            "riesgo_general": {
                "valor": riesgo_general,
                "nivel": nivel_riesgo_general,
                "interpretacion": interpretar_nivel_riesgo(nivel_riesgo_general)
            },
            "recomendaciones_riesgo": generar_recomendaciones_riesgo(nivel_riesgo_general)
        }
        
    except Exception as e:
        logger.error(f"Error analizando riesgo legal: {e}")
        return {"error": f"Error analizando riesgo legal: {str(e)}"}


def interpretar_nivel_riesgo(nivel: str) -> str:
    """Interpreta el nivel de riesgo legal"""
    interpretaciones = {
        "alto": "Alto riesgo legal. Se recomienda revisión exhaustiva y posible consulta con especialista.",
        "medio": "Riesgo legal moderado. Requiere atención especial en áreas críticas.",
        "bajo": "Riesgo legal bajo. Procedimiento estándar recomendado."
    }
    return interpretaciones.get(nivel, "Nivel de riesgo no determinado.")


def generar_recomendaciones_riesgo(nivel_riesgo: str) -> List[str]:
    """Genera recomendaciones específicas según el nivel de riesgo"""
    recomendaciones = {
        "alto": [
            "Revisar exhaustivamente todos los fundamentos jurídicos",
            "Consultar con especialista en derecho administrativo",
            "Verificar cumplimiento de plazos y procedimientos",
            "Preparar argumentos de defensa sólidos",
            "Considerar alternativas de resolución extrajudicial"
        ],
        "medio": [
            "Revisar áreas críticas identificadas",
            "Verificar documentación de respaldo",
            "Preparar argumentos para puntos débiles",
            "Mantener comunicación regular con el cliente"
        ],
        "bajo": [
            "Seguir procedimiento estándar",
            "Mantener documentación actualizada",
            "Monitorear cambios en la normativa"
        ]
    }
    return recomendaciones.get(nivel_riesgo, ["Recomendaciones no disponibles para este nivel de riesgo."])


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
        for categoria, datos in ranking_global.items():
            total = datos["total"]
            
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
        if analisis_riesgo.get("riesgo_general", {}).get("nivel") == "alto":
            insights["alertas"].append({
                "tipo": "riesgo_alto",
                "descripcion": "Nivel de riesgo legal alto detectado",
                "accion_requerida": "Revisión inmediata y consulta con especialista",
                "urgencia": "alta"
            })
        
        # Identificar oportunidades
        if len(insights["patrones_identificados"]) > 3:
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
        for categoria, datos in ranking_global.items():
            total = datos["total"]
            ocurrencias = datos.get("ocurrencias", [])
            
            # Calcular impacto de la categoría
            impacto = "alto" if total > 40 else "medio" if total > 20 else "bajo"
            
            # Analizar contexto de las ocurrencias
            contextos = []
            for ocurrencia in ocurrencias[:5]:  # Top 5 contextos
                contextos.append({
                    "texto": ocurrencia.get("contexto", "")[:100] + "..." if len(ocurrencia.get("contexto", "")) > 100 else ocurrencia.get("contexto", ""),
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
        if predicciones.get("probabilidad_favorable", 0) > 70:
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
        elif predicciones.get("probabilidad_desfavorable", 0) > 70:
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
        nivel_riesgo = analisis_riesgo.get("riesgo_general", {}).get("nivel", "medio")
        
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
        if len(ranking_global) >= 5:
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
        totales = [datos["total"] for datos in ranking_global.values()]
        if not totales:
            return 0.1
        
        # Desviación estándar relativa
        promedio = sum(totales) / len(totales)
        varianza = sum((x - promedio) ** 2 for x in totales) / len(totales)
        desviacion = varianza ** 0.5
        
        # Menor desviación = mayor confianza
        confianza = max(0.1, 1 - (desviacion / promedio) if promedio > 0 else 0.1)
        
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
        confianza_promedio = (sum(confianzas_favorables) + sum(confianzas_desfavorables)) / total_patrones
        
        # Ajustar por cantidad de datos
        factor_cantidad = min(1.0, total_patrones / 10)  # Máximo 10 patrones
        
        confianza_final = confianza_promedio * factor_cantidad
        
        return min(0.95, max(0.1, confianza_final))
        
    except Exception as e:
        logger.error(f"Error calculando confianza específica: {e}")
        return 0.5


def identificar_patrones_favorables(resultado_base: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identifica patrones que suelen llevar a resoluciones favorables"""
    try:
        resultados_por_archivo = resultado_base.get("resultados_por_archivo", {})
        patrones = []
        
        for archivo, resultado in resultados_por_archivo.items():
            if resultado.get("procesado") and resultado.get("prediccion", {}).get("es_favorable"):
                frases_clave = resultado.get("frases_clave", {})
                patrones.append({
                    "archivo": archivo,
                    "frases_clave": list(frases_clave.keys()),
                    "total_frases": sum(datos["total"] for datos in frases_clave.values()),
                    "confianza": resultado.get("prediccion", {}).get("confianza", 0)
                })
        
        return patrones
        
    except Exception as e:
        logger.error(f"Error identificando patrones favorables: {e}")
        return []
