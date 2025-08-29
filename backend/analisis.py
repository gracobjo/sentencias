#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Análisis de IA para Documentos Legales
Asume que el modelo ya está entrenado y guardado
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
import pickle

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalizadorLegal:
    """
    Analizador legal basado en IA pre-entrenada
    Asume que el modelo ya está entrenado y guardado
    """
    
    def __init__(self, modelo_path: str = "models/modelo_legal.pkl"):
        """
        Inicializa el analizador con el modelo pre-entrenado
        
        Args:
            modelo_path: Ruta al archivo del modelo guardado
        """
        self.modelo_path = Path(modelo_path)
        self.modelo = None
        self.vectorizador = None
        self.clasificador = None
        self.frases_clave = self._cargar_frases_clave()
        
        # Intentar cargar el modelo
        self._cargar_modelo()
    
    def _cargar_frases_clave(self) -> Dict[str, List[str]]:
        """Carga las frases clave desde archivo de configuración"""
        frases_default = {
            "incapacidad_permanente_parcial": [
                "incapacidad permanente parcial", "IPP", "permanente parcial",
                "incapacidad parcial permanente", "secuela permanente",
                "incapacidad permanente", "secuelas permanentes"
            ],
            "reclamacion_administrativa": [
                "reclamación administrativa previa", "RAP", "reclamación previa",
                "vía administrativa", "recurso administrativo", "reclamación"
            ],
            "inss": [
                "INSS", "Instituto Nacional de la Seguridad Social", "Seguridad Social",
                "Instituto Nacional", "Seguridad Social"
            ],
            "lesiones_permanentes": [
                "lesiones permanentes no incapacitantes", "LPNI", "secuelas",
                "lesiones permanentes", "secuelas permanentes", "lesiones"
            ],
            "personal_limpieza": [
                "limpiadora", "personal de limpieza", "servicios de limpieza",
                "trabajador de limpieza", "empleada de limpieza", "limpieza"
            ],
            "lesiones_hombro": [
                "rotura del manguito rotador", "supraespinoso", "hombro derecho",
                "lesión de hombro", "manguito rotador", "tendón supraespinoso",
                "hombro", "manguito"
            ],
            "procedimiento_legal": [
                "procedente", "desestimamos", "estimamos", "fundada",
                "infundada", "accedemos", "concedemos", "reconocemos"
            ]
        }
        
        # Intentar cargar desde archivo de configuración
        config_path = Path("models/frases_clave.json")
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"No se pudo cargar configuración de frases clave: {e}")
        
        return frases_default
    
    def _cargar_modelo(self):
        """Carga el modelo pre-entrenado"""
        try:
            if self.modelo_path.exists():
                with open(self.modelo_path, 'rb') as f:
                    modelo_data = pickle.load(f)
                    self.modelo = modelo_data.get('modelo')
                    self.vectorizador = modelo_data.get('vectorizador')
                    self.clasificador = modelo_data.get('clasificador')
                    logger.info("✅ Modelo de IA cargado correctamente")
            else:
                logger.warning(f"⚠️ Modelo no encontrado en {self.modelo_path}")
                logger.info("Se usará análisis basado en reglas")
        except Exception as e:
            logger.error(f"❌ Error cargando modelo: {e}")
            logger.info("Se usará análisis basado en reglas")
    
    def analizar_documento(self, ruta_archivo: str) -> Dict[str, Any]:
        """
        Analiza un documento legal usando IA
        
        Args:
            ruta_archivo: Ruta al archivo a analizar
            
        Returns:
            Diccionario con resultados del análisis
        """
        try:
            # Leer contenido del archivo
            contenido = self._leer_archivo(ruta_archivo)
            if not contenido:
                return self._crear_resultado_error("No se pudo leer el contenido del archivo")
            
            # Extraer nombre del archivo de la ruta
            nombre_archivo = Path(ruta_archivo).name
            
            # Análisis con IA si está disponible
            if self.modelo and self.vectorizador and self.clasificador:
                resultado = self._analisis_con_ia(contenido, nombre_archivo)
            else:
                resultado = self._analisis_basado_reglas(contenido, nombre_archivo)
            
            # Agregar metadatos
            resultado.update({
                "archivo": ruta_archivo,
                "nombre_archivo": Path(ruta_archivo).name,
                "procesado": True,
                "texto_extraido": contenido,  # Mostrar texto completo
                "longitud_texto": len(contenido),
                "timestamp": self._obtener_timestamp(),
                "ruta_archivo": ruta_archivo
            })
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error analizando documento: {e}")
            return self._crear_resultado_error(f"Error en análisis: {str(e)}")
    
    def _leer_archivo(self, ruta: str) -> Optional[str]:
        """Lee el contenido de un archivo"""
        try:
            if ruta.endswith('.txt'):
                # Intentar diferentes encodings
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        with open(ruta, 'r', encoding=encoding) as f:
                            return f.read().strip()
                    except UnicodeDecodeError:
                        continue
                return None
            elif ruta.endswith('.pdf'):
                # Leer archivo PDF
                return self._leer_pdf(ruta)
            else:
                # Para otros formatos, usar función genérica
                return self._leer_archivo_generico(ruta)
        except Exception as e:
            logger.error(f"Error leyendo archivo {ruta}: {e}")
            return None
    
    def _leer_archivo_generico(self, ruta: str) -> str:
        """Lee archivos de diferentes formatos"""
        # Por ahora solo manejamos texto
        # Aquí se podría extender para PDF, DOC, etc.
        return "Contenido del archivo no disponible en formato de texto"
    
    def _leer_pdf(self, ruta: str) -> Optional[str]:
        """Lee archivos PDF y extrae el texto"""
        try:
            # Intentar importar PyPDF2
            try:
                import PyPDF2
            except ImportError:
                logger.warning("PyPDF2 no está instalado. Instala: pip install PyPDF2")
                return "Error: PyPDF2 no está instalado. Ejecuta: pip install PyPDF2"
            
            texto = ""
            with open(ruta, 'rb') as archivo:
                lector = PyPDF2.PdfReader(archivo)
                
                for pagina in lector.pages:
                    texto += pagina.extract_text() + "\n"
                
                return texto.strip()
                
        except Exception as e:
            logger.error(f"Error leyendo PDF {ruta}: {e}")
            return f"Error leyendo PDF: {str(e)}"
    
    def _analisis_con_ia(self, contenido: str, nombre_archivo: str = None) -> Dict[str, Any]:
        """Análisis usando el modelo de IA"""
        try:
            # Vectorizar el texto
            texto_vectorizado = self.vectorizador.transform([contenido])
            
            # Predicción
            prediccion = self.clasificador.predict(texto_vectorizado)[0]
            probabilidades = self.clasificador.predict_proba(texto_vectorizado)[0]
            
            # Obtener confianza
            confianza = max(probabilidades)
            
            # Análisis de frases clave
            frases_encontradas = self._analizar_frases_clave(contenido, nombre_archivo)
            
            # Extraer argumentos
            argumentos = self._extraer_argumentos_avanzados(contenido)
            
            # Generar insights
            insights = self._generar_insights_avanzados(prediccion, frases_encontradas, confianza)
            
            return {
                "prediccion": {
                    "es_favorable": bool(prediccion),
                    "confianza": float(confianza),
                    "interpretacion": "Favorable" if prediccion else "Desfavorable",
                    "probabilidades": {
                        "favorable": float(probabilidades[1] if len(probabilidades) > 1 else 0.5),
                        "desfavorable": float(probabilidades[0] if len(probabilidades) > 1 else 0.5)
                    }
                },
                "argumentos": argumentos,
                "frases_clave": frases_encontradas,
                "resumen_inteligente": self._generar_resumen_ia(prediccion, confianza, frases_encontradas),
                "insights_juridicos": insights,
                "total_frases_clave": sum(datos["total"] for datos in frases_encontradas.values()),
                "modelo_ia": True,
                "metodo_analisis": "IA pre-entrenada"
            }
            
        except Exception as e:
            logger.error(f"Error en análisis con IA: {e}")
            # Fallback a análisis basado en reglas
            return self._analisis_basado_reglas(contenido, nombre_archivo)
    
    def _analisis_basado_reglas(self, contenido: str, nombre_archivo: str = None) -> Dict[str, Any]:
        """Análisis basado en reglas y patrones"""
        # Análisis de frases clave
        frases_encontradas = self._analizar_frases_clave(contenido, nombre_archivo)
        
        # Predicción basada en reglas
        prediccion = self._prediccion_basada_reglas(contenido)
        
        # Extraer argumentos
        argumentos = self._extraer_argumentos_basicos(contenido)
        
        # Generar insights
        insights = self._generar_insights_basicos(prediccion, frases_encontradas)
        
        return {
            "prediccion": prediccion,
            "argumentos": argumentos,
            "frases_clave": frases_encontradas,
            "resumen_inteligente": self._generar_resumen_reglas(prediccion, frases_encontradas),
            "insights_juridicos": insights,
            "total_frases_clave": sum(datos["total"] for datos in frases_encontradas.values()),
            "modelo_ia": False,
            "metodo_analisis": "Reglas y patrones"
        }
    
    def _analizar_frases_clave(self, texto: str, nombre_archivo: str = None) -> Dict[str, Any]:
        """Analiza las frases clave en el texto"""
        if not texto:
            return {}
        
        # Usar el nombre del archivo real o un valor por defecto
        archivo_nombre = nombre_archivo or "archivo_desconocido"
        
        resultados = {}
        for categoria, variantes in self.frases_clave.items():
            total = 0
            ocurrencias = []
            
            for variante in variantes:
                patron = re.compile(re.escape(variante), re.IGNORECASE)
                matches = patron.finditer(texto)
                
                for match in matches:
                    total += 1
                    start_pos = match.start()
                    end_pos = match.end()
                    
                    # Obtener contexto (300 caracteres antes y después para mayor claridad)
                    context_start = max(0, start_pos - 300)
                    context_end = min(len(texto), end_pos + 300)
                    contexto = texto[context_start:context_end]
                    
                    # Marcar la frase encontrada
                    frase_encontrada = texto[start_pos:end_pos]
                    contexto_marcado = contexto.replace(frase_encontrada, f"**{frase_encontrada}**")
                    
                    ocurrencias.append({
                        "frase": variante,
                        "posicion": start_pos,
                        "contexto": contexto_marcado,
                        "linea": texto[:start_pos].count('\n') + 1,
                        "archivo": archivo_nombre
                    })
            
            if total > 0:
                # Obtener frases únicas encontradas
                frases_encontradas = list(set([oc["frase"] for oc in ocurrencias]))
                
                resultados[categoria] = {
                    "total": total,
                    "ocurrencias": ocurrencias,
                    "frases": frases_encontradas
                }
        
        return resultados
    
    def _prediccion_basada_reglas(self, texto: str) -> Dict[str, Any]:
        """Predicción basada en reglas y patrones con sistema de confianza avanzado y detección automática de factores"""
        
        # Sistema de puntuación avanzado con detección automática
        puntuacion = 0
        factores = {}
        
        texto_lower = texto.lower()
        
        # 1. ANÁLISIS AVANZADO DE PALABRAS CLAVE (peso: 25%)
        palabras_favorables = [
            "procedente", "estimamos", "accedemos", "concedemos", "reconocemos",
            "favorable", "justificado", "acreditado", "confirmado", "establecido",
            "fundada", "procede", "accede", "concede", "reconoce", "estimamos",
            "accedemos", "concedemos", "reconocemos", "estimamos", "accedemos"
        ]
        
        palabras_desfavorables = [
            "desestimamos", "infundada", "rechazamos", "denegamos", "no procedente",
            "desfavorable", "no acreditado", "insuficiente", "negligencia", "culpabilidad",
            "infundada", "desestima", "rechaza", "denega", "desestimamos"
        ]
        
        favorables = sum(1 for palabra in palabras_favorables if palabra in texto_lower)
        desfavorables = sum(1 for palabra in palabras_desfavorables if palabra in texto_lower)
        
        total_palabras = favorables + desfavorables
        if total_palabras > 0:
            score_palabras = (favorables - desfavorables) / total_palabras
            puntuacion += score_palabras * 0.25
            factores["palabras_clave"] = {
                "favorables": favorables,
                "desfavorables": desfavorables,
                "score": round(score_palabras, 3),
                "peso": 0.25,
                "recomendacion": self._generar_recomendacion_palabras_clave(favorables, desfavorables)
            }
        
        # 2. ANÁLISIS AVANZADO DE ESTRUCTURA DEL DOCUMENTO (peso: 20%)
        estructura_score = 0
        estructura_elementos = []
        
        if "argumentos" in texto_lower or "fundamentos" in texto_lower:
            estructura_score += 0.3
            estructura_elementos.append("argumentos/fundamentos")
        if "conclusiones" in texto_lower or "resolucion" in texto_lower:
            estructura_score += 0.3
            estructura_elementos.append("conclusiones/resolución")
        if "hechos" in texto_lower or "antecedentes" in texto_lower:
            estructura_score += 0.2
            estructura_elementos.append("hechos/antecedentes")
        if "solicitud" in texto_lower or "petitum" in texto_lower:
            estructura_score += 0.2
            estructura_elementos.append("solicitud/petitum")
        
        puntuacion += estructura_score * 0.2
        factores["estructura"] = {
            "score": round(estructura_score, 3),
            "peso": 0.2,
            "elementos_detectados": estructura_elementos,
            "recomendacion": self._generar_recomendacion_estructura(estructura_score, estructura_elementos)
        }
        
        # 3. ANÁLISIS AVANZADO DE EVIDENCIA MÉDICA (peso: 20%)
        evidencia_score = 0
        evidencia_elementos = []
        
        if "informe médico" in texto_lower or "dictamen pericial" in texto_lower:
            evidencia_score += 0.4
            evidencia_elementos.append("informe médico/dictamen pericial")
        if "lesiones" in texto_lower and ("grave" in texto_lower or "permanente" in texto_lower):
            evidencia_score += 0.3
            evidencia_elementos.append("lesiones graves/permanentes")
        if "accidente laboral" in texto_lower:
            evidencia_score += 0.2
            evidencia_elementos.append("accidente laboral")
        if "secuelas" in texto_lower:
            evidencia_score += 0.1
            evidencia_elementos.append("secuelas")
        
        puntuacion += evidencia_score * 0.2
        factores["evidencia"] = {
            "score": round(evidencia_score, 3),
            "peso": 0.2,
            "elementos_detectados": evidencia_elementos,
            "recomendacion": self._generar_recomendacion_evidencia(evidencia_score, evidencia_elementos)
        }
        
        # 4. ANÁLISIS AVANZADO DE PROCEDIMIENTO LEGAL (peso: 15%)
        procedimiento_score = 0
        procedimiento_elementos = []
        
        if "reclamación administrativa previa" in texto_lower:
            procedimiento_score += 0.4
            procedimiento_elementos.append("reclamación administrativa previa")
        if "trámite" in texto_lower and "cumplido" in texto_lower:
            procedimiento_score += 0.3
            procedimiento_elementos.append("trámites cumplidos")
        if "plazo" in texto_lower and "dentro" in texto_lower:
            procedimiento_score += 0.2
            procedimiento_score += 0.1
            procedimiento_elementos.append("plazos respetados")
        if "notificación" in texto_lower:
            procedimiento_score += 0.1
            procedimiento_elementos.append("notificaciones")
        
        puntuacion += procedimiento_score * 0.15
        factores["procedimiento"] = {
            "score": round(procedimiento_score, 3),
            "peso": 0.15,
            "elementos_detectados": procedimiento_elementos,
            "recomendacion": self._generar_recomendacion_procedimiento(procedimiento_score, procedimiento_elementos)
        }
        
        # 5. ANÁLISIS AVANZADO DE CONTEXTO TEMPORAL Y LABORAL (peso: 10%)
        contexto_score = 0
        contexto_elementos = []
        
        if "durante" in texto_lower and "jornada" in texto_lower:
            contexto_score += 0.3
            contexto_elementos.append("accidente durante jornada")
        if "lugar de trabajo" in texto_lower:
            contexto_score += 0.3
            contexto_elementos.append("accidente en lugar de trabajo")
        if "medidas de seguridad" in texto_lower:
            contexto_score += 0.2
            contexto_elementos.append("medidas de seguridad")
        if "empresa" in texto_lower and "responsabilidad" in texto_lower:
            contexto_score += 0.2
            contexto_elementos.append("responsabilidad empresarial")
        
        puntuacion += contexto_score * 0.1
        factores["contexto"] = {
            "score": round(contexto_score, 3),
            "peso": 0.1,
            "elementos_detectados": contexto_elementos,
            "recomendacion": self._generar_recomendacion_contexto(contexto_score, contexto_elementos)
        }
        
        # 6. ANÁLISIS AVANZADO DE TERMINOLOGÍA JURÍDICA (peso: 10%)
        terminologia_score = 0
        terminologia_elementos = []
        
        juridicos = ["actor", "demandado", "procedimiento", "instancia", "resolución", "recurso", "fundamento", "considerando"]
        for termino in juridicos:
            if termino in texto_lower:
                terminologia_score += 0.125
                terminologia_elementos.append(termino)
        
        puntuacion += terminologia_score * 0.1
        factores["terminologia"] = {
            "score": round(terminologia_score, 3),
            "peso": 0.1,
            "elementos_detectados": terminologia_elementos,
            "recomendacion": self._generar_recomendacion_terminologia(terminologia_score, terminologia_elementos)
        }
        
        # Normalizar puntuación a rango [0, 1]
        puntuacion = max(-1, min(1, puntuacion))
        
        # Convertir a confianza y decisión
        confianza = abs(puntuacion)
        es_favorable = puntuacion > 0
        
        # Ajustar confianza mínima
        confianza = max(0.3, confianza)
        
        # Calcular interpretación
        if confianza >= 0.8:
            interpretacion = "Muy Favorable" if es_favorable else "Muy Desfavorable"
        elif confianza >= 0.6:
            interpretacion = "Favorable" if es_favorable else "Desfavorable"
        else:
            interpretacion = "Parcialmente Favorable" if es_favorable else "Parcialmente Desfavorable"
        
        # Generar recomendaciones generales
        recomendaciones_generales = self._generar_recomendaciones_generales(factores, confianza, es_favorable)
        
        return {
            "es_favorable": es_favorable,
            "confianza": round(confianza, 3),
            "interpretacion": interpretacion,
            "puntuacion_global": round(puntuacion, 3),
            "factores_analisis": factores,
            "recomendaciones_generales": recomendaciones_generales,
            "metodo": "Reglas y patrones avanzados con detección automática",
            "probabilidad_exito": self._calcular_probabilidad_exito(confianza, factores)
        }
    
    def _generar_recomendacion_palabras_clave(self, favorables: int, desfavorables: int) -> str:
        """Genera recomendaciones específicas para palabras clave"""
        if favorables > desfavorables:
            if favorables >= 5:
                return "✅ Excelente uso de terminología favorable. Mantén este enfoque positivo."
            elif favorables >= 3:
                return "✅ Buen uso de terminología favorable. Considera agregar más términos como 'justificado', 'acreditado'."
            else:
                return "⚠️ Uso limitado de terminología favorable. Agrega términos como 'procedente', 'estimamos', 'accedemos'."
        else:
            if desfavorables >= 5:
                return "❌ Uso excesivo de terminología desfavorable. Reemplaza con términos positivos."
            elif desfavorables >= 3:
                return "⚠️ Uso moderado de terminología desfavorable. Revisa y reformula las frases negativas."
            else:
                return "⚠️ Algunos términos desfavorables detectados. Revisa el contexto y reformula si es necesario."
    
    def _generar_recomendacion_estructura(self, score: float, elementos: List[str]) -> str:
        """Genera recomendaciones específicas para la estructura del documento"""
        if score >= 0.8:
            return "✅ Estructura excelente del documento. Incluye todos los elementos necesarios."
        elif score >= 0.6:
            return "✅ Buena estructura del documento. Considera agregar secciones faltantes."
        elif score >= 0.4:
            return "⚠️ Estructura parcial del documento. Agrega secciones como 'argumentos', 'conclusiones'."
        else:
            return "❌ Estructura deficiente del documento. Incluye secciones: hechos, argumentos, conclusiones, solicitud."
    
    def _generar_recomendacion_evidencia(self, score: float, elementos: List[str]) -> str:
        """Genera recomendaciones específicas para evidencia médica"""
        if score >= 0.8:
            return "✅ Excelente evidencia médica. Incluye informes, lesiones y contexto del accidente."
        elif score >= 0.6:
            return "✅ Buena evidencia médica. Considera agregar más detalles sobre lesiones y secuelas."
        elif score >= 0.4:
            return "⚠️ Evidencia médica moderada. Agrega informes médicos y detalles de lesiones."
        else:
            return "❌ Evidencia médica insuficiente. Incluye informes médicos, dictámenes periciales y detalles de lesiones."
    
    def _generar_recomendacion_procedimiento(self, score: float, elementos: List[str]) -> str:
        """Genera recomendaciones específicas para procedimiento legal"""
        if score >= 0.8:
            return "✅ Procedimiento legal excelente. Incluye RAP, trámites y plazos correctamente."
        elif score >= 0.6:
            return "✅ Buen procedimiento legal. Verifica que todos los trámites estén documentados."
        elif score >= 0.4:
            return "⚠️ Procedimiento legal moderado. Asegúrate de incluir RAP y documentar trámites."
        else:
            return "❌ Procedimiento legal deficiente. Incluye reclamación administrativa previa y documenta todos los trámites."
    
    def _generar_recomendacion_contexto(self, score: float, elementos: List[str]) -> str:
        """Genera recomendaciones específicas para contexto laboral"""
        if score >= 0.8:
            return "✅ Excelente contexto laboral. Incluye lugar, jornada y responsabilidad empresarial."
        elif score >= 0.6:
            return "✅ Buen contexto laboral. Agrega detalles sobre medidas de seguridad."
        elif score >= 0.4:
            return "⚠️ Contexto laboral moderado. Incluye detalles sobre lugar de trabajo y jornada laboral."
        else:
            return "❌ Contexto laboral deficiente. Incluye lugar de trabajo, jornada laboral y responsabilidad empresarial."
    
    def _generar_recomendacion_terminologia(self, score: float, elementos: List[str]) -> str:
        """Genera recomendaciones específicas para terminología jurídica"""
        if score >= 0.8:
            return "✅ Excelente uso de terminología jurídica. Incluye todos los términos necesarios."
        elif score >= 0.6:
            return "✅ Buen uso de terminología jurídica. Considera agregar más términos técnicos."
        elif score >= 0.4:
            return "⚠️ Uso moderado de terminología jurídica. Incluye términos como 'actor', 'demandado', 'fundamento'."
        else:
            return "❌ Uso deficiente de terminología jurídica. Incluye términos: actor, demandado, procedimiento, fundamento."
    
    def _generar_recomendaciones_generales(self, factores: Dict, confianza: float, es_favorable: bool) -> List[str]:
        """Genera recomendaciones generales basadas en el análisis completo"""
        recomendaciones = []
        
        # Recomendaciones por nivel de confianza
        if confianza >= 0.8:
            recomendaciones.append("🎯 **ALTA CONFIANZA**: El documento está bien estructurado y argumentado.")
            recomendaciones.append("💡 **RECOMENDACIÓN**: Revisa solo detalles menores antes de presentar.")
        elif confianza >= 0.6:
            recomendaciones.append("✅ **CONFIANZA MEDIA-ALTA**: El documento tiene buena base pero puede mejorarse.")
            recomendaciones.append("💡 **RECOMENDACIÓN**: Implementa las sugerencias específicas para aumentar la confianza.")
        else:
            recomendaciones.append("⚠️ **CONFIANZA BAJA**: El documento necesita mejoras significativas.")
            recomendaciones.append("💡 **RECOMENDACIÓN**: Revisa completamente siguiendo todas las sugerencias.")
        
        # Recomendaciones específicas por factores
        for factor, datos in factores.items():
            if datos.get('score', 0) < 0.5:
                recomendaciones.append(f"🔧 **{factor.replace('_', ' ').title()}**: {datos.get('recomendacion', 'Necesita mejora')}")
        
        # Recomendaciones de probabilidad de éxito
        if es_favorable:
            if confianza >= 0.7:
                recomendaciones.append("🚀 **PROBABILIDAD DE ÉXITO**: ALTA - El caso tiene buenas perspectivas.")
            else:
                recomendaciones.append("📈 **PROBABILIDAD DE ÉXITO**: MEDIA - Con las mejoras sugeridas puede mejorar significativamente.")
        else:
            recomendaciones.append("⚠️ **PROBABILIDAD DE ÉXITO**: BAJA - El caso necesita reformulación completa.")
        
        return recomendaciones
    
    def _calcular_probabilidad_exito(self, confianza: float, factores: Dict) -> Dict[str, Any]:
        """Calcula la probabilidad de éxito basada en confianza y factores"""
        # Calcular score promedio de factores
        scores = [datos.get('score', 0) for datos in factores.values()]
        score_promedio = sum(scores) / len(scores) if scores else 0
        
        # Calcular probabilidad base
        probabilidad_base = (confianza + score_promedio) / 2
        
        # Ajustar por factores críticos
        ajuste = 0
        if 'evidencia' in factores and factores['evidencia'].get('score', 0) >= 0.7:
            ajuste += 0.1
        if 'procedimiento' in factores and factores['procedimiento'].get('score', 0) >= 0.7:
            ajuste += 0.1
        if 'estructura' in factores and factores['estructura'].get('score', 0) >= 0.7:
            ajuste += 0.05
        
        probabilidad_final = min(0.95, probabilidad_base + ajuste)
        
        # Clasificar probabilidad
        if probabilidad_final >= 0.8:
            clasificacion = "Muy Alta"
            color = "success"
        elif probabilidad_final >= 0.6:
            clasificacion = "Alta"
            color = "info"
        elif probabilidad_final >= 0.4:
            clasificacion = "Media"
            color = "warning"
        else:
            clasificacion = "Baja"
            color = "danger"
        
        return {
            "probabilidad": round(probabilidad_final, 3),
            "clasificacion": clasificacion,
            "color": color,
            "score_promedio_factores": round(score_promedio, 3),
            "ajuste_por_factores_criticos": round(ajuste, 3),
            "factores_analizados": len(factores)
        }
    
    def _extraer_argumentos_avanzados(self, texto: str) -> List[Dict[str, Any]]:
        """Extrae argumentos legales avanzados"""
        argumentos = []
        
        patrones_avanzados = [
            r"por\s+(?:lo\s+)?que\s+([^.]*?\.)",
            r"fundamentos?\s+(?:de\s+)?(?:derecho|derecho\s+por\s+lo\s+que)\s+([^.]*?\.)",
            r"considerando\s+que\s+([^.]*?\.)",
            r"vistos\s+([^.]*?\.)",
            r"resultando\s+([^.]*?\.)",
            r"en\s+su\s+virtud\s+([^.]*?\.)",
            r"por\s+ello\s+([^.]*?\.)"
        ]
        
        for patron in patrones_avanzados:
            matches = re.finditer(patron, texto, re.IGNORECASE)
            for match in matches:
                argumento = match.group(1).strip()
                if len(argumento) > 20:
                    # Calcular confianza basada en la longitud y complejidad
                    confianza = min(0.95, 0.6 + (len(argumento) / 1000) * 0.3)
                    
                    argumentos.append({
                        "tipo": "argumento_legal",
                        "texto": argumento,
                        "posicion": match.start(),
                        "confianza": confianza,
                        "categoria": "fundamento_juridico",
                        "longitud": len(argumento)
                    })
        
        return argumentos
    
    def _extraer_argumentos_basicos(self, texto: str) -> List[Dict[str, Any]]:
        """Extrae argumentos legales básicos con contexto mejorado"""
        argumentos = []
        
        patrones = [
            r"por\s+(?:lo\s+)?que\s+([^.]*?\.)",
            r"fundamentos?\s+(?:de\s+)?(?:derecho|derecho\s+por\s+lo\s+que)\s+([^.]*?\.)",
            r"considerando\s+que\s+([^.]*?\.)",
            r"vistos\s+([^.]*?\.)",
            r"resultando\s+([^.]*?\.)",
            r"primer[ao]?\s*[.-]\s*([^.]*?\.)",
            r"segund[ao]?\s*[.-]\s*([^.]*?\.)",
            r"tercer[ao]?\s*[.-]\s*([^.]*?\.)",
            r"decim[ao]?\s*[.-]\s*([^.]*?\.)"
        ]
        
        for patron in patrones:
            matches = re.finditer(patron, texto, re.IGNORECASE)
            for match in matches:
                argumento = match.group(1).strip()
                if len(argumento) > 20:
                    # Obtener contexto más amplio para el argumento
                    start_pos = match.start()
                    end_pos = match.end()
                    
                    # Contexto de 500 caracteres para argumentos completos
                    context_start = max(0, start_pos - 500)
                    context_end = min(len(texto), end_pos + 500)
                    contexto = texto[context_start:context_end]
                    
                    argumentos.append({
                        "tipo": "argumento_legal",
                        "texto": argumento,
                        "posicion": start_pos,
                        "confianza": 0.8,
                        "categoria": "fundamento_juridico",
                        "contexto": contexto
                    })
        
        return argumentos
    
    def _generar_insights_avanzados(self, prediccion: bool, frases_clave: Dict, confianza: float) -> List[str]:
        """Genera insights jurídicos avanzados"""
        insights = []
        
        if prediccion:
            insights.append("El documento presenta argumentos sólidos a favor del caso.")
            insights.append("La resolución favorece al reclamante basándose en evidencia legal.")
        else:
            insights.append("El documento presenta argumentos que pueden ser desfavorables.")
            insights.append("La resolución no favorece al reclamante según el análisis legal.")
        
        if frases_clave:
            categorias = list(frases_clave.keys())
            insights.append(f"Se identificaron {len(categorias)} categorías de frases clave relevantes.")
            
            # Análisis de categorías más importantes
            if "incapacidad_permanente_parcial" in frases_clave:
                insights.append("El caso involucra aspectos de incapacidad permanente parcial.")
            
            if "reclamacion_administrativa" in frases_clave:
                insights.append("Se identificaron elementos de reclamación administrativa previa.")
        
        insights.append(f"Confianza del análisis: {confianza:.1%}")
        insights.append("Análisis realizado con modelo de IA pre-entrenado.")
        
        return insights
    
    def _generar_insights_basicos(self, prediccion: Dict, frases_clave: Dict) -> List[str]:
        """Genera insights jurídicos básicos"""
        insights = []
        
        if prediccion["es_favorable"]:
            insights.append("El documento presenta argumentos sólidos a favor del caso.")
            insights.append("La resolución favorece al reclamante.")
        else:
            insights.append("El documento presenta argumentos que pueden ser desfavorables.")
            insights.append("La resolución no favorece al reclamante.")
        
        if frases_clave:
            categorias = list(frases_clave.keys())
            insights.append(f"Se identificaron {len(categorias)} categorías de frases clave.")
            insights.append(f"Las categorías más relevantes son: {', '.join(categorias[:3])}.")
        
        insights.append(f"Confianza del análisis: {prediccion['confianza']:.1%}")
        insights.append("Análisis realizado con reglas y patrones.")
        
        return insights
    
    def _generar_resumen_ia(self, prediccion: bool, confianza: float, frases_clave: Dict) -> str:
        """Genera resumen inteligente usando IA"""
        if prediccion:
            base = "Análisis favorable del documento legal usando IA. "
        else:
            base = "Análisis desfavorable del documento legal usando IA. "
        
        if frases_clave:
            total_frases = sum(datos["total"] for datos in frases_clave.values())
            base += f"Se identificaron {total_frases} frases clave relevantes. "
        
        base += f"Confianza del análisis: {confianza:.1%}. "
        base += "Análisis realizado con modelo de IA pre-entrenado."
        
        return base
    
    def _generar_resumen_reglas(self, prediccion: Dict, frases_clave: Dict) -> str:
        """Genera resumen basado en reglas con análisis detallado"""
        if prediccion["es_favorable"]:
            base = "Análisis favorable del documento legal. "
        else:
            base = "Análisis desfavorable del documento legal. "
        
        if frases_clave:
            total_frases = sum(datos["total"] for datos in frases_clave.values())
            base += f"Se identificaron {total_frases} frases clave relevantes. "
        
        # Agregar información de factores si está disponible
        if "factores_analisis" in prediccion:
            factores = prediccion["factores_analisis"]
            base += "Factores analizados: "
            
            if "palabras_clave" in factores:
                base += f"Palabras clave ({factores['palabras_clave']['score']:.2f}), "
            if "estructura" in factores:
                base += f"Estructura ({factores['estructura']['score']:.2f}), "
            if "evidencia" in factores:
                base += f"Evidencia médica ({factores['evidencia']['score']:.2f}), "
            if "procedimiento" in factores:
                base += f"Procedimiento legal ({factores['procedimiento']['score']:.2f}), "
            if "contexto" in factores:
                base += f"Contexto laboral ({factores['contexto']['score']:.2f}). "
        
        base += f"Confianza del análisis: {prediccion['confianza']:.1%}. "
        base += f"Método: {prediccion.get('metodo', 'Reglas y patrones')}."
        
        return base
    
    def _obtener_timestamp(self) -> str:
        """Obtiene el timestamp actual"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _crear_resultado_error(self, mensaje: str) -> Dict[str, Any]:
        """Crea un resultado de error estandarizado"""
        return {
            "error": mensaje,
            "procesado": False,
            "nombre_archivo": "archivo_desconocido",
            "prediccion": {"es_favorable": False, "confianza": 0.0},
            "frases_clave": {},
            "argumentos": [],
            "insights_juridicos": [f"Error: {mensaje}"],
            "longitud_texto": 0,
            "total_frases_clave": 0,
            "modelo_ia": False
        }


# Función de conveniencia para crear instancia
def crear_analizador() -> AnalizadorLegal:
    """Crea una instancia del analizador legal"""
    return AnalizadorLegal()


if __name__ == "__main__":
    # Prueba del analizador
    analizador = AnalizadorLegal()
    print(f"Modelo cargado: {'Sí' if analizador.modelo else 'No'}")
    print(f"Frases clave disponibles: {len(analizador.frases_clave)}")
