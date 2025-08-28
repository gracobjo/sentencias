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
                resultados[categoria] = {
                    "total": total,
                    "ocurrencias": ocurrencias
                }
        
        return resultados
    
    def _prediccion_basada_reglas(self, texto: str) -> Dict[str, Any]:
        """Predicción basada en reglas y patrones con sistema de confianza mejorado"""
        
        # Sistema de puntuación avanzado
        puntuacion = 0
        factores = {}
        
        # 1. Análisis de palabras clave (peso: 30%)
        palabras_favorables = [
            "procedente", "estimamos", "accedemos", "concedemos", "reconocemos",
            "favorable", "justificado", "acreditado", "confirmado", "establecido",
            "fundada", "procede", "accede", "concede", "reconoce"
        ]
        
        palabras_desfavorables = [
            "desestimamos", "infundada", "rechazamos", "denegamos", "no procedente",
            "desfavorable", "no acreditado", "insuficiente", "negligencia", "culpabilidad",
            "infundada", "desestima", "rechaza", "denega"
        ]
        
        texto_lower = texto.lower()
        favorables = sum(1 for palabra in palabras_favorables if palabra in texto_lower)
        desfavorables = sum(1 for palabra in palabras_desfavorables if palabra in texto_lower)
        
        # Calcular puntuación de palabras clave
        total_palabras = favorables + desfavorables
        if total_palabras > 0:
            score_palabras = (favorables - desfavorables) / total_palabras
            puntuacion += score_palabras * 0.3  # 30% del peso
            factores["palabras_clave"] = {
                "favorables": favorables,
                "desfavorables": desfavorables,
                "score": score_palabras,
                "peso": 0.3
            }
        
        # 2. Análisis de estructura del documento (peso: 20%)
        estructura_score = 0
        if "argumentos" in texto_lower or "fundamentos" in texto_lower:
            estructura_score += 0.2
        if "conclusiones" in texto_lower or "resolucion" in texto_lower:
            estructura_score += 0.2
        if "hechos" in texto_lower or "antecedentes" in texto_lower:
            estructura_score += 0.1
        
        puntuacion += estructura_score * 0.2
        factores["estructura"] = {
            "score": estructura_score,
            "peso": 0.2
        }
        
        # 3. Análisis de evidencia médica (peso: 25%)
        evidencia_score = 0
        if "informe médico" in texto_lower or "dictamen pericial" in texto_lower:
            evidencia_score += 0.3
        if "lesiones" in texto_lower and ("grave" in texto_lower or "permanente" in texto_lower):
            evidencia_score += 0.2
        if "accidente laboral" in texto_lower:
            evidencia_score += 0.1
        
        puntuacion += evidencia_score * 0.25
        factores["evidencia"] = {
            "score": evidencia_score,
            "peso": 0.25
        }
        
        # 4. Análisis de procedimiento legal (peso: 15%)
        procedimiento_score = 0
        if "reclamación administrativa previa" in texto_lower:
            procedimiento_score += 0.2
        if "trámite" in texto_lower and "cumplido" in texto_lower:
            procedimiento_score += 0.2
        if "plazo" in texto_lower and "dentro" in texto_lower:
            procedimiento_score += 0.1
        
        puntuacion += procedimiento_score * 0.15
        factores["procedimiento"] = {
            "score": procedimiento_score,
            "peso": 0.15
        }
        
        # 5. Análisis de contexto temporal (peso: 10%)
        contexto_score = 0
        if "durante" in texto_lower and "jornada" in texto_lower:
            contexto_score += 0.2
        if "lugar de trabajo" in texto_lower:
            contexto_score += 0.2
        if "medidas de seguridad" in texto_lower:
            contexto_score += 0.1
        
        puntuacion += contexto_score * 0.1
        factores["contexto"] = {
            "score": contexto_score,
            "peso": 0.1
        }
        
        # Normalizar puntuación a rango [0, 1]
        puntuacion = max(-1, min(1, puntuacion))
        
        # Convertir a confianza y decisión
        confianza = abs(puntuacion)
        es_favorable = puntuacion > 0
        
        # Ajustar confianza mínima
        confianza = max(0.3, confianza)  # Mínimo 30% de confianza
        
        # Calcular interpretación
        if confianza >= 0.8:
            interpretacion = "Muy Favorable" if es_favorable else "Muy Desfavorable"
        elif confianza >= 0.6:
            interpretacion = "Favorable" if es_favorable else "Desfavorable"
        else:
            interpretacion = "Parcialmente Favorable" if es_favorable else "Parcialmente Desfavorable"
        
        return {
            "es_favorable": es_favorable,
            "confianza": confianza,
            "interpretacion": interpretacion,
            "puntuacion_global": puntuacion,
            "factores_analisis": factores,
            "metodo": "Reglas y patrones mejorados"
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
