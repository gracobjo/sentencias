#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Análisis de Discrepancias Médicas-Legales
Especializado en identificar contradicciones y argumentos jurídicos específicos
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class AnalizadorDiscrepancias:
    """
    Analizador especializado en identificar discrepancias entre diagnósticos médicos
    y calificaciones legales, especialmente en casos de LPNI vs IPP
    """
    
    def __init__(self):
        """Inicializa el analizador de discrepancias"""
        self.patrones_discrepancias = self._cargar_patrones_discrepancias()
        self.argumentos_juridicos = self._cargar_argumentos_juridicos()
        self.criterios_ipp = self._cargar_criterios_ipp()
        
    def _cargar_patrones_discrepancias(self) -> Dict[str, List[str]]:
        """Carga patrones para detectar discrepancias médicas-legales"""
        return {
            "lesiones_graves": [
                r"rotura\s+(?:de\s+)?espesor\s+completo",
                r"retracción\s+fibrilar\s+\d+\s*mm",
                r"tenopatía\s+severa",
                r"artropatía\s+acromioclavicular\s+severa",
                r"lesión\s+estructural\s+grave",
                r"rotura\s+completa\s+del\s+manguito\s+rotador",
                r"anclajes?\s+(?:corkscrew|tornillos?)",
                r"cirugía\s+reconstructiva"
            ],
            "limitaciones_funcionales": [
                r"flexión\s+activa\s+solo\s+\d+[°º]",
                r"abducción\s+activa\s+\d+[°º]",
                r"fuerza\s+insuficiente\s+para\s+vencer\s+la\s+gravedad",
                r"balance\s+muscular\s+\d+/\d+",
                r"fuerza\s+de\s+garra\s+solo\s+\d+\s*kg",
                r"limitación\s+activa\s+a\s+\d+[°º]",
                r"discinesia\s+escapular",
                r"atrofia\s+periescapular",
                r"prácticamente\s+nulo\s+desarrollo\s+de\s+fuerza"
            ],
            "contradicciones_internas": [
                r"no\s+presenta\s+limitación\s+importante.*?limitación\s+activa",
                r"no\s+impide\s+actividades.*?limitación\s+activa",
                r"alta\s+médica.*?limitaciones?\s+persistentes",
                r"recuperación.*?secuelas?\s+permanentes",
                r"movilidad\s+pasiva.*?activa\s+sigue\s+limitada"
            ],
            "terminologia_lpni": [
                r"lesiones?\s+permanentes?\s+no\s+incapacitantes?",
                r"LPNI",
                r"secuelas?\s+no\s+invalidantes?",
                r"molestias?\s+leves?",
                r"lesiones?\s+menores?"
            ],
            "terminologia_ipp": [
                r"incapacidad\s+permanente\s+parcial",
                r"IPP",
                r"disminución\s+(?:del\s+)?rendimiento.*?33%",
                r"art\.\s*194\.2\s+LGSS",
                r"limitación\s+funcional\s+permanente",
                r"merma\s+funcional.*?33%"
            ],
            "evidencia_objetiva": [
                r"RMN.*?\d{2}\.\d{2}\.\d{4}",
                r"informe\s+de\s+biomecánica",
                r"fuerza.*?normal.*?>\d+\s*kg",
                r"duración\s+del\s+proceso.*?\d+\s*meses?",
                r"múltiples\s+recaídas?",
                r"cirugía.*?\d{2}\.\d{2}\.\d{4}"
            ]
        }
    
    def _cargar_argumentos_juridicos(self) -> Dict[str, List[str]]:
        """Carga argumentos jurídicos específicos para casos LPNI vs IPP"""
        return {
            "argumentos_favorables_ipp": [
                "El art. 194.2 LGSS exige para la IPP una disminución ≥33% en el rendimiento normal de la profesión habitual",
                "La profesión de limpiadora requiere levantar brazos repetidamente por encima del hombro",
                "Con limitación activa que no supera los 90° de abducción/flexión, la merma funcional es objetiva y superior al 33%",
                "Los informes técnicos confirman que la limitación es permanente y relevante",
                "La diferencia entre movilidad pasiva y activa es signo clásico de lesión incapacitante para tareas laborales"
            ],
            "discrepancias_clave": [
                "Diagnóstico vs. calificación final: Los informes técnicos describen lesiones graves y limitantes, sin embargo, la calificación final fue de LPNI",
                "Movilidad pasiva vs. activa: Aunque la pasiva es 'casi completa', lo que importa en el trabajo es la activa, que sigue limitada",
                "Alta contradictoria: Se reconoce discinesia escapular, atrofia periescapular y limitación activa persistente, pero se concluye que 'no hay limitación laboral'",
                "Duración y recaídas: Tras casi dos años de tratamiento, operación y rehabilitación, la persistencia de limitaciones descarta una simple lesión no invalidante"
            ],
            "puntos_clave_defensa": [
                "Lesión estructural grave confirmada por RMN: rotura completa del supraespinoso con retracción fibrilar",
                "Cirugía con anclajes: El hecho de necesitar cirugía reconstructiva marca la gravedad y permanencia del daño",
                "Limitaciones persistentes postquirúrgicas: flexión activa limitada, fuerza insuficiente para vencer la gravedad",
                "Informe de biomecánica: 'Prácticamente nulo desarrollo de fuerza con hombro derecho'",
                "Duración del proceso: 20 meses con múltiples recaídas, cirugía y secuelas"
            ]
        }
    
    def _cargar_criterios_ipp(self) -> Dict[str, Any]:
        """Carga criterios específicos para determinar IPP"""
        return {
            "criterio_principal": {
                "descripcion": "Art. 194.2 LGSS: Disminución ≥33% en el rendimiento normal de la profesión habitual",
                "elementos": [
                    "Profesión habitual identificada",
                    "Rendimiento normal de referencia",
                    "Disminución cuantificable ≥33%",
                    "Limitación permanente"
                ]
            },
            "profesiones_especificas": {
                "limpiadora": {
                    "requisitos_funcionales": [
                        "Levantar brazos repetidamente por encima del hombro",
                        "Esfuerzo de hombros",
                        "Escaleras y movimientos repetitivos",
                        "Cargar peso",
                        "Movimientos de limpieza de cristales"
                    ],
                    "limitaciones_criticas": [
                        "Abducción/flexión activa <90°",
                        "Fuerza <50% de lo normal",
                        "Dolor persistente en movimientos",
                        "Discinesia escapular",
                        "Atrofia muscular"
                    ]
                }
            },
            "evidencia_medica_requerida": [
                "Informes de imagen (RMN, TAC)",
                "Informes de biomecánica",
                "Evaluaciones de fuerza muscular",
                "Seguimiento postquirúrgico",
                "Evaluaciones de capacidad funcional"
            ]
        }
    
    def analizar_discrepancias(self, texto: str) -> Dict[str, Any]:
        """
        Analiza discrepancias médicas-legales en el texto
        
        Args:
            texto: Texto del informe médico-legal
            
        Returns:
            Diccionario con análisis de discrepancias
        """
        try:
            # Detectar tipo de documento
            tipo_documento = self._detectar_tipo_documento(texto)
            logger.info(f"Tipo de documento detectado: {tipo_documento}")
            
            resultado = {
                "tipo_documento": tipo_documento,
                "discrepancias_detectadas": [],
                "argumentos_juridicos": [],
                "evidencia_favorable": [],
                "contradicciones_internas": [],
                "recomendaciones_defensa": [],
                "puntuacion_discrepancia": 0,
                "probabilidad_ipp": 0.0,
                "resumen_ejecutivo": ""
            }
            
            # Análisis específico según tipo de documento
            if tipo_documento == "sentencia":
                return self._analizar_sentencia(texto, resultado)
            elif tipo_documento == "informe_medico":
                return self._analizar_informe_medico(texto, resultado)
            else:
                return self._analizar_documento_generico(texto, resultado)
            
        except Exception as e:
            logger.error(f"Error analizando discrepancias: {e}")
            return {"error": f"Error en análisis de discrepancias: {str(e)}"}
    
    def _detectar_tipo_documento(self, texto: str) -> str:
        """Detecta el tipo de documento basado en su contenido"""
        texto_lower = texto.lower()
        
        # Indicadores de sentencia
        indicadores_sentencia = [
            "tribunal supremo", "sts", "sentencia", "magistrado", "magistrada",
            "fallamos", "estimamos", "desestimamos", "resuelvo", "resolvemos",
            "parte dispositiva", "fundamentos de derecho", "antecedentes de hecho"
        ]
        
        # Indicadores de informe médico
        indicadores_informe = [
            "informe médico", "diagnóstico", "tratamiento", "evolución", "pronóstico",
            "exploración física", "pruebas complementarias", "alta médica", "baja médica",
            "limitaciones funcionales", "capacidad laboral"
        ]
        
        contador_sentencia = sum(1 for indicador in indicadores_sentencia if indicador in texto_lower)
        contador_informe = sum(1 for indicador in indicadores_informe if indicador in texto_lower)
        
        if contador_sentencia > contador_informe and contador_sentencia >= 3:
            return "sentencia"
        elif contador_informe > contador_sentencia and contador_informe >= 3:
            return "informe_medico"
        else:
            return "documento_generico"
    
    def _analizar_sentencia(self, texto: str, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis específico para sentencias"""
        # Análisis específico para sentencias
        discrepancias = self._detectar_discrepancias_sentencia(texto)
        resultado["discrepancias_detectadas"] = discrepancias
        
        evidencia = self._analizar_evidencia_sentencia(texto)
        resultado["evidencia_favorable"] = evidencia
        
        # Detectar contradicciones internas
        contradicciones = self._detectar_contradicciones_sentencia(texto)
        resultado["contradicciones_internas"] = contradicciones
        
        # Generar argumentos jurídicos específicos para sentencias
        argumentos = self._generar_argumentos_sentencia(texto, discrepancias, evidencia)
        resultado["argumentos_juridicos"] = argumentos
        
        # Generar recomendaciones específicas para sentencias
        recomendaciones = self._generar_recomendaciones_sentencia(texto, discrepancias, evidencia, contradicciones)
        resultado["recomendaciones_defensa"] = recomendaciones
        
        # Calcular puntuación específica para sentencias
        puntuacion = self._calcular_puntuacion_sentencia(discrepancias, evidencia, contradicciones)
        resultado["puntuacion_discrepancia"] = puntuacion
        
        # Calcular probabilidad específica para sentencias
        probabilidad = self._calcular_probabilidad_sentencia(texto, discrepancias, evidencia)
        resultado["probabilidad_ipp"] = probabilidad
        
        # Generar resumen específico para sentencias
        resumen = self._generar_resumen_sentencia(resultado)
        resultado["resumen_ejecutivo"] = resumen
        
        return resultado
    
    def _analizar_informe_medico(self, texto: str, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis específico para informes médicos"""
        # Detectar discrepancias específicas
        discrepancias = self._detectar_discrepancias_especificas(texto)
        resultado["discrepancias_detectadas"] = discrepancias
        
        # Analizar evidencia favorable
        evidencia = self._analizar_evidencia_favorable(texto)
        resultado["evidencia_favorable"] = evidencia
        
        # Detectar contradicciones internas
        contradicciones = self._detectar_contradicciones_internas(texto)
        resultado["contradicciones_internas"] = contradicciones
        
        # Generar argumentos jurídicos
        argumentos = self._generar_argumentos_juridicos(texto, discrepancias, evidencia)
        resultado["argumentos_juridicos"] = argumentos
        
        # Generar recomendaciones de defensa
        recomendaciones = self._generar_recomendaciones_defensa(texto, discrepancias, evidencia, contradicciones)
        resultado["recomendaciones_defensa"] = recomendaciones
        
        # Calcular puntuación de discrepancia
        puntuacion = self._calcular_puntuacion_discrepancia(discrepancias, evidencia, contradicciones)
        resultado["puntuacion_discrepancia"] = puntuacion
        
        # Calcular probabilidad de IPP
        probabilidad = self._calcular_probabilidad_ipp(texto, discrepancias, evidencia)
        resultado["probabilidad_ipp"] = probabilidad
        
        # Generar resumen ejecutivo
        resumen = self._generar_resumen_ejecutivo(resultado)
        resultado["resumen_ejecutivo"] = resumen
        
        return resultado
    
    def _analizar_documento_generico(self, texto: str, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis para documentos genéricos"""
        # Usar análisis básico de discrepancias
        discrepancias = self._detectar_discrepancias_especificas(texto)
        resultado["discrepancias_detectadas"] = discrepancias
        
        evidencia = self._analizar_evidencia_favorable(texto)
        resultado["evidencia_favorable"] = evidencia
        
        contradicciones = self._detectar_contradicciones_internas(texto)
        resultado["contradicciones_internas"] = contradicciones
        
        argumentos = self._generar_argumentos_juridicos(texto, discrepancias, evidencia)
        resultado["argumentos_juridicos"] = argumentos
        
        recomendaciones = self._generar_recomendaciones_defensa(texto, discrepancias, evidencia, contradicciones)
        resultado["recomendaciones_defensa"] = recomendaciones
        
        puntuacion = self._calcular_puntuacion_discrepancia(discrepancias, evidencia, contradicciones)
        resultado["puntuacion_discrepancia"] = puntuacion
        
        probabilidad = self._calcular_probabilidad_ipp(texto, discrepancias, evidencia)
        resultado["probabilidad_ipp"] = probabilidad
        
        resumen = self._generar_resumen_ejecutivo(resultado)
        resultado["resumen_ejecutivo"] = resumen
        
        return resultado
    
    def _detectar_discrepancias_especificas(self, texto: str) -> List[Dict[str, Any]]:
        """Detecta discrepancias específicas entre diagnóstico médico y calificación legal"""
        discrepancias = []
        texto_lower = texto.lower()
        
        # Detectar lesiones graves vs calificación LPNI
        lesiones_graves = self._buscar_patrones(texto, self.patrones_discrepancias["lesiones_graves"])
        terminologia_lpni = self._buscar_patrones(texto, self.patrones_discrepancias["terminologia_lpni"])
        
        if lesiones_graves and terminologia_lpni:
            discrepancias.append({
                "tipo": "lesiones_graves_vs_lpni",
                "descripcion": "Se detectan lesiones graves (rotura completa, cirugía reconstructiva) pero se califica como LPNI",
                "evidencia": lesiones_graves,
                "contradiccion": terminologia_lpni,
                "severidad": "alta",
                "argumento_juridico": "Una rotura completa del supraespinoso con cirugía reconstructiva no puede ser calificada como LPNI"
            })
        
        # Detectar limitaciones funcionales vs alta médica
        limitaciones = self._buscar_patrones(texto, self.patrones_discrepancias["limitaciones_funcionales"])
        alta_medica = re.search(r"alta\s+médica.*?(?:no\s+presenta\s+limitación|no\s+impide)", texto_lower)
        
        if limitaciones and alta_medica:
            discrepancias.append({
                "tipo": "limitaciones_vs_alta",
                "descripcion": "Se documentan limitaciones funcionales específicas pero se da alta médica sin limitaciones",
                "evidencia": limitaciones,
                "contradiccion": alta_medica.group() if alta_medica else "Alta médica sin limitaciones",
                "severidad": "alta",
                "argumento_juridico": "Las limitaciones activas documentadas contradicen la conclusión de alta sin limitaciones"
            })
        
        # Detectar evidencia objetiva vs conclusión subjetiva
        evidencia_obj = self._buscar_patrones(texto, self.patrones_discrepancias["evidencia_objetiva"])
        conclusion_subjetiva = re.search(r"(?:molestias?|dolor\s+leve|síntomas?\s+menores?)", texto_lower)
        
        if evidencia_obj and conclusion_subjetiva:
            discrepancias.append({
                "tipo": "evidencia_vs_conclusion",
                "descripcion": "Evidencia objetiva de lesiones graves contradice conclusión de síntomas menores",
                "evidencia": evidencia_obj,
                "contradiccion": conclusion_subjetiva.group() if conclusion_subjetiva else "Conclusión de síntomas menores",
                "severidad": "media",
                "argumento_juridico": "La evidencia objetiva (RMN, biomecánica) debe prevalecer sobre conclusiones subjetivas"
            })
        
        return discrepancias
    
    def _analizar_evidencia_favorable(self, texto: str) -> List[Dict[str, Any]]:
        """Analiza evidencia médica favorable para IPP"""
        evidencia = []
        texto_lower = texto.lower()
        
        # Evidencia de lesiones estructurales graves
        lesiones_graves = self._buscar_patrones(texto, self.patrones_discrepancias["lesiones_graves"])
        for lesion in lesiones_graves:
            evidencia.append({
                "tipo": "lesion_estructural_grave",
                "descripcion": f"Lesión estructural grave confirmada: {lesion['texto']}",
                "relevancia": "alta",
                "argumento": "Las lesiones estructurales graves son incompatibles con LPNI",
                "posicion": lesion.get('posicion', 0)
            })
        
        # Evidencia de limitaciones funcionales objetivas
        limitaciones = self._buscar_patrones(texto, self.patrones_discrepancias["limitaciones_funcionales"])
        for limitacion in limitaciones:
            evidencia.append({
                "tipo": "limitacion_funcional_objetiva",
                "descripcion": f"Limitación funcional objetiva: {limitacion['texto']}",
                "relevancia": "alta",
                "argumento": "Las limitaciones funcionales objetivas indican incapacidad para el trabajo",
                "posicion": limitacion.get('posicion', 0)
            })
        
        # Evidencia de duración prolongada
        duracion = re.search(r"(?:durante\s+)?(\d+)\s*(?:meses?|años?)", texto_lower)
        if duracion:
            meses = int(duracion.group(1))
            if meses >= 12:  # Más de un año
                evidencia.append({
                    "tipo": "duracion_prolongada",
                    "descripcion": f"Proceso de {meses} meses de duración",
                    "relevancia": "media",
                    "argumento": "La duración prolongada descarta una simple lesión no invalidante",
                    "posicion": duracion.start()
                })
        
        return evidencia
    
    def _detectar_contradicciones_internas(self, texto: str) -> List[Dict[str, Any]]:
        """Detecta contradicciones internas en el informe"""
        contradicciones = []
        
        for patron in self.patrones_discrepancias["contradicciones_internas"]:
            matches = re.finditer(patron, texto, re.IGNORECASE | re.DOTALL)
            for match in matches:
                contradicciones.append({
                    "tipo": "contradiccion_interna",
                    "descripcion": "Contradicción interna detectada en el informe",
                    "texto": match.group(),
                    "posicion": match.start(),
                    "severidad": "alta",
                    "argumento": "Las contradicciones internas debilitan la credibilidad del informe"
                })
        
        return contradicciones
    
    def _generar_argumentos_juridicos(self, texto: str, discrepancias: List[Dict], evidencia: List[Dict]) -> List[Dict[str, Any]]:
        """Genera argumentos jurídicos específicos basados en las discrepancias detectadas"""
        argumentos = []
        
        # Solo agregar argumentos si hay evidencia específica del documento
        if evidencia:
            # Argumento principal solo si hay evidencia específica
            argumentos.append({
                "tipo": "argumento_principal",
                "titulo": "Aplicación del Art. 194.2 LGSS",
                "contenido": f"Disminución ≥33% en el rendimiento normal de la profesión habitual. Evidencia específica: {len(evidencia)} elementos documentados",
                "evidencia_soporte": [e["descripcion"] for e in evidencia[:2]],
                "fuerza": "alta"
            })
        
        # Argumentos específicos solo por discrepancias reales detectadas
        for discrepancia in discrepancias:
            if discrepancia["tipo"] == "lesiones_graves_vs_lpni":
                argumentos.append({
                    "tipo": "argumento_especifico",
                    "titulo": "Incompatibilidad LPNI con lesiones graves",
                    "contenido": f"Las lesiones estructurales graves documentadas son anatómicamente incompatibles con LPNI. Evidencia: {len(discrepancia.get('evidencia', []))} hallazgos específicos",
                    "evidencia_soporte": discrepancia.get("evidencia", []),
                    "fuerza": "alta"
                })
            
            elif discrepancia["tipo"] == "limitaciones_vs_alta":
                argumentos.append({
                    "tipo": "argumento_especifico",
                    "titulo": "Contradicción entre limitaciones documentadas y alta médica",
                    "contenido": f"Las limitaciones funcionales objetivas documentadas contradicen directamente la conclusión de alta sin limitaciones. Hallazgos: {len(discrepancia.get('evidencia', []))} limitaciones específicas",
                    "evidencia_soporte": discrepancia.get("evidencia", []),
                    "fuerza": "alta"
                })
        
        # Solo agregar argumentos de defensa si hay discrepancias reales
        if discrepancias and len(discrepancias) > 0:
            argumentos.append({
                "tipo": "argumento_defensa",
                "titulo": "Estrategia de defensa específica",
                "contenido": f"Enfocar la defensa en las {len(discrepancias)} discrepancias detectadas entre evidencia médica y calificación legal",
                "evidencia_soporte": [],
                "fuerza": "alta"
            })
        
        return argumentos
    
    def _generar_recomendaciones_defensa(self, texto: str, discrepancias: List[Dict], evidencia: List[Dict], contradicciones: List[Dict]) -> List[Dict[str, Any]]:
        """Genera recomendaciones específicas para la defensa"""
        recomendaciones = []
        
        # Recomendaciones basadas en discrepancias detectadas
        if discrepancias:
            recomendaciones.append({
                "tipo": "recomendacion_principal",
                "titulo": "Enfocar la defensa en las discrepancias detectadas",
                "contenido": f"Se han detectado {len(discrepancias)} discrepancias importantes que pueden ser utilizadas como argumentos centrales de la defensa",
                "acciones": [
                    "Destacar las contradicciones entre evidencia médica y calificación legal",
                    "Presentar la evidencia objetiva como prueba de incapacidad",
                    "Argumentar la incompatibilidad entre lesiones graves y LPNI"
                ],
                "prioridad": "alta"
            })
        
        # Recomendaciones específicas solo por tipo de evidencia encontrada
        tipos_evidencia = set(e["tipo"] for e in evidencia)
        if "lesion_estructural_grave" in tipos_evidencia:
            recomendaciones.append({
                "tipo": "recomendacion_especifica",
                "titulo": "Utilizar evidencia de lesiones estructurales graves",
                "contenido": f"Las lesiones estructurales graves documentadas ({len([e for e in evidencia if e['tipo'] == 'lesion_estructural_grave'])}) son incompatibles con LPNI",
                "acciones": [
                    "Presentar informes de imagen (RMN) como prueba objetiva",
                    "Argumentar que las lesiones estructurales requieren cirugía reconstructiva",
                    "Demostrar que la gravedad anatómica excluye LPNI"
                ],
                "prioridad": "alta"
            })
        
        if "limitacion_funcional_objetiva" in tipos_evidencia:
            recomendaciones.append({
                "tipo": "recomendacion_especifica",
                "titulo": "Enfatizar limitaciones funcionales objetivas",
                "contenido": f"Las {len([e for e in evidencia if e['tipo'] == 'limitacion_funcional_objetiva'])} limitaciones funcionales objetivas documentadas demuestran incapacidad",
                "acciones": [
                    "Presentar informes de biomecánica como prueba objetiva",
                    "Demostrar que las limitaciones activas impiden el trabajo",
                    "Argumentar que la diferencia pasiva/activa es clave para el trabajo"
                ],
                "prioridad": "alta"
            })
        
        # Solo agregar recomendaciones generales si no hay evidencia específica
        if not evidencia and not discrepancias:
            recomendaciones.append({
                "tipo": "recomendacion_general",
                "titulo": "Estrategia general de defensa",
            "contenido": "Enfocar la defensa en la evidencia objetiva y las contradicciones del informe",
            "acciones": [
                "Preparar argumentos basados en el Art. 194.2 LGSS",
                "Documentar todas las limitaciones funcionales",
                "Presentar evidencia de duración prolongada del proceso",
                "Destacar las contradicciones internas del informe"
            ],
            "prioridad": "media"
        })
        
        return recomendaciones
    
    def _calcular_puntuacion_discrepancia(self, discrepancias: List[Dict], evidencia: List[Dict], contradicciones: List[Dict]) -> int:
        """Calcula una puntuación de discrepancia (0-100)"""
        puntuacion = 0
        
        # Puntuación por discrepancias
        for discrepancia in discrepancias:
            if discrepancia["severidad"] == "alta":
                puntuacion += 25
            elif discrepancia["severidad"] == "media":
                puntuacion += 15
            else:
                puntuacion += 10
        
        # Puntuación por evidencia favorable
        for ev in evidencia:
            if ev["relevancia"] == "alta":
                puntuacion += 15
            elif ev["relevancia"] == "media":
                puntuacion += 10
            else:
                puntuacion += 5
        
        # Puntuación por contradicciones
        puntuacion += len(contradicciones) * 10
        
        return min(100, puntuacion)
    
    def _calcular_probabilidad_ipp(self, texto: str, discrepancias: List[Dict], evidencia: List[Dict]) -> float:
        """Calcula la probabilidad de que el caso corresponda a IPP (0.0-1.0)"""
        probabilidad = 0.0
        
        # Base: presencia de evidencia favorable
        if evidencia:
            probabilidad += 0.3
        
        # Incremento por discrepancias detectadas
        if discrepancias:
            probabilidad += min(0.4, len(discrepancias) * 0.1)
        
        # Incremento por tipos específicos de evidencia
        tipos_evidencia = [e["tipo"] for e in evidencia]
        if "lesion_estructural_grave" in tipos_evidencia:
            probabilidad += 0.2
        if "limitacion_funcional_objetiva" in tipos_evidencia:
            probabilidad += 0.2
        if "duracion_prolongada" in tipos_evidencia:
            probabilidad += 0.1
        
        return min(1.0, probabilidad)
    
    def _generar_resumen_ejecutivo(self, resultado: Dict[str, Any]) -> str:
        """Genera un resumen ejecutivo del análisis"""
        discrepancias = resultado["discrepancias_detectadas"]
        evidencia = resultado["evidencia_favorable"]
        probabilidad = resultado["probabilidad_ipp"]
        puntuacion = resultado["puntuacion_discrepancia"]
        
        resumen = f"ANÁLISIS DE DISCREPANCIAS MÉDICAS-LEGALES\n\n"
        resumen += f"📊 RESUMEN EJECUTIVO:\n"
        resumen += f"• Discrepancias detectadas: {len(discrepancias)}\n"
        resumen += f"• Evidencia favorable: {len(evidencia)} elementos\n"
        resumen += f"• Puntuación de discrepancia: {puntuacion}/100\n"
        resumen += f"• Probabilidad de IPP: {probabilidad:.1%}\n\n"
        
        if probabilidad >= 0.7:
            resumen += "🎯 CONCLUSIÓN: ALTA PROBABILIDAD DE IPP\n"
            resumen += "El análisis revela evidencia sólida que respalda la calificación de Incapacidad Permanente Parcial.\n"
        elif probabilidad >= 0.5:
            resumen += "⚠️ CONCLUSIÓN: PROBABILIDAD MEDIA DE IPP\n"
            resumen += "Se detectan elementos que sugieren IPP, pero se requiere análisis adicional.\n"
        else:
            resumen += "❌ CONCLUSIÓN: BAJA PROBABILIDAD DE IPP\n"
            resumen += "La evidencia disponible no respalda claramente la calificación de IPP.\n"
        
        if discrepancias:
            resumen += f"\n🔍 DISCREPANCIAS PRINCIPALES:\n"
            for i, disc in enumerate(discrepancias[:3], 1):
                resumen += f"{i}. {disc['descripcion']}\n"
        
        if evidencia:
            resumen += f"\n✅ EVIDENCIA CLAVE:\n"
            for i, ev in enumerate(evidencia[:3], 1):
                resumen += f"{i}. {ev['descripcion']}\n"
        
        return resumen
    
    def _detectar_discrepancias_sentencia(self, texto: str) -> List[Dict[str, Any]]:
        """Detecta discrepancias específicas en sentencias"""
        discrepancias = []
        texto_lower = texto.lower()
        
        # Detectar sentencias que hablan de informes médicos
        if "informe" in texto_lower and ("médico" in texto_lower or "médica" in texto_lower):
            discrepancias.append({
                "tipo": "sentencia_referencia_informe",
                "descripcion": "La sentencia hace referencia a un informe médico que no está presente en este documento",
                "severidad": "media",
                "argumento_juridico": "La sentencia se basa en un informe médico que debe ser analizado por separado"
            })
        
        # Detectar conclusiones sobre IPP vs LPNI
        if "incapacidad permanente parcial" in texto_lower or "ipp" in texto_lower:
            discrepancias.append({
                "tipo": "conclusion_ipp",
                "descripcion": "La sentencia contiene conclusiones sobre Incapacidad Permanente Parcial",
                "severidad": "alta",
                "argumento_juridico": "Las conclusiones sobre IPP en la sentencia son vinculantes"
            })
        
        return discrepancias
    
    def _analizar_evidencia_sentencia(self, texto: str) -> List[Dict[str, Any]]:
        """Analiza evidencia específica en sentencias"""
        evidencia = []
        texto_lower = texto.lower()
        
        # Evidencia de fundamentos jurídicos
        if "artículo" in texto_lower and ("194" in texto or "lgss" in texto_lower):
            evidencia.append({
                "tipo": "fundamento_legal",
                "descripcion": "La sentencia contiene fundamentos jurídicos específicos (Art. 194 LGSS)",
                "fuerza": "alta",
                "contexto": "Fundamento legal para IPP"
            })
        
        # Evidencia de lesiones mencionadas
        if "supraespinoso" in texto_lower or "hombro" in texto_lower:
            evidencia.append({
                "tipo": "lesion_especifica",
                "descripcion": "La sentencia menciona lesiones específicas del supraespinoso/hombro",
                "fuerza": "alta",
                "contexto": "Lesiones anatómicas específicas documentadas"
            })
        
        return evidencia
    
    def _detectar_contradicciones_sentencia(self, texto: str) -> List[Dict[str, Any]]:
        """Detecta contradicciones específicas en sentencias"""
        contradicciones = []
        texto_lower = texto.lower()
        
        # Detectar contradicciones entre estimación y desestimación
        if "estimamos" in texto_lower and "desestimamos" in texto_lower:
            contradicciones.append({
                "tipo": "contradiccion_estimacion",
                "descripcion": "La sentencia contiene tanto estimación como desestimación de pretensiones",
                "severidad": "alta",
                "argumento": "Contradicción en las conclusiones de la sentencia"
            })
        
        return contradicciones
    
    def _generar_argumentos_sentencia(self, texto: str, discrepancias: List[Dict], evidencia: List[Dict]) -> List[Dict[str, Any]]:
        """Genera argumentos específicos para sentencias"""
        argumentos = []
        
        # Argumento principal para sentencias
        if evidencia:
            argumentos.append({
                "tipo": "argumento_sentencia",
                "titulo": "Análisis de Sentencia Judicial",
                "contenido": f"Esta es una sentencia del Tribunal Supremo que contiene {len(evidencia)} elementos de evidencia específicos",
                "evidencia_soporte": [e["descripcion"] for e in evidencia],
                "fuerza": "alta"
            })
        
        # Argumentos específicos por discrepancias
        for discrepancia in discrepancias:
            if discrepancia["tipo"] == "sentencia_referencia_informe":
                argumentos.append({
                    "tipo": "argumento_referencia",
                    "titulo": "Referencia a Informe Médico",
                    "contenido": "La sentencia hace referencia a un informe médico que debe ser analizado por separado para un análisis completo",
                    "evidencia_soporte": [],
                    "fuerza": "media"
                })
        
        return argumentos
    
    def _generar_recomendaciones_sentencia(self, texto: str, discrepancias: List[Dict], evidencia: List[Dict], contradicciones: List[Dict]) -> List[Dict[str, Any]]:
        """Genera recomendaciones específicas para sentencias"""
        recomendaciones = []
        
        # Recomendación principal para sentencias
        recomendaciones.append({
            "tipo": "recomendacion_sentencia",
            "titulo": "Análisis de Sentencia Judicial",
            "contenido": f"Esta es una sentencia del Tribunal Supremo. Se detectaron {len(evidencia)} elementos de evidencia y {len(discrepancias)} discrepancias específicas",
            "acciones": [
                "Analizar los fundamentos jurídicos aplicados",
                "Revisar las conclusiones sobre IPP vs LPNI",
                "Identificar referencias a informes médicos",
                "Evaluar la coherencia de la argumentación"
            ],
            "prioridad": "alta"
        })
        
        # Recomendaciones específicas por evidencia
        for ev in evidencia:
            if ev["tipo"] == "fundamento_legal":
                recomendaciones.append({
                    "tipo": "recomendacion_legal",
                    "titulo": "Análisis de Fundamentos Legales",
                    "contenido": "La sentencia contiene fundamentos jurídicos específicos que deben ser analizados",
                    "acciones": [
                        "Revisar la aplicación del Art. 194 LGSS",
                        "Analizar la interpretación jurídica",
                        "Evaluar la coherencia con la jurisprudencia"
                    ],
                    "prioridad": "alta"
                })
        
        return recomendaciones
    
    def _calcular_puntuacion_sentencia(self, discrepancias: List[Dict], evidencia: List[Dict], contradicciones: List[Dict]) -> int:
        """Calcula puntuación específica para sentencias"""
        puntuacion = 0
        
        # Base por evidencia
        puntuacion += len(evidencia) * 10
        
        # Por discrepancias
        puntuacion += len(discrepancias) * 15
        
        # Por contradicciones
        puntuacion += len(contradicciones) * 20
        
        return min(100, puntuacion)
    
    def _calcular_probabilidad_sentencia(self, texto: str, discrepancias: List[Dict], evidencia: List[Dict]) -> float:
        """Calcula probabilidad específica para sentencias"""
        probabilidad = 0.0
        texto_lower = texto.lower()
        
        # Si la sentencia menciona IPP, alta probabilidad
        if "incapacidad permanente parcial" in texto_lower or "ipp" in texto_lower:
            probabilidad = 0.8
        
        # Ajuste por evidencia
        probabilidad += len(evidencia) * 0.05
        
        return min(1.0, probabilidad)
    
    def _generar_resumen_sentencia(self, resultado: Dict[str, Any]) -> str:
        """Genera resumen específico para sentencias"""
        discrepancias = resultado["discrepancias_detectadas"]
        evidencia = resultado["evidencia_favorable"]
        probabilidad = resultado["probabilidad_ipp"]
        puntuacion = resultado["puntuacion_discrepancia"]
        
        resumen = f"ANÁLISIS DE SENTENCIA JUDICIAL\n\n"
        resumen += f"📊 RESUMEN EJECUTIVO:\n"
        resumen += f"• Tipo de documento: Sentencia del Tribunal Supremo\n"
        resumen += f"• Elementos de evidencia: {len(evidencia)}\n"
        resumen += f"• Discrepancias detectadas: {len(discrepancias)}\n"
        resumen += f"• Puntuación de análisis: {puntuacion}/100\n"
        resumen += f"• Relevancia para IPP: {probabilidad:.1%}\n\n"
        
        if probabilidad >= 0.7:
            resumen += "🎯 CONCLUSIÓN: SENTENCIA RELEVANTE PARA IPP\n"
            resumen += "La sentencia contiene elementos importantes para casos de IPP.\n"
        elif probabilidad >= 0.4:
            resumen += "⚠️ CONCLUSIÓN: SENTENCIA PARCIALMENTE RELEVANTE\n"
            resumen += "La sentencia contiene algunos elementos útiles para el análisis.\n"
        else:
            resumen += "ℹ️ CONCLUSIÓN: SENTENCIA DE REFERENCIA\n"
            resumen += "Esta sentencia puede servir como referencia jurídica.\n"
        
        if evidencia:
            resumen += f"\n✅ ELEMENTOS CLAVE:\n"
            for i, ev in enumerate(evidencia[:3], 1):
                resumen += f"{i}. {ev['descripcion']}\n"
        
        return resumen
    
    def _buscar_patrones(self, texto: str, patrones: List[str]) -> List[Dict[str, Any]]:
        """Busca patrones específicos en el texto"""
        resultados = []
        texto_lower = texto.lower()
        
        for patron in patrones:
            matches = re.finditer(patron, texto_lower)
            for match in matches:
                resultados.append({
                    "patron": patron,
                    "texto": texto[match.start():match.end()],
                    "posicion": match.start(),
                    "contexto": self._obtener_contexto(texto, match.start(), match.end())
                })
        
        return resultados
    
    def _obtener_contexto(self, texto: str, start: int, end: int, caracteres: int = 200) -> str:
        """Obtiene contexto alrededor de una coincidencia"""
        context_start = max(0, start - caracteres)
        context_end = min(len(texto), end + caracteres)
        return texto[context_start:context_end]


def crear_analizador_discrepancias() -> AnalizadorDiscrepancias:
    """Crea una instancia del analizador de discrepancias"""
    return AnalizadorDiscrepancias()


if __name__ == "__main__":
    # Prueba del analizador
    analizador = AnalizadorDiscrepancias()
    print("✅ Analizador de discrepancias inicializado correctamente")
    print(f"Patrones cargados: {len(analizador.patrones_discrepancias)} categorías")
    print(f"Argumentos jurídicos: {len(analizador.argumentos_juridicos)} categorías")

